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
"""This example demonstrates usage of remarketing actions.

A new remarketing action will be created for the specified customer, and its
associated tag snippets will be retrieved.
"""


import argparse
import sys
from uuid import uuid4

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException


def main(client, customer_id, page_size):
    remarketing_action_resource_name = _add_remarketing_action(
        client, customer_id
    )

    print(f'Created remarketing action "{remarketing_action_resource_name}".')

    queried_remarketing_action = _query_remarketing_action(
        client, customer_id, remarketing_action_resource_name, page_size
    )

    _print_remarketing_action_attributes(queried_remarketing_action)


# [START add_remarketing_action]
def _add_remarketing_action(client, customer_id):
    remarketing_action_service = client.get_service("RemarketingActionService")
    remarketing_action_operation = client.get_type("RemarketingActionOperation")

    remarketing_action = remarketing_action_operation.create
    remarketing_action.name = f"Remarketing action #{uuid4()}"

    try:
        remarketing_action_response = remarketing_action_service.mutate_remarketing_actions(
            customer_id=customer_id, operations=[remarketing_action_operation],
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

    return remarketing_action_response.results[0].resource_name
    # [END add_remarketing_action]


def _query_remarketing_action(client, customer_id, resource_name, page_size):
    """Retrieves the previously created remarketing action with tag snippets.

    Args:
      client: the Google Ads client
      customer_id: the Google Ads customer ID
      resource_name: the resource name of the remarketing action to query
      page_size: the number of rows to return per page

    Returns:
      the found remarketing action
    """
    # [START add_remarketing_action_1]
    query = f"""
        SELECT
          remarketing_action.id,
          remarketing_action.name,
          remarketing_action.tag_snippets
        FROM remarketing_action
        WHERE remarketing_action.resource_name = '{resource_name}'"""
    # [END add_remarketing_action_1]

    googleads_service_client = client.get_service("GoogleAdsService")
    search_request = client.get_type("SearchGoogleAdsRequest")

    search_request.customer_id = customer_id
    search_request.query = query
    search_request.page_size = page_size

    results = googleads_service_client.search(search_request)

    try:
        return list(results)[0].remarketing_action
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


def _print_remarketing_action_attributes(remarketing_action):
    print(
        f"Remarketing action has ID {remarketing_action.id} and name "
        f'"{remarketing_action.name}". \nIt has the following '
        "generated tag snippets:\n"
    )

    for tag_snippet in remarketing_action.tag_snippets:
        tracking_code_type = tag_snippet.type_.name
        tracking_code_page_format = tag_snippet.page_format.name

        print("=" * 80)
        print(
            f'Tag snippet with code type "{tracking_code_type}", and code '
            f'page format "{tracking_code_page_format}" has the following:\n'
        )
        print("-" * 80)
        print(f"Global site tag: \n\n{tag_snippet.global_site_tag}")
        print("-" * 80)
        print(f"Event snippet: \n\n{tag_snippet.event_snippet}")


if __name__ == "__main__":
    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    googleads_client = GoogleAdsClient.load_from_storage(version="v8")

    parser = argparse.ArgumentParser(
        description="Adds a remarketing action for specified customer."
    )
    # The following argument(s) should be provided to run the example.
    parser.add_argument(
        "-c",
        "--customer_id",
        type=str,
        required=True,
        help="The Google Ads customer ID.",
    )
    # The following argument(s) are optional.
    parser.add_argument(
        "-p",
        "--page_size",
        type=int,
        default=1000,
        help="Number of pages to be returned in the response.",
    )
    args = parser.parse_args()

    main(googleads_client, args.customer_id, args.page_size)
