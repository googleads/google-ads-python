import pytest
from unittest.mock import MagicMock, patch, call
import sys
import uuid

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.v19.services.types.asset_service import AssetOperation
from google.ads.googleads.v19.services.types.campaign_asset_service import CampaignAssetOperation
from google.ads.googleads.v19.enums.types.asset_field_type import AssetFieldTypeEnum
from google.ads.googleads.v19.enums.types.lead_form_call_to_action_type import LeadFormCallToActionTypeEnum
from google.ads.googleads.v19.enums.types.lead_form_field_user_input_type import LeadFormFieldUserInputTypeEnum
from google.ads.googleads.v19.enums.types.lead_form_post_submit_call_to_action_type import LeadFormPostSubmitCallToActionTypeEnum

from examples.assets.add_lead_form_asset import (
    create_lead_form_asset,
    create_lead_form_campaign_asset,
    main as add_lead_form_main,
)
from google.ads.googleads.v19.resources.types.asset import Asset
from google.ads.googleads.v19.common.types.asset_types import (
    LeadFormAsset,
    LeadFormField,
    LeadFormSingleChoiceAnswers,
    LeadFormDeliveryMethod,
    WebhookDelivery,
)
from google.ads.googleads.v19.resources.types.campaign_asset import CampaignAsset


# Define constants for testing
CUSTOMER_ID = "1234567890"
CAMPAIGN_ID = "9876543210"
MOCK_LEAD_FORM_ASSET_RESOURCE_NAME = f"customers/{CUSTOMER_ID}/assets/1"
FIXED_UUID = "fixed-uuid-for-testing"
EXPECTED_ASSET_NAME = f"Interplanetary Cruise Lead Form Asset #{FIXED_UUID}"

@pytest.fixture
def mock_google_ads_client():
    """Provides a mock GoogleAdsClient."""
    mock_client = MagicMock(spec=GoogleAdsClient)
    mock_client.get_service = MagicMock()
    mock_client.get_type = MagicMock()
    mock_client.enums = MagicMock()
    # Mock get_service
    mock_asset_service = MagicMock()
    mock_campaign_asset_service = MagicMock()
    mock_campaign_service = MagicMock() # For campaign_path
    mock_client.get_service.side_effect = lambda service_name: {
        "AssetService": mock_asset_service,
        "CampaignAssetService": mock_campaign_asset_service,
        "CampaignService": mock_campaign_service,
    }.get(service_name)

    # Mock get_type
    def get_type_side_effect(type_name, version=None):
        if type_name == "AssetOperation":
            return AssetOperation
        elif type_name == "CampaignAssetOperation":
            return CampaignAssetOperation
        elif type_name == "Asset":
            return Asset
        elif type_name == "LeadFormAsset":
            return LeadFormAsset
        elif type_name == "LeadFormField":
            return LeadFormField
        elif type_name == "LeadFormSingleChoiceAnswers":
            return LeadFormSingleChoiceAnswers
        elif type_name == "LeadFormDeliveryMethod":
            return LeadFormDeliveryMethod
        elif type_name == "WebhookDelivery":
            return WebhookDelivery
        elif type_name == "CampaignAsset":
            return CampaignAsset
        raise ValueError(f"Unknown type: {type_name}")
    mock_client.get_type.side_effect = get_type_side_effect

    # Mock enums
    mock_client.enums.AssetFieldTypeEnum = AssetFieldTypeEnum
    mock_client.enums.LeadFormCallToActionTypeEnum = LeadFormCallToActionTypeEnum
    mock_client.enums.LeadFormFieldUserInputTypeEnum = LeadFormFieldUserInputTypeEnum
    mock_client.enums.LeadFormPostSubmitCallToActionTypeEnum = LeadFormPostSubmitCallToActionTypeEnum

    # Mock campaign_path for CampaignService
    mock_campaign_service.campaign_path.return_value = f"customers/{CUSTOMER_ID}/campaigns/{CAMPAIGN_ID}"

    return mock_client

