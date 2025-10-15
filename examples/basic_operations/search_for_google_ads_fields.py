#!/usr/bin/env python
# Copyright 2022 Google LLC
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
"""Searches for GoogleAdsFields that match a given prefix.

Retrieves metadata such as whether the field is selectable, filterable, or
sortable, along with the data type and the fields that are selectable with the
field. Each GoogleAdsField represents either a resource (such as customer,
campaign) or a field (such as metrics.impressions, campaign.id).
"""


import argparse
import sys

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
from google.ads.googleads.v22.resources.types.google_ads_field import (
    GoogleAdsField,
)
from google.ads.googleads.v22.services.services.google_ads_field_service import (
    GoogleAdsFieldServiceClient,
)
from google.ads.googleads.v22.services.types.google_ads_field_service import (
    SearchGoogleAdsFieldsRequest,
    SearchGoogleAdsFieldsResponse,
)


def main(client: GoogleAdsClient, name_prefix: str) -> None:
    """The main method that creates all necessary entities for the example.

    Args:
        client: an initialized GoogleAdsClient instance.
        name_prefix: the name prefix to use when searching for Google Ads field
            names.
    """
    gaf_service: GoogleAdsFieldServiceClient = client.get_service(
        "GoogleAdsFieldService"
    )

    # Searches for all fields whose name begins with the specified name prefix.
    query: str = f"""
        SELECT
          name,
          category,
          selectable,
          filterable,
          sortable,
          selectable_with,
          data_type,
          is_repeated
        WHERE name LIKE '{name_prefix}%'"""

    request: SearchGoogleAdsFieldsRequest = client.get_type(
        "SearchGoogleAdsFieldsRequest"
    )
    request.query = query

    response: SearchGoogleAdsFieldsResponse = (
        gaf_service.search_google_ads_fields(request=request)
    )

    # Checks if any results were returned and exits if not.
    if response.total_results_count == 0:
        print(
            "No GoogleAdsFields found with a name that begins with "
            f"'{name_prefix}'."
        )
        sys.exit(0)

    # Retrieves each matching GoogleAdsField and prints its metadata.
    googleads_field: GoogleAdsField
    for googleads_field in response:
        print(f"{googleads_field.name}:")
        # These statements format the printed string so that the left side is
        # always a 16-character string so that the values on the right line up
        # vertically.
        print(f"{'  category:':<16}", googleads_field.category.name)
        print(f"{'  data type:':<16}", googleads_field.data_type.name)
        print(f"{'  selectable:':<16}", googleads_field.selectable)
        print(f"{'  filterable:':<16}", googleads_field.filterable)
        print(f"{'  sortable:':<16}", googleads_field.sortable)
        print(f"{'  repeated:':<16}", googleads_field.is_repeated)

        # Prints the list of fields that are selectable with the field.
        if googleads_field.selectable_with:
            # Sorts the selectable_with list then prints each field name.
            googleads_field.selectable_with.sort()
            print("  selectable with:")
            selectable_with_field: str
            for selectable_with_field in googleads_field.selectable_with:
                print(f"    {selectable_with_field}")

        # Print an extra line to visually separate each GoogleAdsField.
        print()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Lists metadata for the specified artifact."
    )
    # The following argument(s) should be provided to run the example.
    parser.add_argument(
        "-n",
        "--name_prefix",
        type=str,
        required=True,
        help="The name prefix to use when searching for Google Ads field names",
    )
    args: argparse.Namespace = parser.parse_args()

    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    googleads_client: GoogleAdsClient = GoogleAdsClient.load_from_storage(
        version="v22"
    )

    try:
        main(googleads_client, args.name_prefix)
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
