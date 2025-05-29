import pytest
from unittest.mock import MagicMock, patch, call
import sys

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.v19.services.types.asset_service import AssetOperation
from google.ads.googleads.v19.services.types.campaign_asset_service import CampaignAssetOperation
from google.ads.googleads.v19.enums.types.asset_field_type import AssetFieldTypeEnum
from google.ads.googleads.v19.common.types.asset_types import SitelinkAsset
from google.ads.googleads.v19.resources.types.asset import Asset
from google.ads.googleads.v19.resources.types.campaign_asset import CampaignAsset

from examples.assets.add_sitelinks import (
    create_sitelink_assets,
    link_sitelinks_to_campaign,
    main as add_sitelinks_main,
)

# Define constants for testing
CUSTOMER_ID = "1234567890"
CAMPAIGN_ID = "9876543210"
MOCK_SITELINK_ASSET_RESOURCE_NAME_1 = f"customers/{CUSTOMER_ID}/assets/1"
MOCK_SITELINK_ASSET_RESOURCE_NAME_2 = f"customers/{CUSTOMER_ID}/assets/2"
MOCK_SITELINK_ASSET_RESOURCE_NAME_3 = f"customers/{CUSTOMER_ID}/assets/3"
MOCK_SITELINK_ASSET_RESOURCE_NAMES = [
    MOCK_SITELINK_ASSET_RESOURCE_NAME_1,
    MOCK_SITELINK_ASSET_RESOURCE_NAME_2,
    MOCK_SITELINK_ASSET_RESOURCE_NAME_3,
]

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
    mock_campaign_service = MagicMock()
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
        elif type_name == "SitelinkAsset":
            return SitelinkAsset
        elif type_name == "CampaignAsset":
            return CampaignAsset
        raise ValueError(f"Unknown type: {type_name}")
    mock_client.get_type.side_effect = get_type_side_effect

    # Mock enums
    mock_client.enums.AssetFieldTypeEnum = AssetFieldTypeEnum

    # Mock campaign_path for CampaignService
    mock_campaign_service.campaign_path.return_value = f"customers/{CUSTOMER_ID}/campaigns/{CAMPAIGN_ID}"
    return mock_client

# Test for create_sitelink_assets function
def test_create_sitelink_assets(mock_google_ads_client):
    """Tests the create_sitelink_assets function."""
    mock_asset_service = mock_google_ads_client.get_service("AssetService")
    # Mock the response from mutate_assets
    mock_asset_service.mutate_assets.return_value.results = [
        MagicMock(resource_name=MOCK_SITELINK_ASSET_RESOURCE_NAME_1),
        MagicMock(resource_name=MOCK_SITELINK_ASSET_RESOURCE_NAME_2),
        MagicMock(resource_name=MOCK_SITELINK_ASSET_RESOURCE_NAME_3),
    ]

    sitelink_data = [
        {
            "text": "Store Hours",
            "description1": "View our store hours.",
            "description2": "Monday - Friday 9am-6pm",
            "final_url": "http://example.com/storehours",
            "final_mobile_url": "http://m.example.com/storehours",
        },
        {
            "text": "Current Sales",
            "description1": "See our current sales.",
            "description2": "Sales end this week",
            "final_url": "http://example.com/sales",
            "final_mobile_url": "http://m.example.com/sales",
        },
        {
            "text": "About Us",
            "description1": "Learn more about our company.",
            "description2": "Our company history",
            "final_url": "http://example.com/about",
            "final_mobile_url": "http://m.example.com/about",
        },
    ]


    asset_resource_names = create_sitelink_assets(
        mock_google_ads_client, CUSTOMER_ID
    )

    assert asset_resource_names == MOCK_SITELINK_ASSET_RESOURCE_NAMES
    mock_asset_service.mutate_assets.assert_called_once()
    args, _ = mock_asset_service.mutate_assets.call_args
    assert args[0] == CUSTOMER_ID
    operations = args[1]  # Operations is a list
    assert len(operations) == 3

    for i, operation in enumerate(operations):
        assert isinstance(operation, AssetOperation)
        assert operation.create is not None
        created_asset = operation.create
        assert isinstance(created_asset, Asset)
        assert created_asset.sitelink_asset is not None
        sitelink = created_asset.sitelink_asset
        assert isinstance(sitelink, SitelinkAsset)
        assert sitelink.link_text == sitelink_data[i]["text"]
        assert sitelink.description1 == sitelink_data[i]["description1"]
        assert sitelink.description2 == sitelink_data[i]["description2"]
        assert sitelink.final_urls == [sitelink_data[i]["final_url"]]
        assert sitelink.final_mobile_urls == [sitelink_data[i]["final_mobile_url"]]


