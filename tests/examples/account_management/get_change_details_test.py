import unittest
from unittest.mock import patch, MagicMock, call

from google.ads.googleads.errors import GoogleAdsException
from google.ads.googleads.v19.enums.types import (
    ChangeClientTypeEnum,
    ChangeEventResourceTypeEnum,
    ResourceChangeOperationEnum,
)
from examples.account_management.get_change_details import main


class GetChangeDetailsTest(unittest.TestCase):

    def _create_mock_change_event_row(
        self,
        change_date_time="2023-10-26 12:00:00",
        change_resource_name="customers/123/changeEvents/XYZ",
        user_email="test@example.com",
        client_type=ChangeClientTypeEnum.ChangeClientType.GOOGLE_ADS_UI,
        resource_change_operation=ResourceChangeOperationEnum.ResourceChangeOperation.UPDATE,
        resource_type=ChangeEventResourceTypeEnum.ChangeEventResourceType.AD_GROUP,
        old_resource_name="customers/123/adGroups/OLD",
        new_resource_name="customers/123/adGroups/NEW",
        changed_fields=None, # Example: ["status"]
    ):
        """Helper to create a mock GoogleAdsRow representing a ChangeEvent."""
        mock_row = MagicMock()
        event = mock_row.change_event

        event.change_date_time = change_date_time
        event.change_resource_name = change_resource_name
        event.user_email = user_email
        event.client_type = client_type
        event.resource_change_operation = resource_change_operation
        event.change_resource_type = resource_type
        
        # Mock old_resource and new_resource (these are strings in the ChangeEvent message)
        # The script tries to get specific fields from them, e.g. ad.id if it's an AD
        # For simplicity, we'll make them basic MagicMocks for now,
        # and specific tests can add attributes if needed.
        event.old_resource = MagicMock()
        event.new_resource = MagicMock()

        # Based on the script, it tries to access specific sub-fields of old/new_resource
        # e.g., old_resource.ad.id or new_resource.ad_group.name
        # We need to set these up if the print statements rely on them.
        # The script's _get_resource_name_if_present function handles various types.

        if resource_type == ChangeEventResourceTypeEnum.ChangeEventResourceType.AD_GROUP:
            event.old_resource.ad_group.resource_name = old_resource_name
            event.new_resource.ad_group.resource_name = new_resource_name
            if changed_fields:
                 event.changed_fields.paths = changed_fields # changed_fields is a google.protobuf.field_mask_pb2.FieldMask
        elif resource_type == ChangeEventResourceTypeEnum.ChangeEventResourceType.AD:
            event.old_resource.ad.resource_name = old_resource_name
            event.new_resource.ad.resource_name = new_resource_name
        # Add other resource types as needed by tests or the script's logic

        return mock_row

    @patch("examples.account_management.get_change_details.GoogleAdsClient.load_from_storage")
    def test_get_change_details_success(self, mock_load_from_storage):
        """Tests the successful retrieval and printing of change details."""
        mock_google_ads_client = MagicMock()
        mock_load_from_storage.return_value = mock_google_ads_client

        mock_google_ads_service = MagicMock()
        mock_google_ads_client.get_service.return_value = mock_google_ads_service

        customer_id = "1234567890"
        start_date = "20230101"
        end_date = "20230131"

        mock_row1 = self._create_mock_change_event_row(
            change_date_time="2023-01-15 10:00:00",
            user_email="user1@example.com",
            resource_type=ChangeEventResourceTypeEnum.ChangeEventResourceType.AD_GROUP,
            old_resource_name="customers/1234567890/adGroups/111",
            new_resource_name="customers/1234567890/adGroups/222",
            changed_fields=["status"]
        )
        mock_row2 = self._create_mock_change_event_row(
            change_date_time="2023-01-16 11:00:00",
            user_email="user2@example.com",
            client_type=ChangeClientTypeEnum.ChangeClientType.GOOGLE_ADS_API,
            resource_change_operation=ResourceChangeOperationEnum.ResourceChangeOperation.CREATE,
            resource_type=ChangeEventResourceTypeEnum.ChangeEventResourceType.CAMPAIGN,
            new_resource_name="customers/1234567890/campaigns/333"
        )
        # The script expects an iterable of "batches", each batch is an iterable of rows.
        mock_google_ads_service.search_stream.return_value = [iter([mock_row1, mock_row2])]

        with patch("builtins.print") as mock_print:
            main(mock_google_ads_client, customer_id, start_date, end_date)

        mock_google_ads_client.get_service.assert_called_once_with(
            "GoogleAdsService", version="v19"
        )

        # Construct the expected query
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
        WHERE change_event.change_date_time >= '{start_date.replace("-", "")}'
        AND change_event.change_date_time <= '{end_date.replace("-", "")}'
        ORDER BY change_event.change_date_time DESC"""
        
        # Normalize whitespace for comparison
        normalized_expected_query = " ".join(expected_query.split())
        actual_query = mock_google_ads_service.search_stream.call_args[0][1]
        normalized_actual_query = " ".join(actual_query.split())

        self.assertEqual(mock_google_ads_service.search_stream.call_args[0][0], customer_id)
        self.assertEqual(normalized_actual_query, normalized_expected_query)

        # Assertions for print calls
        # Example print from script:
        # "On 2023-01-15 10:00:00, user user1@example.com used Google Ads UI to UPDATE an AD_GROUP."
        # "Changed resource: customers/1234567890/adGroups/222" (from new_resource)
        # "Fields changed: ['status']"
        # "Old resource: customers/1234567890/adGroups/111"

        printed_strings = [c[0][0] for c in mock_print.call_args_list if c[0]] # Get all strings printed

        expected_print_1_line1 = "On 2023-01-15 10:00:00, user user1@example.com used Google Ads UI to UPDATE an AD_GROUP."
        expected_print_1_line2 = "Changed resource: customers/1234567890/adGroups/222" # This comes from _get_resource_name_if_present
        expected_print_1_line3 = "Fields changed: status" # FieldMask paths are printed directly
        expected_print_1_line4 = "Old resource: customers/1234567890/adGroups/111"
        
        expected_print_2_line1 = "On 2023-01-16 11:00:00, user user2@example.com used Google Ads API to CREATE a CAMPAIGN."
        expected_print_2_line2 = "Changed resource: customers/1234567890/campaigns/333"

        self.assertTrue(any(expected_print_1_line1 in s for s in printed_strings))
        self.assertTrue(any(expected_print_1_line2 in s for s in printed_strings))
        self.assertTrue(any(expected_print_1_line3 in s for s in printed_strings))
        self.assertTrue(any(expected_print_1_line4 in s for s in printed_strings))
        self.assertTrue(any(expected_print_2_line1 in s for s in printed_strings))
        self.assertTrue(any(expected_print_2_line2 in s for s in printed_strings))


    @patch("examples.account_management.get_change_details.GoogleAdsClient.load_from_storage")
    def test_get_change_details_google_ads_exception(self, mock_load_from_storage):
        """Tests handling of GoogleAdsException during change detail retrieval."""
        mock_google_ads_client = MagicMock()
        mock_load_from_storage.return_value = mock_google_ads_client

        mock_google_ads_service = MagicMock()
        mock_google_ads_client.get_service.return_value = mock_google_ads_service

        # Configure search_stream to raise GoogleAdsException
        mock_failure = MagicMock()
        mock_error = MagicMock()
        mock_error.message = "Test GoogleAdsException for change_details"
        mock_failure.errors = [mock_error]
        google_ads_exception = GoogleAdsException(
            mock_failure, "call", "trigger", "request_id", "error_code_enum"
        )
        mock_google_ads_service.search_stream.side_effect = google_ads_exception

        customer_id = "1234567890"
        start_date = "20230101"
        end_date = "20230131"

        with patch("sys.exit") as mock_sys_exit, \
             patch("builtins.print") as mock_error_print: # Mock print to check error messages too
            main(mock_google_ads_client, customer_id, start_date, end_date)
            
            mock_sys_exit.assert_called_once_with(1)
            # Check if the exception details were printed
            # The script prints: f"Request with ID '{e.request_id}' failed with status "
            #                  f"'{e.error.code().name}' and includes the following errors:"
            # and then loops through e.failure.errors
            error_printed = False
            for call_args in mock_error_print.call_args_list:
                if "Test GoogleAdsException for change_details" in call_args[0][0]:
                    error_printed = True
                    break
            self.assertTrue(error_printed, "GoogleAdsException details not printed to console.")

        mock_google_ads_client.get_service.assert_called_once_with(
            "GoogleAdsService", version="v19"
        )
        mock_google_ads_service.search_stream.assert_called_once()


if __name__ == "__main__":
    unittest.main()
