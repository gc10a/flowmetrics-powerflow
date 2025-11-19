"""
AI-powered deal scoring example.

This example shows how to use PowerFlow's AI module to automatically
score and prioritize deals based on multiple factors.
"""

import sys
from pathlib import Path

# Add powerflow to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from powerflow import Pipeline, GeneratorSource, ConsoleDestination
from powerflow.ai import DealScoringTransformer, SmartEnrichmentTransformer


def generate_sample_deals():
    """Generate sample deal data."""
    return [
        {
            'id': 'D001',
            'company': 'Acme Corp',
            'amount': 45000,
            'stage': 'negotiation',
            'days_in_stage': 12,
            'days_open': 45,
            'engagement_score': 75,
            'company_size': 500,
            'last_activity_days': 2
        },
        {
            'id': 'D002',
            'company': 'TechStart Inc',
            'amount': 125000,
            'stage': 'proposal',
            'days_in_stage': 8,
            'days_open': 30,
            'engagement_score': 90,
            'company_size': 1200,
            'last_activity_days': 1
        },
        {
            'id': 'D003',
            'company': 'Global Systems',
            'amount': 8500,
            'stage': 'prospecting',
            'days_in_stage': 45,
            'days_open': 60,
            'engagement_score': 30,
            'company_size': 150,
            'last_activity_days': 30
        },
        {
            'id': 'D004',
            'company': 'Enterprise Solutions',
            'amount': 250000,
            'stage': 'negotiation',
            'days_in_stage': 5,
            'days_open': 25,
            'engagement_score': 95,
            'company_size': 5000,
            'last_activity_days': 1
        },
        {
            'id': 'D005',
            'company': 'StartupXYZ',
            'amount': 15000,
            'stage': 'qualification',
            'days_in_stage': 30,
            'days_open': 50,
            'engagement_score': 45,
            'company_size': 50,
            'last_activity_days': 20
        },
    ]


def main():
    print("\n" + "="*80)
    print("AI-POWERED DEAL SCORING DEMO")
    print("="*80)
    
    # Create pipeline with AI transformers
    pipeline = Pipeline(name="AI Deal Scoring Pipeline")
    
    # Generate sample deals
    pipeline.add_stage(GeneratorSource(generate_sample_deals))
    
    # Apply AI deal scoring
    pipeline.add_stage(
        DealScoringTransformer(
            factors=['amount', 'stage', 'days_in_stage', 'engagement_score', 'company_size'],
            name="AI Deal Scorer"
        )
    )
    
    # Add smart enrichments
    pipeline.add_stage(
        SmartEnrichmentTransformer(
            enrichment_rules=['predict_close_probability', 'generate_insights'],
            name="Smart Enrichment"
        )
    )
    
    # Display results
    pipeline.add_stage(ConsoleDestination(limit=10, pretty=True))
    
    # Run pipeline
    result = pipeline.run()
    
    # Analyze results
    print("\n" + "="*80)
    print("ANALYSIS SUMMARY")
    print("="*80)
    
    deals = result.data
    hot_deals = [d for d in deals if d.get('ai_classification') == 'HOT']
    warm_deals = [d for d in deals if d.get('ai_classification') == 'WARM']
    cool_deals = [d for d in deals if d.get('ai_classification') == 'COOL']
    cold_deals = [d for d in deals if d.get('ai_classification') == 'COLD']
    
    print(f"\nDeal Classification:")
    print(f"  🔥 HOT:  {len(hot_deals)} deals - Focus here for quick wins!")
    print(f"  ☀️  WARM: {len(warm_deals)} deals - Good potential")
    print(f"  🌤️  COOL: {len(cool_deals)} deals - Needs nurturing")
    print(f"  ❄️  COLD: {len(cold_deals)} deals - Re-evaluate or disqualify")
    
    # Show top deals
    if hot_deals:
        print(f"\n🎯 Top Priority Deals:")
        for deal in sorted(hot_deals, key=lambda x: x['ai_score'], reverse=True):
            print(f"  • {deal['company']}: ${deal['amount']:,} (Score: {deal['ai_score']}/100)")
            if 'ai_insights' in deal and deal['ai_insights']:
                for insight in deal['ai_insights'][:2]:
                    print(f"    → {insight}")
    
    # Revenue potential
    total_revenue = sum(d['amount'] for d in deals)
    hot_revenue = sum(d['amount'] for d in hot_deals)
    
    print(f"\n💰 Revenue Analysis:")
    print(f"  Total Pipeline: ${total_revenue:,}")
    print(f"  High-Probability: ${hot_revenue:,} ({hot_revenue/total_revenue*100:.1f}%)")
    
    print("\n" + "="*80)
    print("✨ AI analysis complete! Use these insights to prioritize your efforts.")
    print("="*80 + "\n")


if __name__ == "__main__":
    main()

