# coding=utf-8
"""This file is intended to store all available default parameters for IF.."""
__author__ = 'ismailsunni'
__project_name = 'impact_function_registry'
__filename = 'impact_function_parameter'
__date__ = '8/26/14'
__copyright__ = 'imajimatika@gmail.com'
__doc__ = ''

from string_parameter import StringParameter

flooded_target_field = StringParameter()
flooded_target_field.name = 'Target Field'
flooded_target_field.is_required = True
flooded_target_field.help_text = (
    'This field of impact layer marks inundated roads by \'1\' value')
flooded_target_field.description = (
    'This field of impact layer marks inundated roads by \'1\' value. '
    'This is the longer description of this parameter.')
flooded_target_field.value = 'flooded'  # default value

building_type_field = StringParameter()
building_type_field.name = 'Building Type Field'
building_type_field.is_required = True
building_type_field.help_text = (
    'This field of the exposure layer contains information about building '
    'types')
building_type_field.description = (
    'This field of the exposure layer contains information about building '
    'types This is the longer description of this parameter.')
building_type_field.value = 'TYPE'  # default value

affected_field = StringParameter()
affected_field.name = 'Affected Field'
affected_field.is_required = True
affected_field.help_text = (
    'This field of the  hazard layer contains information about inundated '
    'areas')
affected_field.description = (
    'This field of the  hazard layer contains information about inundated '
    'areas. This is the longer description of this parameter.')
affected_field.value = 'affected'  # default value

affected_value = StringParameter()
affected_value.name = 'Affected Value'
affected_value.is_required = True
affected_value.help_text = (
    'This value in \'affected_field\' of the hazard layer marks the areas as '
    'inundated')
affected_value.description = (
    'This value in \'affected_field\' of the hazard layer marks the areas as '
    'inundated. This is the longer description of this parameter.')
affected_value.value = '1'  # default value
