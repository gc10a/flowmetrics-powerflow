"""Pytest configuration and shared fixtures."""

import pytest


@pytest.fixture
def sample_deals_data():
    """Sample deals data for testing."""
    return [
        {
            'deal_id': 'D001',
            'company': 'Acme Corp',
            'amount': 45000,
            'stage': 'negotiation',
            'region': 'North America',
        },
        {
            'deal_id': 'D002',
            'company': 'TechStart Inc',
            'amount': 125000,
            'stage': 'closed_won',
            'region': 'Europe',
        },
        {
            'deal_id': 'D003',
            'company': 'Global Systems',
            'amount': 8500,
            'stage': 'proposal',
            'region': 'Asia',
        },
    ]


@pytest.fixture
def sample_contacts_data():
    """Sample contacts data for testing."""
    return [
        {'id': 1, 'email': 'alice@example.com', 'name': 'Alice', 'role': 'Manager'},
        {'id': 2, 'email': 'bob@example.com', 'name': 'Bob', 'role': 'Director'},
        {'id': 3, 'email': 'charlie@example.com', 'name': 'Charlie', 'role': 'VP'},
    ]

