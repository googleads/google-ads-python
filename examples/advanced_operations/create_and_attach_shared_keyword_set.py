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
from typing import List
import uuid

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
from google.ads.googleads.v22.errors.types.errors import GoogleAdsError
from google.ads.googleads.v22.resources.types.campaign_shared_set import (
    CampaignSharedSet,
)
from google.ads.googleads.v22.resources.types.shared_criterion import (
    SharedCriterion,
)
from google.ads.googleads.v22.resources.types.shared_set import SharedSet
from google.ads.googleads.v22.services.services.campaign_service import (
    CampaignServiceClient,
)
from google.ads.googleads.v22.services.services.campaign_shared_set_service import (
    CampaignSharedSetServiceClient,
)
from google.ads.googleads.v22.services.types.campaign_shared_set_service import (
    CampaignSharedSetOperation,
    MutateCampaignSharedSetsResponse,
)
from google.ads.googleads.v22.services.services.shared_criterion_service import (
    SharedCriterionServiceClient,
)
from google.ads.googleads.v22.services.services.shared_set_service import (
    SharedSetServiceClient,
)
from google.ads.googleads.v22.services.types.shared_criterion_service import (
    MutateSharedCriteriaResponse,
    MutateSharedCriterionResult,
    SharedCriterionOperation,
)
from google.ads.googleads.v22.services.types.shared_set_service import (
    MutateSharedSetsResponse,
    SharedSetOperation,
)


def main(client: GoogleAdsClient, customer_id: str, campaign_id: str) -> None:
    campaign_service: CampaignServiceClient = client.get_service(
        "CampaignService"
    )
    shared_set_service: SharedSetServiceClient = client.get_service(
        "SharedSetService"
    )
    shared_criterion_service: SharedCriterionServiceClient = client.get_service(
        "SharedCriterionService"
    )
    campaign_shared_set_service: CampaignSharedSetServiceClient = (
        client.get_service("CampaignSharedSetService")
    )

    # Create shared negative keyword set.
    shared_set_operation: SharedSetOperation = client.get_type(
        "SharedSetOperation"
    )
    shared_set: SharedSet = shared_set_operation.create
    shared_set.name = f"API Negative keyword list - {uuid.uuid4()}"
    shared_set.type_ = client.enums.SharedSetTypeEnum.NEGATIVE_KEYWORDS

    try:
        shared_set_response: MutateSharedSetsResponse = (
            shared_set_service.mutate_shared_sets(
                customer_id=customer_id, operations=[shared_set_operation]
            )
        )
        shared_set_resource_name: str = shared_set_response.results[
            0
        ].resource_name

        print(f'Created shared set "{shared_set_resource_name}".')
    except GoogleAdsException as ex:
        handle_googleads_exception(ex)

    # Keywords to create a shared set of.
    keywords: List[str] = ["mars cruise", "mars hotels"]
    shared_criteria_operations: List[SharedCriterionOperation] = []
    for keyword in keywords:
        shared_criterion_operation: SharedCriterionOperation = client.get_type(
            "SharedCriterionOperation"
        )
        shared_criterion: SharedCriterion = shared_criterion_operation.create
        shared_criterion.keyword.text = keyword
        shared_criterion.keyword.match_type = (
            client.enums.KeywordMatchTypeEnum.BROAD
        )
        shared_criterion.shared_set = shared_set_resource_name
        shared_criteria_operations.append(shared_criterion_operation)
    try:
        response: MutateSharedCriteriaResponse = (
            shared_criterion_service.mutate_shared_criteria(
                customer_id=customer_id, operations=shared_criteria_operations
            )
        )

        shared_criterion_result: MutateSharedCriterionResult
        for shared_criterion_result in response.results:
            print(
                "Created shared criterion "
                f'"{shared_criterion_result.resource_name}".'
            )
    except GoogleAdsException as ex:
        handle_googleads_exception(ex)

    campaign_set_operation: CampaignSharedSetOperation = client.get_type(
        "CampaignSharedSetOperation"
    )
    campaign_set: CampaignSharedSet = campaign_set_operation.create
    campaign_set.campaign = campaign_service.campaign_path(
        customer_id, campaign_id
    )
    campaign_set.shared_set = shared_set_resource_name

    try:
        campaign_shared_set_response: MutateCampaignSharedSetsResponse = (
            campaign_shared_set_service.mutate_campaign_shared_sets(
                customer_id=customer_id, operations=[campaign_set_operation]
            )
        )

        print(
            "Created campaign shared set "
            f'"{campaign_shared_set_response.results[0].resource_name}".'
        )
    except GoogleAdsException as ex:
        handle_googleads_exception(ex)


def handle_googleads_exception(exception: GoogleAdsException) -> None:
    print(
        f'Request with ID "{exception.request_id}" failed with status '
        f'"{exception.error.code().name}" and includes the following errors:'
    )
    error: GoogleAdsError
    for error in exception.failure.errors:
        print(f'\tError with message "{error.message}".')
        if error.location:
            for field_path_element in error.location.field_path_elements:
                print(f"\t\tOn field: {field_path_element.field_name}")
    sys.exit(1)


if __name__ == "__main__":
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

    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    googleads_client: GoogleAdsClient = GoogleAdsClient.load_from_storage(
        version="v22"
    )

    main(googleads_client, args.customer_id, args.campaign_id)
