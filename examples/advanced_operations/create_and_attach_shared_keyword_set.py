#!/usr/bin/env python
# Copyright 2018 Google LLC
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
"""Demonstrates how to create a shared list of negative broad match keywords.

Note that the keywords will be attached to the specified campaign.
"""


import argparse
import sys
import uuid

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException


def main(client, customer_id, campaign_id):
    campaign_service = client.get_service("CampaignService")
    shared_set_service = client.get_service("SharedSetService")
    shared_criterion_service = client.get_service("SharedCriterionService")
    campaign_shared_set_service = client.get_service("CampaignSharedSetService")

    # Create shared negative keyword set.
    shared_set_operation = client.get_type("SharedSetOperation")
    shared_set = shared_set_operation.create
    shared_set.name = f"API Negative keyword list - {uuid.uuid4()}"
    shared_set.type_ = client.get_type(
        "SharedSetTypeEnum"
    ).SharedSetType.NEGATIVE_KEYWORDS

    try:
        shared_set_response = shared_set_service.mutate_shared_sets(
            customer_id=customer_id, operations=[shared_set_operation]
        )
        shared_set_resource_name = shared_set_response.results[0].resource_name

        print(f'Created shared set "{shared_set_resource_name}".')
    except GoogleAdsException as ex:
        _handle_googleads_exception(ex)

    # Keywords to create a shared set of.
    keywords = ["mars cruise", "mars hotels"]
    shared_criteria_operations = []
    for keyword in keywords:
        shared_criterion_operation = client.get_type("SharedCriterionOperation")
        shared_criterion = shared_criterion_operation.create
        shared_criterion.keyword.text = keyword
        shared_criterion.keyword.match_type = client.get_type(
            "KeywordMatchTypeEnum"
        ).KeywordMatchType.BROAD
        shared_criterion.shared_set = shared_set_resource_name
        shared_criteria_operations.append(shared_criterion_operation)
    try:
        response = shared_criterion_service.mutate_shared_criteria(
            customer_id=customer_id, operations=shared_criteria_operations
        )

        for shared_criterion in response.results:
            print(
                "Created shared criterion "
                f'"{shared_criterion.resource_name}".'
            )
    except GoogleAdsException as ex:
        _handle_googleads_exception(ex)

    campaign_set_operation = client.get_type("CampaignSharedSetOperation")
    campaign_set = campaign_set_operation.create
    campaign_set.campaign = campaign_service.campaign_path(
        customer_id, campaign_id
    )
    campaign_set.shared_set = shared_set_resource_name

    try:
        campaign_shared_set_resource_name = campaign_shared_set_service.mutate_campaign_shared_sets(
            customer_id=customer_id, operations=[campaign_set_operation]
        )

        print(
            "Created campaign shared set "
            '"{campaign_shared_set_resource_name.results[0].resource_name}".'
        )
    except GoogleAdsException as ex:
        _handle_googleads_exception(ex)


def _handle_googleads_exception(exception):
    print(
        f'Request with ID "{exception.request_id}" failed with status '
        f'"{exception.error.code().name}" and includes the following errors:'
    )
    for error in exception.failure.errors:
        print(f'\tError with message "{error.message}".')
        if error.location:
            for field_path_element in error.location.field_path_elements:
                print(f"\t\tOn field: {field_path_element.field_name}")
    sys.exit(1)


if __name__ == "__main__":
    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    googleads_client = GoogleAdsClient.load_from_storage(version="v8")

    parser = argparse.ArgumentParser(
        description=(
            "Adds a list of negative broad match keywords to the "
            "provided campaign, for the specified customer."
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
        "-i", "--campaign_id", type=str, required=True, help="The campaign ID."
    )
    args = parser.parse_args()

    main(googleads_client, args.customer_id, args.campaign_id)
