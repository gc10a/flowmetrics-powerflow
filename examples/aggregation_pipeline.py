"""
Aggregation pipeline example.

This example demonstrates how to aggregate revenue data by region and stage.
"""

from powerflow import (
    Pipeline,
    CSVSource,
    AggregateTransformer,
    MapTransformer,
    CSVDestination,
)


def main():
    # Create a pipeline
    pipeline = Pipeline(name="Revenue Aggregation Pipeline")
    
    # Read deals from CSV
    pipeline.add_stage(
        CSVSource("examples/data/deals.csv")
    )
    
    # Convert amount to float
    pipeline.add_stage(
        MapTransformer(
            lambda deal: {
                **deal,
                "amount": float(deal.get("amount", 0))
            },
            name="Convert Amount to Float"
        )
    )
    
    # Aggregate by region
    pipeline.add_stage(
        AggregateTransformer(
            group_by=["region"],
            aggregations={
                "amount": "sum",
                "deal_id": "count",
            },
            name="Aggregate by Region"
        )
    )
    
    # Calculate average deal size
    pipeline.add_stage(
        MapTransformer(
            lambda record: {
                **record,
                "avg_deal_size": record["amount_sum"] / record["deal_id_count"]
                    if record["deal_id_count"] > 0 else 0
            },
            name="Calculate Average Deal Size"
        )
    )
    
    # Save results
    pipeline.add_stage(
        CSVDestination("output/revenue_by_region.csv")
    )
    
    # Run the pipeline
    result = pipeline.run()
    
    print(f"\nProcessed {result.metadata['record_count']} regions")


if __name__ == "__main__":
    main()

