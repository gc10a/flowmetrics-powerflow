"""
Data destinations for PowerFlow pipelines.
"""

from typing import Any, Dict, List, Optional
import csv
import json
from pathlib import Path
import logging

from powerflow.pipeline import PipelineStage, PipelineContext

logger = logging.getLogger("powerflow")


class Destination(PipelineStage):
    """Base class for data destinations."""
    
    def write(self, data: List[Dict[str, Any]]) -> None:
        """Write data to the destination."""
        raise NotImplementedError("Subclasses must implement write()")
    
    def execute(self, context: PipelineContext) -> PipelineContext:
        """Execute the destination stage."""
        logger.info(f"Writing {len(context.data)} records to {self.name}")
        self.write(context.data)
        logger.info(f"Successfully wrote data to {self.name}")
        return context


class CSVDestination(Destination):
    """Write data to a CSV file."""
    
    def __init__(
        self,
        file_path: str,
        name: Optional[str] = None,
        encoding: str = "utf-8",
        delimiter: str = ",",
        mode: str = "w",
    ):
        super().__init__(name or f"CSVDestination({file_path})")
        self.file_path = Path(file_path)
        self.encoding = encoding
        self.delimiter = delimiter
        self.mode = mode
    
    def write(self, data: List[Dict[str, Any]]) -> None:
        """Write data to CSV file."""
        if not data:
            logger.warning("No data to write")
            return
        
        # Ensure parent directory exists
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Get all unique keys across all records
        fieldnames = list(set().union(*(record.keys() for record in data)))
        
        with open(self.file_path, self.mode, encoding=self.encoding, newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=self.delimiter)
            writer.writeheader()
            writer.writerows(data)


class JSONDestination(Destination):
    """Write data to a JSON file."""
    
    def __init__(
        self,
        file_path: str,
        name: Optional[str] = None,
        encoding: str = "utf-8",
        indent: int = 2,
        mode: str = "w",
    ):
        super().__init__(name or f"JSONDestination({file_path})")
        self.file_path = Path(file_path)
        self.encoding = encoding
        self.indent = indent
        self.mode = mode
    
    def write(self, data: List[Dict[str, Any]]) -> None:
        """Write data to JSON file."""
        # Ensure parent directory exists
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(self.file_path, self.mode, encoding=self.encoding) as f:
            json.dump(data, f, indent=self.indent, default=str)


class ConsoleDestination(Destination):
    """Print data to console for debugging."""
    
    def __init__(
        self,
        name: Optional[str] = None,
        limit: Optional[int] = 10,
        pretty: bool = True,
    ):
        super().__init__(name or "ConsoleDestination")
        self.limit = limit
        self.pretty = pretty
    
    def write(self, data: List[Dict[str, Any]]) -> None:
        """Print data to console."""
        display_data = data[:self.limit] if self.limit else data
        
        if self.pretty:
            import json
            print(json.dumps(display_data, indent=2, default=str))
        else:
            for record in display_data:
                print(record)
        
        if self.limit and len(data) > self.limit:
            print(f"\n... and {len(data) - self.limit} more records")

