# 👋 Welcome to PowerFlow!

## What is this?

**PowerFlow** is an open-source Python framework for building revenue operations data pipelines **with built-in AI**. It helps you extract data from CRMs, transform it with intelligent AI models, and load it wherever you need.

**Now with AI-powered features**: Deal scoring, anomaly detection, forecasting, sentiment analysis, and intelligent insights!

Created by **FlowMetrics** and shared with the community! 🎉

## 🚀 Get Started in 30 Seconds

### Option 1: Run the Demo (Recommended!)

```bash
python demo.py
```

This will show you three working examples of PowerFlow in action!

### Option 2: Run an Example

```bash
python examples/basic_pipeline.py
```

### Option 3: Try It Yourself

Create a file called `my_first_pipeline.py`:

```python
from powerflow import Pipeline, GeneratorSource, FilterTransformer, ConsoleDestination

# Generate some sample data
def generate_deals():
    return [
        {'id': 1, 'amount': 10000, 'status': 'won'},
        {'id': 2, 'amount': 25000, 'status': 'won'},
        {'id': 3, 'amount': 5000, 'status': 'lost'},
    ]

# Build a pipeline
pipeline = Pipeline("My First Pipeline")
pipeline.add_stage(GeneratorSource(generate_deals))
pipeline.add_stage(FilterTransformer(lambda deal: deal['status'] == 'won'))
pipeline.add_stage(ConsoleDestination())

# Run it!
result = pipeline.run()
print(f"✅ Processed {result.metadata['record_count']} winning deals!")
```

Then run:
```bash
python my_first_pipeline.py
```

## 📚 What to Read Next

1. **[QUICKSTART.md](QUICKSTART.md)** - Installation and basic usage (5 min read)
2. **[README.md](README.md)** - Full documentation (15 min read)
3. **[examples/](examples/)** - Working code examples
4. **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** - Project overview and structure

## 🎯 What Can I Build With This?

PowerFlow is perfect for:

- 🤖 **AI-Powered Deal Scoring** - Automatically score and classify deals (NEW!)
- 📊 **Revenue Forecasting** - Predict future revenue with AI (NEW!)
- 🔍 **Anomaly Detection** - Catch unusual patterns in your data (NEW!)
- 💡 **Intelligent Insights** - Get AI-generated recommendations (NEW!)
- 📊 **Revenue Reporting** - Aggregate sales data across systems
- 🔄 **Data Syncing** - Keep CRMs and databases in sync
- 🎯 **Lead Scoring** - Enrich and score leads automatically
- 📈 **Analytics** - Build custom sales dashboards
- 🔔 **Alerts** - Monitor deals and send notifications
- 🧹 **Data Cleaning** - Deduplicate and standardize data

## 💡 Quick Examples

### AI-Powered Deal Scoring 🤖 NEW!
```python
from powerflow import Pipeline, CSVSource
from powerflow.ai import DealScoringTransformer

Pipeline("AI Scoring") \
    .add_stage(CSVSource("deals.csv")) \
    .add_stage(DealScoringTransformer()) \
    .run()

# Automatically adds: ai_score, ai_classification (HOT/WARM/COOL/COLD), ai_priority
```

### Revenue Insights with AI 💡 NEW!
```python
from powerflow.ai.analyzers import RevenueInsightAnalyzer

result = pipeline.run()
analyzer = RevenueInsightAnalyzer()
insights = analyzer.analyze(result.data)

print(insights['recommendations'])  # AI-generated recommendations
print(insights['risk_factors'])     # Identified risks
print(insights['opportunities'])    # Growth opportunities
```

## 📊 Classic Pipeline Examples

### Filter High-Value Deals
```python
Pipeline("High Value Deals") \
    .add_stage(CSVSource("deals.csv")) \
    .add_stage(FilterTransformer(lambda d: float(d['amount']) > 50000)) \
    .add_stage(JSONDestination("high_value.json")) \
    .run()
```

### Aggregate Revenue by Region
```python
Pipeline("Revenue Summary") \
    .add_stage(CSVSource("deals.csv")) \
    .add_stage(AggregateTransformer(
        group_by=['region'],
        aggregations={'revenue': 'sum', 'deals': 'count'}
    )) \
    .add_stage(CSVDestination("summary.csv")) \
    .run()
```

### Fetch from Salesforce
```python
Pipeline("Salesforce Opportunities") \
    .add_stage(SalesforceSource(
        username="user@example.com",
        password="password",
        security_token="token",
        object_type="Opportunity"
    )) \
    .add_stage(CSVDestination("opportunities.csv")) \
    .run()
```

## 🛠️ Installation

PowerFlow works out of the box with just Python 3.8+!

For the full experience with pretty output:
```bash
pip install -e .
```

Or just the basics:
```bash
# No installation needed! Just use it directly
python demo.py
```

## 🤝 Contributing

We'd love your help! Check out [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

**Ways to contribute:**
- 🐛 Report bugs
- ✨ Suggest features
- 📖 Improve docs
- 🔌 Add integrations
- 🧪 Write tests

## 📞 Need Help?

- 📖 Read the [docs](README.md)
- 💬 Ask in [Discussions](https://github.com/flowmetrics/powerflow/discussions)
- 🐛 Report [issues](https://github.com/flowmetrics/powerflow/issues)
- 🌟 Check [examples](examples/)

## 📂 Repository Overview

```
├── demo.py                 # ⭐ Start here! Interactive demo
├── examples/               # Working code examples
├── powerflow/             # Main package
├── tests/                 # Test suite
├── README.md              # Full documentation
└── QUICKSTART.md          # Quick start guide
```

## 🎉 Let's Go!

**Three steps to get started:**

1. Run the demo: `python demo.py`
2. Read the quickstart: [QUICKSTART.md](QUICKSTART.md)
3. Build something awesome! 🚀

---

**Questions?** Open an [issue](https://github.com/flowmetrics/powerflow/issues) or [discussion](https://github.com/flowmetrics/powerflow/discussions)

**Made with ❤️ by FlowMetrics**