# Test for link_sitelinks_to_campaign function
def test_link_sitelinks_to_campaign(mock_google_ads_client):
    """Tests the link_sitelinks_to_campaign function."""
    mock_campaign_asset_service = mock_google_ads_client.get_service(
        "CampaignAssetService"
    )
    mock_campaign_service = mock_google_ads_client.get_service("CampaignService")
    # Mock the response from mutate_campaign_assets
    # We expect three results, one for each asset linked.
    mock_campaign_asset_service.mutate_campaign_assets.return_value.results = [
        MagicMock(
            resource_name=f"customers/{CUSTOMER_ID}/campaignAssets/{CAMPAIGN_ID}~{MOCK_SITELINK_ASSET_RESOURCE_NAME_1.split('/')[-1]}"
        ),
        MagicMock(
            resource_name=f"customers/{CUSTOMER_ID}/campaignAssets/{CAMPAIGN_ID}~{MOCK_SITELINK_ASSET_RESOURCE_NAME_2.split('/')[-1]}"
        ),
        MagicMock(
            resource_name=f"customers/{CUSTOMER_ID}/campaignAssets/{CAMPAIGN_ID}~{MOCK_SITELINK_ASSET_RESOURCE_NAME_3.split('/')[-1]}"
        ),
    ]
    expected_campaign_path = (
        f"customers/{CUSTOMER_ID}/campaigns/{CAMPAIGN_ID}"
    )
    # This was already mocked in the fixture, but good to be explicit if needed for a specific return
    mock_campaign_service.campaign_path.return_value = expected_campaign_path

    link_sitelinks_to_campaign(
        mock_google_ads_client,
        CUSTOMER_ID,
        CAMPAIGN_ID,
        MOCK_SITELINK_ASSET_RESOURCE_NAMES,
    )

    mock_campaign_asset_service.mutate_campaign_assets.assert_called_once()
    args, _ = mock_campaign_asset_service.mutate_campaign_assets.call_args
    assert args[0] == CUSTOMER_ID
    operations = args[1]  # Operations is a list
    assert len(operations) == len(MOCK_SITELINK_ASSET_RESOURCE_NAMES)

    for i, operation in enumerate(operations):
        assert isinstance(operation, CampaignAssetOperation)
        assert operation.create is not None
        created_campaign_asset = operation.create
        assert isinstance(created_campaign_asset, CampaignAsset)
        assert (
            created_campaign_asset.asset
            == MOCK_SITELINK_ASSET_RESOURCE_NAMES[i]
        )
        assert (
            created_campaign_asset.field_type
            == AssetFieldTypeEnum.AssetFieldType.SITELINK
        )
        assert created_campaign_asset.campaign == expected_campaign_path

    mock_campaign_service.campaign_path.assert_called_with(
        CUSTOMER_ID, CAMPAIGN_ID
    )


# Tests for main function and argument parsing
@patch.object(
    sys,
    "argv",
    [
        "examples/assets/add_sitelinks.py",
        f"--customer_id={CUSTOMER_ID}",
        f"--campaign_id={CAMPAIGN_ID}",
    ],
)
@patch("examples.assets.add_sitelinks.GoogleAdsClient.load_from_storage")
@patch("examples.assets.add_sitelinks.create_sitelink_assets")
@patch("examples.assets.add_sitelinks.link_sitelinks_to_campaign")
def test_main_function_and_args(
    mock_link_sitelinks_to_campaign,
    mock_create_sitelink_assets,
    mock_load_from_storage,
    mock_google_ads_client,  # Fixture for client
    capsys,
):
    """Tests the main function and argument parsing."""
    mock_load_from_storage.return_value = mock_google_ads_client
    mock_create_sitelink_assets.return_value = MOCK_SITELINK_ASSET_RESOURCE_NAMES
    # The link_sitelinks_to_campaign function in the example doesn't return anything
    mock_link_sitelinks_to_campaign.return_value = None

    add_sitelinks_main()

    mock_load_from_storage.assert_called_once_with(version="v19")
    mock_create_sitelink_assets.assert_called_once_with(
        mock_google_ads_client, CUSTOMER_ID
    )
    mock_link_sitelinks_to_campaign.assert_called_once_with(
        mock_google_ads_client,
        CUSTOMER_ID,
        CAMPAIGN_ID,
        MOCK_SITELINK_ASSET_RESOURCE_NAMES,
    )

    # Check stdout for printed messages
    captured = capsys.readouterr()
    for resource_name in MOCK_SITELINK_ASSET_RESOURCE_NAMES:
        assert (
            f"Sitelink asset with resource name '{resource_name}' was created."
            in captured.out
        )
    assert (
        f"{len(MOCK_SITELINK_ASSET_RESOURCE_NAMES)} sitelink assets were added "
        f"to campaign ID '{CAMPAIGN_ID}'." in captured.out
    )
