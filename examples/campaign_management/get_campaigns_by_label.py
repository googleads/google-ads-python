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

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException


_DEFAULT_PAGE_SIZE = 1000


# [START get_campaigns_by_label]
def main(client, customer_id, label_id, page_size):
    """Demonstrates how to retrieve all campaigns by a given label ID.

    Args:
        client: An initialized GoogleAdsClient instance.
        customer_id: A client customer ID str.
        label_id: A label ID to use when searching for campaigns.
        page_size: An int of the number of results to include in each page of
            results.
    """
    ga_service = client.get_service("GoogleAdsService")

    # Creates a query that will retrieve all campaign labels with the
    # specified label ID.
    query = f"""
        SELECT
            campaign.id,
            campaign.name,
            label.id,
            label.name
         FROM campaign_label
         WHERE label.id = "{label_id}"
         ORDER BY campaign.id"""

    # Retrieves a google.api_core.page_iterator.GRPCIterator instance
    # initialized with the specified request parameters.
    request = client.get_type("SearchGoogleAdsRequest")
    request.customer_id = customer_id
    request.query = query
    request.page_size = page_size

    iterator = ga_service.search(request=request)

    # Iterates over all rows in all pages and prints the requested field
    # values for the campaigns and labels in each row. The results include
    # the campaign and label objects because these were included in the
    # search criteria.
    for row in iterator:
        print(
            f'Campaign found with name "{row.campaign.id}", ID '
            f'"{row.campaign.name}", and label "{row.label.name}".'
        )


if __name__ == "__main__":
    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    googleads_client = GoogleAdsClient.load_from_storage(version="v8")

    parser = argparse.ArgumentParser(
        description="Lists all campaigns for specified customer."
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
        help="A label ID associated with a campaign.",
    )
    args = parser.parse_args()

    try:
        main(
            googleads_client,
            args.customer_id,
            args.label_id,
            _DEFAULT_PAGE_SIZE,
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
