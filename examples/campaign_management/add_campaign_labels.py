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

from google.ads.google_ads.client import GoogleAdsClient
from google.ads.google_ads.errors import GoogleAdsException


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
    campaign_label_service = client.get_service(
        "CampaignLabelService", version="v6"
    )
    campaign_service = client.get_service("CampaignService", version="v6")
    label_service = client.get_service("LabelService", version="v6")

    # Build the resource name of the label to be added across the campaigns.
    label_resource_name = label_service.label_path(customer_id, label_id)

    operations = []

    for campaign_id in campaign_ids:
        campaign_resource_name = campaign_service.campaign_path(
            customer_id, campaign_id
        )
        campaign_label_operation = client.get_type(
            "CampaignLabelOperation", version="v6"
        )

        campaign_label = campaign_label_operation.create
        campaign_label.campaign = campaign_resource_name
        campaign_label.label = label_resource_name
        operations.append(campaign_label_operation)

    try:
        response = campaign_label_service.mutate_campaign_labels(
            customer_id, operations
        )
        print(f"Added {len(response.results)} campaign labels:")
        for result in response.results:
            print(result.resource_name)
    except GoogleAdsException as error:
        print(
            'Request with ID "{}" failed with status "{}" and includes the '
            "following errors:".format(
                error.request_id, error.error.code().name
            )
        )
        for error in error.failure.errors:
            print('\tError with message "{}".'.format(error.message))
            if error.location:
                for field_path_element in error.location.field_path_elements:
                    print(
                        "\t\tOn field: {}".format(field_path_element.field_name)
                    )
        sys.exit(1)
        # [END add_campaign_labels]


if __name__ == "__main__":
    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    google_ads_client = GoogleAdsClient.load_from_storage()

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
    main(google_ads_client, args.customer_id, args.label_id, args.campaign_ids)
