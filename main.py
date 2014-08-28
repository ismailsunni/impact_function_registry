# coding=utf-8
__author__ = 'Tim Sutton'
__project_name = 'impact_function_registry'
__filename = 'main'
__date__ = '8/26/14'
__copyright__ = 'tim@kartoza.com'
__doc__ = ''

import sys
print sys.path

from registry import Registry
from impact_functions.flood_on_buildings import FloodImpactFunction

from metadata import (
    hazard_tsunami,
    exposure_structure,
    unit_metres_depth,
    unit_building_type_type,
    layer_vector_polygon,
    unit_wetdry
)


def main():
    """Main function."""
    registry = Registry()
    registry.register(FloodImpactFunction)
    registry.list()
    function = registry.get('FloodImpactFunction')
    function_parameters = function.parameters()
    for x in function_parameters:
        print '--', x.name, x.value
    print 'Change value of target field to FLOODED:'
    function_parameters[0].value = 'FLOODED'
    function_parameters = function.parameters()
    for x in function_parameters:
        print '--', x.name, x.value
    function.run()

    hazard_keywords = {
        'subcategory': hazard_tsunami,
        'units': unit_wetdry,
        'layer_constraints': layer_vector_polygon
    }

    exposure_keywords = {
        'subcategory': exposure_structure,
        'units': unit_building_type_type,
        'layer_constraints': layer_vector_polygon
    }

    impact_functions = registry.filter(hazard_keywords, exposure_keywords)
    print len(impact_functions)
    print [x.metadata()['name'] for x in impact_functions]

    hazard_keywords = {
        'subcategory': hazard_tsunami,
        'units': unit_metres_depth,
        'layer_constraints': layer_vector_polygon
    }

    exposure_keywords = {
        'subcategory': exposure_structure,
        'units': unit_building_type_type,
        'layer_constraints': layer_vector_polygon
    }

    impact_functions = registry.filter(hazard_keywords, exposure_keywords)
    print len(impact_functions)
    print [x.metadata()['name'] for x in impact_functions]

if __name__ == '__main__':
    main()
