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
"""Demonstrates how to find and remove shared sets, and shared set criteria."""


import argparse
import sys

from google.ads.google_ads.client import GoogleAdsClient
from google.ads.google_ads.errors import GoogleAdsException


_DEFAULT_PAGE_SIZE = 1000


def main(client, customer_id, page_size, campaign_id):
    ga_service = client.get_service("GoogleAdsService", version="v5")
    shared_criterion_service = client.get_service(
        "SharedCriterionService", version="v5"
    )

    # First, retrieve all shared sets associated with the campaign.
    shared_sets_query = (
        "SELECT shared_set.id, shared_set.name FROM campaign_shared_set "
        f"WHERE campaign.id = {campaign_id}"
    )

    try:
        shared_set_response = ga_service.search(
            customer_id, query=shared_sets_query, page_size=page_size
        )

        shared_set_ids = []
        for row in shared_set_response:
            shared_set = row.shared_set
            shared_set_id = str(shared_set.id)
            shared_set_ids.append(shared_set_id)
            print(
                f'Campaign shared set ID "{shared_set_id}" and name '
                f'"{shared_set.name}" was found.'
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

    # Next, retrieve shared criteria for all found shared sets.
    shared_criteria_query = (
        "SELECT shared_criterion.type, shared_criterion.keyword.text, "
        "shared_criterion.keyword.match_type, shared_set.id "
        "FROM shared_criterion WHERE shared_set.id IN "
        f'({", ".join(shared_set_ids)})'
    )

    try:
        shared_criteria_response = ga_service.search(
            customer_id, query=shared_criteria_query, page_size=page_size
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

    # Use the enum type to determine the enum name from the value.
    keyword_match_type_enum = client.get_type(
        "KeywordMatchTypeEnum", version="v5"
    ).KeywordMatchType

    criterion_ids = []
    for row in shared_criteria_response:
        shared_criterion = row.shared_criterion
        shared_criterion_resource_name = shared_criterion.resource_name
        if (
            shared_criterion.type
            == client.get_type("CriterionTypeEnum", version="v5").KEYWORD
        ):
            keyword = shared_criterion.keyword
            print(
                'Shared criterion with resource name "%s" for negative '
                'keyword with text "%s" and match type "%s" was found.'
                % (
                    shared_criterion_resource_name,
                    keyword.text,
                    keyword_match_type_enum.Name(keyword.match_type),
                )
            )
        criterion_ids.append(shared_criterion_resource_name)

    operations = []

    # Finally, remove the criteria.
    for criteria_id in criterion_ids:
        shared_criterion_operation = client.get_type(
            "SharedCriterionOperation", version="v5"
        )
        shared_criterion_operation.remove = criteria_id
        operations.append(shared_criterion_operation)

    try:
        response = shared_criterion_service.mutate_shared_criteria(
            customer_id, operations
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

    for result in response.results:
        print(f'Removed shared criterion "{result.resource_name}".')


if __name__ == "__main__":
    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    google_ads_client = GoogleAdsClient.load_from_storage()

    parser = argparse.ArgumentParser(
        description=(
            "Finds shared sets, then finds and removes shared set "
            "criteria under them."
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

    main(
        google_ads_client,
        args.customer_id,
        _DEFAULT_PAGE_SIZE,
        args.campaign_id,
    )
