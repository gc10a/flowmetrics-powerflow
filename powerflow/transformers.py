"""
Data transformers for PowerFlow pipelines.
"""

from typing import Any, Dict, List, Optional, Callable
import logging

from powerflow.pipeline import PipelineStage, PipelineContext

logger = logging.getLogger("powerflow")


class Transformer(PipelineStage):
    """Base class for data transformers."""
    
    def transform(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Transform the data."""
        raise NotImplementedError("Subclasses must implement transform()")
    
    def execute(self, context: PipelineContext) -> PipelineContext:
        """Execute the transformer stage."""
        logger.info(f"Transforming data with {self.name}")
        initial_count = len(context.data)
        context.data = self.transform(context.data)
        final_count = len(context.data)
        logger.info(f"Transformed: {initial_count} → {final_count} records")
        return context


class FilterTransformer(Transformer):
    """Filter records based on a predicate function."""
    
    def __init__(
        self,
        predicate: Callable[[Dict[str, Any]], bool],
        name: Optional[str] = None,
    ):
        super().__init__(name or "FilterTransformer")
        self.predicate = predicate
    
    def transform(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Filter records."""
        return [record for record in data if self.predicate(record)]


class MapTransformer(Transformer):
    """Transform each record using a mapping function."""
    
    def __init__(
        self,
        mapper: Callable[[Dict[str, Any]], Dict[str, Any]],
        name: Optional[str] = None,
    ):
        super().__init__(name or "MapTransformer")
        self.mapper = mapper
    
    def transform(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Map transformation to each record."""
        return [self.mapper(record) for record in data]


class AggregateTransformer(Transformer):
    """
    Aggregate records by grouping keys.
    
    Example:
        >>> # Sum revenue by region
        >>> transformer = AggregateTransformer(
        ...     group_by=['region'],
        ...     aggregations={'revenue': 'sum', 'deals': 'count'}
        ... )
    """
    
    def __init__(
        self,
        group_by: List[str],
        aggregations: Dict[str, str],
        name: Optional[str] = None,
    ):
        super().__init__(name or "AggregateTransformer")
        self.group_by = group_by
        self.aggregations = aggregations
    
    def transform(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Aggregate records."""
        groups: Dict[tuple, Dict[str, Any]] = {}
        
        for record in data:
            # Create group key
            key = tuple(record.get(field) for field in self.group_by)
            
            if key not in groups:
                # Initialize group
                groups[key] = {field: record.get(field) for field in self.group_by}
                for agg_field in self.aggregations:
                    groups[key][agg_field] = []
            
            # Add values to aggregate
            for agg_field in self.aggregations:
                value = record.get(agg_field)
                if value is not None:
                    groups[key][agg_field].append(value)
        
        # Compute aggregations
        result = []
        for group_data in groups.values():
            aggregated = {field: value for field, value in group_data.items() 
                         if field in self.group_by}
            
            for agg_field, agg_type in self.aggregations.items():
                values = group_data[agg_field]
                
                if agg_type == "sum":
                    aggregated[f"{agg_field}_sum"] = sum(values)
                elif agg_type == "count":
                    aggregated[f"{agg_field}_count"] = len(values)
                elif agg_type == "avg":
                    aggregated[f"{agg_field}_avg"] = sum(values) / len(values) if values else 0
                elif agg_type == "min":
                    aggregated[f"{agg_field}_min"] = min(values) if values else None
                elif agg_type == "max":
                    aggregated[f"{agg_field}_max"] = max(values) if values else None
            
            result.append(aggregated)
        
        return result


class EnrichTransformer(Transformer):
    """
    Enrich records with additional fields from a lookup function.
    
    Example:
        >>> def lookup_company(record):
        ...     return {"industry": "Tech", "size": "Enterprise"}
        >>> transformer = EnrichTransformer(lookup_company)
    """
    
    def __init__(
        self,
        enrichment_func: Callable[[Dict[str, Any]], Dict[str, Any]],
        name: Optional[str] = None,
    ):
        super().__init__(name or "EnrichTransformer")
        self.enrichment_func = enrichment_func
    
    def transform(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Enrich each record."""
        result = []
        for record in data:
            enriched = record.copy()
            additional_data = self.enrichment_func(record)
            enriched.update(additional_data)
            result.append(enriched)
        return result


class DeduplicateTransformer(Transformer):
    """
    Remove duplicate records based on specified keys.
    
    Example:
        >>> transformer = DeduplicateTransformer(keys=['email'])
    """
    
    def __init__(
        self,
        keys: List[str],
        keep: str = "first",
        name: Optional[str] = None,
    ):
        super().__init__(name or "DeduplicateTransformer")
        self.keys = keys
        self.keep = keep  # 'first' or 'last'
    
    def transform(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Remove duplicates."""
        seen = set()
        result = []
        
        items = data if self.keep == "first" else reversed(data)
        
        for record in items:
            key = tuple(record.get(k) for k in self.keys)
            if key not in seen:
                seen.add(key)
                result.append(record)
        
        return result if self.keep == "first" else list(reversed(result))

