"""
AI-powered analyzers for generating insights from pipeline data.
"""

from typing import Any, Dict, List, Optional
import logging
from datetime import datetime, timedelta

logger = logging.getLogger("powerflow.ai")


class RevenueInsightAnalyzer:
    """
    Generate AI-powered insights from revenue data.
    
    Analyzes patterns, trends, and anomalies to provide actionable insights.
    
    Example:
        >>> analyzer = RevenueInsightAnalyzer()
        >>> insights = analyzer.analyze(pipeline_context.data)
        >>> print(insights['summary'])
    """
    
    def __init__(self):
        self.insights = []
    
    def analyze(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze data and generate insights."""
        logger.info(f"Generating AI insights from {len(data)} records")
        
        insights = {
            'summary': self._generate_summary(data),
            'trends': self._identify_trends(data),
            'recommendations': self._generate_recommendations(data),
            'risk_factors': self._identify_risks(data),
            'opportunities': self._identify_opportunities(data),
        }
        
        return insights
    
    def _generate_summary(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate executive summary."""
        total_revenue = sum(float(r.get('amount', 0)) for r in data)
        avg_deal_size = total_revenue / len(data) if data else 0
        
        high_value_deals = sum(1 for r in data if float(r.get('amount', 0)) > 100000)
        
        return {
            'total_records': len(data),
            'total_revenue': round(total_revenue, 2),
            'average_deal_size': round(avg_deal_size, 2),
            'high_value_deals': high_value_deals,
            'quality_score': round((high_value_deals / len(data) * 100) if data else 0, 2)
        }
    
    def _identify_trends(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Identify trends in the data."""
        trends = []
        
        # Revenue trend
        amounts = [float(r.get('amount', 0)) for r in data]
        if amounts:
            avg = sum(amounts) / len(amounts)
            recent_avg = sum(amounts[-10:]) / min(10, len(amounts))
            
            if recent_avg > avg * 1.2:
                trends.append({
                    'type': 'revenue_increase',
                    'description': 'Recent deals are 20%+ above average',
                    'impact': 'positive',
                    'confidence': 0.85
                })
            elif recent_avg < avg * 0.8:
                trends.append({
                    'type': 'revenue_decrease',
                    'description': 'Recent deals are 20%+ below average',
                    'impact': 'negative',
                    'confidence': 0.85
                })
        
        return trends
    
    def _generate_recommendations(self, data: List[Dict[str, Any]]) -> List[str]:
        """Generate actionable recommendations."""
        recommendations = []
        
        if not data:
            return ["No data available for recommendations"]
        
        # Check deal distribution
        high_value = sum(1 for r in data if float(r.get('amount', 0)) > 100000)
        if high_value / len(data) < 0.2:
            recommendations.append(
                "Consider focusing on larger deals - only {:.0%} of pipeline is high-value".format(high_value / len(data))
            )
        
        # Check for stalled deals
        stalled = sum(1 for r in data if r.get('days_in_stage', 0) > 45)
        if stalled > 0:
            recommendations.append(
                f"Review {stalled} deals that have been stalled for 45+ days"
            )
        
        # Suggest prioritization
        if high_value > 0:
            recommendations.append(
                f"Prioritize {high_value} high-value deals for maximum revenue impact"
            )
        
        return recommendations
    
    def _identify_risks(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Identify risk factors."""
        risks = []
        
        # Check for concentration risk
        total_value = sum(float(r.get('amount', 0)) for r in data)
        if total_value > 0:
            top_deals = sorted(data, key=lambda x: float(x.get('amount', 0)), reverse=True)[:3]
            top_3_value = sum(float(d.get('amount', 0)) for d in top_deals)
            
            if top_3_value / total_value > 0.5:
                risks.append({
                    'type': 'concentration',
                    'severity': 'HIGH',
                    'description': f'Top 3 deals represent {top_3_value/total_value:.0%} of pipeline',
                    'mitigation': 'Diversify pipeline with more mid-sized deals'
                })
        
        return risks
    
    def _identify_opportunities(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Identify opportunities."""
        opportunities = []
        
        # Hot deals
        hot_deals = [r for r in data if r.get('ai_classification') == 'HOT']
        if hot_deals:
            total_value = sum(float(d.get('amount', 0)) for d in hot_deals)
            opportunities.append({
                'type': 'high_probability_deals',
                'count': len(hot_deals),
                'value': round(total_value, 2),
                'description': f'{len(hot_deals)} high-probability deals worth ${total_value:,.0f}',
                'action': 'Focus resources on closing these deals this quarter'
            })
        
        return opportunities


class ChurnPredictionAnalyzer:
    """
    Predict customer churn risk using AI analysis.
    
    Identifies accounts at risk of churning based on engagement patterns.
    
    Example:
        >>> analyzer = ChurnPredictionAnalyzer()
        >>> predictions = analyzer.predict(customer_data)
    """
    
    def __init__(self, risk_threshold: float = 0.6):
        self.risk_threshold = risk_threshold
    
    def predict(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Predict churn risk for accounts."""
        logger.info(f"Analyzing churn risk for {len(data)} accounts")
        
        predictions = []
        
        for record in data:
            risk_score = self._calculate_churn_risk(record)
            
            prediction = {
                'account_id': record.get('id'),
                'churn_risk_score': round(risk_score, 2),
                'risk_level': 'HIGH' if risk_score > 0.7 else 'MEDIUM' if risk_score > 0.4 else 'LOW',
                'factors': self._identify_risk_factors(record),
                'recommended_actions': self._recommend_actions(risk_score, record)
            }
            
            predictions.append(prediction)
        
        high_risk = sum(1 for p in predictions if p['risk_level'] == 'HIGH')
        logger.info(f"Identified {high_risk} high-risk accounts")
        
        return predictions
    
    def _calculate_churn_risk(self, record: Dict[str, Any]) -> float:
        """Calculate churn risk score."""
        risk_score = 0.0
        
        # Factor: Last activity
        last_activity = record.get('last_activity_days', 0)
        if last_activity > 60:
            risk_score += 0.4
        elif last_activity > 30:
            risk_score += 0.2
        
        # Factor: Support tickets
        support_tickets = record.get('support_tickets', 0)
        if support_tickets > 5:
            risk_score += 0.3
        
        # Factor: Engagement score
        engagement = record.get('engagement_score', 50)
        if engagement < 30:
            risk_score += 0.3
        
        # Factor: Contract renewal proximity
        days_to_renewal = record.get('days_to_renewal', 365)
        if days_to_renewal < 90:
            risk_score += 0.2
        
        return min(risk_score, 1.0)
    
    def _identify_risk_factors(self, record: Dict[str, Any]) -> List[str]:
        """Identify specific risk factors."""
        factors = []
        
        if record.get('last_activity_days', 0) > 30:
            factors.append('Low engagement - no activity in 30+ days')
        
        if record.get('support_tickets', 0) > 5:
            factors.append('High support ticket volume')
        
        if record.get('engagement_score', 50) < 30:
            factors.append('Poor engagement score')
        
        if record.get('days_to_renewal', 365) < 90:
            factors.append('Contract renewal approaching')
        
        return factors
    
    def _recommend_actions(self, risk_score: float, record: Dict[str, Any]) -> List[str]:
        """Recommend actions to reduce churn risk."""
        actions = []
        
        if risk_score > 0.7:
            actions.append('Schedule executive business review immediately')
            actions.append('Assign dedicated success manager')
        
        if record.get('last_activity_days', 0) > 30:
            actions.append('Reach out to re-engage')
        
        if record.get('support_tickets', 0) > 5:
            actions.append('Review and resolve outstanding support issues')
        
        return actions


class DealVelocityAnalyzer:
    """
    Analyze deal velocity and pipeline health.
    
    Provides insights on how quickly deals move through the pipeline.
    
    Example:
        >>> analyzer = DealVelocityAnalyzer()
        >>> velocity_metrics = analyzer.analyze(pipeline_data)
    """
    
    def __init__(self):
        pass
    
    def analyze(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze deal velocity metrics."""
        logger.info(f"Analyzing deal velocity for {len(data)} deals")
        
        metrics = {
            'average_velocity': self._calculate_avg_velocity(data),
            'by_stage': self._velocity_by_stage(data),
            'bottlenecks': self._identify_bottlenecks(data),
            'fast_moving_deals': self._identify_fast_movers(data),
            'recommendations': self._velocity_recommendations(data)
        }
        
        return metrics
    
    def _calculate_avg_velocity(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate average deal velocity."""
        velocities = []
        
        for record in data:
            days_open = record.get('days_open', 0)
            amount = float(record.get('amount', 0))
            
            if days_open > 0 and amount > 0:
                velocity = amount / days_open
                velocities.append(velocity)
        
        if velocities:
            avg_velocity = sum(velocities) / len(velocities)
        else:
            avg_velocity = 0
        
        return {
            'average_daily_velocity': round(avg_velocity, 2),
            'deals_analyzed': len(velocities)
        }
    
    def _velocity_by_stage(self, data: List[Dict[str, Any]]) -> Dict[str, float]:
        """Calculate velocity by stage."""
        stage_times = {}
        
        for record in data:
            stage = record.get('stage', 'unknown')
            days_in_stage = record.get('days_in_stage', 0)
            
            if stage not in stage_times:
                stage_times[stage] = []
            stage_times[stage].append(days_in_stage)
        
        return {
            stage: round(sum(times) / len(times), 1)
            for stage, times in stage_times.items()
        }
    
    def _identify_bottlenecks(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Identify bottlenecks in the pipeline."""
        stage_times = self._velocity_by_stage(data)
        
        bottlenecks = []
        for stage, avg_time in stage_times.items():
            if avg_time > 30:  # More than 30 days
                bottlenecks.append({
                    'stage': stage,
                    'average_days': avg_time,
                    'severity': 'HIGH' if avg_time > 60 else 'MEDIUM'
                })
        
        return bottlenecks
    
    def _identify_fast_movers(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Identify fast-moving deals."""
        fast_movers = []
        
        for record in data:
            days_open = record.get('days_open', 0)
            amount = float(record.get('amount', 0))
            
            if 0 < days_open < 30 and amount > 50000:
                fast_movers.append({
                    'id': record.get('id'),
                    'amount': amount,
                    'days_open': days_open,
                    'velocity': round(amount / days_open, 2)
                })
        
        return sorted(fast_movers, key=lambda x: x['velocity'], reverse=True)[:10]
    
    def _velocity_recommendations(self, data: List[Dict[str, Any]]) -> List[str]:
        """Generate velocity improvement recommendations."""
        recommendations = []
        
        bottlenecks = self._identify_bottlenecks(data)
        if bottlenecks:
            for bottleneck in bottlenecks[:3]:
                recommendations.append(
                    f"Address {bottleneck['stage']} stage - avg {bottleneck['average_days']:.0f} days"
                )
        
        return recommendations

