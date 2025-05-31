import unittest
from unittest import mock
import sys

# Add the examples directory to the system path to allow importing the example
# module.
sys.path.insert(0, '/app')

from examples.advanced_operations import add_ad_customizer


class TestAddAdCustomizer(unittest.TestCase):

    @mock.patch("examples.advanced_operations.add_ad_customizer.GoogleAdsClient.load_from_storage")
    def test_main_functional(self, mock_load_from_storage):
        # Create a mock GoogleAdsClient
        mock_google_ads_client = mock.Mock()
        mock_load_from_storage.return_value = mock_google_ads_client

        # Mock services
        mock_customizer_attribute_service = mock.Mock()
        mock_ad_group_customizer_service = mock.Mock()
        mock_google_ads_service = mock.Mock()
        mock_ad_group_ad_service = mock.Mock()

        # Configure client.get_service to return the mock services
        def get_service_side_effect(service_name, version=None):
            self.assertEqual("v19", version if version else mock_google_ads_client.version) # Check version
            if service_name == "CustomizerAttributeService":
                return mock_customizer_attribute_service
            elif service_name == "AdGroupCustomizerService":
                return mock_ad_group_customizer_service
            elif service_name == "GoogleAdsService":
                return mock_google_ads_service
            elif service_name == "AdGroupAdService":
                return mock_ad_group_ad_service
            else:
                self.fail(f"Unexpected service requested: {service_name}")

        mock_google_ads_client.get_service.side_effect = get_service_side_effect
        # Set a default version on the mock client if not passed to get_service
        # In the actual script, version is passed to load_from_storage,
        # which then would set it on the client instance.
        mock_google_ads_client.version = "v19"


        # Mock enum types (Path 1: Direct mock)
        mock_google_ads_client.enums.CustomizerAttributeTypeEnum.TEXT = "TEXT_ENUM_VAL"
        mock_google_ads_client.enums.CustomizerAttributeTypeEnum.PRICE = "PRICE_ENUM_VAL"
        mock_google_ads_client.enums.ServedAssetFieldTypeEnum.HEADLINE_1 = "HEADLINE_1_ENUM_VAL"

        # Mock get_type for operations and other objects
        # This needs to return a new mock object each time to simulate factory behavior
        def mock_get_type(type_name, version=None):
            mock_obj = mock.Mock()
            mock_obj.name = type_name # Store for debugging if needed
            # If it's an operation, it should have a 'create' attribute
            if "Operation" in type_name:
                mock_obj.create = mock.Mock()
            return mock_obj

        mock_google_ads_client.get_type.side_effect = mock_get_type

        # Mock service responses
        mock_customizer_attribute_service.mutate_customizer_attributes.return_value = mock.Mock(
            results=[mock.Mock(resource_name="test_text_customizer_rn"), mock.Mock(resource_name="test_price_customizer_rn")]
        )
        mock_ad_group_customizer_service.mutate_ad_group_customizers.return_value = mock.Mock(
            results=[mock.Mock(resource_name="test_agc_rn_1"), mock.Mock(resource_name="test_agc_rn_2")]
        )
        mock_ad_group_ad_service.mutate_ad_group_ads.return_value = mock.Mock(
            results=[mock.Mock(resource_name="test_ad_rn")]
        )

        # Mock GoogleAdsService ad_group_path method
        mock_google_ads_service.ad_group_path.return_value = "test/ad_group_path"

        # Dummy arguments for the main function
        customer_id = "1234567890"
        ad_group_id = "9876543210"

        # Call the main function
        add_ad_customizer.main(mock_google_ads_client, customer_id, ad_group_id)

        # Assertions
        # mock_load_from_storage.assert_called_once_with(version="v19") # Removed: main is called with a client instance directly

        # Check that get_service was called for each service
        expected_get_service_calls = [
            mock.call("CustomizerAttributeService"),
            mock.call("AdGroupCustomizerService"),
            mock.call("GoogleAdsService"),
            mock.call("AdGroupAdService")
        ]
        mock_google_ads_client.get_service.assert_has_calls(expected_get_service_calls, any_order=True)

        # Assert that mutate_customizer_attributes was called twice (once for text, once for price)
        self.assertEqual(mock_customizer_attribute_service.mutate_customizer_attributes.call_count, 2)

        # Example assertion for one of the calls to mutate_customizer_attributes
        # This is tricky because the operations are created dynamically.
        # We can check the customer_id and that operations list is not empty.
        call_args_list_cas = mock_customizer_attribute_service.mutate_customizer_attributes.call_args_list

        # First call for Text Customizer
        args_cas_text, kwargs_cas_text = call_args_list_cas[0]
        self.assertEqual(kwargs_cas_text['customer_id'], customer_id)
        self.assertEqual(len(kwargs_cas_text['operations']), 1)
        # Check properties of the created customizer attribute for text
        # The actual object passed to operations[0].create is a mock from get_type
        # We need to ensure the attributes were set on *that* mock.
        # This requires capturing the mock object created by get_type.

        # Assert that mutate_ad_group_customizers was called
        mock_ad_group_customizer_service.mutate_ad_group_customizers.assert_called_once()
        args_agcs, kwargs_agcs = mock_ad_group_customizer_service.mutate_ad_group_customizers.call_args
        self.assertEqual(kwargs_agcs['customer_id'], customer_id)
        self.assertEqual(len(kwargs_agcs['operations']), 2) # Mars and Price customizers

        # Assert that mutate_ad_group_ads was called
        mock_ad_group_ad_service.mutate_ad_group_ads.assert_called_once()
        args_agas, kwargs_agas = mock_ad_group_ad_service.mutate_ad_group_ads.call_args
        self.assertEqual(kwargs_agas['customer_id'], customer_id)
        self.assertEqual(len(kwargs_agas['operations']), 1)

        # Check some details of the ad creation
        ad_operation = kwargs_agas['operations'][0]
        # ad_group_ad.ad.final_urls.append("https://www.example.com") -> check final_urls on the *mock* for AdGroupAd
        # This gets complicated quickly due to nested mocks.
        # For now, checking the call counts and basic args is a good start.

        # Verify ad_group_path was called multiple times
        mock_google_ads_service.ad_group_path.assert_any_call(customer_id, ad_group_id)
        # It's called for each ad group customizer (2) and for the ad itself (1)
        self.assertEqual(mock_google_ads_service.ad_group_path.call_count, 3)


if __name__ == "__main__":
    unittest.main()
