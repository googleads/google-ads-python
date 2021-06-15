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
"""This example adds a campaign draft for a campaign.

Make sure you specify a campaign that has a non-shared budget.
"""


import argparse
import sys
from uuid import uuid4

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException


def main(client, customer_id, base_campaign_id):
    campaign_service = client.get_service("CampaignService")
    campaign_draft_service = client.get_service("CampaignDraftService")

    # Creates a campaign draft operation.
    campaign_draft_operation = client.get_type("CampaignDraftOperation")
    campaign_draft = campaign_draft_operation.create

    # Creates a campaign draft.
    campaign_draft.base_campaign = campaign_service.campaign_path(
        customer_id, base_campaign_id
    )
    campaign_draft.name = f"Campaign Draft #{uuid4()}"

    # Issues a mutate request to add the campaign draft.
    campaign_draft_response = campaign_draft_service.mutate_campaign_drafts(
        customer_id=customer_id, operations=[campaign_draft_operation]
    )
    print(
        "Created campaign draft: "
        f'"{campaign_draft_response.results[0].resource_name}".'
    )


if __name__ == "__main__":
    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    googleads_client = GoogleAdsClient.load_from_storage(version="v8")

    parser = argparse.ArgumentParser(
        description="Adds a campaign draft for the specified base campaign "
        "ID for the given customer ID."
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
        "--base_campaign_id",
        type=str,
        required=True,
        help="The base campaign ID.",
    )
    args = parser.parse_args()

    try:
        main(googleads_client, args.customer_id, args.base_campaign_id)
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
