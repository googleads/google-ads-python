#!/usr/bin/env python
# Copyright 2019 Google LLC
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
"""This example adds a gmail ad to a given ad group.

The ad group's campaign needs to have an AdvertisingChannelSubtype of
DISPLAY_GMAIL_AD. To get ad groups, run basic_operations/get_ad_groups.py
"""


import argparse
import sys
from uuid import uuid4
import requests

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException

LOGO_URL = "https://goo.gl/mtt54n"
MARKETING_IMG_URL = "http://goo.gl/3b9Wfh"


def main(client, customer_id, ad_group_id):
    logo_img_bytes, logo_img_content_type = _get_image(LOGO_URL)
    marketing_img_bytes, marketing_img_content_type = _get_image(
        MARKETING_IMG_URL
    )

    if logo_img_content_type != "image/png":
        raise ValueError("Logo image has invalid content-type.")

    if marketing_img_content_type != "image/jpeg":
        raise ValueError("Marketing image has invalid content-type.")

    media_file_service = client.get_service("MediaFileService")
    media_file_logo_op = client.get_type("MediaFileOperation")
    media_file_logo = media_file_logo_op.create
    media_file_logo.type_ = client.get_type("MediaTypeEnum").MediaType.IMAGE
    media_file_logo.image.data = logo_img_bytes
    media_file_logo.mime_type = client.get_type(
        "MimeTypeEnum"
    ).MimeType.IMAGE_PNG

    media_file_marketing_op = client.get_type("MediaFileOperation")
    media_file_marketing = media_file_marketing_op.create
    media_file_marketing.type_ = client.get_type(
        "MediaTypeEnum"
    ).MediaType.IMAGE
    media_file_marketing.image.data = marketing_img_bytes
    media_file_marketing.mime_type = client.get_type(
        "MimeTypeEnum"
    ).MimeType.IMAGE_JPEG

    image_response = media_file_service.mutate_media_files(
        customer_id=customer_id,
        operations=[media_file_logo_op, media_file_marketing_op],
    )

    image_resource_names = list(
        map(lambda response: response.resource_name, image_response.results)
    )

    ad_group_ad_service = client.get_service("AdGroupAdService")
    ad_group_service = client.get_service("AdGroupService")
    ad_group_ad_op = client.get_type("AdGroupAdOperation")
    ad_group_ad = ad_group_ad_op.create
    gmail_ad = ad_group_ad.ad.gmail_ad
    gmail_ad.teaser.headline = "Dream"
    gmail_ad.teaser.description = "Create your own adventure."
    gmail_ad.teaser.business_name = "Interplanetary Ships"
    gmail_ad.teaser.logo_image = image_resource_names[0]
    gmail_ad.marketing_image = image_resource_names[1]
    gmail_ad.marketing_image_headline = "Travel"
    gmail_ad.marketing_image_description = "Take to the skies!"

    ad_group_ad.ad.final_urls.append("http://www.example.com")
    ad_group_ad.ad.name = f"Gmail Ad #{uuid4()}"

    ad_group_ad.status = client.get_type(
        "AdGroupAdStatusEnum"
    ).AdGroupAdStatus.PAUSED
    ad_group_ad.ad_group = ad_group_service.ad_group_path(
        customer_id, ad_group_id
    )

    add_gmail_ad_response = ad_group_ad_service.mutate_ad_group_ads(
        customer_id=customer_id, operations=[ad_group_ad_op]
    )

    print(f"Created gmail ad {add_gmail_ad_response.results[0].resource_name}.")


def _get_image(url):
    """Loads image data from a URL.

    Args:
        url: a URL str.

    Returns:
        Images bytes loaded from the given URL and content-type as a str.
    """
    response = requests.get(url)
    headers = response.headers
    return response.content, headers["content-type"]


if __name__ == "__main__":
    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    googleads_client = GoogleAdsClient.load_from_storage(version="v8")

    parser = argparse.ArgumentParser(
        description=(
            "Adds a gmail ad to the specified ad group ID, "
            "for the given customer ID."
        )
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
        "-a", "--ad_group_id", type=str, required=True, help="The ad group ID."
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