# Test for create_lead_form_asset function
@patch("uuid.uuid4", return_value=FIXED_UUID)
def test_create_lead_form_asset(mock_uuid, mock_google_ads_client):
    """Tests the create_lead_form_asset function."""
    mock_asset_service = mock_google_ads_client.get_service("AssetService")
    # Mock the response from mutate_assets
    mock_asset_service.mutate_assets.return_value.results = [
        MagicMock(resource_name=MOCK_LEAD_FORM_ASSET_RESOURCE_NAME)
    ]

    asset_resource_name = create_lead_form_asset(
        mock_google_ads_client, CUSTOMER_ID
    )

    assert asset_resource_name == MOCK_LEAD_FORM_ASSET_RESOURCE_NAME
    mock_asset_service.mutate_assets.assert_called_once()
    args, _ = mock_asset_service.mutate_assets.call_args
    assert args[0] == CUSTOMER_ID
    operation = args[1][0] # Operations is a list
    assert isinstance(operation, AssetOperation)
    assert operation.create is not None
    created_asset = operation.create
    assert isinstance(created_asset, Asset)
    assert created_asset.name == EXPECTED_ASSET_NAME
    assert created_asset.final_urls == ["http://example.com/lead_form"]
    assert created_asset.lead_form_asset is not None

    lead_form = created_asset.lead_form_asset
    assert isinstance(lead_form, LeadFormAsset)
    assert lead_form.call_to_action_type == LeadFormCallToActionTypeEnum.LeadFormCallToActionType.BOOK_NOW
    assert lead_form.call_to_action_description == "Book Now"
    assert lead_form.business_name == "Interplanetary Cruise"
    assert lead_form.headline == "Trip to Mars"
    assert lead_form.description == "Lead Form for Interplanetary Cruise"
    assert lead_form.privacy_policy_url == "http://example.com/privacy"
    assert lead_form.post_submit_headline == "Thanks for signing up!"
    assert lead_form.post_submit_description == "We will reach out to you shortly."
    assert lead_form.post_submit_call_to_action_type == LeadFormPostSubmitCallToActionTypeEnum.LeadFormPostSubmitCallToActionType.VISIT_SITE
    assert lead_form.custom_disclosure == "This is a custom disclosure."

    # Check fields
    assert len(lead_form.fields) == 4
    field_input_types = [
        LeadFormFieldUserInputTypeEnum.LeadFormFieldUserInputType.FULL_NAME,
        LeadFormFieldUserInputTypeEnum.LeadFormFieldUserInputType.EMAIL,
        LeadFormFieldUserInputTypeEnum.LeadFormFieldUserInputType.PHONE_NUMBER,
        LeadFormFieldUserInputTypeEnum.LeadFormFieldUserInputType.MULTIPLE_CHOICE,
    ]
    for i, field in enumerate(lead_form.fields):
        assert isinstance(field, LeadFormField)
        assert field.input_type == field_input_types[i]
        if field.input_type == LeadFormFieldUserInputTypeEnum.LeadFormFieldUserInputType.MULTIPLE_CHOICE:
            assert isinstance(field.single_choice_answers, LeadFormSingleChoiceAnswers)
            assert field.single_choice_answers.answers == ["Mars", "Venus", "Jupiter"]

    # Check delivery methods
    assert len(lead_form.delivery_methods) == 1
    delivery_method = lead_form.delivery_methods[0]
    assert isinstance(delivery_method, LeadFormDeliveryMethod)
    assert delivery_method.webhook is not None
    webhook = delivery_method.webhook
    assert isinstance(webhook, WebhookDelivery)
    assert webhook.advertiser_webhook_url == "https://example.com/webhook"
    assert webhook.google_secret == "interplanetary_cruise_secret"
    assert webhook.payload_schema_version == 3

    mock_uuid.assert_called_once()


