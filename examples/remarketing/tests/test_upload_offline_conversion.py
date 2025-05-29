import unittest
from unittest.mock import MagicMock, patch, PropertyMock, call

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.v19.services.services.conversion_upload_service.client import (
    ConversionUploadServiceClient,
)
from google.ads.googleads.v19.services.services.conversion_action_service.client import (
    ConversionActionServiceClient,
)
from google.ads.googleads.v19.enums.types.consent_status import ConsentStatusEnum

from examples.remarketing.upload_offline_conversion import main


class TestUploadOfflineConversionScenarios(unittest.TestCase):
    def setUp(self):
        """Common setup for all tests."""
        self.mock_google_ads_client = MagicMock(spec=GoogleAdsClient)
        self.mock_google_ads_client.api_version = "v19"

        self.mock_conversion_upload_service = MagicMock(spec=ConversionUploadServiceClient)
        self.mock_conversion_action_service = MagicMock(spec=ConversionActionServiceClient)

        def get_service_side_effect(service_name, version=None):
            if service_name == "ConversionUploadService":
                return self.mock_conversion_upload_service
            elif service_name == "ConversionActionService":
                return self.mock_conversion_action_service
            raise ValueError(f"Unexpected service requested: {service_name}")
        self.mock_google_ads_client.get_service.side_effect = get_service_side_effect

        # This will be the core mock for the ClickConversion object
        self.mock_click_conversion = MagicMock(name="ClickConversionInstance")
        
        # Attach PropertyMocks for all attributes that might be set
        # We can create these on demand in each test or all here. For clarity, some will be in tests.
        self.mock_conversion_action_prop = PropertyMock()
        type(self.mock_click_conversion).conversion_action = self.mock_conversion_action_prop
        
        self.mock_gclid_prop = PropertyMock()
        type(self.mock_click_conversion).gclid = self.mock_gclid_prop
        
        self.mock_gbraid_prop = PropertyMock()
        type(self.mock_click_conversion).gbraid = self.mock_gbraid_prop

        self.mock_wbraid_prop = PropertyMock()
        type(self.mock_click_conversion).wbraid = self.mock_wbraid_prop
        
        self.mock_conversion_value_prop = PropertyMock()
        type(self.mock_click_conversion).conversion_value = self.mock_conversion_value_prop
        
        self.mock_conversion_date_time_prop = PropertyMock()
        type(self.mock_click_conversion).conversion_date_time = self.mock_conversion_date_time_prop
        
        self.mock_currency_code_prop = PropertyMock()
        type(self.mock_click_conversion).currency_code = self.mock_currency_code_prop

        self.mock_order_id_prop = PropertyMock()
        type(self.mock_click_conversion).order_id = self.mock_order_id_prop

        # Setup for nested objects/lists
        self.mock_click_conversion.custom_variables = [] # Real list for append
        self.mock_click_conversion.consent = MagicMock(name="ConsentOnclick_conversion") # Nested mock

        # Mock for client.enums.ConsentStatusEnum
        self.mock_google_ads_client.enums = MagicMock() 
        self.mock_consent_status_enum_dict = MagicMock()
        self.mock_consent_status_enum_dict.__getitem__.side_effect = lambda key: getattr(ConsentStatusEnum.ConsentStatus, key, ConsentStatusEnum.ConsentStatus.UNKNOWN)
        self.mock_google_ads_client.enums.ConsentStatusEnum = self.mock_consent_status_enum_dict

        # Default return value for conversion_action_path
        self.formatted_conversion_action_path = "customers/test_customer_id/conversionActions/test_conv_action_id"
        self.mock_conversion_action_service.conversion_action_path.return_value = self.formatted_conversion_action_path

        # Default mock response for upload_click_conversions
        mock_upload_response = MagicMock(name="UploadResponse")
        mock_conversion_result = MagicMock(name="ConversionResult")
        mock_upload_response.results = [mock_conversion_result]
        mock_upload_response.partial_failure_error = None
        self.mock_conversion_upload_service.upload_click_conversions.return_value = mock_upload_response
        # Make result attributes callable for the print statement
        mock_conversion_result.conversion_date_time = "default_date_time"
        mock_conversion_result.gclid = "default_gclid"
        mock_conversion_result.conversion_action = "default_conv_action"


    def get_type_side_effect_config(self, mock_custom_variable_to_return=None):
        """Helper to configure get_type side effect, potentially returning a specific mock for CustomVariable."""
        def get_type_side_effect(type_name, **kwargs):
            if type_name == "ClickConversion":
                return self.mock_click_conversion 
            elif type_name == "UploadClickConversionsRequest":
                mock_req = MagicMock(name="UploadClickConversionsRequestInstance")
                mock_req.conversions = [] 
                return mock_req
            elif type_name == "CustomVariable":
                return mock_custom_variable_to_return if mock_custom_variable_to_return else MagicMock(name="CustomVariableInstance")
            elif type_name == "Consent":
                 return MagicMock(name="ConsentInstance") # For client.get_type("Consent")
            return MagicMock(name=f"UnknownType_{type_name}")
        return get_type_side_effect

    @patch("examples.remarketing.upload_offline_conversion.GoogleAdsClient.load_from_storage")
    def test_main_gclid_scenario(self, mock_load_from_storage):
        mock_load_from_storage.return_value = self.mock_google_ads_client
        self.mock_google_ads_client.get_type.side_effect = self.get_type_side_effect_config()
        
        # Test arguments
        customer_id = "test_customer_id"
        conversion_action_id = "test_conv_action_id"
        gclid = "test_gclid_val"
        conversion_date_time = "2024-01-01 10:00:00+00:00"
        conversion_value_str = "12.34"

        main(
            self.mock_google_ads_client, customer_id, conversion_action_id, gclid,
            conversion_date_time, conversion_value_str, None, None, None, None, None, None
        )

        self.mock_conversion_action_service.conversion_action_path.assert_called_once_with(customer_id, conversion_action_id)
        self.mock_conversion_action_prop.assert_called_once_with(self.formatted_conversion_action_path)
        self.mock_gclid_prop.assert_called_once_with(gclid)
        self.mock_conversion_value_prop.assert_called_once_with(float(conversion_value_str))
        self.mock_conversion_date_time_prop.assert_called_once_with(conversion_date_time)
        self.mock_currency_code_prop.assert_called_once_with("USD")

        self.mock_conversion_upload_service.upload_click_conversions.assert_called_once()
        upload_call_args = self.mock_conversion_upload_service.upload_click_conversions.call_args
        request_obj = upload_call_args.kwargs.get('request')
        self.assertEqual(request_obj.customer_id, customer_id)
        self.assertTrue(request_obj.partial_failure)
        self.assertEqual(len(request_obj.conversions), 1)
        self.assertIs(request_obj.conversions[0], self.mock_click_conversion)

    @patch("examples.remarketing.upload_offline_conversion.GoogleAdsClient.load_from_storage")
    def test_main_gbraid_scenario(self, mock_load_from_storage):
        mock_load_from_storage.return_value = self.mock_google_ads_client
        self.mock_google_ads_client.get_type.side_effect = self.get_type_side_effect_config()

        gbraid_val = "test_gbraid_val_001" # Ensure unique value
        main(
            client=self.mock_google_ads_client,
            customer_id="cust_gbraid",
            conversion_action_id="ca_gbraid",
            gclid=None, # Explicitly None
            conversion_date_time="dt_gbraid",
            conversion_value="1.0",
            conversion_custom_variable_id=None,
            conversion_custom_variable_value=None,
            gbraid=gbraid_val, # Set gbraid
            wbraid=None, # Explicitly None
            order_id=None, 
            ad_user_data_consent=None
        )
        self.mock_gbraid_prop.assert_called_once_with(gbraid_val)

    @patch("examples.remarketing.upload_offline_conversion.GoogleAdsClient.load_from_storage")
    def test_main_wbraid_scenario(self, mock_load_from_storage):
        mock_load_from_storage.return_value = self.mock_google_ads_client
        self.mock_google_ads_client.get_type.side_effect = self.get_type_side_effect_config()

        wbraid_val = "UNIQUE_WBRAID_VALUE_999" # Make it super unique
        
        # Call main with keyword arguments for clarity
        main(
            client=self.mock_google_ads_client,
            customer_id="cust_wbraid",
            conversion_action_id="ca_wbraid",
            gclid=None,
            conversion_date_time="dt_wbraid",
            conversion_value="1.0",
            conversion_custom_variable_id=None,
            conversion_custom_variable_value=None,
            gbraid=None,
            wbraid=wbraid_val, # This is the key parameter
            order_id=None,
            ad_user_data_consent=None
        )
        self.mock_wbraid_prop.assert_called_once_with(wbraid_val)

    @patch("examples.remarketing.upload_offline_conversion.GoogleAdsClient.load_from_storage")
    def test_main_order_id_scenario(self, mock_load_from_storage):
        mock_load_from_storage.return_value = self.mock_google_ads_client
        self.mock_google_ads_client.get_type.side_effect = self.get_type_side_effect_config()
        
        order_id_val = "test_order_id_002" # Ensure unique value
        main(
            client=self.mock_google_ads_client,
            customer_id="cust_order_id",
            conversion_action_id="ca_order_id",
            gclid="gclid_for_order_id_test", # gclid needs to be present for order_id to be processed in some contexts
            conversion_date_time="dt_order_id",
            conversion_value="2.0",
            conversion_custom_variable_id=None,
            conversion_custom_variable_value=None,
            gbraid=None,
            wbraid=None,
            order_id=order_id_val, # Set order_id
            ad_user_data_consent=None
        )
        self.mock_order_id_prop.assert_called_once_with(order_id_val)

    @patch("examples.remarketing.upload_offline_conversion.GoogleAdsClient.load_from_storage")
    def test_main_custom_variable_scenario(self, mock_load_from_storage):
        mock_load_from_storage.return_value = self.mock_google_ads_client
        
        mock_custom_var_instance = MagicMock(name="SpecificCustomVariableInstance")
        # Attach PropertyMocks to this specific custom variable mock
        mock_cv_path_prop = PropertyMock()
        type(mock_custom_var_instance).conversion_custom_variable = mock_cv_path_prop
        mock_cv_value_prop = PropertyMock()
        type(mock_custom_var_instance).value = mock_cv_value_prop
        
        self.mock_google_ads_client.get_type.side_effect = self.get_type_side_effect_config(
            mock_custom_variable_to_return=mock_custom_var_instance
        )

        customer_id = "cust_cv"
        custom_var_id = "cv_id_1"
        custom_var_value = "cv_val_abc"
        expected_cv_path = f"customers/{customer_id}/conversionCustomVariables/{custom_var_id}"
        self.mock_conversion_upload_service.conversion_custom_variable_path.return_value = expected_cv_path

        # Clear custom_variables list on the shared mock_click_conversion before this test
        self.mock_click_conversion.custom_variables = []

        main(
            self.mock_google_ads_client, customer_id, "ca_cv", "gclid_cv", "dt_cv", "3.0",
            custom_var_id, custom_var_value, None, None, None, None
        )

        self.mock_conversion_upload_service.conversion_custom_variable_path.assert_called_once_with(customer_id, custom_var_id)
        mock_cv_path_prop.assert_called_once_with(expected_cv_path)
        mock_cv_value_prop.assert_called_once_with(custom_var_value)
        
        self.assertEqual(len(self.mock_click_conversion.custom_variables), 1)
        self.assertIs(self.mock_click_conversion.custom_variables[0], mock_custom_var_instance)

    @patch("examples.remarketing.upload_offline_conversion.GoogleAdsClient.load_from_storage")
    def test_main_ad_user_data_consent_scenario(self, mock_load_from_storage):
        mock_load_from_storage.return_value = self.mock_google_ads_client
        self.mock_google_ads_client.get_type.side_effect = self.get_type_side_effect_config()

        # Attach PropertyMock to the ad_user_data attribute of the pre-configured consent mock
        mock_ad_user_data_prop = PropertyMock()
        # self.mock_click_conversion.consent is already a MagicMock from setUp
        type(self.mock_click_conversion.consent).ad_user_data = mock_ad_user_data_prop
        
        consent_str = "GRANTED"
        expected_enum_member = ConsentStatusEnum.ConsentStatus.GRANTED 

        main(
            self.mock_google_ads_client, "cust_consent", "ca_consent", "gclid_consent",
            "dt_consent", "4.0", None, None, None, None, None, consent_str
        )
        
        self.mock_consent_status_enum_dict.__getitem__.assert_called_once_with(consent_str)
        mock_ad_user_data_prop.assert_called_once_with(expected_enum_member)


if __name__ == "__main__":
    unittest.main()
