"""
AI-powered transformers for intelligent data processing.
"""

from typing import Any, Dict, List, Optional, Callable
import logging
from datetime import datetime, timedelta

from powerflow.transformers import Transformer

logger = logging.getLogger("powerflow.ai")


class DealScoringTransformer(Transformer):
    """
    Score deals based on AI-powered analysis of multiple factors.
    
    Uses a weighted scoring algorithm to predict deal likelihood and value.
    Can be extended with custom ML models.
    
    Example:
        >>> transformer = DealScoringTransformer(
        ...     factors=['amount', 'stage', 'age_days', 'engagement_score'],
        ...     weights={'amount': 0.3, 'stage': 0.3, 'age_days': 0.2, 'engagement_score': 0.2}
        ... )
        >>> scored_deals = transformer.transform(deals)
    """
    
    def __init__(
        self,
        factors: Optional[List[str]] = None,
        weights: Optional[Dict[str, float]] = None,
        scoring_function: Optional[Callable] = None,
        name: Optional[str] = None,
    ):
        super().__init__(name or "DealScoringTransformer")
        self.factors = factors or ['amount', 'stage', 'days_in_stage']
        self.weights = weights or self._default_weights()
        self.scoring_function = scoring_function or self._default_scoring
    
    def _default_weights(self) -> Dict[str, float]:
        """Default weights for common deal factors."""
        return {
            'amount': 0.25,
            'stage': 0.25,
            'days_in_stage': 0.20,
            'engagement_score': 0.15,
            'company_size': 0.15,
        }
    
    def _normalize_value(self, value: Any, field: str) -> float:
        """Normalize a value to 0-1 range."""
        if isinstance(value, (int, float)):
            # Simple normalization for numeric values
            if field == 'amount':
                return min(value / 1000000, 1.0)  # Cap at $1M
            elif field == 'days_in_stage':
                return max(1 - (value / 90), 0)  # Penalty after 90 days
            elif field == 'company_size':
                return min(value / 10000, 1.0)  # Cap at 10k employees
            else:
                return min(value / 100, 1.0)  # Generic 0-100 scale
        elif isinstance(value, str):
            # Stage scoring
            stage_scores = {
                'prospecting': 0.2,
                'qualification': 0.3,
                'proposal': 0.5,
                'negotiation': 0.7,
                'closed_won': 1.0,
                'closed_lost': 0.0,
            }
            return stage_scores.get(value.lower().replace(' ', '_'), 0.5)
        return 0.5
    
    def _default_scoring(self, record: Dict[str, Any]) -> float:
        """Calculate a composite score for a deal."""
        score = 0.0
        total_weight = 0.0
        
        for factor in self.factors:
            if factor in record:
                weight = self.weights.get(factor, 0.1)
                normalized = self._normalize_value(record[factor], factor)
                score += normalized * weight
                total_weight += weight
        
        return (score / total_weight * 100) if total_weight > 0 else 50.0
    
    def transform(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Add AI-powered deal scores to records."""
        logger.info(f"Scoring {len(data)} deals using AI model")
        
        for record in data:
            score = self.scoring_function(record)
            record['ai_score'] = round(score, 2)
            
            # Add classification
            if score >= 80:
                record['ai_classification'] = 'HOT'
                record['ai_priority'] = 'URGENT'
            elif score >= 60:
                record['ai_classification'] = 'WARM'
                record['ai_priority'] = 'HIGH'
            elif score >= 40:
                record['ai_classification'] = 'COOL'
                record['ai_priority'] = 'MEDIUM'
            else:
                record['ai_classification'] = 'COLD'
                record['ai_priority'] = 'LOW'
        
        logger.info(f"Scored {len(data)} deals: {sum(1 for d in data if d['ai_score'] >= 60)} high-quality deals identified")
        return data


class AnomalyDetectionTransformer(Transformer):
    """
    Detect anomalies in data using statistical analysis and pattern recognition.
    
    Identifies unusual patterns that may indicate data quality issues,
    fraud, or significant business events.
    
    Example:
        >>> transformer = AnomalyDetectionTransformer(
        ...     fields=['amount', 'velocity', 'conversion_rate'],
        ...     sensitivity=2.0
        ... )
        >>> analyzed_data = transformer.transform(data)
    """
    
    def __init__(
        self,
        fields: List[str],
        sensitivity: float = 2.0,
        method: str = "zscore",
        name: Optional[str] = None,
    ):
        super().__init__(name or "AnomalyDetectionTransformer")
        self.fields = fields
        self.sensitivity = sensitivity  # Standard deviations for z-score
        self.method = method
    
    def _calculate_zscore(self, values: List[float]) -> List[float]:
        """Calculate z-scores for a list of values."""
        if not values or len(values) < 2:
            return [0.0] * len(values)
        
        mean = sum(values) / len(values)
        variance = sum((x - mean) ** 2 for x in values) / len(values)
        std_dev = variance ** 0.5
        
        if std_dev == 0:
            return [0.0] * len(values)
        
        return [(x - mean) / std_dev for x in values]
    
    def transform(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Detect and flag anomalies in the data."""
        logger.info(f"Analyzing {len(data)} records for anomalies")
        
        anomalies_detected = 0
        
        for field in self.fields:
            # Extract numeric values for this field
            values = []
            indices = []
            for i, record in enumerate(data):
                if field in record:
                    try:
                        val = float(record[field])
                        values.append(val)
                        indices.append(i)
                    except (ValueError, TypeError):
                        pass
            
            if not values:
                continue
            
            # Calculate z-scores
            zscores = self._calculate_zscore(values)
            
            # Flag anomalies
            for idx, zscore in zip(indices, zscores):
                if abs(zscore) > self.sensitivity:
                    if 'ai_anomalies' not in data[idx]:
                        data[idx]['ai_anomalies'] = []
                        data[idx]['ai_anomaly_detected'] = True
                    
                    data[idx]['ai_anomalies'].append({
                        'field': field,
                        'zscore': round(zscore, 2),
                        'severity': 'HIGH' if abs(zscore) > 3 else 'MEDIUM'
                    })
                    anomalies_detected += 1
        
        # Add anomaly flag to records without anomalies
        for record in data:
            if 'ai_anomaly_detected' not in record:
                record['ai_anomaly_detected'] = False
        
        logger.info(f"Detected {anomalies_detected} anomalies across {len(data)} records")
        return data


class SentimentAnalysisTransformer(Transformer):
    """
    Analyze sentiment in text fields (notes, emails, descriptions).
    
    Uses simple keyword-based sentiment analysis. Can be extended with
    NLP libraries like TextBlob or transformers.
    
    Example:
        >>> transformer = SentimentAnalysisTransformer(
        ...     text_fields=['notes', 'last_email'],
        ...     output_field='sentiment'
        ... )
        >>> enriched_data = transformer.transform(data)
    """
    
    def __init__(
        self,
        text_fields: List[str],
        output_field: str = "ai_sentiment",
        name: Optional[str] = None,
    ):
        super().__init__(name or "SentimentAnalysisTransformer")
        self.text_fields = text_fields
        self.output_field = output_field
        
        # Simple keyword-based sentiment
        self.positive_keywords = {
            'excellent', 'great', 'good', 'happy', 'satisfied', 'love', 'amazing',
            'fantastic', 'wonderful', 'perfect', 'excited', 'interested', 'ready',
            'yes', 'absolutely', 'definitely', 'agreed', 'approve', 'success'
        }
        self.negative_keywords = {
            'bad', 'poor', 'terrible', 'hate', 'angry', 'frustrated', 'disappointed',
            'unhappy', 'problem', 'issue', 'concern', 'worried', 'cancel', 'no',
            'reject', 'decline', 'denied', 'failed', 'loss', 'lost'
        }
    
    def _analyze_text(self, text: str) -> Dict[str, Any]:
        """Analyze sentiment of text."""
        if not text or not isinstance(text, str):
            return {'sentiment': 'neutral', 'score': 0.0, 'confidence': 0.0}
        
        text_lower = text.lower()
        words = text_lower.split()
        
        positive_count = sum(1 for word in words if word in self.positive_keywords)
        negative_count = sum(1 for word in words if word in self.negative_keywords)
        total_words = len(words)
        
        if total_words == 0:
            return {'sentiment': 'neutral', 'score': 0.0, 'confidence': 0.0}
        
        # Calculate sentiment score (-1 to 1)
        score = (positive_count - negative_count) / total_words
        
        # Determine sentiment
        if score > 0.05:
            sentiment = 'positive'
        elif score < -0.05:
            sentiment = 'negative'
        else:
            sentiment = 'neutral'
        
        confidence = min(abs(score) * 10, 1.0)
        
        return {
            'sentiment': sentiment,
            'score': round(score, 3),
            'confidence': round(confidence, 2)
        }
    
    def transform(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Add sentiment analysis to records."""
        logger.info(f"Analyzing sentiment for {len(data)} records")
        
        for record in data:
            # Combine all text fields
            combined_text = " ".join(
                str(record.get(field, "")) for field in self.text_fields
            )
            
            analysis = self._analyze_text(combined_text)
            record[self.output_field] = analysis
        
        sentiments = [r[self.output_field]['sentiment'] for r in data]
        logger.info(f"Sentiment distribution: "
                   f"Positive={sentiments.count('positive')}, "
                   f"Neutral={sentiments.count('neutral')}, "
                   f"Negative={sentiments.count('negative')}")
        
        return data


class ForecastTransformer(Transformer):
    """
    Generate forecasts based on historical data patterns.
    
    Uses simple time-series analysis for revenue forecasting.
    Can be extended with advanced ML models.
    
    Example:
        >>> transformer = ForecastTransformer(
        ...     date_field='close_date',
        ...     value_field='amount',
        ...     forecast_periods=3
        ... )
        >>> forecast_data = transformer.transform(historical_data)
    """
    
    def __init__(
        self,
        date_field: str,
        value_field: str,
        forecast_periods: int = 3,
        method: str = "moving_average",
        name: Optional[str] = None,
    ):
        super().__init__(name or "ForecastTransformer")
        self.date_field = date_field
        self.value_field = value_field
        self.forecast_periods = forecast_periods
        self.method = method
    
    def _moving_average(self, values: List[float], window: int = 3) -> float:
        """Calculate moving average."""
        if not values:
            return 0.0
        recent = values[-window:]
        return sum(recent) / len(recent)
    
    def _calculate_trend(self, values: List[float]) -> float:
        """Calculate trend coefficient."""
        if len(values) < 2:
            return 0.0
        
        n = len(values)
        x = list(range(n))
        y = values
        
        # Simple linear regression
        x_mean = sum(x) / n
        y_mean = sum(y) / n
        
        numerator = sum((x[i] - x_mean) * (y[i] - y_mean) for i in range(n))
        denominator = sum((x[i] - x_mean) ** 2 for i in range(n))
        
        if denominator == 0:
            return 0.0
        
        return numerator / denominator
    
    def transform(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Add forecast data to records."""
        logger.info(f"Generating {self.forecast_periods}-period forecast from {len(data)} historical records")
        
        # Extract and sort historical values
        historical = []
        for record in data:
            if self.value_field in record:
                try:
                    value = float(record[self.value_field])
                    historical.append(value)
                except (ValueError, TypeError):
                    pass
        
        if not historical:
            logger.warning("No historical data found for forecasting")
            return data
        
        # Generate forecast
        current_value = self._moving_average(historical)
        trend = self._calculate_trend(historical)
        
        forecasts = []
        for i in range(1, self.forecast_periods + 1):
            forecast_value = current_value + (trend * i)
            forecasts.append({
                'period': i,
                'forecast': round(forecast_value, 2),
                'confidence': round(max(0, 1 - (i * 0.15)), 2)  # Decreasing confidence
            })
        
        # Add forecast to all records (summary data)
        forecast_summary = {
            'ai_forecast': forecasts,
            'ai_forecast_trend': 'increasing' if trend > 0 else 'decreasing' if trend < 0 else 'stable',
            'ai_forecast_confidence': round(max(0, 1 - len(forecasts) * 0.1), 2)
        }
        
        for record in data:
            record.update(forecast_summary)
        
        total_forecast = sum(f['forecast'] for f in forecasts)
        logger.info(f"Generated forecast: {self.forecast_periods} periods, total=${total_forecast:,.0f}")
        
        return data


class SmartEnrichmentTransformer(Transformer):
    """
    Intelligently enrich records with computed fields and insights.
    
    Automatically derives useful fields from existing data using AI/ML logic.
    
    Example:
        >>> transformer = SmartEnrichmentTransformer(
        ...     enrichment_rules=['calculate_velocity', 'predict_close_date', 'score_engagement']
        ... )
        >>> enriched_data = transformer.transform(data)
    """
    
    def __init__(
        self,
        enrichment_rules: Optional[List[str]] = None,
        custom_enrichers: Optional[Dict[str, Callable]] = None,
        name: Optional[str] = None,
    ):
        super().__init__(name or "SmartEnrichmentTransformer")
        self.enrichment_rules = enrichment_rules or ['all']
        self.custom_enrichers = custom_enrichers or {}
    
    def _calculate_deal_velocity(self, record: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate deal velocity metrics."""
        enrichments = {}
        
        if 'created_date' in record and 'amount' in record:
            # Simple velocity calculation
            try:
                amount = float(record['amount'])
                # Assume deals move through stages
                enrichments['ai_velocity'] = 'high' if amount > 100000 else 'medium' if amount > 50000 else 'low'
                enrichments['ai_priority_score'] = min(amount / 10000, 10.0)
            except (ValueError, TypeError):
                pass
        
        return enrichments
    
    def _predict_close_probability(self, record: Dict[str, Any]) -> Dict[str, Any]:
        """Predict probability of deal closing."""
        enrichments = {}
        
        factors = {
            'amount': record.get('amount', 0),
            'stage': record.get('stage', ''),
            'days_open': record.get('days_open', 0),
        }
        
        # Simple probability model
        stage_probs = {
            'prospecting': 0.1,
            'qualification': 0.3,
            'proposal': 0.5,
            'negotiation': 0.7,
            'closed_won': 1.0,
        }
        
        stage = str(factors['stage']).lower().replace(' ', '_')
        base_prob = stage_probs.get(stage, 0.3)
        
        # Adjust for age
        days_open = factors.get('days_open', 30)
        age_factor = max(0.5, 1 - (days_open / 180))
        
        close_probability = base_prob * age_factor
        enrichments['ai_close_probability'] = round(close_probability, 2)
        enrichments['ai_risk_level'] = 'HIGH' if close_probability < 0.3 else 'MEDIUM' if close_probability < 0.6 else 'LOW'
        
        return enrichments
    
    def _generate_insights(self, record: Dict[str, Any]) -> Dict[str, Any]:
        """Generate actionable insights."""
        enrichments = {}
        insights = []
        
        # Check for stalled deals
        if record.get('days_in_stage', 0) > 30:
            insights.append("Deal has been in current stage for over 30 days - consider reaching out")
        
        # Check for high-value opportunities
        if record.get('amount', 0) > 100000:
            insights.append("High-value opportunity - prioritize for executive involvement")
        
        # Check for engagement
        if record.get('last_activity_days', 999) > 14:
            insights.append("No activity in 14+ days - risk of going cold")
        
        enrichments['ai_insights'] = insights
        enrichments['ai_insight_count'] = len(insights)
        
        return enrichments
    
    def transform(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Enrich records with AI-powered insights."""
        logger.info(f"Enriching {len(data)} records with AI insights")
        
        enrichment_functions = {
            'calculate_velocity': self._calculate_deal_velocity,
            'predict_close_probability': self._predict_close_probability,
            'generate_insights': self._generate_insights,
        }
        enrichment_functions.update(self.custom_enrichers)
        
        total_enrichments = 0
        
        for record in data:
            record_enrichments = {}
            
            # Apply selected enrichment rules
            rules = self.enrichment_rules if 'all' not in self.enrichment_rules else enrichment_functions.keys()
            
            for rule in rules:
                if rule in enrichment_functions:
                    enrichments = enrichment_functions[rule](record)
                    record_enrichments.update(enrichments)
                    total_enrichments += len(enrichments)
            
            record.update(record_enrichments)
        
        logger.info(f"Added {total_enrichments} AI-powered enrichments to {len(data)} records")
        return data