# Test for create_lead_form_campaign_asset function
def test_create_lead_form_campaign_asset(mock_google_ads_client):
    """Tests the create_lead_form_campaign_asset function."""
    mock_campaign_asset_service = mock_google_ads_client.get_service(
        "CampaignAssetService"
    )
    mock_campaign_service = mock_google_ads_client.get_service("CampaignService")
    # Mock the response from mutate_campaign_assets
    mock_campaign_asset_service.mutate_campaign_assets.return_value.results = [
        MagicMock(
            resource_name=f"customers/{CUSTOMER_ID}/campaignAssets/{CAMPAIGN_ID}~{MOCK_LEAD_FORM_ASSET_RESOURCE_NAME.split('/')[-1]}"
        )
    ]
    expected_campaign_path = (
        f"customers/{CUSTOMER_ID}/campaigns/{CAMPAIGN_ID}"
    )
    mock_campaign_service.campaign_path.return_value = expected_campaign_path

    create_lead_form_campaign_asset(
        mock_google_ads_client,
        CUSTOMER_ID,
        CAMPAIGN_ID,
        MOCK_LEAD_FORM_ASSET_RESOURCE_NAME,
    )

    mock_campaign_asset_service.mutate_campaign_assets.assert_called_once()
    args, _ = mock_campaign_asset_service.mutate_campaign_assets.call_args
    assert args[0] == CUSTOMER_ID
    operation = args[1][0] # Operations is a list
    assert isinstance(operation, CampaignAssetOperation)
    assert operation.create is not None
    created_campaign_asset = operation.create
    assert isinstance(created_campaign_asset, CampaignAsset)
    assert created_campaign_asset.asset == MOCK_LEAD_FORM_ASSET_RESOURCE_NAME
    assert (
        created_campaign_asset.field_type
        == AssetFieldTypeEnum.AssetFieldType.LEAD_FORM
    )
    assert created_campaign_asset.campaign == expected_campaign_path
    mock_campaign_service.campaign_path.assert_called_once_with(
        CUSTOMER_ID, CAMPAIGN_ID
    )


# Tests for main function and argument parsing
@patch.object(
    sys,
    "argv",
    [
        "examples/assets/add_lead_form_asset.py",
        f"--customer_id={CUSTOMER_ID}",
        f"--campaign_id={CAMPAIGN_ID}",
    ],
)
@patch("examples.assets.add_lead_form_asset.GoogleAdsClient.load_from_storage")
@patch("examples.assets.add_lead_form_asset.create_lead_form_asset")
@patch("examples.assets.add_lead_form_asset.create_lead_form_campaign_asset")
def test_main_function_and_args(
    mock_create_lead_form_campaign_asset,
    mock_create_lead_form_asset,
    mock_load_from_storage,
    mock_google_ads_client,  # Fixture for client
    capsys,
):
    """Tests the main function and argument parsing."""
    mock_load_from_storage.return_value = mock_google_ads_client
    mock_create_lead_form_asset.return_value = (
        MOCK_LEAD_FORM_ASSET_RESOURCE_NAME
    )
    # The create_lead_form_campaign_asset function in the example doesn't return anything
    mock_create_lead_form_campaign_asset.return_value = None

    add_lead_form_main()

    mock_load_from_storage.assert_called_once_with(version="v19")
    mock_create_lead_form_asset.assert_called_once_with(
        mock_google_ads_client, CUSTOMER_ID
    )
    mock_create_lead_form_campaign_asset.assert_called_once_with(
        mock_google_ads_client,
        CUSTOMER_ID,
        CAMPAIGN_ID,
        MOCK_LEAD_FORM_ASSET_RESOURCE_NAME,
    )

    # Check stdout for printed messages
    captured = capsys.readouterr()
    assert (
        f"Lead form asset created with resource name: '{MOCK_LEAD_FORM_ASSET_RESOURCE_NAME}'"
        in captured.out
    )
    assert (
        f"Lead form asset with resource name '{MOCK_LEAD_FORM_ASSET_RESOURCE_NAME}' "
        f"was added to campaign with ID '{CAMPAIGN_ID}'." in captured.out
    )
