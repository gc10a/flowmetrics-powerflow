"""Tests for data transformers."""

import pytest
from powerflow.transformers import (
    FilterTransformer,
    MapTransformer,
    AggregateTransformer,
    EnrichTransformer,
    DeduplicateTransformer,
)
from powerflow.pipeline import PipelineContext


def test_filter_transformer():
    """Test FilterTransformer."""
    transformer = FilterTransformer(lambda x: x['value'] > 100)
    data = [
        {'id': 1, 'value': 50},
        {'id': 2, 'value': 150},
        {'id': 3, 'value': 200},
    ]
    
    result = transformer.transform(data)
    
    assert len(result) == 2
    assert result[0]['value'] == 150
    assert result[1]['value'] == 200


def test_filter_transformer_execute():
    """Test FilterTransformer execute method."""
    transformer = FilterTransformer(lambda x: x['active'], name="FilterActive")
    context = PipelineContext([
        {'id': 1, 'active': True},
        {'id': 2, 'active': False},
        {'id': 3, 'active': True},
    ])
    
    result = transformer.execute(context)
    
    assert len(result.data) == 2
    assert all(x['active'] for x in result.data)


def test_map_transformer():
    """Test MapTransformer."""
    transformer = MapTransformer(lambda x: {**x, 'doubled': x['value'] * 2})
    data = [
        {'id': 1, 'value': 10},
        {'id': 2, 'value': 20},
    ]
    
    result = transformer.transform(data)
    
    assert len(result) == 2
    assert result[0]['doubled'] == 20
    assert result[1]['doubled'] == 40


def test_map_transformer_execute():
    """Test MapTransformer execute method."""
    transformer = MapTransformer(
        lambda x: {'id': x['id'], 'upper_name': x['name'].upper()},
        name="UppercaseNames"
    )
    context = PipelineContext([
        {'id': 1, 'name': 'alice'},
        {'id': 2, 'name': 'bob'},
    ])
    
    result = transformer.execute(context)
    
    assert result.data[0]['upper_name'] == 'ALICE'
    assert result.data[1]['upper_name'] == 'BOB'


def test_aggregate_transformer_sum():
    """Test AggregateTransformer with sum."""
    transformer = AggregateTransformer(
        group_by=['region'],
        aggregations={'revenue': 'sum'}
    )
    data = [
        {'region': 'North', 'revenue': 100},
        {'region': 'South', 'revenue': 200},
        {'region': 'North', 'revenue': 150},
    ]
    
    result = transformer.transform(data)
    
    assert len(result) == 2
    north = [r for r in result if r['region'] == 'North'][0]
    assert north['revenue_sum'] == 250


def test_aggregate_transformer_count():
    """Test AggregateTransformer with count."""
    transformer = AggregateTransformer(
        group_by=['status'],
        aggregations={'id': 'count'}
    )
    data = [
        {'id': 1, 'status': 'active'},
        {'id': 2, 'status': 'active'},
        {'id': 3, 'status': 'inactive'},
    ]
    
    result = transformer.transform(data)
    
    assert len(result) == 2
    active = [r for r in result if r['status'] == 'active'][0]
    assert active['id_count'] == 2


def test_aggregate_transformer_avg():
    """Test AggregateTransformer with average."""
    transformer = AggregateTransformer(
        group_by=['category'],
        aggregations={'value': 'avg'}
    )
    data = [
        {'category': 'A', 'value': 10},
        {'category': 'A', 'value': 20},
        {'category': 'B', 'value': 30},
    ]
    
    result = transformer.transform(data)
    
    category_a = [r for r in result if r['category'] == 'A'][0]
    assert category_a['value_avg'] == 15


def test_aggregate_transformer_min_max():
    """Test AggregateTransformer with min and max."""
    transformer = AggregateTransformer(
        group_by=['group'],
        aggregations={'value': 'min', 'score': 'max'}
    )
    data = [
        {'group': 'X', 'value': 10, 'score': 90},
        {'group': 'X', 'value': 5, 'score': 95},
    ]
    
    result = transformer.transform(data)
    
    assert result[0]['value_min'] == 5
    assert result[0]['score_max'] == 95


def test_enrich_transformer():
    """Test EnrichTransformer."""
    def enrich_func(record):
        return {
            'full_name': f"{record['first']} {record['last']}",
            'category': 'premium'
        }
    
    transformer = EnrichTransformer(enrich_func)
    data = [
        {'id': 1, 'first': 'John', 'last': 'Doe'},
        {'id': 2, 'first': 'Jane', 'last': 'Smith'},
    ]
    
    result = transformer.transform(data)
    
    assert result[0]['full_name'] == 'John Doe'
    assert result[1]['full_name'] == 'Jane Smith'
    assert all(r['category'] == 'premium' for r in result)


def test_deduplicate_transformer_first():
    """Test DeduplicateTransformer keeping first occurrence."""
    transformer = DeduplicateTransformer(keys=['email'], keep='first')
    data = [
        {'id': 1, 'email': 'john@example.com', 'name': 'John'},
        {'id': 2, 'email': 'jane@example.com', 'name': 'Jane'},
        {'id': 3, 'email': 'john@example.com', 'name': 'John Doe'},
    ]
    
    result = transformer.transform(data)
    
    assert len(result) == 2
    john = [r for r in result if r['email'] == 'john@example.com'][0]
    assert john['id'] == 1
    assert john['name'] == 'John'


def test_deduplicate_transformer_last():
    """Test DeduplicateTransformer keeping last occurrence."""
    transformer = DeduplicateTransformer(keys=['email'], keep='last')
    data = [
        {'id': 1, 'email': 'john@example.com', 'name': 'John'},
        {'id': 2, 'email': 'jane@example.com', 'name': 'Jane'},
        {'id': 3, 'email': 'john@example.com', 'name': 'John Doe'},
    ]
    
    result = transformer.transform(data)
    
    assert len(result) == 2
    john = [r for r in result if r['email'] == 'john@example.com'][0]
    assert john['id'] == 3
    assert john['name'] == 'John Doe'


def test_deduplicate_transformer_multiple_keys():
    """Test DeduplicateTransformer with multiple keys."""
    transformer = DeduplicateTransformer(keys=['first', 'last'])
    data = [
        {'id': 1, 'first': 'John', 'last': 'Doe'},
        {'id': 2, 'first': 'Jane', 'last': 'Smith'},
        {'id': 3, 'first': 'John', 'last': 'Doe'},
    ]
    
    result = transformer.transform(data)
    
    assert len(result) == 2

