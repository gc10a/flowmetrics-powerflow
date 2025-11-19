"""
Data sources for PowerFlow pipelines.
"""

from typing import Any, Dict, List, Optional, Callable
import csv
import json
from pathlib import Path
import logging

from powerflow.pipeline import PipelineStage, PipelineContext

logger = logging.getLogger("powerflow")


class DataSource(PipelineStage):
    """Base class for data sources."""
    
    def fetch(self) -> List[Dict[str, Any]]:
        """Fetch data from the source."""
        raise NotImplementedError("Subclasses must implement fetch()")
    
    def execute(self, context: PipelineContext) -> PipelineContext:
        """Execute the data source stage."""
        logger.info(f"Fetching data from {self.name}")
        data = self.fetch()
        context.data = data
        context.metadata["record_count"] = len(data)
        logger.info(f"Fetched {len(data)} records")
        return context


class CSVSource(DataSource):
    """Read data from a CSV file."""
    
    def __init__(
        self,
        file_path: str,
        name: Optional[str] = None,
        encoding: str = "utf-8",
        delimiter: str = ",",
    ):
        super().__init__(name or f"CSVSource({file_path})")
        self.file_path = Path(file_path)
        self.encoding = encoding
        self.delimiter = delimiter
    
    def fetch(self) -> List[Dict[str, Any]]:
        """Read CSV file."""
        if not self.file_path.exists():
            raise FileNotFoundError(f"CSV file not found: {self.file_path}")
        
        with open(self.file_path, "r", encoding=self.encoding) as f:
            reader = csv.DictReader(f, delimiter=self.delimiter)
            return list(reader)


class JSONSource(DataSource):
    """Read data from a JSON file."""
    
    def __init__(
        self,
        file_path: str,
        name: Optional[str] = None,
        encoding: str = "utf-8",
    ):
        super().__init__(name or f"JSONSource({file_path})")
        self.file_path = Path(file_path)
        self.encoding = encoding
    
    def fetch(self) -> List[Dict[str, Any]]:
        """Read JSON file."""
        if not self.file_path.exists():
            raise FileNotFoundError(f"JSON file not found: {self.file_path}")
        
        with open(self.file_path, "r", encoding=self.encoding) as f:
            data = json.load(f)
            
        # Ensure data is a list
        if isinstance(data, dict):
            return [data]
        elif isinstance(data, list):
            return data
        else:
            raise ValueError(f"Expected list or dict, got {type(data)}")


class GeneratorSource(DataSource):
    """Generate data using a custom function."""
    
    def __init__(
        self,
        generator: Callable[[], List[Dict[str, Any]]],
        name: Optional[str] = None,
    ):
        super().__init__(name or "GeneratorSource")
        self.generator = generator
    
    def fetch(self) -> List[Dict[str, Any]]:
        """Generate data using the provided function."""
        return self.generator()

