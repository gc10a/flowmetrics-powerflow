#!/usr/bin/env python3
"""
Quick demo of PowerFlow.

This script demonstrates basic PowerFlow functionality without requiring installation.
"""

import sys
from pathlib import Path

# Add powerflow to path for demo purposes
sys.path.insert(0, str(Path(__file__).parent))

from powerflow import (
    Pipeline,
    GeneratorSource,
    FilterTransformer,
    MapTransformer,
    AggregateTransformer,
    ConsoleDestination,
)


def generate_sample_deals():
    """Generate sample deal data."""
    return [
        {'id': 'D001', 'company': 'Acme Corp', 'amount': 45000, 'region': 'North America'},
        {'id': 'D002', 'company': 'TechStart Inc', 'amount': 125000, 'region': 'Europe'},
        {'id': 'D003', 'company': 'Global Systems', 'amount': 8500, 'region': 'Asia'},
        {'id': 'D004', 'company': 'Enterprise Solutions', 'amount': 250000, 'region': 'North America'},
        {'id': 'D005', 'company': 'DataFlow LLC', 'amount': 75000, 'region': 'Europe'},
        {'id': 'D006', 'company': 'CloudTech', 'amount': 15000, 'region': 'North America'},
        {'id': 'D007', 'company': 'StartupXYZ', 'amount': 5000, 'region': 'Asia'},
        {'id': 'D008', 'company': 'MegaCorp', 'amount': 500000, 'region': 'North America'},
    ]


def demo_basic_pipeline():
    """Demo: Basic filtering and transformation."""
    print("\n" + "="*80)
    print("DEMO 1: Basic Pipeline - Filter High-Value Deals")
    print("="*80)
    
    pipeline = Pipeline(name="High Value Deals Filter")
    
    # Generate sample data
    pipeline.add_stage(GeneratorSource(generate_sample_deals))
    
    # Filter for high-value deals (> $50k)
    pipeline.add_stage(
        FilterTransformer(
            lambda deal: deal['amount'] > 50000,
            name="Filter > $50k"
        )
    )
    
    # Add priority flag
    pipeline.add_stage(
        MapTransformer(
            lambda deal: {
                **deal,
                'priority': 'URGENT' if deal['amount'] > 200000 else 'HIGH',
                'amount_str': f"${deal['amount']:,}"
            },
            name="Add Priority"
        )
    )
    
    # Show results
    pipeline.add_stage(ConsoleDestination(limit=10, pretty=True))
    
    result = pipeline.run()
    
    print(f"\n✅ Processed {result.metadata['record_count']} high-value deals")


def demo_aggregation_pipeline():
    """Demo: Revenue aggregation by region."""
    print("\n" + "="*80)
    print("DEMO 2: Aggregation Pipeline - Revenue by Region")
    print("="*80)
    
    pipeline = Pipeline(name="Revenue by Region")
    
    # Generate sample data
    pipeline.add_stage(GeneratorSource(generate_sample_deals))
    
    # Aggregate by region
    pipeline.add_stage(
        AggregateTransformer(
            group_by=['region'],
            aggregations={
                'amount': 'sum',
                'id': 'count',
            },
            name="Aggregate by Region"
        )
    )
    
    # Format output
    pipeline.add_stage(
        MapTransformer(
            lambda record: {
                'region': record['region'],
                'total_revenue': f"${record['amount_sum']:,}",
                'deal_count': record['id_count'],
                'avg_deal_size': f"${record['amount_sum'] / record['id_count']:,.0f}",
            },
            name="Format Output"
        )
    )
    
    # Show results
    pipeline.add_stage(ConsoleDestination(limit=10, pretty=True))
    
    result = pipeline.run()
    
    print(f"\n✅ Analyzed {result.metadata['record_count']} regions")


def demo_pipeline_with_hooks():
    """Demo: Pipeline with hooks for monitoring."""
    print("\n" + "="*80)
    print("DEMO 3: Pipeline with Hooks - Monitoring & Logging")
    print("="*80)
    
    # Track stage execution
    stage_info = []
    
    def log_stage(pipeline, context, stage):
        """Log stage completion."""
        stage_info.append({
            'stage': stage.name,
            'record_count': len(context.data)
        })
    
    pipeline = Pipeline(name="Monitored Pipeline")
    pipeline.add_hook("post_stage", log_stage)
    
    # Build pipeline
    pipeline.add_stage(GeneratorSource(generate_sample_deals))
    pipeline.add_stage(
        FilterTransformer(lambda d: d['amount'] > 20000, name="Filter > $20k")
    )
    pipeline.add_stage(
        MapTransformer(lambda d: {**d, 'size': 'Large'}, name="Tag as Large")
    )
    
    result = pipeline.run()
    
    # Show monitoring info
    print("\n📊 Stage Execution Summary:")
    for info in stage_info:
        print(f"  • {info['stage']}: {info['record_count']} records")


def main():
    """Run all demos."""
    print("\n" + "🚀"*40)
    print(" "*20 + "PowerFlow Demo")
    print(" "*10 + "A Python Framework for Revenue Operations Pipelines")
    print("🚀"*40)
    
    try:
        demo_basic_pipeline()
        demo_aggregation_pipeline()
        demo_pipeline_with_hooks()
        
        print("\n" + "="*80)
        print("✨ All demos completed successfully!")
        print("="*80)
        print("\nNext steps:")
        print("  1. Check out examples/ directory for more use cases")
        print("  2. Read the README.md for full documentation")
        print("  3. Install with: pip install -e .")
        print("  4. Run tests with: pytest tests/")
        print("\n")
        
    except Exception as e:
        print(f"\n❌ Error running demo: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

