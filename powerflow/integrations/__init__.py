"""
Integrations with popular CRM and marketing platforms.
"""

from powerflow.integrations.salesforce import SalesforceSource
from powerflow.integrations.hubspot import HubSpotSource

__all__ = [
    "SalesforceSource",
    "HubSpotSource",
]

