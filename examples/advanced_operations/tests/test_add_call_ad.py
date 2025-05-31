import unittest
from unittest import mock
import sys

sys.path.insert(0, '/app') # For subtask environment

from examples.advanced_operations import add_call_ad

class TestAddCallAd(unittest.TestCase):

    def _setup_common_mocks(self, mock_google_ads_client):
        mock_google_ads_client.version = "v19"

        mock_google_ads_service = mock.Mock()
        mock_ad_group_ad_service = mock.Mock()

        def get_service_side_effect(service_name, version=None):
            self.assertEqual("v19", version if version else mock_google_ads_client.version)
            if service_name == "GoogleAdsService":
                return mock_google_ads_service
            elif service_name == "AdGroupAdService":
                return mock_ad_group_ad_service
            self.fail(f"Unexpected service: {service_name}")
        mock_google_ads_client.get_service.side_effect = get_service_side_effect

        mock_ad_group_ad_operation = mock.Mock()
        mock_ad_group_ad_create_obj = mock.Mock()
        mock_ad_group_ad_operation.create = mock_ad_group_ad_create_obj

        mock_ad_obj = mock.Mock()
        mock_ad_group_ad_create_obj.ad = mock_ad_obj

        mock_call_ad_obj = mock.Mock()
        mock_ad_obj.call_ad = mock_call_ad_obj

        appended_urls = []
        def append_url_side_effect(url):
            appended_urls.append(url)
        # final_urls is a RepeatedScalarFieldContainer, mock it and its append method
        mock_final_urls_container = mock.Mock()
        mock_final_urls_container.append.side_effect = append_url_side_effect
        mock_ad_obj.final_urls = mock_final_urls_container

        def get_type_side_effect(type_name, version=None):
            if type_name == "AdGroupAdOperation":
                return mock_ad_group_ad_operation
            self.fail(f"Unexpected type: {type_name}")
        mock_google_ads_client.get_type.side_effect = get_type_side_effect

        mock_ad_status_enum = mock.Mock()
        mock_ad_status_enum.PAUSED = "PAUSED_AD_STATUS"
        mock_google_ads_client.enums.AdGroupAdStatusEnum = mock_ad_status_enum

        # Mock CallConversionReportingStateEnum states
        mock_call_conversion_enum = mock.Mock()
        mock_call_conversion_enum.UNSPECIFIED = "UNSPECIFIED_CONV_STATE" # Default/zero value for enums
        mock_call_conversion_enum.USE_RESOURCE_LEVEL_CALL_CONVERSION_ACTION = "USE_RESOURCE_CONVERSION"
        mock_call_conversion_enum.DISABLED = "DISABLED_CONVERSION_STATE" # Script does not use this if ID is None
        mock_google_ads_client.enums.CallConversionReportingStateEnum = mock_call_conversion_enum

        mock_google_ads_service.ad_group_path.return_value = "test_ad_group_path"

        mock_mutate_response = mock.Mock()
        mock_mutate_response.results = [mock.Mock(resource_name="test_ad_group_ad_rn")]
        mock_ad_group_ad_service.mutate_ad_group_ads.return_value = mock_mutate_response

        return (mock_google_ads_service, mock_ad_group_ad_service,
                mock_ad_group_ad_operation, mock_ad_group_ad_create_obj,
                mock_ad_obj, mock_call_ad_obj, appended_urls)


    @mock.patch("examples.advanced_operations.add_call_ad.GoogleAdsClient.load_from_storage")
    def test_main_functional_with_conversion_action(self, mock_load_from_storage):
        mock_google_ads_client = mock.Mock()
        (mock_google_ads_service, mock_ad_group_ad_service,
         mock_ad_group_ad_operation, mock_ad_group_ad_create_obj,
         mock_ad_obj, mock_call_ad_obj, appended_urls) = self._setup_common_mocks(mock_google_ads_client)

        # Specific mock for this case
        mock_google_ads_service.conversion_action_path.return_value = "test_conversion_action_path"

        customer_id = "cust123"
        ad_group_id = "ag123"
        phone_num = "(800) 555-0100"
        phone_country = "US"
        conv_action_id = "conv123"

        add_call_ad.main(
            mock_google_ads_client,
            customer_id,
            ad_group_id,
            phone_num,
            phone_country,
            conv_action_id
        )

        mock_google_ads_client.get_service.assert_any_call("GoogleAdsService")
        mock_google_ads_client.get_service.assert_any_call("AdGroupAdService")
        mock_google_ads_client.get_type.assert_called_once_with("AdGroupAdOperation")

        self.assertEqual(mock_ad_group_ad_create_obj.ad_group, "test_ad_group_path")
        self.assertEqual(mock_ad_group_ad_create_obj.status, "PAUSED_AD_STATUS")

        mock_ad_obj.final_urls.append.assert_called_with("https://www.example.com")
        self.assertIn("https://www.example.com", appended_urls)

        # Assertions based on add_call_ad.py script content
        self.assertEqual(mock_call_ad_obj.business_name, "Google")
        self.assertEqual(mock_call_ad_obj.headline1, "Travel")
        self.assertEqual(mock_call_ad_obj.headline2, "Discover")
        self.assertEqual(mock_call_ad_obj.description1, "Travel the World")
        self.assertEqual(mock_call_ad_obj.description2, "Travel the Universe")
        self.assertEqual(mock_call_ad_obj.phone_number, phone_num)
        self.assertEqual(mock_call_ad_obj.country_code, phone_country)
        self.assertTrue(mock_call_ad_obj.call_tracked)
        self.assertEqual(mock_call_ad_obj.path1, "services")
        self.assertEqual(mock_call_ad_obj.path2, "travels")

        self.assertEqual(mock_call_ad_obj.conversion_action, "test_conversion_action_path")
        self.assertEqual(mock_call_ad_obj.conversion_reporting_state, "USE_RESOURCE_CONVERSION")

        mock_ad_group_ad_service.mutate_ad_group_ads.assert_called_once_with(
            customer_id=customer_id, operations=[mock_ad_group_ad_operation]
        )
        mock_google_ads_service.conversion_action_path.assert_called_once_with(customer_id, conv_action_id)
        mock_google_ads_service.ad_group_path.assert_called_once_with(customer_id, ad_group_id)


    @mock.patch("examples.advanced_operations.add_call_ad.GoogleAdsClient.load_from_storage")
    def test_main_functional_without_conversion_action(self, mock_load_from_storage):
        mock_google_ads_client = mock.Mock()
        (mock_google_ads_service, mock_ad_group_ad_service,
         mock_ad_group_ad_operation, mock_ad_group_ad_create_obj,
         mock_ad_obj, mock_call_ad_obj, appended_urls) = self._setup_common_mocks(mock_google_ads_client)

        customer_id = "cust456"
        ad_group_id = "ag456"
        phone_num = "(800) 555-0101"
        phone_country = "CA"

        add_call_ad.main(
            mock_google_ads_client,
            customer_id,
            ad_group_id,
            phone_num,
            phone_country,
            None # No conversion_action_id
        )

        mock_google_ads_client.get_service.assert_any_call("GoogleAdsService")
        mock_google_ads_client.get_service.assert_any_call("AdGroupAdService")
        mock_google_ads_client.get_type.assert_called_once_with("AdGroupAdOperation")

        self.assertEqual(mock_ad_group_ad_create_obj.ad_group, "test_ad_group_path")
        self.assertEqual(mock_ad_group_ad_create_obj.status, "PAUSED_AD_STATUS")

        mock_ad_obj.final_urls.append.assert_called_with("https://www.example.com")
        self.assertIn("https://www.example.com", appended_urls)

        self.assertEqual(mock_call_ad_obj.business_name, "Google")
        self.assertEqual(mock_call_ad_obj.phone_number, phone_num)
        self.assertEqual(mock_call_ad_obj.country_code, phone_country)
        self.assertTrue(mock_call_ad_obj.call_tracked)
        # Path1 and path2 from script
        self.assertEqual(mock_call_ad_obj.path1, "services")
        self.assertEqual(mock_call_ad_obj.path2, "travels")


        mock_google_ads_service.conversion_action_path.assert_not_called()
        # If conversion_action_id is None, the script does not set these attributes.
        # They should remain as default Mock objects if accessed, or not exist if not accessed by script.
        # Asserting they are Mocks means they were not set to a concrete value by the script.
        self.assertIsInstance(mock_call_ad_obj.conversion_action, mock.Mock,
                              "conversion_action should remain a mock (i.e. not set by script)")
        self.assertIsInstance(mock_call_ad_obj.conversion_reporting_state, mock.Mock,
                              "conversion_reporting_state should remain a mock (i.e. not set by script)")

        mock_ad_group_ad_service.mutate_ad_group_ads.assert_called_once_with(
            customer_id=customer_id, operations=[mock_ad_group_ad_operation]
        )
        mock_google_ads_service.ad_group_path.assert_called_once_with(customer_id, ad_group_id)

if __name__ == "__main__":
    unittest.main()
