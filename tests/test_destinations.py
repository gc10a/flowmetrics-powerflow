"""Tests for data destinations."""

import pytest
import tempfile
import csv
import json
from pathlib import Path

from powerflow.destinations import CSVDestination, JSONDestination, ConsoleDestination
from powerflow.pipeline import PipelineContext


@pytest.fixture
def temp_output_dir():
    """Create a temporary output directory."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


def test_csv_destination_write(temp_output_dir):
    """Test writing to CSV file."""
    output_file = temp_output_dir / "output.csv"
    destination = CSVDestination(str(output_file))
    
    data = [
        {'id': 1, 'name': 'Alice', 'value': 100},
        {'id': 2, 'name': 'Bob', 'value': 200},
    ]
    
    destination.write(data)
    
    assert output_file.exists()
    
    with open(output_file, 'r') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    
    assert len(rows) == 2
    assert rows[0]['name'] == 'Alice'


def test_csv_destination_execute(temp_output_dir):
    """Test CSVDestination execute method."""
    output_file = temp_output_dir / "output.csv"
    destination = CSVDestination(str(output_file))
    
    context = PipelineContext([
        {'id': 1, 'value': 100},
        {'id': 2, 'value': 200},
    ])
    
    result = destination.execute(context)
    
    assert output_file.exists()
    assert result.data == context.data


def test_csv_destination_empty_data(temp_output_dir):
    """Test CSVDestination with empty data."""
    output_file = temp_output_dir / "empty.csv"
    destination = CSVDestination(str(output_file))
    
    destination.write([])
    
    # File should not be created or should be empty
    assert not output_file.exists() or output_file.stat().st_size == 0


def test_csv_destination_creates_directory(temp_output_dir):
    """Test CSVDestination creates parent directories."""
    output_file = temp_output_dir / "subdir" / "output.csv"
    destination = CSVDestination(str(output_file))
    
    data = [{'id': 1, 'name': 'Test'}]
    destination.write(data)
    
    assert output_file.exists()


def test_json_destination_write(temp_output_dir):
    """Test writing to JSON file."""
    output_file = temp_output_dir / "output.json"
    destination = JSONDestination(str(output_file))
    
    data = [
        {'id': 1, 'name': 'Alice', 'value': 100},
        {'id': 2, 'name': 'Bob', 'value': 200},
    ]
    
    destination.write(data)
    
    assert output_file.exists()
    
    with open(output_file, 'r') as f:
        loaded_data = json.load(f)
    
    assert len(loaded_data) == 2
    assert loaded_data[0]['name'] == 'Alice'


def test_json_destination_execute(temp_output_dir):
    """Test JSONDestination execute method."""
    output_file = temp_output_dir / "output.json"
    destination = JSONDestination(str(output_file))
    
    context = PipelineContext([
        {'id': 1, 'value': 100},
        {'id': 2, 'value': 200},
    ])
    
    result = destination.execute(context)
    
    assert output_file.exists()
    assert result.data == context.data


def test_json_destination_indent(temp_output_dir):
    """Test JSONDestination with custom indent."""
    output_file = temp_output_dir / "output.json"
    destination = JSONDestination(str(output_file), indent=4)
    
    data = [{'id': 1, 'name': 'Test'}]
    destination.write(data)
    
    with open(output_file, 'r') as f:
        content = f.read()
    
    # Check that output is formatted with indentation
    assert '\n' in content
    assert '    ' in content  # 4-space indent


def test_json_destination_creates_directory(temp_output_dir):
    """Test JSONDestination creates parent directories."""
    output_file = temp_output_dir / "subdir" / "output.json"
    destination = JSONDestination(str(output_file))
    
    data = [{'id': 1, 'name': 'Test'}]
    destination.write(data)
    
    assert output_file.exists()


def test_console_destination_write(capsys):
    """Test ConsoleDestination write method."""
    destination = ConsoleDestination(limit=2)
    
    data = [
        {'id': 1, 'name': 'Alice'},
        {'id': 2, 'name': 'Bob'},
        {'id': 3, 'name': 'Charlie'},
    ]
    
    destination.write(data)
    
    captured = capsys.readouterr()
    assert 'Alice' in captured.out
    assert 'Bob' in captured.out
    # Should show message about more records
    assert '1 more record' in captured.out


def test_console_destination_no_limit(capsys):
    """Test ConsoleDestination with no limit."""
    destination = ConsoleDestination(limit=None)
    
    data = [
        {'id': 1, 'name': 'Alice'},
        {'id': 2, 'name': 'Bob'},
    ]
    
    destination.write(data)
    
    captured = capsys.readouterr()
    assert 'Alice' in captured.out
    assert 'Bob' in captured.out


def test_console_destination_execute(capsys):
    """Test ConsoleDestination execute method."""
    destination = ConsoleDestination()
    context = PipelineContext([{'id': 1}, {'id': 2}])
    
    result = destination.execute(context)
    
    assert result.data == context.data
    captured = capsys.readouterr()
    assert captured.out  # Should have printed something

