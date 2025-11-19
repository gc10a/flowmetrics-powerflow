"""
Salesforce integration example.

This example shows how to fetch opportunities from Salesforce and analyze them.

NOTE: You'll need to set up Salesforce credentials to run this example.
Set these environment variables:
  - SALESFORCE_USERNAME
  - SALESFORCE_PASSWORD
  - SALESFORCE_SECURITY_TOKEN
"""

import os
from powerflow import (
    Pipeline,
    SalesforceSource,
    FilterTransformer,
    AggregateTransformer,
    CSVDestination,
)


def main():
    # Get credentials from environment
    username = os.getenv("SALESFORCE_USERNAME")
    password = os.getenv("SALESFORCE_PASSWORD")
    security_token = os.getenv("SALESFORCE_SECURITY_TOKEN")
    
    if not all([username, password, security_token]):
        print("⚠️  Salesforce credentials not found in environment variables")
        print("Set SALESFORCE_USERNAME, SALESFORCE_PASSWORD, and SALESFORCE_SECURITY_TOKEN")
        return
    
    # Create pipeline
    pipeline = Pipeline(name="Salesforce Opportunity Analysis")
    
    # Fetch opportunities from Salesforce
    pipeline.add_stage(
        SalesforceSource(
            username=username,
            password=password,
            security_token=security_token,
            object_type="Opportunity",
            fields=["Id", "Name", "Amount", "StageName", "CloseDate"],
            where_clause="Amount > 0 AND StageName != 'Closed Lost'",
            limit=1000,
        )
    )
    
    # Filter for opportunities closing this quarter
    pipeline.add_stage(
        FilterTransformer(
            lambda opp: opp.get("StageName") in ["Negotiation", "Proposal", "Closed Won"],
            name="Filter Active Opportunities"
        )
    )
    
    # Aggregate by stage
    pipeline.add_stage(
        AggregateTransformer(
            group_by=["StageName"],
            aggregations={
                "Amount": "sum",
                "Id": "count",
            },
            name="Aggregate by Stage"
        )
    )
    
    # Save results
    pipeline.add_stage(
        CSVDestination("output/salesforce_pipeline_analysis.csv")
    )
    
    # Run the pipeline
    result = pipeline.run()
    
    print(f"\nAnalyzed {result.metadata.get('record_count', 0)} opportunity stages")


if __name__ == "__main__":
    main()

