import unittest
import sys
from unittest.mock import MagicMock, AsyncMock, patch

# Mocking modules before import because the environment seems to lack dependencies
mock_google = MagicMock()
sys.modules["google"] = mock_google
sys.modules["google.ads"] = mock_google
sys.modules["google.ads.googleads"] = mock_google
sys.modules["google.ads.googleads.client"] = mock_google
sys.modules["google.ads.googleads.errors"] = mock_google
sys.modules["google.ads.googleads.v23"] = mock_google
sys.modules["google.ads.googleads.v23.services"] = mock_google
sys.modules["google.ads.googleads.v23.services.services"] = mock_google
sys.modules["google.ads.googleads.v23.services.services.google_ads_service"] = mock_google
sys.modules["google.ads.googleads.v23.services.types"] = mock_google
sys.modules["google.ads.googleads.v23.services.types.google_ads_service"] = mock_google

# Import module under test AFTER mocking
from examples.asyncio import async_search


class TestAsyncSearch(unittest.IsolatedAsyncioTestCase):
    async def test_main(self):
        # Setup Mocks
        mock_client_instance = MagicMock()
        mock_googleads_service = AsyncMock()
        mock_client_instance.get_service.return_value = mock_googleads_service

        # Mock the search response (AsyncPager)
        # search returns an object that is an async iterator
        
        # Create a mock row
        mock_row = MagicMock()
        mock_row.campaign.id = 123
        mock_row.campaign.name = "Test Campaign"
        
        # Async iterator setup for the pager
        async def async_gen():
            yield mock_row
        
        mock_googleads_service.search.return_value = async_gen()

        customer_id = "1234567890"

        # Execute
        await async_search.main(mock_client_instance, customer_id)

        # Verification
        
        # Check if service was retrieved correctly
        mock_client_instance.get_service.assert_called_with("GoogleAdsService", is_async=True)

        # Verify search called
        mock_googleads_service.search.assert_called_once()
        call_args = mock_googleads_service.search.call_args
        self.assertEqual(call_args.kwargs["customer_id"], customer_id)
        
        # Verify Query does NOT contain LIMIT 10
        query = call_args.kwargs["query"]
        self.assertNotIn("LIMIT 10", query)
        self.assertIn("SELECT", query)
        self.assertIn("FROM campaign", query)
