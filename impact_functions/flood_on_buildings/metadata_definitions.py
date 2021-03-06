
"""Concrete implementation of metadata class for flood impacts."""

from metadata.base import MetadataBase
# TODO - switch to Qt4 tr()
from utilities import ugettext as tr
from metadata import (
    hazard_definition,
    hazard_flood,
    hazard_tsunami,
    unit_wetdry,
    exposure_definition,
    exposure_structure,
    unit_building_type_type,
    layer_vector_polygon)

from parameter_definitions import (
    flooded_target_field,
    affected_field,
    building_type_field,
    affected_value)


class FloodImpactMetadata(MetadataBase):
    """Metadata for Flood Impact Function.

    .. versionadded:: 2.1

    We only need to re-implement get_metadata(), all other behaviours
    are inherited from the abstract base class.
    """
    @staticmethod
    def as_dict():
        """Return metadata as a dictionary.

        This is a static method. You can use it to get the metadata in
        dictionary format for an impact function.

        :returns: A dictionary representing all the metadata for the
            concrete impact function.
        :rtype: dict
        """
        dict_meta = {
            'id': 'Flood',
            'name': tr('Flood Native Polygon Experimental Function'),
            'impact': tr('Be-flooded'),
            'author': 'Dmitry Kolesov',
            'date_implemented': 'N/A',
            'overview': tr('N/A'),
            'categories': {
                'hazard': {
                    'definition': hazard_definition,
                    'subcategory': [
                        hazard_flood,
                        hazard_tsunami
                    ],
                    'units': unit_wetdry,
                    'layer_constraints': [layer_vector_polygon]
                },
                'exposure': {
                    'definition': exposure_definition,
                    'subcategory': exposure_structure,
                    'units': [unit_building_type_type],
                    'layer_constraints': [layer_vector_polygon]
                }
            },
            'parameters': [
                flooded_target_field(),
                building_type_field(),
                affected_field(),
                affected_value()
            ]
        }
        return dict_meta

