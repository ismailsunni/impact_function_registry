"""Abstract base class for all impact functions."""
from metadata_definitions import FloodImpactMetadata
from impact_functions.base import ImpactFunction


class FloodImpactFunction(ImpactFunction):

    _metadata = FloodImpactMetadata


    def __init__(self):
        """Constructor."""


    def run (self):
        """Run the impact function."""
        print 'Run called for flood impact function.'
