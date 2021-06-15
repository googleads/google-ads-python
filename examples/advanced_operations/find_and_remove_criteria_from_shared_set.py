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

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException


_DEFAULT_PAGE_SIZE = 10000


def main(client, customer_id, page_size, campaign_id):
    ga_service = client.get_service("GoogleAdsService")
    shared_criterion_service = client.get_service("SharedCriterionService")

    # First, retrieve all shared sets associated with the campaign.
    shared_sets_query = f"""
        SELECT
          shared_set.id,
          shared_set.name
        FROM campaign_shared_set
        WHERE campaign.id = {campaign_id}"""

    try:
        shared_set_search_request = client.get_type("SearchGoogleAdsRequest")
        shared_set_search_request.customer_id = customer_id
        shared_set_search_request.query = shared_sets_query
        shared_set_search_request.page_size = _DEFAULT_PAGE_SIZE

        shared_set_response = ga_service.search(
            request=shared_set_search_request
        )

        shared_set_ids = []
        for row in shared_set_response:
            shared_set = row.shared_set
            shared_set_ids.append(str(shared_set.id))
            print(
                f'Campaign shared set ID "{shared_set.id}" and name '
                f'"{shared_set.name}" was found.'
            )
    except GoogleAdsException as ex:
        _handle_googleads_exception(ex)

    # Next, retrieve shared criteria for all found shared sets.
    ids = ", ".join(shared_set_ids)
    shared_criteria_query = f"""
        SELECT
          shared_criterion.type,
          shared_criterion.keyword.text,
          shared_criterion.keyword.match_type,
          shared_set.id
        FROM shared_criterion
        WHERE shared_set.id IN ({ids})"""

    try:
        shared_criteria_search_request = client.get_type(
            "SearchGoogleAdsRequest"
        )
        shared_criteria_search_request.customer_id = customer_id
        shared_criteria_search_request.query = shared_criteria_query
        shared_criteria_search_request.page_size = _DEFAULT_PAGE_SIZE

        shared_criteria_response = ga_service.search(
            request=shared_criteria_search_request
        )
    except GoogleAdsException as ex:
        _handle_googleads_exception(ex)

    criterion_type_enum = client.get_type("CriterionTypeEnum").CriterionType
    criterion_ids = []
    for row in shared_criteria_response:
        shared_criterion = row.shared_criterion
        shared_criterion_resource_name = shared_criterion.resource_name

        if shared_criterion.type_ == criterion_type_enum.KEYWORD:
            keyword = shared_criterion.keyword
            print(
                "Shared criterion with resource name "
                f'"{shared_criterion_resource_name}" for negative keyword '
                f'with text "{keyword.text}" and match type '
                f'"{keyword.match_type.name}" was found.'
            )

        criterion_ids.append(shared_criterion_resource_name)

    operations = []

    # Finally, remove the criteria.
    for criteria_id in criterion_ids:
        shared_criterion_operation = client.get_type("SharedCriterionOperation")
        shared_criterion_operation.remove = criteria_id
        operations.append(shared_criterion_operation)

    try:
        response = shared_criterion_service.mutate_shared_criteria(
            customer_id=customer_id, operations=operations
        )

        for result in response.results:
            print(f'Removed shared criterion "{result.resource_name}".')
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
        googleads_client, args.customer_id, _DEFAULT_PAGE_SIZE, args.campaign_id
    )
