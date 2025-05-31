import unittest
from unittest import mock

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.v18.services.types.feed_item_service import (
    FeedItemOperation,
    MutateFeedItemsResponse,
)
from google.ads.googleads.v18.services.types.google_ads_service import (
    GoogleAdsRow,
    SearchGoogleAdsResponse,
)
from google.ads.googleads.v18.resources.types.feed_item import FeedItem, FeedItemAttributeValue
from google.ads.googleads.v18.resources.types.feed import Feed

from examples.feeds.remove_flights_feed_item_attribute_value import main


class RemoveFlightsFeedItemAttributeValueTest(unittest.TestCase):
    @mock.patch("google.ads.googleads.client.GoogleAdsClient.load_from_storage")
    @mock.patch(
        "google.ads.googleads.v18.services.services.google_ads_service.GoogleAdsServiceClient"
    )
    @mock.patch(
        "google.ads.googleads.v18.services.services.feed_item_service.FeedItemServiceClient"
    )
    def test_remove_flights_feed_item_attribute_value(
        self,
        mock_feed_item_service_client,
        mock_google_ads_service_client,
        mock_load_from_storage,
    ):
        # Mock GoogleAdsClient
        mock_google_ads_client = mock.MagicMock(spec=GoogleAdsClient)
        mock_load_from_storage.return_value = mock_google_ads_client

        # Mock GoogleAdsService
        mock_google_ads_service = mock_google_ads_service_client.return_value

        # Define responses for the two search calls
        mock_search_responses = [
            iter([GoogleAdsRow({"feed": Feed(resource_name="customers/1234567890/feeds/111222")})]),
            iter([GoogleAdsRow({
                "feed_item": FeedItem(
                    resource_name="customers/1234567890/feedItems/333444",
                    attribute_values=[
                        FeedItemAttributeValue(
                            feed_attribute_id=1, string_value="Value to remove"
                        ),
                        FeedItemAttributeValue(
                            feed_attribute_id=2, string_value="Another value"
                        ),
                    ],
                )
            })])
        ]
        # Set side_effect to a function that consumes these responses
        mock_google_ads_service.search.side_effect = lambda *args, **kwargs: mock_search_responses.pop(0)

        # Mock FeedItemService
        mock_feed_item_service = mock_feed_item_service_client.return_value
        mock_feed_item_service.mutate_feed_items.return_value = (
            MutateFeedItemsResponse()
        )

        # Run the main function
        main(
            mock_google_ads_client,
            "1234567890",
            "TEST_FEED_NAME",
            "TEST_FEED_ITEM_RESOURCE_ID",
            "String value",  # This corresponds to feed_attribute_id=1 in the mock
        )

        # Assertions
        mock_load_from_storage.assert_called_once_with(version="v18")
        mock_google_ads_service.search.assert_any_call(
            customer_id="1234567890",
            query='''
            SELECT feed.resource_name
            FROM feed
            WHERE feed.name = "TEST_FEED_NAME"
            LIMIT 1''',
        )
        mock_google_ads_service.search.assert_any_call(
            customer_id="1234567890",
            query='''
            SELECT feed_item.resource_name, feed_item.attribute_values
            FROM feed_item
            WHERE feed_item.resource_name = "TEST_FEED_ITEM_RESOURCE_ID"
            LIMIT 1''',
        )

        # Check that mutate_feed_items was called with the correct operation
        call_args = mock_feed_item_service.mutate_feed_items.call_args
        self.assertIsNotNone(call_args)
        request = call_args[1]["request"]  # Using keyword argument access
        self.assertEqual(request.customer_id, "1234567890")
        self.assertEqual(len(request.operations), 1)
        operation = request.operations[0]
        self.assertIsInstance(operation, FeedItemOperation)
        self.assertTrue(operation.update)
        updated_feed_item = operation.update
        self.assertEqual(
            updated_feed_item.resource_name,
            "customers/1234567890/feedItems/333444",
        )
        # Verify that the attribute value with feed_attribute_id=1 is removed
        # and the one with feed_attribute_id=2 is preserved.
        self.assertEqual(len(updated_feed_item.attribute_values), 1)
        self.assertEqual(updated_feed_item.attribute_values[0].feed_attribute_id, 2)
        self.assertEqual(updated_feed_item.attribute_values[0].string_value, "Another value")


if __name__ == "__main__":
    unittest.main()
