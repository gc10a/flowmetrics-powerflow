"""
HubSpot integration for PowerFlow.
"""

from typing import Any, Dict, List, Optional
import logging

from powerflow.sources import DataSource

logger = logging.getLogger("powerflow")


class HubSpotSource(DataSource):
    """
    Fetch data from HubSpot.
    
    Example:
        >>> source = HubSpotSource(
        ...     access_token="your-access-token",
        ...     object_type="deals",
        ...     properties=["dealname", "amount", "dealstage"],
        ...     limit=100
        ... )
    """
    
    def __init__(
        self,
        access_token: Optional[str] = None,
        object_type: str = "deals",
        properties: Optional[List[str]] = None,
        limit: Optional[int] = 100,
        name: Optional[str] = None,
    ):
        super().__init__(name or f"HubSpotSource({object_type})")
        self.access_token = access_token
        self.object_type = object_type
        self.properties = properties or []
        self.limit = limit
    
    def fetch(self) -> List[Dict[str, Any]]:
        """Fetch data from HubSpot."""
        try:
            from hubspot import HubSpot
        except ImportError:
            raise ImportError(
                "hubspot-api-client is required for HubSpot integration. "
                "Install it with: pip install powerflow[hubspot]"
            )
        
        # Connect to HubSpot
        logger.info("Connecting to HubSpot")
        client = HubSpot(access_token=self.access_token)
        
        # Fetch objects
        logger.info(f"Fetching {self.object_type} from HubSpot")
        
        results = []
        after = None
        
        while True:
            # Fetch page of results
            response = client.crm.objects.basic_api.get_page(
                object_type=self.object_type,
                limit=min(self.limit - len(results), 100) if self.limit else 100,
                after=after,
                properties=self.properties,
                archived=False,
            )
            
            # Extract records
            for item in response.results:
                record = {"id": item.id}
                record.update(item.properties)
                results.append(record)
            
            # Check if we should continue paginating
            if not response.paging or (self.limit and len(results) >= self.limit):
                break
            
            after = response.paging.next.after
        
        logger.info(f"Fetched {len(results)} records from HubSpot")
        return results[:self.limit] if self.limit else results


class HubSpotDestination:
    """
    Write data to HubSpot (placeholder for future implementation).
    
    This would allow you to create/update HubSpot records from pipeline data.
    """
    
    def __init__(self):
        raise NotImplementedError(
            "HubSpotDestination is not yet implemented. "
            "Contributions welcome!"
        )

