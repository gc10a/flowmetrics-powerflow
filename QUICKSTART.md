# PowerFlow Quick Start Guide

Get up and running with PowerFlow in 5 minutes!

## Installation

### Option 1: Install from source (recommended for development)

```bash
git clone https://github.com/flowmetrics/powerflow.git
cd powerflow
pip install -e .
```

### Option 2: Install from PyPI (coming soon)

```bash
pip install powerflow
```

### Option 3: With optional integrations

```bash
# With Salesforce support
pip install powerflow[salesforce]

# With HubSpot support
pip install powerflow[hubspot]

# With all integrations
pip install powerflow[salesforce,hubspot]

# For development
pip install powerflow[dev]
```

## Your First Pipeline

Create a file called `my_pipeline.py`:

```python
from powerflow import Pipeline, GeneratorSource, FilterTransformer, ConsoleDestination

# Generate sample data
def generate_deals():
    return [
        {'id': 1, 'amount': 10000, 'status': 'won'},
        {'id': 2, 'amount': 25000, 'status': 'won'},
        {'id': 3, 'amount': 5000, 'status': 'lost'},
    ]

# Create pipeline
pipeline = Pipeline("My First Pipeline")

# Add stages
pipeline.add_stage(GeneratorSource(generate_deals))
pipeline.add_stage(FilterTransformer(lambda deal: deal['status'] == 'won'))
pipeline.add_stage(ConsoleDestination())

# Run!
result = pipeline.run()

print(f"Processed {result.metadata['record_count']} deals")
```

Run it:

```bash
python my_pipeline.py
```

## Try the Demo

```bash
python demo.py
```

This will run three demos showing different PowerFlow features:
1. Filtering and transforming data
2. Aggregating revenue by region
3. Using pipeline hooks for monitoring

## Common Use Cases

### 1. CSV to JSON Conversion

```python
from powerflow import Pipeline, CSVSource, JSONDestination

Pipeline("CSV to JSON") \
    .add_stage(CSVSource("input.csv")) \
    .add_stage(JSONDestination("output.json")) \
    .run()
```

### 2. Filter High-Value Deals

```python
from powerflow import Pipeline, CSVSource, FilterTransformer, CSVDestination

Pipeline("High Value Deals") \
    .add_stage(CSVSource("deals.csv")) \
    .add_stage(FilterTransformer(lambda d: float(d['amount']) > 50000)) \
    .add_stage(CSVDestination("high_value_deals.csv")) \
    .run()
```

### 3. Revenue Aggregation

```python
from powerflow import Pipeline, CSVSource, AggregateTransformer, CSVDestination

pipeline = Pipeline("Revenue by Region")
pipeline.add_stage(CSVSource("deals.csv"))
pipeline.add_stage(
    AggregateTransformer(
        group_by=['region'],
        aggregations={'revenue': 'sum', 'deal_id': 'count'}
    )
)
pipeline.add_stage(CSVDestination("revenue_summary.csv"))
pipeline.run()
```

### 4. Salesforce Integration

```python
from powerflow import Pipeline, SalesforceSource, CSVDestination

pipeline = Pipeline("Salesforce Opportunities")
pipeline.add_stage(
    SalesforceSource(
        username="user@example.com",
        password="password",
        security_token="token",
        object_type="Opportunity",
        fields=["Id", "Name", "Amount", "StageName"],
        where_clause="Amount > 10000"
    )
)
pipeline.add_stage(CSVDestination("opportunities.csv"))
pipeline.run()
```

## Next Steps

1. **Explore Examples**: Check out the `examples/` directory for more use cases
2. **Read the Docs**: See [README.md](README.md) for comprehensive documentation
3. **Run Tests**: `pytest tests/` to see the test suite
4. **Build Something**: Create your own pipeline!

## Getting Help

- 📖 [Full Documentation](README.md)
- 💬 [GitHub Discussions](https://github.com/flowmetrics/powerflow/discussions)
- 🐛 [Report Issues](https://github.com/flowmetrics/powerflow/issues)
- 🌟 [Examples](examples/)

## Key Concepts

### Pipeline Stages

PowerFlow pipelines have three types of stages:

1. **Sources** - Where data comes from
   - `CSVSource`, `JSONSource`, `SalesforceSource`, `HubSpotSource`, `GeneratorSource`

2. **Transformers** - How data is processed
   - `FilterTransformer`, `MapTransformer`, `AggregateTransformer`, `EnrichTransformer`, `DeduplicateTransformer`

3. **Destinations** - Where data goes
   - `CSVDestination`, `JSONDestination`, `ConsoleDestination`, `WebhookDestination`

### Building Pipelines

Two ways to build pipelines:

**Method 1: Fluent API**
```python
Pipeline("Name") \
    .add_stage(Source()) \
    .add_stage(Transformer()) \
    .add_stage(Destination()) \
    .run()
```

**Method 2: Step by step**
```python
pipeline = Pipeline("Name")
pipeline.add_stage(Source())
pipeline.add_stage(Transformer())
pipeline.add_stage(Destination())
result = pipeline.run()
```

### Error Handling

```python
# Fail on first error
pipeline = Pipeline("Name", fail_fast=True)

# Or collect all errors
pipeline = Pipeline("Name", fail_fast=False)
result = pipeline.run()

if result.errors:
    for error in result.errors:
        print(f"Error: {error}")
```

## Tips & Tricks

1. **Chain transformers** for complex data processing
2. **Use hooks** to monitor pipeline progress
3. **Start simple** and add complexity as needed
4. **Test with small data** before scaling up
5. **Check the examples** for patterns

Happy building! 🚀

