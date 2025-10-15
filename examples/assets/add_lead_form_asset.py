#!/usr/bin/env python
# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Creates a lead form and a lead form extension for a campaign.

Run add_campaigns.py to create a campaign.
"""


import argparse
import sys
from uuid import uuid4

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
from google.ads.googleads.v22.services.types.asset_service import AssetOperation
from google.ads.googleads.v22.resources.types.asset import Asset
from google.ads.googleads.v22.common.types.asset_types import LeadFormAsset
from google.ads.googleads.v22.common.types.asset_types import LeadFormField
from google.ads.googleads.v22.common.types.asset_types import (
    LeadFormDeliveryMethod,
)
from google.ads.googleads.v22.services.types.campaign_asset_service import (
    CampaignAssetOperation,
)
from google.ads.googleads.v22.resources.types.campaign_asset import (
    CampaignAsset,
)


def main(client: GoogleAdsClient, customer_id: str, campaign_id: str) -> None:
    """Creates a lead form and lead form extension for the given campaign.

    Args:
        client: An initialized GoogleAdsClient instance.
        customer_id: The Google Ads customer ID.
        campaign_id: The ID for a Campaign belonging to the given customer.
    """
    lead_form_asset_resource_name: str = create_lead_form_asset(
        client, customer_id
    )
    create_lead_form_campaign_asset(
        client, customer_id, campaign_id, lead_form_asset_resource_name
    )


# [START add_lead_form_asset]
def create_lead_form_asset(client: GoogleAdsClient, customer_id: str) -> str:
    """Creates a lead form asset using the given customer ID.

    Args:
        client: An initialized GoogleAdsClient instance.
        customer_id: The Google Ads customer ID.

    Returns:
        A str of the resource name for the newly created lead form asset.
    """
    asset_service = client.get_service("AssetService")
    asset_operation: AssetOperation = client.get_type("AssetOperation")
    asset: Asset = asset_operation.create
    asset.name = f"Interplanetary Cruise #{uuid4()} Lead Form"
    asset.final_urls.append("http://example.com/jupiter")

    # Creates a new LeadFormAsset instance.
    lead_form_asset: LeadFormAsset = asset.lead_form_asset

    # Specify the details of the extension that the users will see.
    lead_form_asset.call_to_action_type = (
        client.enums.LeadFormCallToActionTypeEnum.BOOK_NOW
    )
    lead_form_asset.call_to_action_description = "Latest trip to Jupiter!"

    # Define the form details.
    lead_form_asset.business_name = "Interplanetary Cruise"
    lead_form_asset.headline = "Trip to Jupiter"
    lead_form_asset.description = (
        "Our latest trip to Jupiter is now open for booking."
    )
    lead_form_asset.privacy_policy_url = "http://example.com/privacy"

    # Define the fields to be displayed to the user.
    input_type_enum = client.enums.LeadFormFieldUserInputTypeEnum
    lead_form_field_1: LeadFormField = client.get_type("LeadFormField")
    lead_form_field_1.input_type = input_type_enum.FULL_NAME
    lead_form_asset.fields.append(lead_form_field_1)

    lead_form_field_2: LeadFormField = client.get_type("LeadFormField")
    lead_form_field_2.input_type = input_type_enum.EMAIL
    lead_form_asset.fields.append(lead_form_field_2)

    lead_form_field_3: LeadFormField = client.get_type("LeadFormField")
    lead_form_field_3.input_type = input_type_enum.PHONE_NUMBER
    lead_form_asset.fields.append(lead_form_field_3)

    lead_form_field_4: LeadFormField = client.get_type("LeadFormField")
    lead_form_field_4.input_type = input_type_enum.PREFERRED_CONTACT_TIME
    lead_form_field_4.single_choice_answers.answers.extend(
        ["Before 9 AM", "Anytime", "After 5 PM"]
    )
    lead_form_asset.fields.append(lead_form_field_4)

    # Optional: You can also specify a background image asset.
    # To upload an asset, see misc/upload_image.py.
    # lead_form_asset.background_image_asset = "INSERT_IMAGE_ASSET_HERE"

    # Optional: Define the response page after the user signs up on the form.
    lead_form_asset.post_submit_headline = "Thanks for signing up!"
    lead_form_asset.post_submit_description = (
        "We will reach out to you shortly. Visit our website to see past trip "
        "details."
    )
    lead_form_asset.post_submit_call_to_action_type = (
        client.enums.LeadFormPostSubmitCallToActionTypeEnum.VISIT_SITE
    )

    # Optional: Display a custom disclosure that displays along with the Google
    # disclaimer on the form.
    lead_form_asset.custom_disclosure = (
        "Trip may get cancelled due to meteor shower"
    )

    # Optional: Define a delivery method for the form response. See
    # https://developers.google.com/google-ads/webhook/docs/overview for more
    # details on how to define a webhook.
    delivery_method: LeadFormDeliveryMethod = client.get_type(
        "LeadFormDeliveryMethod"
    )
    delivery_method.webhook.advertiser_webhook_url = (
        "http://example.com/webhook"
    )
    delivery_method.webhook.google_secret = "interplanetary google secret"
    delivery_method.webhook.payload_schema_version = 3
    lead_form_asset.delivery_methods.append(delivery_method)

    asset_service = client.get_service("AssetService")
    response = asset_service.mutate_assets(
        customer_id=customer_id, operations=[asset_operation]
    )
    resource_name: str = response.results[0].resource_name

    print(f"Asset with resource name {resource_name} was created.")

    return resource_name
    # [END add_lead_form_asset]


# [START add_lead_form_asset_1]
def create_lead_form_campaign_asset(
    client: GoogleAdsClient,
    customer_id: str,
    campaign_id: str,
    lead_form_asset_resource_name: str,
) -> None:
    """Creates the lead form campaign asset.

    Args:
        client: An initialized GoogleAdsClient instance.
        customer_id: The Google Ads customer ID.
        campaign_id: The ID for a Campaign belonging to the given customer.
        lead_form_asset_resource_name: The resource name of the lead form asset.
    """
    campaign_service = client.get_service("CampaignService")
    campaign_asset_service = client.get_service("CampaignAssetService")
    campaign_asset_operation: CampaignAssetOperation = client.get_type(
        "CampaignAssetOperation"
    )
    campaign_asset: CampaignAsset = campaign_asset_operation.create
    campaign_asset.asset = lead_form_asset_resource_name
    campaign_asset.field_type = client.enums.AssetFieldTypeEnum.LEAD_FORM
    campaign_asset.campaign = campaign_service.campaign_path(
        customer_id, campaign_id
    )

    response = campaign_asset_service.mutate_campaign_assets(
        customer_id=customer_id, operations=[campaign_asset_operation]
    )
    for result in response.results:
        print(
            "Created campaign asset with resource name "
            f'"{result.resource_name}" for campaign with ID {campaign_id}'
        )
        # [END add_lead_form_asset_1]


if __name__ == "__main__":
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description="This code example creates a lead form and a lead form "
        "asset for a campaign. Run add_campaigns.py to create a "
        "campaign."
    )
    # The following argument(s) should be provided to run the example.
    parser.add_argument(
        "-c",
        "--customer_id",
        type=str,
        required=True,
        help="The Google Ads customer ID.",
    )
    parser.add_argument(
        "-i",
        "--campaign_id",
        type=str,
        required=True,
        help="The ID of a Campaign belonging to the given customer.",
    )
    args: argparse.Namespace = parser.parse_args()

    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    googleads_client: GoogleAdsClient = GoogleAdsClient.load_from_storage(
        version="v22"
    )

    try:
        main(googleads_client, args.customer_id, args.campaign_id)
    except GoogleAdsException as ex:
        print(
            f'Request with ID "{ex.request_id}" failed with status '
            f'"{ex.error.code().name}" and includes the following errors:'
        )
        for error in ex.failure.errors:
            print(f'\tError with message "{error.message}".')
            if error.location:
                for field_path_element in error.location.field_path_elements:
                    print(f"\t\tOn field: {field_path_element.field_name}")
        sys.exit(1)
