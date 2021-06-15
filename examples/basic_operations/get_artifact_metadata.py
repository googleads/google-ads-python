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
"""This example illustrates how to retrieve artifact metadata.

The metadata retrieved can provide additional context about the artifact,
such as whether it is selectable, filterable, or sortable. The artifact can be
either a resource (such as customer, or campaign) or a field (such as
metrics.impressions, campaign.id). It also shows the data type and artifacts
that are selectable with the artifact.
"""


import argparse
import sys
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException


_DEFAULT_PAGE_SIZE = 1000


def _is_or_is_not(bool_value):
    """Produces display text for whether metadata is applicable to artifact.

    Args:
        bool_value: a BoolValue instance.

    Returns:
        A str with value "is" if bool_value is True, else "is not".
    """
    return "is" if bool_value else "isn't"


def main(client, artifact_name, page_size):
    gaf_service = client.get_service("GoogleAdsFieldService")

    # Searches for an artifact with the specified name.
    query = f"""
        SELECT
          name,
          category,
          selectable,
          filterable,
          sortable,
          selectable_with,
          data_type,
          is_repeated
        WHERE name = '{artifact_name}'"""

    request = client.get_type("SearchGoogleAdsFieldsRequest")
    request.query = query
    request.page_size = page_size

    response = gaf_service.search_google_ads_fields(request=request)

    # Iterates over all rows and prints out the metadata of the returned
    # artifacts.
    for googleads_field in response:
        # Note that the category and data type printed below are enum
        # values. For example, a value of 2 will be returned when the
        # category is "RESOURCE".
        #
        # A mapping of enum names to values can be found in
        # GoogleAdsFieldCategoryEnum for the category and
        # GoogleAdsFieldDataTypeEnum for the data type.
        selectable = _is_or_is_not(googleads_field.selectable)
        filterable = _is_or_is_not(googleads_field.filterable)
        sortable = _is_or_is_not(googleads_field.sortable)
        is_repeated = _is_or_is_not(googleads_field.is_repeated)

        print(
            f'An artifact named "{googleads_field.name}" with '
            f"category {googleads_field.category.name} and data type "
            f"{googleads_field.data_type.name} {selectable} "
            f"selectable, {filterable} filterable, {sortable} sortable, "
            f"and {is_repeated} repeated."
        )

        if len(googleads_field.selectable_with) > 0:
            selectable_artifacts = [
                wrapped_selectable_artifact
                for wrapped_selectable_artifact in googleads_field.selectable_with
            ]

            print("")
            print(
                "The artifact can be selected with the following " "artifacts:"
            )
            for artifact in selectable_artifacts:
                print(artifact)


if __name__ == "__main__":
    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    googleads_client = GoogleAdsClient.load_from_storage(version="v8")

    parser = argparse.ArgumentParser(
        description="Lists metadata for the specified artifact."
    )
    # The following argument(s) should be provided to run the example.
    parser.add_argument(
        "-a",
        "--artifact_name",
        type=str,
        required=True,
        help="The name of the artifact for which we are "
        "retrieving metadata.",
    )
    args = parser.parse_args()

    try:
        main(googleads_client, args.artifact_name, _DEFAULT_PAGE_SIZE)
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
