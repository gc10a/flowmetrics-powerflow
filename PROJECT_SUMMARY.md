# PowerFlow - Project Summary

## 🎯 What is PowerFlow?

PowerFlow is an open-source Python framework for building revenue operations data pipelines. It's designed to make it easy to extract, transform, and load (ETL) data from CRMs like Salesforce and HubSpot, process it, and output results.

**Created by FlowMetrics** - Shared with the open source community ❤️

## 📁 Repository Structure

```
flowmetrics-powerflow/
├── powerflow/                  # Main package
│   ├── __init__.py            # Package exports
│   ├── pipeline.py            # Core pipeline framework
│   ├── sources.py             # Data sources (CSV, JSON, etc.)
│   ├── transformers.py        # Data transformations
│   ├── destinations.py        # Output destinations
│   └── integrations/          # Third-party integrations
│       ├── salesforce.py      # Salesforce connector
│       ├── hubspot.py         # HubSpot connector
│       └── webhook.py         # Webhook sender
│
├── tests/                      # Test suite
│   ├── test_pipeline.py       # Pipeline tests
│   ├── test_sources.py        # Source tests
│   ├── test_transformers.py   # Transformer tests
│   ├── test_destinations.py   # Destination tests
│   └── test_integration.py    # End-to-end tests
│
├── examples/                   # Example scripts
│   ├── basic_pipeline.py      # Simple CSV to JSON
│   ├── aggregation_pipeline.py # Revenue aggregation
│   ├── salesforce_example.py  # Salesforce integration
│   └── webhook_example.py     # Webhook alerts
│
├── docs/                       # Documentation
│   └── ARCHITECTURE.md        # Architecture overview
│
├── .github/                    # GitHub configuration
│   ├── workflows/             # CI/CD pipelines
│   └── ISSUE_TEMPLATE/        # Issue templates
│
├── demo.py                     # Interactive demo (run this!)
├── README.md                   # Main documentation
├── QUICKSTART.md              # Quick start guide
├── CONTRIBUTING.md            # Contribution guidelines
├── LICENSE                     # MIT License
├── setup.py                    # Package setup
├── requirements.txt           # Dependencies
└── Makefile                   # Dev commands
```

## 🚀 Quick Start

### 1. Run the Demo
```bash
python demo.py
```

This runs three demos showing different features:
- Filtering and transforming deals
- Aggregating revenue by region
- Using pipeline hooks for monitoring

### 2. Try the Examples
```bash
cd examples
python basic_pipeline.py
python aggregation_pipeline.py
```

### 3. Install and Use
```bash
pip install -e .
python your_pipeline.py
```

## 🔑 Key Features

### ✅ Implemented
- **Core Pipeline Framework** - Build data workflows with stages
- **Built-in Sources** - CSV, JSON, Salesforce, HubSpot
- **Powerful Transformers** - Filter, map, aggregate, enrich, deduplicate
- **Multiple Destinations** - CSV, JSON, console, webhooks
- **Error Handling** - Fail-fast or collect all errors
- **Monitoring Hooks** - Track pipeline execution
- **Rich Console Output** - Beautiful progress bars (optional)
- **Full Test Suite** - >80% code coverage
- **CI/CD** - GitHub Actions for testing
- **Comprehensive Docs** - README, examples, architecture docs

### 🎯 Use Cases
- Revenue reporting and analytics
- Data synchronization between systems
- Lead scoring and enrichment
- Sales pipeline analysis
- Automated alerts and notifications
- Custom data transformations

## 📊 Example Pipeline

```python
from powerflow import Pipeline, CSVSource, FilterTransformer, JSONDestination

# Create pipeline
pipeline = Pipeline("High Value Deals")

# Add stages
pipeline.add_stage(CSVSource("deals.csv"))
pipeline.add_stage(FilterTransformer(lambda d: float(d['amount']) > 50000))
pipeline.add_stage(JSONDestination("high_value_deals.json"))

# Run it!
result = pipeline.run()
print(f"Processed {result.metadata['record_count']} deals")
```

