"""Tests for data sources."""

import pytest
import tempfile
import csv
import json
from pathlib import Path

from powerflow.sources import CSVSource, JSONSource, GeneratorSource
from powerflow.pipeline import PipelineContext


@pytest.fixture
def temp_csv_file():
    """Create a temporary CSV file."""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as f:
        writer = csv.DictWriter(f, fieldnames=['id', 'name', 'value'])
        writer.writeheader()
        writer.writerow({'id': '1', 'name': 'Alice', 'value': '100'})
        writer.writerow({'id': '2', 'name': 'Bob', 'value': '200'})
        temp_path = f.name
    
    yield temp_path
    
    # Cleanup
    Path(temp_path).unlink()


@pytest.fixture
def temp_json_file():
    """Create a temporary JSON file."""
    data = [
        {'id': 1, 'name': 'Alice', 'value': 100},
        {'id': 2, 'name': 'Bob', 'value': 200},
    ]
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        json.dump(data, f)
        temp_path = f.name
    
    yield temp_path
    
    # Cleanup
    Path(temp_path).unlink()


def test_csv_source_read(temp_csv_file):
    """Test reading from CSV file."""
    source = CSVSource(temp_csv_file)
    data = source.fetch()
    
    assert len(data) == 2
    assert data[0]['id'] == '1'
    assert data[0]['name'] == 'Alice'
    assert data[1]['id'] == '2'


def test_csv_source_execute(temp_csv_file):
    """Test CSVSource execute method."""
    source = CSVSource(temp_csv_file)
    context = PipelineContext()
    
    result = source.execute(context)
    
    assert len(result.data) == 2
    assert result.metadata['record_count'] == 2


def test_csv_source_file_not_found():
    """Test CSVSource with non-existent file."""
    source = CSVSource("nonexistent.csv")
    
    with pytest.raises(FileNotFoundError):
        source.fetch()


def test_json_source_read(temp_json_file):
    """Test reading from JSON file."""
    source = JSONSource(temp_json_file)
    data = source.fetch()
    
    assert len(data) == 2
    assert data[0]['id'] == 1
    assert data[0]['name'] == 'Alice'


def test_json_source_execute(temp_json_file):
    """Test JSONSource execute method."""
    source = JSONSource(temp_json_file)
    context = PipelineContext()
    
    result = source.execute(context)
    
    assert len(result.data) == 2
    assert result.metadata['record_count'] == 2


def test_json_source_single_object():
    """Test JSONSource with single object instead of array."""
    data = {'id': 1, 'name': 'Test'}
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        json.dump(data, f)
        temp_path = f.name
    
    try:
        source = JSONSource(temp_path)
        result = source.fetch()
        
        assert len(result) == 1
        assert result[0]['id'] == 1
    finally:
        Path(temp_path).unlink()


def test_json_source_file_not_found():
    """Test JSONSource with non-existent file."""
    source = JSONSource("nonexistent.json")
    
    with pytest.raises(FileNotFoundError):
        source.fetch()


def test_generator_source():
    """Test GeneratorSource."""
    def generate_data():
        return [
            {'id': 1, 'value': 100},
            {'id': 2, 'value': 200},
        ]
    
    source = GeneratorSource(generate_data)
    data = source.fetch()
    
    assert len(data) == 2
    assert data[0]['id'] == 1


def test_generator_source_execute():
    """Test GeneratorSource execute method."""
    def generate_data():
        return [{'id': 1}, {'id': 2}, {'id': 3}]
    
    source = GeneratorSource(generate_data, name="CustomGenerator")
    context = PipelineContext()
    
    result = source.execute(context)
    
    assert len(result.data) == 3
    assert result.metadata['record_count'] == 3
    assert source.name == "CustomGenerator"

