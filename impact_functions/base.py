"""Abstract base class for all impact functions."""

from metadata.base import MetadataBase
from errors import InvalidExtentError


class ImpactFunction(object):

    # class properties
    _metadata = MetadataBase

    def __init__(self):
        """Base class constructor."""
        self._function_type = 'legacy'  # or 'qgis2'
        # Analysis extent to use
        self._extent = None
        # CRS as EPSG number
        self._extent_crs = 4326
        # set this to a gui call back / web callback etc as needed.
        self._callback = self.console_callback

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
                try:
                    function = registry.get('FloodImpactFunction')
                except:
                    pass  # function is not valid

        """
        return self._function_type

    @property
    def extent(self):
        """Property for the extent of impact function analysis.

        :returns: A list in the form [xmin, ymin, xmax, ymax].
        :rtype: list
        """
        return self._extent

    @extent.setter
    def extent(self, extent):
        """Setter for extent property.

        :param extent: Analysis boundaries expressed as
            [xmin, ymin, xmax, ymax]. The extent CRS should match the
            extent_crs property of this IF instance.
        :type extent: list
        """
        # add more robust checks here
        if len(extent) != 4:
            raise InvalidExtentError('%s is not a valid extent.' % extent)
        self._extent = extent

    @property
    def extent_crs(self):
        """Property for the extent CRS of impact function analysis.

        :returns: An number representing the EPSG code for the CRS. e.g. 4326
        :rtype: int
        """
        return self._extent_crs

    @extent_crs.setter
    def extent(self, crs):
        """Setter for extent property.

        :param extent_crs: Analysis boundary EPSG CRS expressed as an integer.
        :type extent_crs: int
        """
        self._extent_crs = crs

    @property
    def callback(self):
        """Property for the callback used to relay processing progress.

        :returns: A callback function. The callback function will have the
            following parameter requirements.

            progress_callback(current, maximum, message=None)

        :rtype: function

        .. seealso:: console_progress_callback
        """
        return self._callback

    @callback.setter
    def callback(self, callback):
        """Setter for callback property.

        :param callback: A callback function reference that provides the
            following signature:

            progress_callback(current, maximum, message=None)

        :type callback: function
        """
        self._callback = callback


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

    @staticmethod
    def console_progress_callback(current, maximum, message=None):
        """Simple console based callback implementation for tests.

        :param current: Current progress.
        :type current: int

        :param maximum: Maximum range (point at which task is complete.
        :type maximum: int

        :param message: Optional message to display in the progress bar
        :type message: str, QString
        """
        # noinspection PyChainedComparisons
        if maximum > 1000 and current % 1000 != 0 and current != maximum:
            return
        if message is not None:
            print message
        print 'Task progress: %i of %i' % (current, maximum)
