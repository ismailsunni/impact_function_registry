"""Abstract base class for all impact functions."""

from metadata_base import MetadataBase


class ImpactFunction(object):

    _metadata = MetadataBase

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

