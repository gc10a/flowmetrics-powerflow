# PowerFlow Architecture

This document describes the architecture and design decisions behind PowerFlow.

## Overview

PowerFlow is built around a simple yet powerful pipeline pattern. Data flows through a series of stages, where each stage performs a specific operation (fetch, transform, or write).

## Core Components

### 1. Pipeline (`pipeline.py`)

The central orchestrator that manages the execution flow.

**Key Classes:**
- `Pipeline` - Main pipeline orchestrator
- `PipelineContext` - State container passed between stages
- `PipelineStage` - Base class for all pipeline stages

**Responsibilities:**
- Execute stages in sequence
- Manage context and state
- Handle errors and exceptions
- Provide hooks for monitoring
- Track execution statistics

### 2. Sources (`sources.py`)

Components that fetch data from various sources.

**Built-in Sources:**
- `CSVSource` - Read from CSV files
- `JSONSource` - Read from JSON files
- `GeneratorSource` - Generate data programmatically
- `DataSource` - Base class for custom sources

**Pattern:**
```python
class MySource(DataSource):
    def fetch(self) -> List[Dict[str, Any]]:
        # Fetch and return data
        pass
```

### 3. Transformers (`transformers.py`)

Components that process and transform data.

**Built-in Transformers:**
- `FilterTransformer` - Filter records
- `MapTransformer` - Transform each record
- `AggregateTransformer` - Group and aggregate
- `EnrichTransformer` - Add additional data
- `DeduplicateTransformer` - Remove duplicates

**Pattern:**
```python
class MyTransformer(Transformer):
    def transform(self, data: List[Dict]) -> List[Dict]:
        # Process and return data
        pass
```

### 4. Destinations (`destinations.py`)

Components that write data to various outputs.

**Built-in Destinations:**
- `CSVDestination` - Write to CSV files
- `JSONDestination` - Write to JSON files
- `ConsoleDestination` - Print to console
- `WebhookDestination` - Send to HTTP endpoints

**Pattern:**
```python
class MyDestination(Destination):
    def write(self, data: List[Dict]) -> None:
        # Write data
        pass
```

### 5. Integrations (`integrations/`)

Pre-built connectors for popular platforms.

**Current Integrations:**
- Salesforce (via simple-salesforce)
- HubSpot (via hubspot-api-client)
- Webhooks (via requests)

## Design Principles

### 1. Simple and Intuitive

PowerFlow follows a straightforward linear pipeline model. Complexity is managed through composition, not configuration.

### 2. Type Safety

PowerFlow uses Python type hints throughout for better IDE support and early error detection.

### 3. Extensibility

Every component can be extended by subclassing base classes. No plugin system needed - just inherit and implement.

### 4. Fail-Safe by Default

Pipelines continue on error by default, collecting errors for review. Users can opt into fail-fast behavior.

### 5. Observable

Hooks at every stage allow monitoring, logging, and metrics collection without modifying pipeline code.

## Data Flow

```
┌─────────────┐
│   Source    │  Fetch data from external source
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ Transformer │  Process/filter/transform data
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ Transformer │  Additional transformations
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ Destination │  Write data to output
└─────────────┘
```

## Context Flow

The `PipelineContext` object flows through each stage:

```python
context = PipelineContext(initial_data=[])

# Source stage
context.data = source.fetch()
context.metadata['record_count'] = len(context.data)

# Transformer stage
context.data = transformer.transform(context.data)

# Destination stage
destination.write(context.data)

# Return context with stats
return context
```

## Error Handling

Two modes:

**Fail-Fast Mode (strict):**
```python
pipeline = Pipeline(fail_fast=True)
# Raises exception on first error
```

**Continue Mode (default):**
```python
pipeline = Pipeline(fail_fast=False)
result = pipeline.run()
# Errors collected in result.errors
```

## Hook System

Hooks allow monitoring without modifying pipeline:

```python
def log_completion(pipeline, context, stage=None):
    if stage:
        print(f"Completed: {stage.name}")

pipeline.add_hook("post_stage", log_completion)
```

**Available Hooks:**
- `pre_run` - Before pipeline starts
- `post_run` - After pipeline completes
- `pre_stage` - Before each stage
- `post_stage` - After each stage

## Performance Considerations

### Memory

- Data is processed in-memory as a list of dictionaries
- For large datasets, consider:
  - Processing in batches
  - Streaming through stages
  - Using external storage between stages

### Speed

- Stages execute sequentially (no parallel processing yet)
- For performance-critical applications:
  - Use efficient data structures
  - Minimize transformations
  - Batch API calls

### Future Optimizations

- Parallel stage execution
- Streaming/chunked processing
- Async I/O support
- Caching layer

## Dependencies

**Core:**
- Python 3.8+
- pandas (for data manipulation)
- pydantic (for validation)
- python-dotenv (for configuration)

**Optional:**
- rich (for pretty output) - gracefully degrades if not available
- simple-salesforce (for Salesforce integration)
- hubspot-api-client (for HubSpot integration)

## Testing Strategy

### Unit Tests
Test individual components in isolation.

### Integration Tests
Test complete pipelines end-to-end.

### Mocking
External services (Salesforce, HubSpot) are mocked in tests.

### Coverage Goal
Target: >80% code coverage

## Future Architecture

### Planned Features

1. **Parallel Execution**
   - Execute independent transformers in parallel
   - Thread or process-based parallelism

2. **Streaming Support**
   - Process records one at a time
   - Reduce memory footprint

3. **Pipeline DAG**
   - Support non-linear pipelines
   - Conditional branching
   - Parallel paths

4. **Data Quality**
   - Built-in validation framework
   - Schema enforcement
   - Data profiling

5. **Scheduling**
   - Built-in scheduler
   - Cron-like syntax
   - Event-driven triggers

## Contributing

When contributing to PowerFlow architecture:

1. **Maintain simplicity** - Don't over-engineer
2. **Follow patterns** - Use existing base classes
3. **Add tests** - Cover new functionality
4. **Document** - Update this file for major changes
5. **Consider performance** - Profile before optimizing

## References

- [Design Patterns](https://refactoring.guru/design-patterns)
- [Python Type Hints](https://docs.python.org/3/library/typing.html)
- [Pipeline Pattern](https://martinfowler.com/articles/data-monolith-to-mesh.html)

