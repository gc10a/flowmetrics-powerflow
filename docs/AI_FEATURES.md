# PowerFlow AI Features

PowerFlow includes powerful AI and machine learning capabilities designed specifically for revenue operations.

## Overview

The AI module provides intelligent transformers and analyzers that go beyond simple data processing to deliver actionable insights, predictions, and recommendations.

## AI Transformers

### 1. DealScoringTransformer

Automatically score and classify deals based on multiple factors.

**Features:**
- Weighted scoring algorithm
- Automatic classification (HOT/WARM/COOL/COLD)
- Priority assignment (URGENT/HIGH/MEDIUM/LOW)
- Customizable factors and weights

**Example:**
```python
from powerflow import Pipeline
from powerflow.ai import DealScoringTransformer

pipeline = Pipeline("Deal Scoring")
pipeline.add_stage(
    DealScoringTransformer(
        factors=['amount', 'stage', 'days_in_stage', 'engagement_score'],
        weights={'amount': 0.3, 'stage': 0.3, 'days_in_stage': 0.2, 'engagement_score': 0.2}
    )
)
```

**Output Fields:**
- `ai_score` - Composite score (0-100)
- `ai_classification` - HOT, WARM, COOL, or COLD
- `ai_priority` - URGENT, HIGH, MEDIUM, or LOW

### 2. AnomalyDetectionTransformer

Detect unusual patterns and outliers in your data.

**Features:**
- Statistical anomaly detection (z-score method)
- Configurable sensitivity
- Multi-field analysis
- Severity classification

**Example:**
```python
from powerflow.ai import AnomalyDetectionTransformer

pipeline.add_stage(
    AnomalyDetectionTransformer(
        fields=['amount', 'velocity', 'conversion_rate'],
        sensitivity=2.0  # 2 standard deviations
    )
)
```

**Output Fields:**
- `ai_anomaly_detected` - Boolean flag
- `ai_anomalies` - List of detected anomalies with details

**Use Cases:**
- Detect fraudulent transactions
- Identify data quality issues
- Spot significant business events
- Monitor metric changes

### 3. SentimentAnalysisTransformer

Analyze sentiment in text fields (notes, emails, comments).

**Features:**
- Keyword-based sentiment analysis
- Sentiment classification (positive/neutral/negative)
- Confidence scoring
- Multi-field support

**Example:**
```python
from powerflow.ai import SentimentAnalysisTransformer

pipeline.add_stage(
    SentimentAnalysisTransformer(
        text_fields=['notes', 'last_email', 'feedback'],
        output_field='ai_sentiment'
    )
)
```

**Output:**
```python
{
    'ai_sentiment': {
        'sentiment': 'positive',
        'score': 0.15,
        'confidence': 0.75
    }
}
```

**Use Cases:**
- Gauge customer satisfaction
- Identify at-risk deals
- Prioritize support tickets
- Track team morale

### 4. ForecastTransformer

Generate revenue forecasts from historical data.

**Features:**
- Moving average forecasting
- Trend analysis
- Confidence scoring
- Multi-period forecasts

**Example:**
```python
from powerflow.ai import ForecastTransformer

pipeline.add_stage(
    ForecastTransformer(
        date_field='close_date',
        value_field='amount',
        forecast_periods=3
    )
)
```

**Output:**
```python
{
    'ai_forecast': [
        {'period': 1, 'forecast': 125000, 'confidence': 0.85},
        {'period': 2, 'forecast': 130000, 'confidence': 0.70},
        {'period': 3, 'forecast': 135000, 'confidence': 0.55}
    ],
    'ai_forecast_trend': 'increasing'
}
```

### 5. SmartEnrichmentTransformer

Intelligently enrich records with computed insights.

**Features:**
- Deal velocity calculation
- Close probability prediction
- Risk level assessment
- Actionable insights generation

**Example:**
```python
from powerflow.ai import SmartEnrichmentTransformer

pipeline.add_stage(
    SmartEnrichmentTransformer(
        enrichment_rules=['predict_close_probability', 'generate_insights']
    )
)
```

**Enrichment Rules:**
- `calculate_velocity` - Deal velocity metrics
- `predict_close_probability` - Probability of closing
- `generate_insights` - Actionable insights

**Output Fields:**
- `ai_close_probability` - Probability (0-1)
- `ai_risk_level` - HIGH, MEDIUM, or LOW
- `ai_insights` - List of actionable insights

## AI Analyzers

### 1. RevenueInsightAnalyzer

Generate comprehensive insights from revenue data.

**Example:**
```python
from powerflow.ai.analyzers import RevenueInsightAnalyzer

analyzer = RevenueInsightAnalyzer()
insights = analyzer.analyze(pipeline_context.data)

print(insights['summary'])
print(insights['recommendations'])
```

**Output:**
```python
{
    'summary': {
        'total_revenue': 1250000,
        'average_deal_size': 50000,
        'high_value_deals': 15,
        'quality_score': 75
    },
    'trends': [...],
    'recommendations': [
        'Focus on high-value deals',
        'Review stalled opportunities'
    ],
    'risk_factors': [...],
    'opportunities': [...]
}
```

