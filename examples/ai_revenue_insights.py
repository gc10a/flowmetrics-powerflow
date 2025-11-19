"""
AI-powered revenue insights example.

This example shows how to generate intelligent insights from your
revenue data using PowerFlow's AI analyzers.
"""

import sys
from pathlib import Path
import json

sys.path.insert(0, str(Path(__file__).parent.parent))

from powerflow import Pipeline, CSVSource
from powerflow.ai import DealScoringTransformer
from powerflow.ai.analyzers import RevenueInsightAnalyzer


def main():
    print("\n" + "="*80)
    print("AI-POWERED REVENUE INSIGHTS DEMO")
    print("="*80)
    
    # Create pipeline
    pipeline = Pipeline(name="Revenue Insights Pipeline")
    
    # Load deals from CSV
    pipeline.add_stage(CSVSource("examples/data/deals.csv"))
    
    # Score deals with AI
    pipeline.add_stage(
        DealScoringTransformer(
            factors=['amount', 'stage', 'region'],
            name="AI Deal Scorer"
        )
    )
    
    # Run pipeline
    result = pipeline.run()
    
    # Generate AI insights
    print("\n" + "="*80)
    print("GENERATING AI INSIGHTS...")
    print("="*80)
    
    analyzer = RevenueInsightAnalyzer()
    insights = analyzer.analyze(result.data)
    
    # Display insights
    print("\n📊 EXECUTIVE SUMMARY")
    print("-" * 80)
    summary = insights['summary']
    print(f"  Total Deals: {summary['total_records']}")
    print(f"  Total Revenue: ${summary['total_revenue']:,.0f}")
    print(f"  Average Deal Size: ${summary['average_deal_size']:,.0f}")
    print(f"  High-Value Deals: {summary['high_value_deals']}")
    print(f"  Pipeline Quality Score: {summary['quality_score']}/100")
    
    # Trends
    if insights['trends']:
        print("\n📈 TRENDS IDENTIFIED")
        print("-" * 80)
        for trend in insights['trends']:
            icon = "🟢" if trend['impact'] == 'positive' else "🔴"
            print(f"  {icon} {trend['description']}")
            print(f"     Confidence: {trend['confidence']:.0%}")
    
    # Recommendations
    if insights['recommendations']:
        print("\n💡 AI RECOMMENDATIONS")
        print("-" * 80)
        for i, rec in enumerate(insights['recommendations'], 1):
            print(f"  {i}. {rec}")
    
    # Risks
    if insights['risk_factors']:
        print("\n⚠️  RISK FACTORS")
        print("-" * 80)
        for risk in insights['risk_factors']:
            print(f"  🔴 {risk['severity']}: {risk['description']}")
            print(f"     Mitigation: {risk['mitigation']}")
    
    # Opportunities
    if insights['opportunities']:
        print("\n🎯 OPPORTUNITIES")
        print("-" * 80)
        for opp in insights['opportunities']:
            print(f"  • {opp['description']}")
            print(f"    Action: {opp['action']}")
    
    # Deal Classification Summary
    print("\n🔥 DEAL CLASSIFICATION")
    print("-" * 80)
    hot = sum(1 for d in result.data if d.get('ai_classification') == 'HOT')
    warm = sum(1 for d in result.data if d.get('ai_classification') == 'WARM')
    cool = sum(1 for d in result.data if d.get('ai_classification') == 'COOL')
    cold = sum(1 for d in result.data if d.get('ai_classification') == 'COLD')
    
    print(f"  🔥 HOT:  {hot} deals ({hot/len(result.data)*100:.0f}%)")
    print(f"  ☀️  WARM: {warm} deals ({warm/len(result.data)*100:.0f}%)")
    print(f"  🌤️  COOL: {cool} deals ({cool/len(result.data)*100:.0f}%)")
    print(f"  ❄️  COLD: {cold} deals ({cold/len(result.data)*100:.0f}%)")
    
    print("\n" + "="*80)
    print("✨ AI analysis complete! Use these insights to drive your revenue strategy.")
    print("="*80 + "\n")


if __name__ == "__main__":
    main()

