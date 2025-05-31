import unittest
from unittest.mock import patch, MagicMock
import io
import sys
from datetime import datetime, timedelta

from examples.account_management import get_change_details
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.v19.services.services.google_ads_service import GoogleAdsServiceClient
from google.ads.googleads.v19.services.types import GoogleAdsRow
from google.ads.googleads.v19.services.types import SearchGoogleAdsRequest # Corrected path
from proto.enums import ProtoEnumMeta # For mocking enum behavior


class TestGetChangeDetails(unittest.TestCase):

    @patch('examples.account_management.get_change_details.get_nested_attr')
    @patch('examples.account_management.get_change_details.datetime')
    @patch('examples.account_management.get_change_details.GoogleAdsClient')
    def test_main_prints_change_details(self, mock_google_ads_client_class, mock_datetime, mock_get_nested_attr):
        # 1. Setup Mocks
        mock_client_instance = MagicMock(spec=GoogleAdsClient)
        mock_google_ads_client_class.load_from_storage.return_value = mock_client_instance

        mock_google_ads_service = MagicMock(spec=GoogleAdsServiceClient)
        mock_client_instance.get_service.return_value = mock_google_ads_service

        # Mock datetime to control date range in query
        fixed_now = datetime(2023, 1, 15)
        mock_datetime.now.return_value = fixed_now
        # Script calculates tomorrow and two_weeks_ago
        expected_tomorrow_str = (fixed_now + timedelta(1)).strftime("%Y-%m-%d")
        expected_two_weeks_ago_str = (fixed_now + timedelta(-14)).strftime("%Y-%m-%d")

        # 2. Prepare arguments for main function
        customer_id = "test_customer_123"

        # 3. Mock the response for googleads_service.search()
        # Make mock_row1 a MagicMock so its attributes (like change_event) are also MagicMocks
        mock_row1 = MagicMock(spec=GoogleAdsRow)
        mock_row1.change_event = MagicMock() # Explicitly define change_event on the mock_row1
        event = mock_row1.change_event # event is now the MagicMock assigned above
        event.change_date_time = "2023-01-15 10:00:00" # Within mocked date range
        event.change_resource_name = "customers/123/adGroups/789" # Corrected resource name
        event.user_email = "testuser@example.com" # Corrected email

        # Mock enums using name attribute, as script accesses .name
        mock_client_type_enum = MagicMock()
        mock_client_type_enum.name = "GOOGLE_ADS_API"
        event.client_type = mock_client_type_enum

        mock_change_resource_type_enum = MagicMock()
        mock_change_resource_type_enum.name = "AD_GROUP"
        event.change_resource_type = mock_change_resource_type_enum

        mock_resource_change_op_enum = MagicMock()
        mock_resource_change_op_enum.name = "UPDATE"
        event.resource_change_operation = mock_resource_change_op_enum

        # event.changed_fields is a MagicMock. Its .paths attribute should be an iterable list.
        event.changed_fields.paths = ["status", "name"]

        # Mock old and new resources (nested under event.old_resource.ad_group etc.)
        # Make event.old_resource and event.new_resource themselves MagicMocks
        # so that their sub-attributes like .ad_group can be easily assigned.
        event.old_resource = MagicMock(spec=event.old_resource) # spec helps with isinstance if needed
        event.new_resource = MagicMock(spec=event.new_resource)

        mock_old_ad_group_details = MagicMock()
        mock_new_ad_group_details = MagicMock()

        # Assign these to the .ad_group attribute of the mocked old_resource/new_resource
        event.old_resource.ad_group = mock_old_ad_group_details
        event.new_resource.ad_group = mock_new_ad_group_details

        # Configure mock_get_nested_attr
        # For "status" field, return the string directly. This bypasses the
        # isinstance(type(value), ProtoEnumMeta) check in the script, and the
        # script will use the string as is.
        def get_nested_attr_side_effect(resource, field_path):
            if resource == mock_old_ad_group_details:
                if field_path == "status": return "PAUSED"
                if field_path == "name": return "Old Ad Group Name"
            elif resource == mock_new_ad_group_details:
                if field_path == "status": return "ENABLED"
                if field_path == "name": return "New Ad Group Name"
            return MagicMock() # Default for other fields
        mock_get_nested_attr.side_effect = get_nested_attr_side_effect

        # search returns an iterator of rows
        mock_google_ads_service.search.return_value = iter([mock_row1])

        # Mock client.get_type for SearchGoogleAdsRequest
        mock_search_request = MagicMock(spec=SearchGoogleAdsRequest)
        mock_client_instance.get_type.return_value = mock_search_request

        # 4. Capture stdout
        captured_output = io.StringIO()
        sys.stdout = captured_output

        # 5. Call the main function (only client and customer_id)
        get_change_details.main(mock_client_instance, customer_id)

        # 6. Restore stdout
        sys.stdout = sys.__stdout__

        # 7. Assertions
        # Assert get_type was called for SearchGoogleAdsRequest
        mock_client_instance.get_type.assert_called_once_with("SearchGoogleAdsRequest")

        # Assert search was called with the request object
        mock_google_ads_service.search.assert_called_once_with(request=mock_search_request)

        # Verify attributes of the search_request object
        self.assertEqual(mock_search_request.customer_id, customer_id)
        actual_query_arg = mock_search_request.query

        # Verify query content (important parts)
        self.assertIn(f"change_event.change_date_time <= '{expected_tomorrow_str}'", actual_query_arg)
        self.assertIn(f"change_event.change_date_time >= '{expected_two_weeks_ago_str}'", actual_query_arg)
        self.assertIn("ORDER BY change_event.change_date_time DESC", actual_query_arg)
        self.assertIn("LIMIT 5", actual_query_arg) # Script uses LIMIT 5
        self.assertIn("change_event.user_email", actual_query_arg) # Spot check field

        # Verify printed output
        output = captured_output.getvalue()

        expected_intro_line = (
            f"On {event.change_date_time}, user {event.user_email} "
            f"used interface {event.client_type.name} to perform a(n) "
            f"{event.resource_change_operation.name} operation on a "
            f"{event.change_resource_type.name} with resource name "
            f"'{event.change_resource_name}'\n"
        )

        expected_change_lines = [
            f"\tstatus changed from PAUSED to ENABLED", # Use direct strings
            f"\tname changed from Old Ad Group Name to New Ad Group Name"
        ]

        expected_output = expected_intro_line + "\n".join(expected_change_lines) + "\n"

        self.assertEqual(output, expected_output)

if __name__ == "__main__":
    unittest.main()
