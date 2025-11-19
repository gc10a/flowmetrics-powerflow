"""
AI-powered anomaly detection example.

This example shows how to detect unusual patterns in your revenue data
using PowerFlow's AI anomaly detection.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from powerflow import Pipeline, GeneratorSource, ConsoleDestination
from powerflow.ai import AnomalyDetectionTransformer


def generate_revenue_data():
    """Generate sample revenue data with some anomalies."""
    return [
        {'month': '2025-01', 'revenue': 100000, 'deals': 10, 'conversion_rate': 0.25},
        {'month': '2025-02', 'revenue': 105000, 'deals': 11, 'conversion_rate': 0.26},
        {'month': '2025-03', 'revenue': 98000, 'deals': 9, 'conversion_rate': 0.24},
        {'month': '2025-04', 'revenue': 102000, 'deals': 10, 'conversion_rate': 0.25},
        {'month': '2025-05', 'revenue': 250000, 'deals': 10, 'conversion_rate': 0.25},  # Anomaly: spike
        {'month': '2025-06', 'revenue': 103000, 'deals': 11, 'conversion_rate': 0.26},
        {'month': '2025-07', 'revenue': 107000, 'deals': 12, 'conversion_rate': 0.27},
        {'month': '2025-08', 'revenue': 35000, 'deals': 10, 'conversion_rate': 0.08},   # Anomaly: drop
        {'month': '2025-09', 'revenue': 104000, 'deals': 10, 'conversion_rate': 0.25},
        {'month': '2025-10', 'revenue': 109000, 'deals': 11, 'conversion_rate': 0.26},
    ]


def main():
    print("\n" + "="*80)
    print("AI-POWERED ANOMALY DETECTION DEMO")
    print("="*80)
    
    # Create pipeline
    pipeline = Pipeline(name="Anomaly Detection Pipeline")
    
    # Load data
    pipeline.add_stage(GeneratorSource(generate_revenue_data))
    
    # Detect anomalies
    pipeline.add_stage(
        AnomalyDetectionTransformer(
            fields=['revenue', 'conversion_rate'],
            sensitivity=2.0,  # 2 standard deviations
            name="AI Anomaly Detector"
        )
    )
    
    # Display results
    pipeline.add_stage(ConsoleDestination(limit=None, pretty=True))
    
    # Run pipeline
    result = pipeline.run()
    
    # Analyze anomalies
    print("\n" + "="*80)
    print("ANOMALY ANALYSIS")
    print("="*80)
    
    data = result.data
    anomalies = [d for d in data if d.get('ai_anomaly_detected')]
    
    if anomalies:
        print(f"\n⚠️  Detected {len(anomalies)} anomalies:\n")
        for record in anomalies:
            print(f"📅 {record['month']}:")
            for anomaly in record.get('ai_anomalies', []):
                print(f"   • {anomaly['field']}: Z-score = {anomaly['zscore']} ({anomaly['severity']} severity)")
            print(f"   Revenue: ${record['revenue']:,}")
            print(f"   Conversion: {record['conversion_rate']:.1%}")
            print()
        
        print("💡 Recommendations:")
        print("   1. Investigate the cause of anomalies")
        print("   2. Verify data accuracy")
        print("   3. Look for seasonal patterns or one-time events")
        print("   4. Adjust forecasts if needed")
    else:
        print("\n✅ No anomalies detected - data looks healthy!")
    
    print("\n" + "="*80 + "\n")


if __name__ == "__main__":
    main()

