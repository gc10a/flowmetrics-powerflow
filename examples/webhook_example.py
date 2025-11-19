"""
Webhook integration example.

This example shows how to send pipeline results to a webhook endpoint.
"""

from powerflow import (
    Pipeline,
    CSVSource,
    FilterTransformer,
    MapTransformer,
)
from powerflow.integrations.webhook import WebhookDestination


def main():
    # Create pipeline
    pipeline = Pipeline(name="Webhook Notification Pipeline")
    
    # Read deals
    pipeline.add_stage(
        CSVSource("examples/data/deals.csv")
    )
    
    # Filter for very high-value deals
    pipeline.add_stage(
        FilterTransformer(
            lambda deal: float(deal.get("amount", 0)) > 100000,
            name="Filter Very High Value Deals"
        )
    )
    
    # Format for webhook
    pipeline.add_stage(
        MapTransformer(
            lambda deal: {
                "deal_id": deal.get("deal_id"),
                "amount": float(deal.get("amount", 0)),
                "company": deal.get("company"),
                "alert_type": "HIGH_VALUE_DEAL",
                "priority": "URGENT",
            },
            name="Format Alert Data"
        )
    )
    
    # Send to webhook (replace with your webhook URL)
    pipeline.add_stage(
        WebhookDestination(
            url="https://hooks.example.com/alerts",
            headers={"Authorization": "Bearer your-token-here"},
            batch_size=10,
        )
    )
    
    # Run the pipeline
    result = pipeline.run()
    
    print(f"\nSent {result.metadata['record_count']} alerts")


if __name__ == "__main__":
    main()

