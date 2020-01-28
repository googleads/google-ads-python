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
import uuid

import google.ads.google_ads.client


def main(client, customer_id, page_size):
    remarketing_action_resource_name = _add_remarketing_action(
        client, customer_id)

    print(f'Created remarketing action "{remarketing_action_resource_name}".')

    queried_remarketing_action = _query_remarketing_action(
        client, customer_id, remarketing_action_resource_name, page_size)

    _print_remarketing_action_attributes(queried_remarketing_action)


def _add_remarketing_action(client, customer_id):
    remarketing_action_service = client.get_service(
        'RemarketingActionService', version='v2')

    # Create the operation.
    remarketing_action_operation = client.get_type(
        'RemarketingActionOperation', version='v2')

    # Create remarketing action.
    remarketing_action = remarketing_action_operation.create
    remarketing_action.name.value = 'Remarketing action #%s' % uuid.uuid4()

    # Add the remarketing action.
    try:
        remarketing_action_response = (
            remarketing_action_service.mutate_remarketing_actions(
                customer_id, [remarketing_action_operation]))
    except google.ads.google_ads.errors.GoogleAdsException as ex:
        print(f'Request with ID "{ex.request_id}" failed with status '
              f'"{ex.error.code().name}" and includes the following errors:')
        for error in ex.failure.errors:
            print(f'\tError with message "{error.message}".')
            if error.location:
                for field_path_element in error.location.field_path_elements:
                    print(f'\t\tOn field: {field_path_element.field_name}')
        sys.exit(1)

    return remarketing_action_response.results[0].resource_name


def _query_remarketing_action(client, customer_id, resource_name, page_size):
    google_ads_service_client = client.get_service(
        'GoogleAdsService', version='v2')

    # Creates a query that retrieves the previously created remarketing action
    # with its generated tag snippets.
    query = ('SELECT remarketing_action.id, '
             'remarketing_action.name, '
             'remarketing_action.tag_snippets '
             'FROM remarketing_action '
             'WHERE remarketing_action.resource_name = %s' % resource_name)

    # Issues a search request by specifying page size.
    response = google_ads_service_client.search(customer_id, query,
                                                page_size=page_size)

    # There is only one row because we limited the search using the resource
    # name, which is unique.
    return response.results[0]


def _print_remarketing_action_attributes(remarketing_action):
    print(f'Remarketing action has ID {remarketing_action.id.value} and name '
          f'"{remarketing_action.name.value}".')

    print('It has the following generated tag snippets:')

    for tag_snippet in remarketing_action.tag_snippets:
      print(f'Tag snippet with code type "{tag_snippet.type}", and code page '
            f'format "{tag_snippet.page_format}" has the following global site '
            f'tag: {tag_snippet.global_site_tag}')

      print(f'and the following event snippet: {tag_snippet.event_snippet}')


if __name__ == '__main__':
    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    google_ads_client = (google.ads.google_ads.client.GoogleAdsClient
                         .load_from_storage())

    parser = argparse.ArgumentParser(
        description='Adds a remarketing action for specified customer.')
    # The following argument(s) should be provided to run the example.
    parser.add_argument('-c', '--customer_id', type=str,
                        required=True, help='The Google Ads customer ID.')
    # The following argument(s) are optional.
    parser.add_argument('-p', '--page_size', type=int, default=1000,
                        help='Number of pages to be returned in the response.')
    args = parser.parse_args()

    main(google_ads_client, args.customer_id, args.page_size)
