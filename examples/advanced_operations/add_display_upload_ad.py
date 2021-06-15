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
"""Adds a display upload ad to a given ad group.

To get ad groups, run get_ad_groups.py.
"""


import argparse
import sys

import requests

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException


BUNDLE_URL = "https://goo.gl/9Y7qI2"


def main(client, customer_id, ad_group_id):
    """Adds a display upload ad to a given ad group.

    Args:
        client: An initialized Google Ads client.
        customer_id: The Google Ads customer ID.
        ad_group_id: The ID of the ad group to which the new ad will be added.
    """
    # There are several types of display upload ads. For this example, we will
    # create an HTML5 upload ad, which requires a media bundle.
    # This feature is only available to allowlisted accounts.
    # See https://support.google.com/google-ads/answer/1722096 for more details.
    # The DisplayUploadProductType field lists the available display upload types:
    # https://developers.google.com/google-ads/api/reference/rpc/latest/DisplayUploadAdInfo

    # Creates a new media bundle asset and returns the resource name.
    ad_asset_resource_name = _create_media_bundle_asset(client, customer_id)

    # Creates a new display upload ad and associates it with the specified
    # ad group.
    _create_display_upload_ad_group_ad(
        client, customer_id, ad_group_id, ad_asset_resource_name
    )


def _create_media_bundle_asset(client, customer_id):
    """Creates a media bundle from the assets in a zip file.

    The zip file contains the HTML5 components.

    Args:
        client: An initialized Google Ads client.
        customer_id: The Google Ads customer ID for which the call is made.
    Returns:
        The string resource name of the newly uploaded media bundle.
    """
    # Get the AssetService client.
    asset_service = client.get_service("AssetService")

    # Construct an asset operation and populate its fields.
    asset_operation = client.get_type("AssetOperation")
    media_bundle_asset = asset_operation.create
    media_bundle_asset.type_ = client.get_type(
        "AssetTypeEnum"
    ).AssetType.MEDIA_BUNDLE
    # The HTML5 zip file contains all the HTML, CSS, and images needed for the
    # HTML5 ad. For help on creating an HTML5 zip file, check out Google Web
    # Designer (https://www.google.com/webdesigner/).
    # Download the ZIP as bytes from the URL
    media_bundle_asset.media_bundle_asset.data = requests.get(
        BUNDLE_URL
    ).content

    # Adds the asset to the client account.
    mutate_asset_response = asset_service.mutate_assets(
        customer_id=customer_id, operations=[asset_operation]
    )

    # Display and return the resulting resource name.
    uploaded_asset_resource_name = mutate_asset_response.results[
        0
    ].resource_name
    print(f"Uploaded file with resource name '{uploaded_asset_resource_name}'.")

    return uploaded_asset_resource_name


def _create_display_upload_ad_group_ad(
    client, customer_id, ad_group_id, ad_asset_resource_name
):
    """Creates a new HTML5 display upload ad and adds it to the given ad group.

    Args:
        client: An initialized Google Ads client.
        customer_id: The Google Ads customer ID.
        ad_group_id: The ID of the ad group to which the new ad will be added.
        ad_asset_resource_name: The resource name of the media bundle containing
            the HTML5 components.
    """
    # Get the AdGroupAdService client.
    ad_group_ad_service = client.get_service("AdGroupAdService")

    # Create an AdGroupAdOperation.
    ad_group_ad_operation = client.get_type("AdGroupAdOperation")

    # Configure the ad group ad fields.
    ad_group_ad = ad_group_ad_operation.create
    ad_group_ad.status = client.get_type(
        "AdGroupAdStatusEnum"
    ).AdGroupAdStatus.PAUSED
    ad_group_ad.ad_group = client.get_service("AdGroupService").ad_group_path(
        customer_id, ad_group_id
    )

    # Configured the ad as a display upload ad.
    display_upload_ad = ad_group_ad.ad
    display_upload_ad.name = "Ad for HTML5"
    display_upload_ad.final_urls.append("http://example.com/html5")
    # Exactly one of the ad_data "oneof" fields must be included to specify the
    # ad type. See: https://developers.google.com/google-ads/api/reference/rpc/latest/Ad for
    # the full list of available types. By setting a "display_upload_ad"
    # subfield it sets that as the "oneof" field for the Ad.
    display_upload_ad.display_upload_ad.media_bundle.asset = (
        ad_asset_resource_name
    )
    display_upload_ad.display_upload_ad.display_upload_product_type = client.get_type(
        "DisplayUploadProductTypeEnum"
    ).DisplayUploadProductType.HTML5_UPLOAD_AD

    # Add the ad group ad to the client account and display the resulting
    # ad's resource name.
    mutate_ad_group_ads_response = ad_group_ad_service.mutate_ad_group_ads(
        customer_id=customer_id, operations=[ad_group_ad_operation]
    )
    print(
        "Created new ad group ad with resource name "
        f"'{mutate_ad_group_ads_response.results[0].resource_name}'."
    )


if __name__ == "__main__":
    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    googleads_client = GoogleAdsClient.load_from_storage(version="v8")

    parser = argparse.ArgumentParser(
        description="Adds a display upload ad to a given ad group."
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
        "-a",
        "--ad_group_id",
        type=int,
        required=True,
        help="The ID of the ad group to which the new ad will be added.",
    )
    args = parser.parse_args()

    try:
        main(googleads_client, args.customer_id, args.ad_group_id)
    except GoogleAdsException as ex:
        print(
            f'Request with ID "{ex.request_id}" failed with status '
            f'"{ex.error.code().name}" and includes the following errors:'
        )
        for error in ex.failure.errors:
            print(f'	Error with message "{error.message}".')
            if error.location:
                for field_path_element in error.location.field_path_elements:
                    print(f"\t\tOn field: {field_path_element.field_name}")
        sys.exit(1)
