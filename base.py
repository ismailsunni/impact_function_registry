"""Abstract base class for all impact functions."""

from metadata.base import MetadataBase


class ImpactFunction(object):

    # class properties
    _metadata = MetadataBase

    def __init__(self):
        """Base class constructor."""
        self._function_type = 'legacy'  # or 'qgis2'


    @property
    def function_type(self):
        """Property for the type of impact function ('legacy' or 'qgis2').

        QGIS2 impact functions are using the QGIS api and have more
        dependencies. Legacy IF's use only numpy, gdal etc. and can be
        used in contexts where no QGIS is present.

        Example usage::

                from registry import Registry
                from flood_impact_function import FloodImpactFunction
                registry = Registry()
                registry.register(FloodImpactFunction)
                registry.list()
                function = registry.get('FloodImpactFunction')


        """
        return self._function_type

    @classmethod
    def instance(cls):
        """Make an instance of the impact function."""
        return cls()

    @classmethod
    def metadata(cls):
        """Get the metadata for this class."""
        return cls._metadata.get_metadata()

    @classmethod
    def parameters(cls):
        """Get the parameter for this class."""
        return cls._metadata.get_parameters()

    def run(self):
        """Run the impact function."""
        raise NotImplementedError('Run is not yet implemented for this class.')

