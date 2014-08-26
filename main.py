# coding=utf-8
__author__ = 'Tim Sutton'
__project_name = 'impact_function_registry'
__filename = 'main'
__date__ = '8/26/14'
__copyright__ = 'tim@kartoza.com'
__doc__ = ''

from registry import Registry
from flood_impact_function import FloodImpactFunction


def main():
    """Main function."""
    registry = Registry()
    registry.register(FloodImpactFunction)
    registry.list()
    function = registry.get('FloodImpactFunction')
    function.run()

if __name__ == '__main__':
    main()
