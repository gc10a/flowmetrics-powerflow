"""Integration tests for complete pipelines."""

import pytest
import tempfile
import csv
import json
from pathlib import Path

from powerflow import (
    Pipeline,
    CSVSource,
    JSONSource,
    FilterTransformer,
    MapTransformer,
    AggregateTransformer,
    CSVDestination,
    JSONDestination,
)


@pytest.fixture
def temp_dir():
    """Create a temporary directory for test files."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def sample_csv_file(temp_dir):
    """Create a sample CSV file."""
    csv_file = temp_dir / "input.csv"
    
    with open(csv_file, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['id', 'name', 'amount', 'region'])
        writer.writeheader()
        writer.writerows([
            {'id': '1', 'name': 'Deal A', 'amount': '10000', 'region': 'North'},
            {'id': '2', 'name': 'Deal B', 'amount': '25000', 'region': 'South'},
            {'id': '3', 'name': 'Deal C', 'amount': '15000', 'region': 'North'},
            {'id': '4', 'name': 'Deal D', 'amount': '5000', 'region': 'South'},
        ])
    
    return csv_file


def test_csv_to_json_pipeline(sample_csv_file, temp_dir):
    """Test complete pipeline from CSV to JSON."""
    output_file = temp_dir / "output.json"
    
    pipeline = Pipeline("CSV to JSON")
    pipeline.add_stage(CSVSource(str(sample_csv_file)))
    pipeline.add_stage(
        FilterTransformer(lambda x: float(x['amount']) > 10000)
    )
    pipeline.add_stage(JSONDestination(str(output_file)))
    
    result = pipeline.run()
    
    assert result.metadata['record_count'] == 2
    assert output_file.exists()
    
    with open(output_file) as f:
        data = json.load(f)
    
    assert len(data) == 2
    assert all(float(d['amount']) > 10000 for d in data)


def test_aggregation_pipeline(sample_csv_file, temp_dir):
    """Test pipeline with aggregation."""
    output_file = temp_dir / "aggregated.csv"
    
    pipeline = Pipeline("Aggregation Pipeline")
    pipeline.add_stage(CSVSource(str(sample_csv_file)))
    pipeline.add_stage(
        MapTransformer(lambda x: {**x, 'amount': float(x['amount'])})
    )
    pipeline.add_stage(
        AggregateTransformer(
            group_by=['region'],
            aggregations={'amount': 'sum', 'id': 'count'}
        )
    )
    pipeline.add_stage(CSVDestination(str(output_file)))
    
    result = pipeline.run()
    
    assert result.metadata['record_count'] == 2  # Two regions
    assert output_file.exists()


def test_transform_chain_pipeline(sample_csv_file, temp_dir):
    """Test pipeline with multiple transformations."""
    output_file = temp_dir / "transformed.json"
    
    pipeline = Pipeline("Transform Chain")
    pipeline.add_stage(CSVSource(str(sample_csv_file)))
    
    # Convert amount to float
    pipeline.add_stage(
        MapTransformer(lambda x: {**x, 'amount': float(x['amount'])})
    )
    
    # Add priority field
    pipeline.add_stage(
        MapTransformer(
            lambda x: {
                **x,
                'priority': 'HIGH' if x['amount'] > 15000 else 'LOW'
            }
        )
    )
    
    # Filter for high priority
    pipeline.add_stage(
        FilterTransformer(lambda x: x['priority'] == 'HIGH')
    )
    
    pipeline.add_stage(JSONDestination(str(output_file)))
    
    result = pipeline.run()
    
    assert result.metadata['record_count'] == 1
    
    with open(output_file) as f:
        data = json.load(f)
    
    assert all(d['priority'] == 'HIGH' for d in data)


def test_pipeline_with_hooks(sample_csv_file, temp_dir):
    """Test pipeline with hooks."""
    output_file = temp_dir / "output.json"
    
    hook_calls = []
    
    def track_hook(pipeline, context, stage=None):
        if stage:
            hook_calls.append(f"stage_{stage.name}")
        else:
            hook_calls.append("pipeline")
    
    pipeline = Pipeline("Hooks Test")
    pipeline.add_hook("pre_run", track_hook)
    pipeline.add_hook("post_run", track_hook)
    pipeline.add_hook("pre_stage", track_hook)
    pipeline.add_hook("post_stage", track_hook)
    
    pipeline.add_stage(CSVSource(str(sample_csv_file)))
    pipeline.add_stage(JSONDestination(str(output_file)))
    
    result = pipeline.run()
    
    assert len(hook_calls) > 0
    assert result.metadata['record_count'] == 4


def test_empty_pipeline():
    """Test pipeline with no stages."""
    pipeline = Pipeline("Empty")
    result = pipeline.run([{'id': 1}])
    
    assert len(result.data) == 1
    assert result.metadata['stages_completed'] == []


def test_pipeline_error_collection(sample_csv_file, temp_dir):
    """Test that pipeline collects errors when fail_fast=False."""
    
    def failing_transform(x):
        if x['id'] == '2':
            raise ValueError("Intentional error")
        return x
    
    pipeline = Pipeline("Error Collection", fail_fast=False)
    pipeline.add_stage(CSVSource(str(sample_csv_file)))
    pipeline.add_stage(MapTransformer(failing_transform))
    
    result = pipeline.run()
    
    # Pipeline should complete but collect the error
    assert len(result.errors) > 0

