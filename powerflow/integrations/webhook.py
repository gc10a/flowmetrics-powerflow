"""
Webhook integration for PowerFlow.
"""

from typing import Any, Dict, List, Optional
import logging
import requests

from powerflow.destinations import Destination

logger = logging.getLogger("powerflow")


class WebhookDestination(Destination):
    """
    Send data to a webhook endpoint.
    
    Example:
        >>> destination = WebhookDestination(
        ...     url="https://api.example.com/webhook",
        ...     headers={"Authorization": "Bearer token"},
        ...     batch_size=100
        ... )
    """
    
    def __init__(
        self,
        url: str,
        method: str = "POST",
        headers: Optional[Dict[str, str]] = None,
        batch_size: Optional[int] = None,
        timeout: int = 30,
        name: Optional[str] = None,
    ):
        super().__init__(name or f"WebhookDestination({url})")
        self.url = url
        self.method = method.upper()
        self.headers = headers or {}
        self.batch_size = batch_size
        self.timeout = timeout
    
    def write(self, data: List[Dict[str, Any]]) -> None:
        """Send data to webhook."""
        if not data:
            logger.warning("No data to send")
            return
        
        # Set content type if not specified
        if "Content-Type" not in self.headers:
            self.headers["Content-Type"] = "application/json"
        
        if self.batch_size:
            # Send in batches
            for i in range(0, len(data), self.batch_size):
                batch = data[i:i + self.batch_size]
                self._send_batch(batch)
        else:
            # Send all at once
            self._send_batch(data)
    
    def _send_batch(self, batch: List[Dict[str, Any]]) -> None:
        """Send a batch of records to the webhook."""
        logger.info(f"Sending {len(batch)} records to {self.url}")
        
        try:
            response = requests.request(
                method=self.method,
                url=self.url,
                json=batch,
                headers=self.headers,
                timeout=self.timeout,
            )
            response.raise_for_status()
            logger.info(f"Successfully sent batch (status: {response.status_code})")
        
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to send batch: {e}")
            raise

