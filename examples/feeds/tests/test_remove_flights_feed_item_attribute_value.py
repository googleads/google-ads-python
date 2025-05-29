import argparse
import unittest
from unittest import mock
from typing import Any # For type hints if needed for mocks

# Properly import the specific types used for mocking and type checking if available
# These imports are based on the structure observed in the SUT
from google.ads.googleads.client import GoogleAdsClient
# The following direct type imports are problematic with google-ads > 23.0.0 for v19
# We will rely on client.get_type() for objects and Any for type hints where needed.
# from google.ads.googleads.v19.types import feed_item as feed_item_type
# from google.ads.googleads.v19.types import feed as feed_type
# from google.ads.googleads.v19.services.types import (
#     feed_item_service as feed_item_service_type,
# )
# from google.ads.googleads.v19.services.types import (
#     google_ads_service as google_ads_service_type,
# )
# from google.ads.googleads.v19.types import (
#     feed_item_operation as feed_item_operation_type,
# )
from google.api_core import protobuf_helpers

# Import the script to be tested
from examples.feeds import remove_flights_feed_item_attribute_value


class TestRemoveFlightsFeedItemAttributeValue(unittest.TestCase):

    def _setup_mock_google_ads_client(self):
        """Helper to create a mock GoogleAdsClient with enums."""
        mock_google_ads_client = mock.MagicMock(spec=GoogleAdsClient)

        # Mock the enums structure
        mock_enums = mock.MagicMock()
        mock_flight_placeholder_field_enum = mock.MagicMock()
        # Define some mock enum members. The actual values (like .value) might not be needed
        # if the code uses the member object itself as dict keys or for comparison.
        # The script uses client.enums.FlightPlaceholderFieldEnum[str_name]
        # so we need to mock the __getitem__ behavior for the enum.
        
        # Create mock enum members
        mock_enum_price = mock.MagicMock(name="FLIGHT_PRICE")
        mock_enum_destination = mock.MagicMock(name="DESTINATION_ID")
        mock_enum_desc = mock.MagicMock(name="FLIGHT_DESCRIPTION")
        mock_enum_sale_price = mock.MagicMock(name="FLIGHT_SALE_PRICE")
        mock_enum_final_urls = mock.MagicMock(name="FINAL_URLS")

        def flight_placeholder_getitem(key):
            if key == "FLIGHT_PRICE":
                return mock_enum_price
            elif key == "DESTINATION_ID":
                return mock_enum_destination
            elif key == "FLIGHT_DESCRIPTION":
                return mock_enum_desc
            elif key == "FLIGHT_SALE_PRICE":
                return mock_enum_sale_price
            elif key == "FINAL_URLS":
                return mock_enum_final_urls
            raise KeyError(key)

        mock_flight_placeholder_field_enum.__getitem__.side_effect = flight_placeholder_getitem
        # Also allow access like FlightPlaceholderFieldEnum.FLIGHT_PRICE
        mock_flight_placeholder_field_enum.FLIGHT_PRICE = mock_enum_price
        mock_flight_placeholder_field_enum.DESTINATION_ID = mock_enum_destination
        mock_flight_placeholder_field_enum.FLIGHT_DESCRIPTION = mock_enum_desc
        mock_flight_placeholder_field_enum.FLIGHT_SALE_PRICE = mock_enum_sale_price
        mock_flight_placeholder_field_enum.FINAL_URLS = mock_enum_final_urls


        mock_enums.FlightPlaceholderFieldEnum = mock_flight_placeholder_field_enum
        mock_google_ads_client.enums = mock_enums
        
        # Mock client.get_type for creating operation objects
        def get_type_side_effect(type_name, version="v19"):
            # Return MagicMock for type_name, so it can be instantiated in tests
            # e.g. mock_google_ads_client.get_type("FeedItemOperation")()
            # The spec for these types will be loose (MagicMock itself)
            m = mock.MagicMock()
            m._pb = mock.MagicMock() # for field_mask operations
            m.name = type_name # for debugging if needed
            return m

        mock_google_ads_client.get_type.side_effect = get_type_side_effect

        # Mock client.copy_from to simulate actual copying for relevant fields
        def copy_from_side_effect(target_mock, source_object):
            # This function is called when client.copy_from(target, source) is used in SUT.
            # target_mock is the mock object that should receive the fields from source_object.
            # source_object is the object being copied from (e.g., a FeedItem or a FieldMask).

            if hasattr(source_object, "DESCRIPTOR"): # Checks if it's a protobuf message
                # If target_mock is supposed to become like a protobuf message (e.g. FieldMask)
                # we need to ensure it has the necessary attributes for equality checks.
                # For FieldMask, equality is often based on its 'paths'.
                if source_object.DESCRIPTOR.full_name == 'google.protobuf.FieldMask':
                    target_mock.paths = list(source_object.paths)
                    # Removed custom __eq__ override; will compare paths directly in test
                else:
                    # For other protobuf messages like FeedItem, copy relevant fields
                    # The SUT uses field_mask(None, feed_item._pb), so feed_item needs _pb
                    # And copy_from(operation.update, feed_item)
                    fields_to_copy = ['resource_name', 'attribute_values'] # Add more if needed
                    for field in fields_to_copy:
                        if hasattr(source_object, field):
                            setattr(target_mock, field, getattr(source_object, field))
                    # If source_object has _pb, ensure target_mock has it for field_mask
                    if hasattr(source_object, '_pb'):
                         target_mock._pb = source_object._pb

            else: # Fallback for non-protobuf source_object or simpler mocks
                # Generic attribute copy for other fields if source is a simple mock
                for key, value in source_object.__dict__.items():
                    if not key.startswith('_') and not callable(value):
                        setattr(target_mock, key, value)
        
        mock_google_ads_client.copy_from.side_effect = copy_from_side_effect

        return mock_google_ads_client

    @mock.patch("examples.feeds.remove_flights_feed_item_attribute_value.argparse.ArgumentParser")
    @mock.patch("google.ads.googleads.client.GoogleAdsClient.load_from_storage")
    @mock.patch("examples.feeds.remove_flights_feed_item_attribute_value.get_feed")
    @mock.patch("examples.feeds.remove_flights_feed_item_attribute_value.remove_attribute_value_from_feed_item")
    def test_main(
        self,
        mock_remove_attribute_value_from_feed_item,
        mock_get_feed,
        mock_load_from_storage,
        mock_argument_parser,
    ):
        mock_google_ads_client = self._setup_mock_google_ads_client()
        mock_load_from_storage.return_value = mock_google_ads_client

        mock_feed_item_service = mock.MagicMock()
        mock_google_ads_client.get_service.return_value = mock_feed_item_service # Default for now

        def get_service_side_effect(service_name, version="v19"):
            if service_name == "FeedItemService":
                return mock_feed_item_service
            # Add other services if main directly calls them
            return mock.MagicMock()
        mock_google_ads_client.get_service.side_effect = get_service_side_effect
        
        # Setup argparse mock
        mock_args = mock.Mock()
        mock_args.customer_id = "test_customer_id"
        mock_args.feed_id = "test_feed_id"
        mock_args.feed_item_id = "test_feed_item_id"
        mock_args.flight_placeholder_field_name = "FLIGHT_PRICE" # Use string name as per script
        mock_argument_parser.return_value.parse_args.return_value = mock_args

        # Setup return values for patched functions
        mock_placeholders_map = {"mock_placeholder_map"} # Simplified
        mock_get_feed.return_value = mock_placeholders_map
        
        mock_updated_feed_item = self._setup_mock_google_ads_client().get_type("FeedItem")() # Instantiate via mock get_type
        mock_updated_feed_item.resource_name = "updated_feed_item_resource_name"
        # Ensure attribute_values is a list-like mock if pop is called on it by SUT (it is)
        mock_updated_feed_item.attribute_values = mock.MagicMock() # or [] if simpler and SUT allows
        mock_remove_attribute_value_from_feed_item.return_value = mock_updated_feed_item

        # Call main
        remove_flights_feed_item_attribute_value.main(
            mock_google_ads_client,
            mock_args.customer_id,
            mock_args.feed_id,
            mock_args.feed_item_id,
            mock_args.flight_placeholder_field_name,
        )

        # Assertions
        # mock_load_from_storage.assert_called_once_with(version="v19") # This is incorrect for main unit test
        mock_get_feed.assert_called_once_with(
            mock_google_ads_client, mock_args.customer_id, mock_args.feed_id
        )
        
        # Check that the correct enum member is passed to remove_attribute_value_from_feed_item
        # The script does: client.enums.FlightPlaceholderFieldEnum[flight_placeholder_field_name]
        # So, we expect the mock enum member corresponding to "FLIGHT_PRICE"
        expected_enum_member = mock_google_ads_client.enums.FlightPlaceholderFieldEnum["FLIGHT_PRICE"]
        mock_remove_attribute_value_from_feed_item.assert_called_once_with(
            mock_google_ads_client,
            mock_args.customer_id,
            mock_args.feed_id,
            mock_args.feed_item_id,
            mock_placeholders_map,
            expected_enum_member,
        )

        mock_feed_item_service.mutate_feed_items.assert_called_once()
        call_args, call_kwargs = mock_feed_item_service.mutate_feed_items.call_args
        self.assertEqual(call_kwargs["customer_id"], mock_args.customer_id)
        self.assertEqual(len(call_kwargs["operations"]), 1)
        operation = call_kwargs["operations"][0]
        self.assertEqual(operation.update.resource_name, mock_updated_feed_item.resource_name)
        # Check update_mask (important!)
        # Ensure mock_updated_feed_item has a _pb attribute for field_mask
        if not hasattr(mock_updated_feed_item, '_pb'): # Should be set by get_type mock
            mock_updated_feed_item._pb = mock.MagicMock() 
            
        expected_mask = protobuf_helpers.field_mask(None, mock_updated_feed_item._pb)
        # Compare paths of the FieldMask
        self.assertIsInstance(operation.update_mask, mock.MagicMock, "operation.update_mask should be a MagicMock populated by copy_from")
        self.assertTrue(hasattr(operation.update_mask, 'paths'), "operation.update_mask should have 'paths' attribute after copy_from")
        self.assertEqual(list(operation.update_mask.paths), list(expected_mask.paths))

    def test_get_feed(self):
        mock_google_ads_client = self._setup_mock_google_ads_client()
        mock_google_ads_service = mock.MagicMock() # For GoogleAdsService
        mock_feed_service = mock.MagicMock()       # For FeedService

        def get_service_side_effect(service_name, version="v19"):
            if service_name == "GoogleAdsService":
                return mock_google_ads_service
            elif service_name == "FeedService":
                return mock_feed_service
            return mock.MagicMock()
        mock_google_ads_client.get_service.side_effect = get_service_side_effect

        customer_id = "test_customer_id"
        feed_id = "test_feed_id"
        feed_resource_name = f"customers/{customer_id}/feeds/{feed_id}"
        mock_feed_service.feed_path.return_value = feed_resource_name

        # Mock GoogleAdsService search response
        mock_row = mock.MagicMock() # spec removed
        # Use get_type to create FeedAttribute instances for mocking
        mock_feed_attribute_price = self._setup_mock_google_ads_client().get_type("FeedAttribute")()
        mock_feed_attribute_price.name = "Flight Price"
        mock_feed_attribute_price.id = 1
        mock_feed_attribute_dest = self._setup_mock_google_ads_client().get_type("FeedAttribute")()
        mock_feed_attribute_dest.name = "Destination ID"
        mock_feed_attribute_dest.id = 2

        mock_row.feed.attributes = [mock_feed_attribute_price, mock_feed_attribute_dest]
        mock_google_ads_service.search.return_value = [mock_row]

        # Expected map keys are enum members from the mock client
        expected_map = {
            mock_google_ads_client.enums.FlightPlaceholderFieldEnum.FLIGHT_PRICE: mock_feed_attribute_price,
            mock_google_ads_client.enums.FlightPlaceholderFieldEnum.DESTINATION_ID: mock_feed_attribute_dest,
        }

        # Call get_feed
        result_map = remove_flights_feed_item_attribute_value.get_feed(
            mock_google_ads_client, customer_id, feed_id
        )

        # Assertions
        mock_feed_service.feed_path.assert_called_once_with(customer_id, feed_id)
        # Adjusted expected_query to match the SUT's formatting (leading newline and indentation)
        # Note: The exact spacing might need to be captured from an actual run if this still fails.
        # For now, assuming a standard f-string formatting from the SUT.
        expected_query = f"""
        SELECT feed.attributes
        FROM feed
        WHERE feed.resource_name = '{feed_resource_name}'"""
        # Extract actual query from search_request
        self.assertEqual(mock_google_ads_service.search.call_count, 1)
        search_request_arg = mock_google_ads_service.search.call_args[1]['request']
        self.assertEqual(search_request_arg.customer_id, customer_id)
        # Compare query, removing initial newline if present in actual for cleaner comparison start
        actual_query = search_request_arg.query
        if actual_query.startswith("\n"):
            actual_query = actual_query[1:]
        expected_query_to_compare = expected_query.strip() # Original script query is likely stripped or consistently formatted
        # Let's assume the script generates a query that, when stripped of bookending newlines/spaces, matches.
        # The error indicated the SUT query started with "\n        SELECT"
        # The SUT query is: f"\n        SELECT feed.attributes\n        FROM feed\n        WHERE feed.resource_name = '{feed_resource_name}'"
        # So, we expect the actual query to be exactly that, and we should compare against that.
        # The key is that the SUT's query string has leading spaces on each line, not just the first.
        expected_query_from_sut_format = f"""\
        SELECT feed.attributes
        FROM feed
        WHERE feed.resource_name = '{feed_resource_name}'""" # No leading newline for the whole block
        
        # The error was: "\n        SELECT..." != "SELECT..."
        # This means the SUT's query string starts with a newline then indentation.
        # Let's construct the expected query to match this exactly.
        expected_query_exact = f"""
        SELECT feed.attributes
        FROM feed
        WHERE feed.resource_name = '{feed_resource_name}'"""
        self.assertEqual(search_request_arg.query, expected_query_exact)
        
        self.assertEqual(result_map, expected_map)

    def test_get_feed_item(self):
        mock_google_ads_client = self._setup_mock_google_ads_client()
        mock_google_ads_service = mock.MagicMock()
        mock_feed_item_service = mock.MagicMock()

        def get_service_side_effect(service_name, version="v19"):
            if service_name == "GoogleAdsService":
                return mock_google_ads_service
            elif service_name == "FeedItemService":
                return mock_feed_item_service
            return mock.MagicMock()
        mock_google_ads_client.get_service.side_effect = get_service_side_effect
        
        customer_id = "test_customer_id"
        feed_id = "test_feed_id"
        feed_item_id = "test_feed_item_id"
        feed_item_resource_name = f"customers/{customer_id}/feedItems/{feed_id}~{feed_item_id}"
        mock_feed_item_service.feed_item_path.return_value = feed_item_resource_name

        # Mock GoogleAdsService search response
        mock_row = mock.MagicMock() # spec removed
        expected_feed_item = self._setup_mock_google_ads_client().get_type("FeedItem")() # Instantiate via mock get_type
        expected_feed_item.resource_name = feed_item_resource_name
        mock_row.feed_item = expected_feed_item
        mock_google_ads_service.search.return_value = [mock_row]

        # Call get_feed_item
        result_feed_item = remove_flights_feed_item_attribute_value.get_feed_item(
            mock_google_ads_client, customer_id, feed_id, feed_item_id
        )

        # Assertions
        mock_feed_item_service.feed_item_path.assert_called_once_with(customer_id, feed_id, feed_item_id)
        # Adjusted expected_query to match the SUT's formatting
        expected_query_exact = f"""
        SELECT feed_item.attribute_values
        FROM feed_item
        WHERE feed_item.resource_name = '{feed_item_resource_name}'"""
        self.assertEqual(mock_google_ads_service.search.call_count, 1)
        search_request_arg = mock_google_ads_service.search.call_args[1]['request']
        self.assertEqual(search_request_arg.customer_id, customer_id)
        self.assertEqual(search_request_arg.query, expected_query_exact)
        self.assertEqual(result_feed_item, expected_feed_item)

    @mock.patch("examples.feeds.remove_flights_feed_item_attribute_value.get_feed_item")
    def test_remove_attribute_value_from_feed_item_success(self, mock_get_feed_item_func):
        mock_google_ads_client = self._setup_mock_google_ads_client()
        customer_id = "test_customer_id"
        feed_id = "test_feed_id"
        feed_item_id = "test_feed_item_id"

        # Enum member to remove (use the mock from _setup_mock_google_ads_client)
        enum_to_remove = mock_google_ads_client.enums.FlightPlaceholderFieldEnum.FLIGHT_PRICE
        
        # Setup placeholders_to_feed_attributes_map
        # Key is the enum member, value is a FeedAttribute object
        mock_feed_attribute_price = self._setup_mock_google_ads_client().get_type("FeedAttribute")()
        mock_feed_attribute_price.id = 101
        mock_feed_attribute_price.name = "Flight Price"
        mock_feed_attribute_dest = self._setup_mock_google_ads_client().get_type("FeedAttribute")()
        mock_feed_attribute_dest.id = 102
        mock_feed_attribute_dest.name = "Destination ID"
        placeholders_map = {
            enum_to_remove: mock_feed_attribute_price,
            mock_google_ads_client.enums.FlightPlaceholderFieldEnum.DESTINATION_ID: mock_feed_attribute_dest,
        }

        # Setup the feed item that get_feed_item will return
        original_feed_item = self._setup_mock_google_ads_client().get_type("FeedItem")()
        original_feed_item.attribute_values = [] # Ensure it's a list to extend
        # Attribute to be removed
        attr_value_to_remove = self._setup_mock_google_ads_client().get_type("FeedItemAttributeValue")()
        attr_value_to_remove.feed_attribute_id = 101
        attr_value_to_remove.string_value="100.00 USD"
        # Attribute to keep
        attr_value_to_keep = self._setup_mock_google_ads_client().get_type("FeedItemAttributeValue")()
        attr_value_to_keep.feed_attribute_id = 102
        attr_value_to_keep.string_value = "SFO"
        original_feed_item.attribute_values.extend([attr_value_to_remove, attr_value_to_keep])
        mock_get_feed_item_func.return_value = original_feed_item
        
        # Call the function
        updated_feed_item = remove_flights_feed_item_attribute_value.remove_attribute_value_from_feed_item(
            mock_google_ads_client,
            customer_id,
            feed_id,
            feed_item_id,
            placeholders_map,
            enum_to_remove,
        )

        # Assertions
        mock_get_feed_item_func.assert_called_once_with(mock_google_ads_client, customer_id, feed_id, feed_item_id)
        self.assertEqual(len(updated_feed_item.attribute_values), 1)
        self.assertIn(attr_value_to_keep, updated_feed_item.attribute_values)
        self.assertNotIn(attr_value_to_remove, updated_feed_item.attribute_values)
        self.assertEqual(updated_feed_item.attribute_values[0].feed_attribute_id, 102)

    @mock.patch("examples.feeds.remove_flights_feed_item_attribute_value.get_feed_item")
    def test_remove_attribute_value_from_feed_item_not_found(self, mock_get_feed_item_func):
        mock_google_ads_client = self._setup_mock_google_ads_client()
        customer_id = "test_customer_id"
        feed_id = "test_feed_id"
        feed_item_id = "test_feed_item_id"

        enum_to_remove = mock_google_ads_client.enums.FlightPlaceholderFieldEnum.FLIGHT_PRICE
        
        mock_feed_attribute_price = self._setup_mock_google_ads_client().get_type("FeedAttribute")()
        mock_feed_attribute_price.id = 101
        mock_feed_attribute_price.name = "Flight Price"
        placeholders_map = {enum_to_remove: mock_feed_attribute_price}

        original_feed_item = self._setup_mock_google_ads_client().get_type("FeedItem")()
        original_feed_item.attribute_values = [] # Ensure it's a list to extend
        # Attribute that does NOT match the one to remove
        attr_value_other = self._setup_mock_google_ads_client().get_type("FeedItemAttributeValue")()
        attr_value_other.feed_attribute_id = 102
        attr_value_other.string_value="SFO"
        original_feed_item.attribute_values.extend([attr_value_other])
        mock_get_feed_item_func.return_value = original_feed_item

        with self.assertRaisesRegex(ValueError, "No matching feed attribute found for value"):
            remove_flights_feed_item_attribute_value.remove_attribute_value_from_feed_item(
                mock_google_ads_client,
                customer_id,
                feed_id,
                feed_item_id,
                placeholders_map,
                enum_to_remove,
            )

if __name__ == "__main__":
    unittest.main()
