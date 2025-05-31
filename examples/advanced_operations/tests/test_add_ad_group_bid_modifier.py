import unittest
from unittest import mock
import sys

# Add the examples directory to the system path
sys.path.insert(0, '/app')

from examples.advanced_operations import add_ad_group_bid_modifier

class TestAddAdGroupBidModifier(unittest.TestCase):

    @mock.patch("examples.advanced_operations.add_ad_group_bid_modifier.GoogleAdsClient.load_from_storage")
    def test_main_functional(self, mock_load_from_storage):
        # Create a mock GoogleAdsClient
        mock_google_ads_client = mock.Mock()
        # The example script's main function expects the client to be passed in,
        # so we don't need to mock load_from_storage behavior here,
        # but the patch is to prevent actual client loading if the example's
        # __main__ block were somehow invoked.
        # The crucial part is that the main function in the script uses the
        # client we pass it.

        # Mock services
        mock_ad_group_service = mock.Mock()
        mock_ad_group_bm_service = mock.Mock()

        # Configure client.get_service to return the mock services
        def get_service_side_effect(service_name, version=None):
            # Ensure v19 is used, assuming client is configured for v19
            self.assertEqual("v19", version if version else mock_google_ads_client.version)
            if service_name == "AdGroupService":
                return mock_ad_group_service
            elif service_name == "AdGroupBidModifierService":
                return mock_ad_group_bm_service
            else:
                self.fail(f"Unexpected service requested: {service_name}")

        mock_google_ads_client.get_service.side_effect = get_service_side_effect
        mock_google_ads_client.version = "v19" # Simulate client loaded with v19

        # Mock enum types
        mock_device_enum = mock.Mock()
        mock_device_enum.MOBILE = "MOBILE_ENUM_VALUE"
        mock_google_ads_client.enums.DeviceEnum = mock_device_enum

        # Mock get_type for AdGroupBidModifierOperation
        mock_operation_obj = mock.Mock()
        mock_ad_group_bid_modifier = mock.Mock()
        # The .create attribute should be a reference to the mock_ad_group_bid_modifier
        mock_operation_obj.create = mock_ad_group_bid_modifier

        def get_type_side_effect(type_name, version=None):
            if type_name == "AdGroupBidModifierOperation":
                return mock_operation_obj
            self.fail(f"Unexpected type requested: {type_name}")

        mock_google_ads_client.get_type.side_effect = get_type_side_effect

        # Mock AdGroupService's ad_group_path method
        mock_ad_group_service.ad_group_path.return_value = "customers/1234567890/adGroups/9876543210"

        # Mock AdGroupBidModifierService's mutate_ad_group_bid_modifiers method
        mock_mutate_response = mock.Mock()
        mock_mutate_response.results = [mock.Mock(resource_name="test_bid_modifier_rn")]
        mock_ad_group_bm_service.mutate_ad_group_bid_modifiers.return_value = mock_mutate_response

        # Dummy arguments for the main function
        customer_id = "1234567890"
        ad_group_id = "9876543210"
        bid_modifier_value = 1.5

        # Call the main function from the example script
        add_ad_group_bid_modifier.main(
            mock_google_ads_client,
            customer_id,
            ad_group_id,
            bid_modifier_value
        )

        # Assertions
        # Check get_service calls
        mock_google_ads_client.get_service.assert_any_call("AdGroupService")
        mock_google_ads_client.get_service.assert_any_call("AdGroupBidModifierService")

        # Check get_type call for AdGroupBidModifierOperation
        mock_google_ads_client.get_type.assert_called_once_with("AdGroupBidModifierOperation")

        # Check that the 'create' attribute of the operation was accessed to get the modifier object
        # This is implicitly tested by checking attributes set on mock_ad_group_bid_modifier

        # Check AdGroupService's ad_group_path call
        mock_ad_group_service.ad_group_path.assert_called_once_with(customer_id, ad_group_id)

        # Check attributes set on the ad_group_bid_modifier object
        self.assertEqual(mock_ad_group_bid_modifier.ad_group, "customers/1234567890/adGroups/9876543210")
        self.assertEqual(mock_ad_group_bid_modifier.bid_modifier, bid_modifier_value)
        self.assertEqual(mock_ad_group_bid_modifier.device.type_, "MOBILE_ENUM_VALUE")

        # Check AdGroupBidModifierService's mutate_ad_group_bid_modifiers call
        mock_ad_group_bm_service.mutate_ad_group_bid_modifiers.assert_called_once_with(
            customer_id=customer_id,
            operations=[mock_operation_obj]
        )

if __name__ == "__main__":
    unittest.main()