### 2. ChurnPredictionAnalyzer

Predict which customers are at risk of churning.

**Example:**
```python
from powerflow.ai.analyzers import ChurnPredictionAnalyzer

analyzer = ChurnPredictionAnalyzer(risk_threshold=0.6)
predictions = analyzer.predict(customer_data)

high_risk = [p for p in predictions if p['risk_level'] == 'HIGH']
```

**Risk Factors:**
- Low engagement (no activity in 30+ days)
- High support ticket volume
- Poor engagement scores
- Upcoming contract renewal

**Output:**
```python
{
    'account_id': 'ACC123',
    'churn_risk_score': 0.75,
    'risk_level': 'HIGH',
    'factors': ['Low engagement', 'High support tickets'],
    'recommended_actions': ['Schedule business review', 'Reach out to re-engage']
}
```

### 3. DealVelocityAnalyzer

Analyze how quickly deals move through your pipeline.

**Example:**
```python
from powerflow.ai.analyzers import DealVelocityAnalyzer

analyzer = DealVelocityAnalyzer()
metrics = analyzer.analyze(pipeline_data)

print(f"Average velocity: {metrics['average_velocity']}")
print(f"Bottlenecks: {metrics['bottlenecks']}")
```

**Metrics:**
- Average deal velocity ($/day)
- Velocity by stage
- Pipeline bottlenecks
- Fast-moving deals
- Improvement recommendations

## Complete Example

Here's a complete pipeline using multiple AI features:

```python
from powerflow import Pipeline, CSVSource, JSONDestination
from powerflow.ai import (
    DealScoringTransformer,
    AnomalyDetectionTransformer,
    SmartEnrichmentTransformer
)
from powerflow.ai.analyzers import RevenueInsightAnalyzer

# Build pipeline
pipeline = Pipeline("AI-Powered Revenue Analysis")

pipeline.add_stage(CSVSource("deals.csv"))

# AI transformations
pipeline.add_stage(
    DealScoringTransformer(
        factors=['amount', 'stage', 'engagement_score']
    )
)

pipeline.add_stage(
    AnomalyDetectionTransformer(
        fields=['amount', 'days_in_stage']
    )
)

pipeline.add_stage(
    SmartEnrichmentTransformer(
        enrichment_rules=['all']
    )
)

pipeline.add_stage(JSONDestination("ai_analysis.json"))

# Run pipeline
result = pipeline.run()

# Generate insights
analyzer = RevenueInsightAnalyzer()
insights = analyzer.analyze(result.data)

# Print recommendations
for rec in insights['recommendations']:
    print(f"💡 {rec}")
```

## Best Practices

### 1. Start Simple
Begin with one AI transformer and gradually add more as needed.

### 2. Tune Sensitivity
Adjust sensitivity parameters based on your data characteristics.

### 3. Validate Results
Compare AI predictions with actual outcomes to improve accuracy.

### 4. Combine Features
Use multiple AI transformers together for comprehensive analysis.

### 5. Act on Insights
AI insights are only valuable if you act on them!

## Customization

### Custom Scoring Function

```python
def custom_scorer(record):
    score = 0
    if record['amount'] > 100000:
        score += 40
    if record['stage'] == 'negotiation':
        score += 30
    if record['engagement_score'] > 80:
        score += 30
    return score

transformer = DealScoringTransformer(
    scoring_function=custom_scorer
)
```

### Custom Enrichment Rules

```python
def calculate_roi(record):
    return {
        'estimated_roi': record['amount'] * 0.25,
        'payback_period': 12
    }

transformer = SmartEnrichmentTransformer(
    custom_enrichers={'calculate_roi': calculate_roi}
)
```

## Future AI Features

Coming soon:
- Deep learning models for deal prediction
- NLP integration (TextBlob, spaCy, transformers)
- Real-time anomaly detection
- Automated A/B testing
- Recommendation engine
- Natural language insights generation

## Performance Considerations

- AI transformers add minimal overhead (<100ms per 1000 records)
- Anomaly detection scales linearly with data size
- Consider batching for very large datasets (>1M records)
- Sentiment analysis can be CPU-intensive for large text fields

## Technical Details

### Algorithms Used

- **Deal Scoring**: Weighted multi-factor scoring
- **Anomaly Detection**: Z-score (standard deviation method)
- **Sentiment**: Keyword-based classification
- **Forecasting**: Moving average with trend analysis
- **Churn Prediction**: Multi-factor risk scoring

### Extensibility

All AI transformers extend the base `Transformer` class and can be customized or replaced with your own ML models.

## Support

For questions about AI features:
- 📖 See examples in `examples/ai_*.py`
- 💬 Ask in [GitHub Discussions](https://github.com/flowmetrics/powerflow/discussions)
- 🐛 Report issues on [GitHub](https://github.com/flowmetrics/powerflow/issues)

---

**Powered by AI • Built for Revenue Operations** 🤖📊

