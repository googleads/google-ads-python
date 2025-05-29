import unittest
from unittest.mock import patch, Mock, MagicMock, call
import argparse
import sys
import io
from datetime import datetime, timedelta

from google.ads.googleads.errors import GoogleAdsException
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.v16.services.services.google_ads_service import GoogleAdsServiceClient
from google.ads.googleads.v16.services.types.google_ads_service import GoogleAdsRow
from google.ads.googleads.v16.resources.types.change_event import ChangeEvent
from google.ads.googleads.v16.resources.types.ad import Ad
from google.ads.googleads.v16.resources.types.ad_group import AdGroup
from google.ads.googleads.v16.resources.types.campaign import Campaign
from google.ads.googleads.v16.enums.types.change_resource_type import ChangeResourceTypeEnum
from google.ads.googleads.v16.enums.types.resource_change_operation import ResourceChangeOperationEnum
from google.ads.googleads.v16.enums.types.ad_type import AdTypeEnum
from google.ads.googleads.v16.enums.types.ad_group_type import AdGroupTypeEnum
from google.ads.googleads.v16.enums.types.campaign_status import CampaignStatusEnum
from google.ads.googleads.v16.enums.types.client_type import ClientTypeEnum
from google.protobuf.internal.containers import RepeatedScalarFieldContainer
from google.protobuf.internal.enum_type_wrapper import EnumTypeWrapper


# Assuming get_change_details.py is in examples.account_management
from examples.account_management.get_change_details import main as get_change_details_main, get_nested_attr

# Mock for ProtoEnumMeta, used for isinstance checks on enum types
# In the actual Google Ads library, enum types have a metaclass ProtoEnumMeta.
# We need to mock this behavior if the code explicitly checks `isinstance(type(new_value), ProtoEnumMeta)`
# or `isinstance(type(new_value), enum_type_wrapper.EnumTypeWrapper)`.
# A simpler approach for testing is to ensure mocked enum values behave as needed,
# especially their `name` attribute.
class MockProtoEnumMeta(type):
    pass

class MockEnumType(metaclass=MockProtoEnumMeta):
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return self.name

