"""
PowerFlow - A Python framework for building revenue operations data pipelines.

PowerFlow helps you build robust, scalable data pipelines for revenue operations,
with built-in support for popular CRM and marketing automation platforms.
"""

__version__ = "0.1.0"

from powerflow.pipeline import Pipeline, PipelineContext
from powerflow.sources import DataSource, CSVSource, JSONSource, GeneratorSource
from powerflow.transformers import (
    Transformer,
    FilterTransformer,
    MapTransformer,
    AggregateTransformer,
    EnrichTransformer,
    DeduplicateTransformer,
)
from powerflow.destinations import Destination, CSVDestination, JSONDestination, ConsoleDestination
from powerflow.integrations import SalesforceSource, HubSpotSource

# AI module is optional - import what's available
try:
    from powerflow import ai
    HAS_AI = True
except ImportError:
    HAS_AI = False
    ai = None

__all__ = [
    "Pipeline",
    "PipelineContext",
    "DataSource",
    "CSVSource",
    "JSONSource",
    "GeneratorSource",
    "Transformer",
    "FilterTransformer",
    "MapTransformer",
    "AggregateTransformer",
    "EnrichTransformer",
    "DeduplicateTransformer",
    "Destination",
    "CSVDestination",
    "JSONDestination",
    "ConsoleDestination",
    "SalesforceSource",
    "HubSpotSource",
    "ai",
    "HAS_AI",
]

