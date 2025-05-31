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
from google.ads.googleads.v18.resources.types.feed import Feed, FeedAttribute
from google.protobuf import field_mask_pb2

from examples.feeds.update_flights_feed_item_string_attribute_value import main


class UpdateFlightsFeedItemStringAttributeValueTest(unittest.TestCase):
    @mock.patch("google.ads.googleads.client.GoogleAdsClient.load_from_storage")
    @mock.patch(
        "google.ads.googleads.v18.services.services.google_ads_service.GoogleAdsServiceClient"
    )
    @mock.patch(
        "google.ads.googleads.v18.services.services.feed_item_service.FeedItemServiceClient"
    )
    def test_update_flights_feed_item_string_attribute_value(
        self,
        mock_feed_item_service_client,
        mock_google_ads_service_client,
        mock_load_from_storage,
    ):
        # Mock GoogleAdsClient
        mock_google_ads_client = mock.MagicMock(spec=GoogleAdsClient)
        mock_load_from_storage.return_value = mock_google_ads_client

        # Mock the enums structure needed by flight_placeholder_fields_map
        mock_enums = mock.MagicMock()
        mock_flight_placeholder_field_enum = mock.MagicMock()
        # Based on the mocked Feed: FeedAttribute(id=3, name="Flight Description")
        # The script will call client.enums.FlightPlaceholderFieldEnum.Value("Flight Description")
        # and expect it to return the id (3).
        mock_flight_placeholder_field_enum.Value = mock.MagicMock(return_value=3)
        mock_enums.FlightPlaceholderFieldEnum = mock_flight_placeholder_field_enum
        mock_google_ads_client.enums = mock_enums

        # Mock GoogleAdsService
        mock_google_ads_service = mock_google_ads_service_client.return_value
        # This script makes two calls to google_ads_service.search
        mock_search_responses = [
            iter([GoogleAdsRow({
                "feed": Feed(
                    resource_name="customers/1234567890/feeds/111222",
                    attributes=[
                        FeedAttribute(id=1, name="Destination ID"),
                        FeedAttribute(id=2, name="Origin ID"),
                        FeedAttribute(id=3, name="Flight Description"), # This is the one we'll update
                    ],
                )
            })]),
            iter([GoogleAdsRow({
                "feed_item": FeedItem(
                    resource_name="customers/1234567890/feedItems/333444",
                    attribute_values=[
                        FeedItemAttributeValue(
                            feed_attribute_id=1, string_value="SFO"
                        ),
                        FeedItemAttributeValue(
                            feed_attribute_id=2, string_value="JFK"
                        ),
                        FeedItemAttributeValue(
                            feed_attribute_id=3,
                            string_value="Original flight description",
                        ),
                    ],
                )
            })])
        ]
        mock_google_ads_service.search.side_effect = lambda *args, **kwargs: mock_search_responses.pop(0)

        # Mock FeedItemService
        mock_feed_item_service = mock_feed_item_service_client.return_value
        mock_feed_item_service.mutate_feed_items.return_value = (
            MutateFeedItemsResponse()
        )

        new_flight_description = "New updated flight description"
        # Run the main function
        main(
            mock_google_ads_client,
            "1234567890",
            "TEST_FEED_NAME",
            "TEST_FEED_ITEM_RESOURCE_ID",
            "Flight Description",
            new_flight_description,
        )

        # Assertions
        mock_load_from_storage.assert_called_once_with(version="v18")
        mock_google_ads_service.search.assert_any_call(
            customer_id="1234567890",
            query='''
            SELECT feed.resource_name, feed.attributes
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
        request = call_args[1]["request"]
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

        # Verify that the attribute value with feed_attribute_id=3 is updated
        # and others are preserved.
        self.assertEqual(len(updated_feed_item.attribute_values), 3)
        updated_value_found = False
        for val in updated_feed_item.attribute_values:
            if val.feed_attribute_id == 3:
                self.assertEqual(val.string_value, new_flight_description)
                updated_value_found = True
            elif val.feed_attribute_id == 1:
                 self.assertEqual(val.string_value, "SFO")
            elif val.feed_attribute_id == 2:
                self.assertEqual(val.string_value, "JFK")
        self.assertTrue(updated_value_found)

        # Assert the field mask
        expected_mask = field_mask_pb2.FieldMask(paths=["attribute_values"])
        self.assertEqual(operation.update_mask, expected_mask)


if __name__ == "__main__":
    unittest.main()