## 🧪 Testing

```bash
# Run all tests
pytest tests/

# With coverage
pytest tests/ --cov=powerflow --cov-report=term-missing

# Run specific test
pytest tests/test_pipeline.py
```

## 🛠️ Development

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Format code
black powerflow tests examples

# Lint
flake8 powerflow tests --max-line-length=100

# Type check
mypy powerflow --ignore-missing-imports

# Or use Makefile
make install-dev
make test
make format
make lint
```

## 📦 Package Components

### Core (`powerflow/`)
- `Pipeline` - Main orchestrator
- `PipelineContext` - State container
- `PipelineStage` - Base class for stages

### Sources (`sources.py`)
- `CSVSource` - Read CSV files
- `JSONSource` - Read JSON files
- `GeneratorSource` - Programmatic data generation
- `DataSource` - Base class for custom sources

### Transformers (`transformers.py`)
- `FilterTransformer` - Filter records
- `MapTransformer` - Transform each record
- `AggregateTransformer` - Group and aggregate
- `EnrichTransformer` - Add data to records
- `DeduplicateTransformer` - Remove duplicates

### Destinations (`destinations.py`)
- `CSVDestination` - Write to CSV
- `JSONDestination` - Write to JSON
- `ConsoleDestination` - Print to console
- `WebhookDestination` - Send to HTTP endpoint

### Integrations (`integrations/`)
- `SalesforceSource` - Fetch from Salesforce
- `HubSpotSource` - Fetch from HubSpot
- More coming soon!

## 📈 Project Stats

- **Lines of Code**: ~2,000
- **Test Coverage**: >80%
- **Python Version**: 3.8+
- **Dependencies**: Minimal (pandas, pydantic, python-dotenv)
- **License**: MIT
- **Status**: Alpha (v0.1.0)

## 🗺️ Roadmap

### Short Term (v0.2.0)
- [ ] More integrations (Pipedrive, Zendesk)
- [ ] Data validation framework
- [ ] Incremental loading
- [ ] Better error messages

### Medium Term (v0.3.0)
- [ ] Parallel processing
- [ ] Streaming support
- [ ] Pipeline scheduling
- [ ] Web UI for visual pipeline building

### Long Term (v1.0.0)
- [ ] Pipeline DAG (non-linear flows)
- [ ] Cloud connectors (Snowflake, BigQuery)
- [ ] Real-time data processing
- [ ] Enterprise features

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

**Areas we'd love help with:**
- New integrations (Pipedrive, Zendesk, etc.)
- Performance optimizations
- Documentation improvements
- Bug fixes
- Example pipelines

## 📄 License

MIT License - See [LICENSE](LICENSE) file

## 🙏 Acknowledgments

Built with ❤️ by the FlowMetrics team and open source contributors.

**Technologies:**
- Python
- pandas
- pydantic
- rich (optional)
- pytest

## 📞 Support

- 📖 [Documentation](README.md)
- 🚀 [Quick Start](QUICKSTART.md)
- 💬 [GitHub Discussions](https://github.com/flowmetrics/powerflow/discussions)
- 🐛 [Issue Tracker](https://github.com/flowmetrics/powerflow/issues)
- 🌟 [Examples](examples/)

## 🎉 Getting Started

1. **Clone the repo**
   ```bash
   git clone https://github.com/flowmetrics/powerflow.git
   cd powerflow
   ```

2. **Run the demo**
   ```bash
   python demo.py
   ```

3. **Read the docs**
   - Start with [QUICKSTART.md](QUICKSTART.md)
   - Then read [README.md](README.md)
   - Check out [examples/](examples/)

4. **Build something awesome!**

---

**Made with ❤️ by FlowMetrics** | [Website](https://flowmetrics.com) | [GitHub](https://github.com/flowmetrics/powerflow)

