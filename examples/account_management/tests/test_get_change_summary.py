import unittest
from unittest.mock import patch, Mock, MagicMock, call
import argparse
import sys
import io

from google.ads.googleads.errors import GoogleAdsException
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.v19.services.services.google_ads_service import GoogleAdsServiceClient
from google.ads.googleads.v19.services.types.google_ads_service import GoogleAdsRow
from google.ads.googleads.v19.resources.types.change_status import ChangeStatus
from google.ads.googleads.v19.enums.types.change_status_resource_type import ChangeStatusResourceTypeEnum
from google.ads.googleads.v19.enums.types.change_status_operation import ChangeStatusOperationEnum # Although not explicitly used in output, it's good to be aware of related enums.
from google.ads.googleads.v19.enums.types.resource_status import ResourceStatusEnum # For cs.resource_status

# Assuming get_change_summary.py is in examples.account_management
from examples.account_management.get_change_summary import main as get_change_summary_main

# Mock for EnumTypeWrapper if needed, or just ensure mock enums have a .name attribute
class MockEnum:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

class TestGetChangeSummary(unittest.TestCase):
    def setUp(self):
        self.mock_google_ads_client_patcher = patch('examples.account_management.get_change_summary.GoogleAdsClient')
        self.mock_google_ads_client_class = self.mock_google_ads_client_patcher.start()
        
        self.mock_google_ads_client_instance = MagicMock(spec=GoogleAdsClient)
        self.mock_google_ads_client_class.load_from_storage.return_value = self.mock_google_ads_client_instance
        
        self.mock_googleads_service = MagicMock(spec=GoogleAdsServiceClient)
        self.mock_google_ads_client_instance.get_service.return_value = self.mock_googleads_service

        # Capture stdout
        self.held_stdout = sys.stdout
        sys.stdout = io.StringIO()

    def tearDown(self):
        sys.stdout = self.held_stdout  # Restore stdout
        self.mock_google_ads_client_patcher.stop()

    def _create_mock_change_status_row(
        self,
        cs_resource_name="customers/123/changeStatus/test_cs_id",
        last_change_date_time="2024-01-15 10:00:00",
        resource_type_enum_val=ChangeStatusResourceTypeEnum.ChangeStatusResourceType.CAMPAIGN, # Enum value
        resource_status_enum_val=ResourceStatusEnum.ResourceStatus.ENABLED, # Enum value
        changed_resource_name_field_value="customers/123/campaigns/campaign_1" # e.g. cs.campaign value
    ):
        mock_row = MagicMock(spec=GoogleAdsRow)
        mock_cs = MagicMock(spec=ChangeStatus)
        
        mock_cs.resource_name = cs_resource_name
        mock_cs.last_change_date_time = last_change_date_time
        
        # For enums, assign a mock object that has a .name attribute
        mock_cs.resource_type = MockEnum(name=ChangeStatusResourceTypeEnum.ChangeStatusResourceType.Name(resource_type_enum_val))
        mock_cs.resource_status = MockEnum(name=ResourceStatusEnum.ResourceStatus.Name(resource_status_enum_val))

        # Set the specific resource name field (e.g., campaign, ad_group)
        # The script accesses these directly, e.g., change_status.campaign
        resource_type_name_lower = ChangeStatusResourceTypeEnum.ChangeStatusResourceType.Name(resource_type_enum_val).lower()
        
        # Handle cases like AD_GROUP_AD which becomes ad_group_ad
        if resource_type_name_lower == "ad_group_ad":
            setattr(mock_cs, "ad_group_ad", changed_resource_name_field_value)
        elif resource_type_name_lower == "ad_group_criterion":
             setattr(mock_cs, "ad_group_criterion", changed_resource_name_field_value)
        elif resource_type_name_lower == "campaign_criterion":
            setattr(mock_cs, "campaign_criterion", changed_resource_name_field_value)
        elif resource_type_name_lower in ["campaign", "ad_group"]: # common ones
             setattr(mock_cs, resource_type_name_lower, changed_resource_name_field_value)
        # else: for UNKNOWN or other types, no specific field might be set or checked beyond resource_name

        mock_row.change_status = mock_cs
        return mock_row

    def test_main_success_various_resource_types(self):
        customer_id = "test_customer_id_123"

        # --- CAMPAIGN ---
        campaign_row = self._create_mock_change_status_row(
            cs_resource_name="customers/123/changeStatus/cs_campaign_1",
            last_change_date_time="2024-01-15 11:00:00",
            resource_type_enum_val=ChangeStatusResourceTypeEnum.ChangeStatusResourceType.CAMPAIGN,
            resource_status_enum_val=ResourceStatusEnum.ResourceStatus.ENABLED,
            changed_resource_name_field_value="customers/123/campaigns/campaign_1_details"
        )

        # --- AD_GROUP ---
        ad_group_row = self._create_mock_change_status_row(
            cs_resource_name="customers/123/changeStatus/cs_adgroup_1",
            last_change_date_time="2024-01-15 12:00:00",
            resource_type_enum_val=ChangeStatusResourceTypeEnum.ChangeStatusResourceType.AD_GROUP,
            resource_status_enum_val=ResourceStatusEnum.ResourceStatus.PAUSED,
            changed_resource_name_field_value="customers/123/adGroups/adgroup_1_details"
        )

        # --- AD_GROUP_AD ---
        ad_group_ad_row = self._create_mock_change_status_row(
            cs_resource_name="customers/123/changeStatus/cs_ad_1",
            last_change_date_time="2024-01-15 13:00:00",
            resource_type_enum_val=ChangeStatusResourceTypeEnum.ChangeStatusResourceType.AD_GROUP_AD,
            resource_status_enum_val=ResourceStatusEnum.ResourceStatus.REMOVED,
            changed_resource_name_field_value="customers/123/adGroupAds/ad_1_details"
        )
        
        # --- UNKNOWN ---
        unknown_row = self._create_mock_change_status_row(
            cs_resource_name="customers/123/changeStatus/cs_unknown_1",
            last_change_date_time="2024-01-15 14:00:00",
            resource_type_enum_val=ChangeStatusResourceTypeEnum.ChangeStatusResourceType.UNKNOWN,
            resource_status_enum_val=ResourceStatusEnum.ResourceStatus.UNKNOWN,
            changed_resource_name_field_value="customers/123/unknown/unknown_1_details" # This won't be used by script for UNKNOWN
        )
        
        self.mock_googleads_service.search.return_value = [
            campaign_row,
            ad_group_row,
            ad_group_ad_row,
            unknown_row
        ]

        get_change_summary_main(self.mock_google_ads_client_instance, customer_id)
        
        expected_query = f"""
        SELECT
          change_status.last_change_date_time,
          change_status.resource_type,
          change_status.campaign,
          change_status.ad_group,
          change_status.resource_status,
          change_status.ad_group_ad,
          change_status.ad_group_criterion,
          change_status.campaign_criterion
        FROM change_status
        WHERE change_status.last_change_date_time DURING LAST_14_DAYS
        ORDER BY change_status.last_change_date_time DESC
        LIMIT 10000""" # Default limit in script is 10000
        
        self.mock_googleads_service.search.assert_called_once_with(
            customer_id=customer_id, query=expected_query
        )

        output = sys.stdout.getvalue()

        self.assertIn(
            "On 2024-01-15 11:00:00, resource 'customers/123/campaigns/campaign_1_details' of type CAMPAIGN was ENABLED.",
            output
        )
        self.assertIn(
            "On 2024-01-15 12:00:00, resource 'customers/123/adGroups/adgroup_1_details' of type AD_GROUP was PAUSED.",
            output
        )
        self.assertIn(
            "On 2024-01-15 13:00:00, resource 'customers/123/adGroupAds/ad_1_details' of type AD_GROUP_AD was REMOVED.",
            output
        )
        # For UNKNOWN, the script prints the change_status.resource_name as the identifier
        self.assertIn(
            "On 2024-01-15 14:00:00, resource 'customers/123/changeStatus/cs_unknown_1' of type UNKNOWN was UNKNOWN.",
            output
        )

    @patch('sys.exit') # To check if sys.exit is called
    def test_main_google_ads_exception(self, mock_sys_exit):
        customer_id = "test_customer_id_error"

        # Configure GoogleAdsService.search to raise GoogleAdsException
        mock_error_payload = MagicMock()
        mock_error_payload.message = "Test GoogleAdsException from API search"
        mock_failure = MagicMock()
        mock_failure.errors = [mock_error_payload]
        
        google_ads_exception = GoogleAdsException(
            error=None, # This would be the original gRPC error if available
            call=None,  # This would be the gRPC call object if available
            failure=mock_failure,
            error_code=None, # Could be a more specific error code if available
            message="Simulated GoogleAdsException during search operation"
        )
        self.mock_googleads_service.search.side_effect = google_ads_exception

        get_change_summary_main(self.mock_google_ads_client_instance, customer_id)

        mock_sys_exit.assert_called_once_with(1)
        output = sys.stdout.getvalue()
        
        # Check for parts of the generic GoogleAdsException message format
        self.assertIn("Request with ID", output) 
        # Check for the specific error message from the mock_error_payload
        self.assertIn("Test GoogleAdsException from API search", output)
        
        self.mock_googleads_service.search.assert_called_once()

    @patch('examples.account_management.get_change_summary.main') # Mock the script's main function
    @patch('argparse.ArgumentParser.parse_args')
    def test_argument_parser(self, mock_parse_args, mock_script_main_function):
        # self.mock_google_ads_client_class is already set up by setUp to patch
        # 'examples.account_management.get_change_summary.GoogleAdsClient'
        # and self.mock_google_ads_client_instance is returned by load_from_storage.

        test_customer_id_cli = "test_customer_id_from_cli"
        sys.argv = ["get_change_summary.py", "-c", test_customer_id_cli]

        # Mock parse_args to return the customer_id
        mock_parse_args.return_value = argparse.Namespace(customer_id=test_customer_id_cli)
        
        # The script's __main__ block will call GoogleAdsClient.load_from_storage(),
        # which is already mocked in setUp to return self.mock_google_ads_client_instance.

        # Execute the script's main block using runpy
        import runpy
        runpy.run_module("examples.account_management.get_change_summary", run_name="__main__")

        # Assert that GoogleAdsClient.load_from_storage was called (implicitly by __main__)
        self.mock_google_ads_client_class.load_from_storage.assert_called_once()
        
        mock_parse_args.assert_called_once()
        
        # Assert that the script's main function was called with the loaded client and customer_id
        # The script's __main__ block calls: main(client, args.customer_id)
        mock_script_main_function.assert_called_once_with(
            self.mock_google_ads_client_instance, 
            test_customer_id_cli
        )


if __name__ == "__main__":
    unittest.main()
