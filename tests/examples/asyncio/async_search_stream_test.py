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
from examples.asyncio import async_search_stream


class TestAsyncSearchStream(unittest.IsolatedAsyncioTestCase):
    async def test_main(self):
        # Setup Mocks
        mock_client_instance = MagicMock()
        mock_googleads_service = AsyncMock()
        mock_client_instance.get_service.return_value = mock_googleads_service

        # Mock the stream response
        # search_stream returns an async iterator of batches
        
        # Create a mock batch
        mock_row = MagicMock()
        mock_row.campaign.id = 123
        mock_row.campaign.name = "Test Campaign"
        
        mock_batch = MagicMock()
        mock_batch.results = [mock_row]

        # Async iterator setup
        async def async_gen():
            yield mock_batch
        
        mock_googleads_service.search_stream.return_value = async_gen()

        customer_id = "1234567890"

        # Execute
        await async_search_stream.main(mock_client_instance, customer_id)

        # Verification
        
        # Check if service was retrieved correctly
        mock_client_instance.get_service.assert_called_with("GoogleAdsService", is_async=True)

        # Verify search_stream called
        mock_googleads_service.search_stream.assert_called_once()
        call_args = mock_googleads_service.search_stream.call_args
        self.assertEqual(call_args.kwargs["customer_id"], customer_id)
        
        # Verify Query does NOT contain LIMIT 10
        query = call_args.kwargs["query"]
        self.assertNotIn("LIMIT 10", query)
        self.assertIn("SELECT", query)
        self.assertIn("FROM campaign", query)
