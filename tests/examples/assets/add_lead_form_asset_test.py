import unittest
from unittest.mock import MagicMock, patch, call
from uuid import UUID  # For checking UUID patch

from examples.assets import add_lead_form_asset


class TestAddLeadFormAsset(unittest.TestCase):
    @patch("examples.assets.add_lead_form_asset.uuid4")
    @patch("examples.assets.add_lead_form_asset.GoogleAdsClient")
    def test_create_lead_form_asset(
        self, mock_google_ads_client_constructor, mock_uuid4
    ):
        mock_client_instance = mock_google_ads_client_constructor.return_value
        mock_asset_service = MagicMock()
        mock_client_instance.get_service.return_value = mock_asset_service

        mock_asset_operation = MagicMock()
        # mock_client_instance.get_type.return_value = mock_asset_operation # Modified by side_effect below
        mock_created_asset = mock_asset_operation.create
        mock_created_asset.final_urls = (
            []
        )  # Initialize as a list for append and assertIn
        # Ensure lead_form_asset and its sub-attributes are also MagicMocks
        # to allow attribute assignment and list appends
        mock_created_asset.lead_form_asset = MagicMock()
        mock_created_asset.lead_form_asset.fields = []
        mock_created_asset.lead_form_asset.delivery_methods = []

        # Mock enums
        mock_client_instance.enums.LeadFormCallToActionTypeEnum.BOOK_NOW = (
            "BOOK_NOW_ENUM"
        )
        mock_client_instance.enums.LeadFormFieldUserInputTypeEnum.FULL_NAME = (
            "FULL_NAME_ENUM"
        )
        mock_client_instance.enums.LeadFormFieldUserInputTypeEnum.EMAIL = (
            "EMAIL_ENUM"
        )
        mock_client_instance.enums.LeadFormFieldUserInputTypeEnum.PHONE_NUMBER = (
            "PHONE_NUMBER_ENUM"
        )
        mock_client_instance.enums.LeadFormFieldUserInputTypeEnum.PREFERRED_CONTACT_TIME = (
            "PREFERRED_CONTACT_TIME_ENUM"
        )
        mock_client_instance.enums.LeadFormPostSubmitCallToActionTypeEnum.VISIT_SITE = (
            "VISIT_SITE_ENUM"
        )

        # Mock LeadFormField type (called multiple times)
        # Let get_type return the operation for "AssetOperation", and field type for "LeadFormField" etc.
        def get_type_side_effect(type_name):
            if type_name == "AssetOperation":
                return mock_asset_operation
            elif type_name == "LeadFormField":
                # Return a new MagicMock each time to simulate creating new field objects
                field_mock = MagicMock()
                # If single_choice_answers might be accessed, it needs to be a mock that supports .answers.extend
                field_mock.single_choice_answers = MagicMock()
                field_mock.single_choice_answers.answers = MagicMock(
                    spec=list
                )  # Mock .answers as a list-like object
                field_mock.single_choice_answers.answers.extend = (
                    MagicMock()
                )  # Mock the extend method
                return field_mock
            elif type_name == "LeadFormDeliveryMethod":
                delivery_mock = MagicMock()
                delivery_mock.webhook = (
                    MagicMock()
                )  # Ensure webhook attribute exists
                return delivery_mock
            return MagicMock()  # Default mock for other types

        mock_client_instance.get_type.side_effect = get_type_side_effect

        fake_uuid = UUID("12345678-1234-5678-1234-567812345678")
        mock_uuid4.return_value = fake_uuid

        customer_id = "test_customer_123"
        expected_asset_name = f"Interplanetary Cruise #{fake_uuid} Lead Form"

        mock_asset_service.mutate_assets.return_value.results = [
            MagicMock(resource_name="lead_form_asset_rn")
        ]

        resource_name = add_lead_form_asset.create_lead_form_asset(
            mock_client_instance, customer_id
        )

        self.assertEqual(resource_name, "lead_form_asset_rn")
        mock_uuid4.assert_called_once()

        mock_client_instance.get_service.assert_called_with("AssetService")
        self.assertEqual(mock_client_instance.get_service.call_count, 2)

        self.assertEqual(mock_created_asset.name, expected_asset_name)
        self.assertIn(
            "http://example.com/jupiter", mock_created_asset.final_urls
        )

        lead_form_asset_mock = mock_created_asset.lead_form_asset
        self.assertEqual(
            lead_form_asset_mock.call_to_action_type, "BOOK_NOW_ENUM"
        )
        self.assertEqual(
            lead_form_asset_mock.call_to_action_description,
            "Latest trip to Jupiter!",
        )
        self.assertEqual(
            lead_form_asset_mock.business_name, "Interplanetary Cruise"
        )
        self.assertEqual(lead_form_asset_mock.headline, "Trip to Jupiter")
        self.assertEqual(
            lead_form_asset_mock.description,
            "Our latest trip to Jupiter is now open for booking.",
        )
        self.assertEqual(
            lead_form_asset_mock.privacy_policy_url,
            "http://example.com/privacy",
        )

        self.assertEqual(len(lead_form_asset_mock.fields), 4)
        # Check that single_choice_answers.answers.extend was called for the relevant field
        # This requires finding which mock LeadFormField had single_choice_answers set.
        # The get_type_side_effect returns new mocks, so we'd have to inspect mock_client_instance.get_type.side_effect.call_args_list
        # or more simply, check if *any* of the .extend mocks were called if possible, or rely on other field attributes.
        # For now, the length check for fields is the main structural check here.

        self.assertEqual(
            lead_form_asset_mock.post_submit_headline, "Thanks for signing up!"
        )
        self.assertEqual(
            lead_form_asset_mock.post_submit_description,
            "We will reach out to you shortly. Visit our website to see past trip details.",
        )
        self.assertEqual(
            lead_form_asset_mock.post_submit_call_to_action_type,
            "VISIT_SITE_ENUM",
        )
        self.assertEqual(
            lead_form_asset_mock.custom_disclosure,
            "Trip may get cancelled due to meteor shower",
        )

        self.assertEqual(len(lead_form_asset_mock.delivery_methods), 1)
        # Example check for webhook details (assuming the first delivery method is the webhook)
        delivery_method_mock = lead_form_asset_mock.delivery_methods[0]
        self.assertEqual(
            delivery_method_mock.webhook.advertiser_webhook_url,
            "http://example.com/webhook",
        )
        self.assertEqual(
            delivery_method_mock.webhook.google_secret,
            "interplanetary google secret",
        )
        self.assertEqual(delivery_method_mock.webhook.payload_schema_version, 3)

        mock_asset_service.mutate_assets.assert_called_once_with(
            customer_id=customer_id, operations=[mock_asset_operation]
        )

    @patch("examples.assets.add_lead_form_asset.GoogleAdsClient")
    def test_create_lead_form_campaign_asset(
        self, mock_google_ads_client_constructor
    ):
        mock_client_instance = mock_google_ads_client_constructor.return_value
        mock_campaign_service = MagicMock()
        mock_campaign_asset_service = MagicMock()

        def get_service_side_effect(service_name):
            if service_name == "CampaignService":
                return mock_campaign_service
            elif service_name == "CampaignAssetService":
                return mock_campaign_asset_service
            return MagicMock()

        mock_client_instance.get_service.side_effect = get_service_side_effect

        mock_campaign_asset_operation = MagicMock()
        mock_client_instance.get_type.return_value = (
            mock_campaign_asset_operation
        )
        mock_created_campaign_asset = mock_campaign_asset_operation.create

        mock_client_instance.enums.AssetFieldTypeEnum.LEAD_FORM = (
            "LEAD_FORM_ENUM"
        )

        customer_id = "test_customer_123"
        campaign_id = "campaign_x"
        lead_form_asset_rn = "lead_form_asset_rn"
        expected_campaign_path = (
            "customers/test_customer_123/campaigns/campaign_x"
        )
        mock_campaign_service.campaign_path.return_value = (
            expected_campaign_path
        )

        mock_campaign_asset_service.mutate_campaign_assets.return_value.results = [
            MagicMock(resource_name="ca_lf_asset_rn")
        ]

        add_lead_form_asset.create_lead_form_campaign_asset(
            mock_client_instance, customer_id, campaign_id, lead_form_asset_rn
        )

        mock_client_instance.get_service.assert_any_call("CampaignService")
        mock_client_instance.get_service.assert_any_call("CampaignAssetService")
        mock_client_instance.get_type.assert_called_once_with(
            "CampaignAssetOperation"
        )

        mock_campaign_service.campaign_path.assert_called_once_with(
            customer_id, campaign_id
        )

        self.assertEqual(mock_created_campaign_asset.asset, lead_form_asset_rn)
        self.assertEqual(
            mock_created_campaign_asset.field_type, "LEAD_FORM_ENUM"
        )
        self.assertEqual(
            mock_created_campaign_asset.campaign, expected_campaign_path
        )

        mock_campaign_asset_service.mutate_campaign_assets.assert_called_once_with(
            customer_id=customer_id, operations=[mock_campaign_asset_operation]
        )

    @patch(
        "examples.assets.add_lead_form_asset.create_lead_form_campaign_asset"
    )
    @patch("examples.assets.add_lead_form_asset.create_lead_form_asset")
    def test_main_function_logic(
        self, mock_create_lf_asset, mock_create_lf_campaign_asset
    ):
        mock_client = MagicMock()
        customer_id = "cust1"
        campaign_id = "camp1"
        lead_form_asset_rn = "lf_asset_rn"
        mock_create_lf_asset.return_value = lead_form_asset_rn

        add_lead_form_asset.main(mock_client, customer_id, campaign_id)

        mock_create_lf_asset.assert_called_once_with(mock_client, customer_id)
        mock_create_lf_campaign_asset.assert_called_once_with(
            mock_client, customer_id, campaign_id, lead_form_asset_rn
        )
