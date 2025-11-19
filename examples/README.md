# PowerFlow Examples

This directory contains example scripts demonstrating various PowerFlow features.

## Running the Examples

1. Install PowerFlow:
   ```bash
   pip install -e ..
   ```

2. Run any example:
   ```bash
   python basic_pipeline.py
   python aggregation_pipeline.py
   ```

## Examples

### basic_pipeline.py
Demonstrates a simple pipeline that reads CSV data, filters and transforms it, and outputs to JSON.

**What it does:**
- Reads deals from CSV
- Filters for high-value deals (>$10,000)
- Enriches data with priority levels
- Outputs results to console and JSON file

### aggregation_pipeline.py
Shows how to aggregate and analyze revenue data.

**What it does:**
- Reads deals from CSV
- Aggregates revenue by region
- Calculates average deal sizes
- Outputs summary to CSV

### salesforce_example.py
Fetches and analyzes Salesforce opportunities.

**Requirements:**
- Salesforce credentials (set as environment variables)
- `pip install powerflow[salesforce]`

**What it does:**
- Fetches opportunities from Salesforce
- Filters for active opportunities
- Aggregates by stage
- Outputs analysis to CSV

### webhook_example.py
Sends pipeline results to a webhook endpoint.

**What it does:**
- Identifies very high-value deals (>$100,000)
- Formats alert data
- Sends alerts to webhook endpoint

## Sample Data

The `data/` directory contains sample CSV files for testing:
- `deals.csv` - Sample deal/opportunity data

## Output

Pipeline outputs will be saved to the `output/` directory (created automatically).

