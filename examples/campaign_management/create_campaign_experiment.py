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
"""This demonstrates how to create a campaign experiment.

It requests the creation based on a draft and waits for completion.
"""


import argparse
import sys
import uuid

from google.ads.google_ads.client import GoogleAdsClient
from google.ads.google_ads.errors import GoogleAdsException
from google.ads.google_ads.util import ResourceName


def main(client, customer_id, base_campaign_id, draft_id):
    # Create the campaign experiment.
    campaign_experiment = client.get_type("CampaignExperiment", version="v5")
    campaign_draft_service = client.get_service(
        "CampaignDraftService", version="v5"
    )
    campaign_draft_resource_name = campaign_draft_service.campaign_draft_path(
        customer_id, ResourceName.format_composite(base_campaign_id, draft_id)
    )

    campaign_experiment.campaign_draft.value = campaign_draft_resource_name
    campaign_experiment.name.value = f"Campaign Experiment #{uuid.uuid4()}"
    campaign_experiment.traffic_split_percent.value = 50
    campaign_experiment.traffic_split_type = client.get_type(
        "CampaignExperimentTrafficSplitTypeEnum", version="v5"
    ).RANDOM_QUERY

    try:
        campaign_experiment_service = client.get_service(
            "CampaignExperimentService", version="v5"
        )

        # A Long Running Operation (LRO) is returned from this
        # asynchronous request by the API.
        campaign_experiment_lro = campaign_experiment_service.create_campaign_experiment(
            customer_id, campaign_experiment
        )
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

    print(
        "Asynchronous request to create campaign experiment with "
        "resource name "
        f'"{campaign_experiment_lro.metadata.campaign_experiment}" started.'
    )
    print("Waiting until operation completes.")

    # Poll until the operation completes.
    campaign_experiment_lro.result()

    # Retrieve the campaign experiment that has been created.
    ga_service = client.get_service("GoogleAdsService", version="v5")
    query = f"""
        SELECT campaign_experiment.experiment_campaign
        FROM campaign_experiment
        WHERE
          campaign_experiment.resource_name =
          '{campaign_experiment_lro.metadata.campaign_experiment}'"""

    results = ga_service.search(customer_id, query=query, page_size=1)

    try:
        for row in results:
            print(
                "Experiment campaign "
                f'"{row.campaign_experiment.experiment_campaign.value}" '
                "creation completed."
            )
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


if __name__ == "__main__":
    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    google_ads_client = GoogleAdsClient.load_from_storage()

    parser = argparse.ArgumentParser(
        description=("Create a campaign experiment based on a campaign draft.")
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
        help="The base campaign id.",
    )
    parser.add_argument(
        "-d", "--draft_id", type=str, required=True, help="The id of the draft."
    )
    args = parser.parse_args()

    main(
        google_ads_client,
        args.customer_id,
        args.base_campaign_id,
        args.draft_id,
    )
