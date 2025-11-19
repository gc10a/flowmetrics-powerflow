"""
Basic PowerFlow pipeline example.

This example shows how to create a simple pipeline that reads from a CSV file,
filters and transforms the data, and writes to a JSON file.
"""

from powerflow import (
    Pipeline,
    CSVSource,
    FilterTransformer,
    MapTransformer,
    JSONDestination,
    ConsoleDestination,
)


def main():
    # Create a pipeline
    pipeline = Pipeline(name="Revenue Analysis Pipeline")
    
    # Add stages
    pipeline.add_stage(
        CSVSource("examples/data/deals.csv")
    )
    
    # Filter for high-value deals
    pipeline.add_stage(
        FilterTransformer(
            lambda deal: float(deal.get("amount", 0)) > 10000,
            name="Filter High Value Deals"
        )
    )
    
    # Transform and enrich data
    pipeline.add_stage(
        MapTransformer(
            lambda deal: {
                **deal,
                "amount_usd": float(deal.get("amount", 0)),
                "priority": "HIGH" if float(deal.get("amount", 0)) > 50000 else "MEDIUM",
            },
            name="Enrich Deal Data"
        )
    )
    
    # Output to console (for debugging)
    pipeline.add_stage(
        ConsoleDestination(limit=5)
    )
    
    # Save to JSON
    pipeline.add_stage(
        JSONDestination("output/high_value_deals.json")
    )
    
    # Run the pipeline
    result = pipeline.run()
    
    # Print statistics
    print("\nPipeline Statistics:")
    stats = result.get_stats()
    print(f"  Duration: {stats['duration']:.2f}s")
    print(f"  Records: {stats['record_count']}")
    print(f"  Errors: {stats['error_count']}")


if __name__ == "__main__":
    main()

