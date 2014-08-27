"""Abstract base class for all impact functions."""
from flood_impact_metadata import FloodImpactMetadata
from impact_function_base import ImpactFunction


class FloodImpactFunction(ImpactFunction):

    _metadata = FloodImpactMetadata


    def run (self):
        """Run the impact function."""
        print 'Run called for flood impact function.'
