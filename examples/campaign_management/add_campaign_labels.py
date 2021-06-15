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
"""This code example adds a campaign label to a list of campaigns.

This example assumes that a label has already been prepared.
"""

import argparse
import sys

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException


# [START add_campaign_labels]
def main(client, customer_id, label_id, campaign_ids):
    """This code example adds a campaign label to a list of campaigns.

    Args:
        client: An initialized GoogleAdsClient instance.
        customer_id: A client customer ID str.
        label_id: The ID of the label to attach to campaigns.
        campaign_ids: A list of campaign IDs to which the label will be added.
    """

    # Get an instance of CampaignLabelService client.
    campaign_label_service = client.get_service("CampaignLabelService")
    campaign_service = client.get_service("CampaignService")
    label_service = client.get_service("LabelService")

    # Build the resource name of the label to be added across the campaigns.
    label_resource_name = label_service.label_path(customer_id, label_id)

    operations = []

    for campaign_id in campaign_ids:
        campaign_resource_name = campaign_service.campaign_path(
            customer_id, campaign_id
        )
        campaign_label_operation = client.get_type("CampaignLabelOperation")

        campaign_label = campaign_label_operation.create
        campaign_label.campaign = campaign_resource_name
        campaign_label.label = label_resource_name
        operations.append(campaign_label_operation)

    response = campaign_label_service.mutate_campaign_labels(
        customer_id=customer_id, operations=operations
    )
    print(f"Added {len(response.results)} campaign labels:")
    for result in response.results:
        print(result.resource_name)
    # [END add_campaign_labels]


if __name__ == "__main__":
    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    googleads_client = GoogleAdsClient.load_from_storage(version="v8")

    parser = argparse.ArgumentParser(
        description="This code example adds a campaign label to a list of "
        "campaigns."
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
        "-l",
        "--label_id",
        type=str,
        required=True,
        help="The ID of the label to attach to campaigns.",
    )
    parser.add_argument(
        "-i",
        "--campaign_ids",
        nargs="+",
        type=str,
        required=True,
        help="The campaign IDs to receive the label.",
    )
    args = parser.parse_args()
    try:
        main(
            googleads_client, args.customer_id, args.label_id, args.campaign_ids
        )
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
