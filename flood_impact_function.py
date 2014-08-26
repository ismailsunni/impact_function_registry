"""Abstract base class for all impact functions."""
from flood_impact_metadata import FloodImpactMetadata


class FloodImpactFunction(object):

    _metadata = FloodImpactMetadata

    @classmethod
    def instance(cls):
        """Make an instance of the impact function."""
        return cls()

    @classmethod
    def metadata(cls):
        """Get the metadata for this class."""
        return cls._metadata.get_metadata()

    def run(self):
        """Run the impact function."""
        print 'Run called for flood impact function.'