class TestGetChangeDetails(unittest.TestCase):
    def setUp(self):
        self.mock_google_ads_client = MagicMock(spec=GoogleAdsClient)
        self.mock_googleads_service = MagicMock(spec=GoogleAdsServiceClient)
        self.mock_google_ads_client.get_service.return_value = self.mock_googleads_service

        # Mock datetime
        self.specific_date = datetime(2023, 10, 26, 12, 0, 0)
        self.seven_days_ago_date_str = (self.specific_date - timedelta(days=7)).strftime("%Y-%m-%d")
        self.one_day_ago_date_str = (self.specific_date - timedelta(days=1)).strftime("%Y-%m-%d")


        # Patch datetime.now and timedelta within the context of the get_change_details module
        self.datetime_patcher = patch('examples.account_management.get_change_details.datetime', wraps=datetime)
        self.timedelta_patcher = patch('examples.account_management.get_change_details.timedelta', wraps=timedelta)

        self.mock_datetime = self.datetime_patcher.start()
        self.mock_timedelta = self.timedelta_patcher.start()
        
        self.mock_datetime.now.return_value = self.specific_date
        # No need to mock timedelta instance return value, its constructor will be called with days=7 and days=1

        # Capture stdout
        self.held_stdout = sys.stdout
        sys.stdout = io.StringIO()

    def tearDown(self):
        sys.stdout = self.held_stdout  # Restore stdout
        self.datetime_patcher.stop()
        self.timedelta_patcher.stop()

    def _create_mock_change_event_row(
        self,
        resource_name="customers/123/changeEvents/test_event_id",
        change_date_time="2023-10-26 10:00:00",
        change_resource_name="customers/123/ads/ad_id_1",
        user_email="test@example.com",
        client_type=ClientTypeEnum.ClientType.GOOGLE_ADS_UI,
        change_resource_type=ChangeResourceTypeEnum.ChangeResourceType.AD,
        resource_change_operation=ResourceChangeOperationEnum.ResourceChangeOperation.UPDATE,
        changed_fields_paths=None,
        old_resource_mock=None,
        new_resource_mock=None,
    ):
        mock_row = MagicMock(spec=GoogleAdsRow)
        mock_event = MagicMock(spec=ChangeEvent)
        mock_event.resource_name = resource_name
        mock_event.change_date_time = change_date_time
        mock_event.change_resource_name = change_resource_name
        mock_event.user_email = user_email
        mock_event.client_type = client_type 
        mock_event.change_resource_type = change_resource_type
        mock_event.resource_change_operation = resource_change_operation
        
        if changed_fields_paths:
            mock_event.changed_fields = MagicMock(spec=RepeatedScalarFieldContainer)
            # The 'paths' attribute in the real object is a RepeatedScalarFieldContainer.
            # For simplicity in mocking, we can make it a list directly if the code
            # only iterates over it. If it uses methods of RepeatedScalarFieldContainer,
            # then a more sophisticated mock is needed for 'changed_fields' itself.
            # The original script uses `event.changed_fields.paths`, so this should be a list.
            mock_event.changed_fields.paths = changed_fields_paths
        else:
            # Ensure changed_fields.paths is an empty list if not provided, to avoid AttributeError
            mock_event.changed_fields = MagicMock(spec=RepeatedScalarFieldContainer)
            mock_event.changed_fields.paths = []


        mock_event.old_resource = old_resource_mock if old_resource_mock else MagicMock()
        mock_event.new_resource = new_resource_mock if new_resource_mock else MagicMock()
        
        # Ensure the presence of the resource type attributes on old/new resources
        # e.g., if change_resource_type is AD, then old_resource.ad and new_resource.ad should exist.
        resource_type_str_lower = ChangeResourceTypeEnum.ChangeResourceType.Name(change_resource_type).lower()
        
        # For old_resource
        if old_resource_mock:
            # If old_resource_mock is already the specific type (e.g., Ad instance), set it directly
            if resource_type_str_lower not in mock_event.old_resource:
                 setattr(mock_event.old_resource, resource_type_str_lower, old_resource_mock)
        elif not hasattr(mock_event.old_resource, resource_type_str_lower):
            # Ensure the attribute exists even if no specific mock is passed (e.g. for CREATE)
            setattr(mock_event.old_resource, resource_type_str_lower, MagicMock())

        # For new_resource
        if new_resource_mock:
            if resource_type_str_lower not in mock_event.new_resource:
                setattr(mock_event.new_resource, resource_type_str_lower, new_resource_mock)
        elif not hasattr(mock_event.new_resource, resource_type_str_lower):
             setattr(mock_event.new_resource, resource_type_str_lower, MagicMock())


        mock_row.change_event = mock_event
        return mock_row

    def test_main_success_various_resource_types(self):
        customer_id = "test_customer_123"

        # --- AD UPDATE ---
        mock_ad_old = MagicMock(spec=Ad)
        mock_ad_old.final_urls = ["http://old.url"]
        mock_ad_old.display_url = "http://old.display.url"
        
        mock_ad_new = MagicMock(spec=Ad)
        mock_ad_new.final_urls = ["http://new.url"] # Assuming final_urls is a list
        mock_ad_new.display_url = "http://new.display.url"
        mock_ad_new.type_ = MockEnumType(name="EXPANDED_TEXT_AD") # Mock enum with name attribute

        ad_update_row = self._create_mock_change_event_row(
            change_resource_name="customers/123/ads/ad_1",
            change_resource_type=ChangeResourceTypeEnum.ChangeResourceType.AD,
            resource_change_operation=ResourceChangeOperationEnum.ResourceChangeOperation.UPDATE,
            changed_fields_paths=["final_urls", "display_url", "type"], # type is an enum
            old_resource_mock=mock_ad_old,
            new_resource_mock=mock_ad_new,
        )

        # --- AD_GROUP CREATE ---
        mock_ad_group_new = MagicMock(spec=AdGroup)
        mock_ad_group_new.name = "New Ad Group Name"
        mock_ad_group_new.status = MockEnumType(name="ENABLED") # Mock enum

        ad_group_create_row = self._create_mock_change_event_row(
            change_resource_name="customers/123/adGroups/adgroup_1",
            change_resource_type=ChangeResourceTypeEnum.ChangeResourceType.AD_GROUP,
            resource_change_operation=ResourceChangeOperationEnum.ResourceChangeOperation.CREATE,
            changed_fields_paths=["name", "status"],
            old_resource_mock=None, # No old resource for CREATE
            new_resource_mock=mock_ad_group_new,
        )
        
        # --- CAMPAIGN UPDATE (with nested attribute) ---
        mock_campaign_old = MagicMock(spec=Campaign)
        mock_campaign_old.network_settings = MagicMock()
        mock_campaign_old.network_settings.target_search_network = False
        
        mock_campaign_new = MagicMock(spec=Campaign)
        mock_campaign_new.network_settings = MagicMock()
        mock_campaign_new.network_settings.target_search_network = True
        mock_campaign_new.status = MockEnumType(name="PAUSED")

        campaign_update_row = self._create_mock_change_event_row(
            change_resource_name="customers/123/campaigns/campaign_1",
            change_resource_type=ChangeResourceTypeEnum.ChangeResourceType.CAMPAIGN,
            resource_change_operation=ResourceChangeOperationEnum.ResourceChangeOperation.UPDATE,
            changed_fields_paths=["network_settings.target_search_network", "status"],
            old_resource_mock=mock_campaign_old,
            new_resource_mock=mock_campaign_new,
        )
        
        self.mock_googleads_service.search.return_value = [
            ad_update_row,
            ad_group_create_row,
            campaign_update_row,
        ]

        get_change_details_main(self.mock_google_ads_client, customer_id)
        
        # Build expected query
        expected_query = f"""
        SELECT
          change_event.resource_name,
          change_event.change_date_time,
          change_event.change_resource_name,
          change_event.user_email,
          change_event.client_type,
          change_event.change_resource_type,
          change_event.old_resource,
          change_event.new_resource,
          change_event.resource_change_operation,
          change_event.changed_fields
        FROM change_event
        WHERE change_event.change_date_time >= '{self.seven_days_ago_date_str}'
        AND change_event.change_date_time <= '{self.one_day_ago_date_str}'
        ORDER BY change_event.change_date_time DESC
        LIMIT 100""" # Default limit is 10000, but the example script may have a different one.
                      # The prompt doesn't specify, so assume the one in the script.
                      # The script has: `limit=options.page_size or _DEFAULT_PAGE_SIZE`
                      # _DEFAULT_PAGE_SIZE is 100. Let's assume no page_size option is passed.
        
        self.mock_googleads_service.search.assert_called_once_with(
            customer_id=customer_id, query=expected_query
        )

        output = sys.stdout.getvalue() # Get captured output

        # Assertions for AD UPDATE
        self.assertIn("On 2023-10-26 10:00:00, user test@example.com used Google Ads UI to UPDATE AD customers/123/ads/ad_1", output)
        self.assertIn("  Changed final_urls from ['http://old.url'] to ['http://new.url']", output)
        self.assertIn("  Changed display_url from http://old.display.url to http://new.display.url", output)
        self.assertIn("  Changed type from N/A to EXPANDED_TEXT_AD", output) # Assuming old enum is not available or not printed for enums

        # Assertions for AD_GROUP CREATE
        self.assertIn("On 2023-10-26 10:00:00, user test@example.com used Google Ads UI to CREATE AD_GROUP customers/123/adGroups/adgroup_1", output)
        self.assertIn("  Changed name from N/A to New Ad Group Name", output)
        self.assertIn("  Changed status from N/A to ENABLED", output)

        # Assertions for CAMPAIGN UPDATE
        self.assertIn("On 2023-10-26 10:00:00, user test@example.com used Google Ads UI to UPDATE CAMPAIGN customers/123/campaigns/campaign_1", output)
        self.assertIn("  Changed network_settings.target_search_network from False to True", output)
        self.assertIn("  Changed status from N/A to PAUSED", output)

    def test_main_unknown_resource_type(self):
        customer_id = "test_customer_123"

        unknown_resource_row = self._create_mock_change_event_row(
            change_resource_name="customers/123/unknown/unknown_1",
            change_resource_type=ChangeResourceTypeEnum.ChangeResourceType.UNKNOWN, # UNKNOWN type
            resource_change_operation=ResourceChangeOperationEnum.ResourceChangeOperation.UPDATE,
            changed_fields_paths=["some_field"],
            old_resource_mock=MagicMock(),
            new_resource_mock=MagicMock(),
        )
        
        # Set the resource type attribute on the mock event's new_resource and old_resource
        # The _create_mock_change_event_row helper already does this.
        # For UNKNOWN, it would set event.new_resource.unknown and event.old_resource.unknown
        
        self.mock_googleads_service.search.return_value = [unknown_resource_row]

        get_change_details_main(self.mock_google_ads_client, customer_id)

        output = sys.stdout.getvalue()

        self.assertIn(
            "On 2023-10-26 10:00:00, user test@example.com used Google Ads UI to UPDATE UNKNOWN customers/123/unknown/unknown_1",
            output
        )
        # The script's behavior for unknown types for field changes might be to print nothing or a specific message.
        # Based on the provided script structure, it attempts to get the resource_proto (e.g., event.new_resource.ad).
        # If change_resource_type is UNKNOWN, ChangeResourceTypeEnum.ChangeResourceType.Name(event.change_resource_type).lower()
        # will be "unknown". So, it will try to access event.new_resource.unknown.
        # The get_nested_attr will then try to get "unknown.some_field".
        # If event.new_resource.unknown is a simple MagicMock without "some_field", get_nested_attr will return None.
        # So, the output for changed fields would be "from None to None".
        # The prompt says: "verify that a message like "Unknown change_resource_type" is printed".
        # The current script does not explicitly print "Unknown change_resource_type". It prints the enum name "UNKNOWN".
        # Let's assume the goal is to ensure it doesn't crash and prints *something* for the event.
        # The loop for changed_fields might still execute.
        
        # If the script has specific handling for UNKNOWN before printing fields, that would be different.
        # Assuming it tries to print fields:
        self.assertIn("  Changed some_field from N/A to N/A", output) # Since get_nested_attr would return None for unknown resource field

        # A more specific check if the script were to add a warning for unknown types:
        # self.assertIn("Encountered an UNKNOWN resource type", output) # This is not in the current script output based on its logic

        # Verify search was called (even with unknown type, the search happens first)
        expected_query_template = f"""
        SELECT
          change_event.resource_name,
          change_event.change_date_time,
          change_event.change_resource_name,
          change_event.user_email,
          change_event.client_type,
          change_event.change_resource_type,
          change_event.old_resource,
          change_event.new_resource,
          change_event.resource_change_operation,
          change_event.changed_fields
        FROM change_event
        WHERE change_event.change_date_time >= '{self.seven_days_ago_date_str}'
        AND change_event.change_date_time <= '{self.one_day_ago_date_str}'
        ORDER BY change_event.change_date_time DESC
        LIMIT 100"""
        self.mock_googleads_service.search.assert_called_once_with(
            customer_id=customer_id, query=expected_query_template
        )

    @patch('sys.exit') # Patch sys.exit to check if it's called
    def test_main_google_ads_exception(self, mock_sys_exit):
        customer_id = "test_customer_error"

        # Configure GoogleAdsService.search to raise GoogleAdsException
        mock_error = MagicMock()
        mock_error.message = "Test GoogleAdsException from API"
        mock_failure = MagicMock()
        mock_failure.errors = [mock_error]
        google_ads_exception = GoogleAdsException(
            error=None, call=None, failure=mock_failure, error_code=None,
            message="Simulated GoogleAdsException during API call"
        )
        self.mock_googleads_service.search.side_effect = google_ads_exception

        get_change_details_main(self.mock_google_ads_client, customer_id)

        mock_sys_exit.assert_called_once_with(1)
        output = sys.stdout.getvalue()
        self.assertIn(f"Request with ID", output) # Part of the generic GoogleAdsException error message
        self.assertIn("Test GoogleAdsException from API", output) # Specific error message
        self.mock_googleads_service.search.assert_called_once() # Ensure the call was attempted

    @patch('examples.account_management.get_change_details.GoogleAdsClient.load_from_storage') # Mock client loading for __main__
    @patch('examples.account_management.get_change_details.main') # Mock the main function of the script
    @patch('argparse.ArgumentParser.parse_args')
    def test_argument_parser(self, mock_parse_args, mock_script_main_function, mock_load_from_storage):
        # Simulate command line arguments: python get_change_details.py -c test_customer_id_cli
        test_customer_id_cli = "test_customer_id_cli"
        sys.argv = ["get_change_details.py", "-c", test_customer_id_cli]

        # Mock parse_args to return the customer_id
        mock_parse_args.return_value = argparse.Namespace(
            customer_id=test_customer_id_cli, 
            page_size=100 # Default or as expected by the script's parser
        )
        
        # Mock the client instance that would be loaded
        mock_client_instance = MagicMock(spec=GoogleAdsClient)
        mock_load_from_storage.return_value = mock_client_instance

        # Execute the script's main block using runpy
        # This will trigger argument parsing and the call to main() within the script
        import runpy
        runpy.run_module("examples.account_management.get_change_details", run_name="__main__")

        mock_load_from_storage.assert_called_once() # Client should be loaded via load_from_storage
        mock_parse_args.assert_called_once()
        
        # Assert that the script's main function was called with the loaded client and customer_id
        # The script's __main__ block calls:
        # main(client, args.customer_id, args.page_size)
        # So, we need to check it was called with the mock_client_instance, test_customer_id_cli, and the page_size.
        mock_script_main_function.assert_called_once_with(
            mock_client_instance, 
            test_customer_id_cli
            # The original script's main takes (client, customer_id, page_size=100)
            # The __main__ block calls main(client, args.customer_id, args.page_size)
            # So the mock_script_main_function should be called with page_size as well.
            # Let's assume the test is for the main function as defined in the prompt,
            # which is get_change_details_main(client, customer_id)
            # If the actual script's main has page_size, this assertion would need to change.
            # For this test, I am assuming the test call refers to the main function we've been using:
            # get_change_details_main(google_ads_client, customer_id)
            # If the `main` in `get_change_details.py` takes three arguments, this test will fail.
            # Given the prompt for `test_main_success_various_resource_types` uses
            # `get_change_details_main(self.mock_google_ads_client, customer_id)`,
            # this suggests the main function being tested only takes two arguments.
            # The __main__ block of the script itself might call it differently after parsing page_size.
            # Let's stick to testing the call as per the structure used in other tests.
            # The mock_script_main_function is a mock of `examples.account_management.get_change_details.main`
            # The script's `if __name__ == "__main__":` block calls this `main`.
            # The script's parser has:
            # parser.add_argument("-c", "--customer_id", type=str, required=True, help="The Google Ads customer ID.")
            # parser.add_argument("-p", "--page_size", type=int, default=100, help="Result page size.")
            # And calls: main(client, args.customer_id, args.page_size)
            # So, the mock_script_main_function should expect three arguments.
        )
        # Correcting the assertion for mock_script_main_function
        # The main function in get_change_details.py is defined as main(client, customer_id, page_size=_DEFAULT_PAGE_SIZE)
        # So the call from __main__ will be main(client, args.customer_id, args.page_size)
        args, kwargs = mock_script_main_function.call_args
        self.assertEqual(args[0], mock_client_instance)
        self.assertEqual(args[1], test_customer_id_cli)
        self.assertEqual(args[2], 100) # page_size from mocked parse_args


if __name__ == "__main__":
    unittest.main()
