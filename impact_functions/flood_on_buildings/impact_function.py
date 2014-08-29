# coding=utf-8
"""Flood on buildings impact function."""
from PyQt4.QtCore import QVariant
from qgis.core import (
    QgsField,
    QgsVectorLayer,
    QgsFeature,
    QgsRectangle,
    QgsFeatureRequest,
    QgsGeometry
)

from metadata_definitions import FloodImpactMetadata
from impact_functions.base import ImpactFunction
# TODO - switch to Qt4 tr()
from utilities import ugettext as tr
from errors import GetDataError


class FloodImpactFunction(ImpactFunction):
    """Impact function for flood on buildings."""

    _metadata = FloodImpactMetadata

    def __init__(self):
        """Constructor (calls ctor of base class)."""
        super(FloodImpactFunction, self).__init__()

        self.hazard_provider = None
        self.affected_field_index = -1

    def prepare_for_run(self):
        """Prepare this impact function for running the analysis.

        .. seealso:: impact_functions.base.prepare_for_run()

        Calls the prepare_for_run method of the impact function base class and
        then implements any specfic checks needed by this impact function.

        :raises: GetDataError
        """
        super(FloodImpactFunction, self).prepare_for_run()

        affected_field = self.parameters['affected_field']
        self.hazard_provider = self.hazard.dataProvider()
        self.affected_field_index = self.hazard_provider.fieldNameIndex(
            affected_field)
        if self.affected_field_index == -1:
            message = tr('''Parameter "Affected Field"(='%s')
                is not present in the
                attribute table of the hazard layer.''' % (affected_field, ))
            raise GetDataError(message)

    def run(self):
        """Run the impact function."""
        # First fo any generic run work defined in the ABC.
        self.prepare_for_run()

        target_field = self.parameters['target_field']
        building_type_field = self.parameters['building_type_field']
        affected_value = self.parameters['affected_value']

        crs = self.exposure.crs().toWkt()
        e_provider = self.exposure.dataProvider()
        fields = e_provider.fields()
        # If target_field does not exist, add it:
        if fields.indexFromName(target_field) == -1:
            e_provider.addAttributes(
                [QgsField(target_field, QVariant.Int)])
        target_field_index = e_provider.fieldNameIndex(target_field)
        fields = e_provider.fields()

        # Create layer for store the lines from exposure and extent
        building_layer = QgsVectorLayer(
            'Polygon?crs=' + crs, 'impact_buildings', 'memory')
        building_provider = building_layer.dataProvider()

        # Set attributes
        building_provider.addAttributes(fields.toList())
        building_layer.startEditing()
        building_layer.commitChanges()

        # Filter geometry and data using the extent
        extent = QgsRectangle(*self.extent)
        request = QgsFeatureRequest()
        request.setFilterRect(extent)

        # Split building_layer by hazard and save as result:
        #   1) Filter from hazard inundated features
        #   2) Mark buildings as inundated (1) or not inundated (0)

        affected_field_type = self.hazard_provider.fields()[
            self.affected_field_index].typeName()
        if affected_field_type in ['Real', 'Integer']:
            affected_value = float(affected_value)

        hazard_data = self.hazard.getFeatures(request)
        hazard_poly = None
        for multi_polygon in hazard_data:
            attributes = multi_polygon.attributes()
            if attributes[self.affected_field_index] != affected_value:
                continue
            if hazard_poly is None:
                hazard_poly = QgsGeometry(multi_polygon.geometry())
            else:
                # Make geometry union of inundated polygons

                # But some multi_polygon.geometry() could be invalid, skip them
                tmp_geometry = hazard_poly.combine(multi_polygon.geometry())
                try:
                    if tmp_geometry.isGeosValid():
                        hazard_poly = tmp_geometry
                except AttributeError:
                    pass

        if hazard_poly is None:
            message = tr(
                '''There are no objects in the hazard layer with "Affected
                value"='%s'. Please check the value or use other extent.''' %
                (affected_value, ))
            raise GetDataError(message)

        e_data = self.exposure.getFeatures(request)
        for feat in e_data:
            building_geom = feat.geometry()
            attributes = feat.attributes()
            l_feat = QgsFeature()
            l_feat.setGeometry(building_geom)
            l_feat.setAttributes(attributes)
            if hazard_poly.intersects(building_geom):
                l_feat.setAttribute(target_field_index, 1)
            else:

                l_feat.setAttribute(target_field_index, 0)
            (_, __) = building_layer.dataProvider().addFeatures([l_feat])
        building_layer.updateExtents()

        # Generate simple impact report

        building_count = flooded_count = 0  # Count of buildings
        buildings_by_type = dict()      # Length of flooded roads by types

        buildings_data = building_layer.getFeatures()
        building_type_field_index = building_layer.fieldNameIndex(
            building_type_field)
        for building in buildings_data:
            building_count += 1
            attributes = building.attributes()
            building_type = attributes[building_type_field_index]
            if building_type in [None, 'NULL', 'null', 'Null']:
                building_type = 'Unknown type'
            if not building_type in buildings_by_type:
                buildings_by_type[building_type] = {'flooded': 0, 'total': 0}
            buildings_by_type[building_type]['total'] += 1

            if attributes[target_field_index] == 1:
                flooded_count += 1
                buildings_by_type[building_type]['flooded'] += 1

        result = {}
        result['question'] = self.question()
        result['headings'] = [
            tr('Building Type'),
            tr('Flooded'),
            tr('Total')
        ]
        result['totals'] = [
            tr('All'),
            int(flooded_count),
            int(building_count)]
        result['tabulation_title'] = tr('Breakdown by building type')

        tabulation = []
        for t, v in buildings_by_type.iteritems():
            tabulation.append([t, int(v['flooded']), int(v['total'])])
        result['tabulation'] = tabulation

        result['title'] = tr('Buildings inundated')
        self.result = result

        style_classes = [
            dict(label=tr('Not Inundated'), value=0, colour='#1EFC7C',
                 transparency=0, size=0.5),
            dict(label=tr('Inundated'), value=1, colour='#F31A1C',
                 transparency=0, size=0.5)]
        style_info = dict(
            target_field=target_field,
            style_classes=style_classes,
            style_type='categorizedSymbol')
        self.style_info = style_classes

        return building_layer
        # Convert QgsVectorLayer to inasafe layer and return it.
        # building_layer = Vector(
        #     data=building_layer,
        #     name=tr('Flooded buildings'),
        #     keywords={
        #         'impact_summary': impact_summary,
        #         'map_title': map_title,
        #         'target_field': target_field},
        #     style_info=style_info)
        # return building_layer
