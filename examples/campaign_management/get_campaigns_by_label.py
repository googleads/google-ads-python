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
"""This example illustrates how to get all campaigns with a specific label ID.

To add campaigns, run add_campaigns.py.
"""


import argparse
import sys

from google.ads.google_ads.client import GoogleAdsClient
from google.ads.google_ads.errors import GoogleAdsException


_DEFAULT_PAGE_SIZE = 1000


def main(client, customer_id, label_id, page_size):
    """Demonstrates how to retrieve all campaigns by a given label ID.

    Args:
        client: An initialized GoogleAdsClient instance.
        customer_id: A client customer ID str.
        label_id: A label ID to use when searching for campaigns.
        page_size: An int of the number of results to include in each page of
            results.
    """
    ga_service = client.get_service('GoogleAdsService', version='v4')

    # Creates a query that will retrieve all campaign labels with the
    # specified label ID.
    query = '''
            SELECT
                campaign.id,
                campaign.name,
                label.id,
                label.name
             FROM campaign_label
             WHERE label.id = "{}"
             ORDER BY campaign.id
             '''.format(label_id)

    # Retrieves a google.api_core.page_iterator.GRPCIterator instance
    # initialized with the specified request parameters.
    iterator = ga_service.search(customer_id, query=query, page_size=page_size)

    try:
        # Iterates over all rows in all pages and prints the requested field
        # values for the campaigns and labels in each row. The results include
        # the campaign and label objects because these were included in the
        # search criteria.
        for row in iterator:
            print('Campaign found with name "{}", ID "{}", and '
                  'label "{}".'.format(row.campaign.id.value,
                                       row.campaign.name.value,
                                       row.label.name.value))
    except GoogleAdsException as ex:
        print_error_and_exit_process(ex)


def print_error_and_exit_process(error):
    """Prints the details of a GoogleAdsException and exits the current process.

    Args:
        error: An instance of a GoogleAdsException.
    """
    print('Request with ID "{}" failed with status "{}" and includes the '
          'following errors:'.format(error.request_id, error.error.code().name))
    for error in error.failure.errors:
        print('\tError with message "{}".'.format(error.message))
        if error.location:
            for field_path_element in error.location.field_path_elements:
                print('\t\tOn field: {}'.format(
                    field_path_element.field_name))
    sys.exit(1)


if __name__ == '__main__':
    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    google_ads_client = GoogleAdsClient.load_from_storage()

    parser = argparse.ArgumentParser(
        description='Lists all campaigns for specified customer.')
    # The following argument(s) should be provided to run the example.
    parser.add_argument('-c', '--customer_id', type=str,
                        required=True, help='The Google Ads customer ID.')
    parser.add_argument('-l', '--label_id', type=str, required=True,
                        help='A label ID associated with a campaign.')
    args = parser.parse_args()

    main(google_ads_client, args.customer_id, args.label_id, _DEFAULT_PAGE_SIZE)
