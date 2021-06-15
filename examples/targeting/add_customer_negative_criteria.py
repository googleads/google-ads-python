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
"""Adds various types of negative criteria as exclusions at the customer level.

These criteria will be applied to all campaigns for the given customer.
"""


import argparse
import sys

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException


def main(client, customer_id):
    """The main method that creates all necessary entities for the example.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.
    """
    tragedy_criterion_op = client.get_type("CustomerNegativeCriterionOperation")
    tragedy_criterion = tragedy_criterion_op.create
    # Creates a negative customer criterion excluding the content label type
    # of 'TRAGEDY'.
    tragedy_criterion.content_label.type_ = client.get_type(
        "ContentLabelTypeEnum"
    ).ContentLabelType.TRAGEDY

    placement_criterion_op = client.get_type(
        "CustomerNegativeCriterionOperation"
    )
    placement_criterion = placement_criterion_op.create
    # Creates a negative customer criterion excluding the placement with URL
    # 'http://www.example.com'.
    placement_criterion.placement.url = "http://www.example.com"

    customer_negative_criterion_service = client.get_service(
        "CustomerNegativeCriterionService"
    )

    # Issues a mutate request to add the negative customer criteria.
    response = customer_negative_criterion_service.mutate_customer_negative_criteria(
        customer_id=customer_id,
        operations=[tragedy_criterion_op, placement_criterion_op],
    )
    print(f"Added {len(response.results)} negative customer criteria:")
    for negative_criterion in response.results:
        print(f"Resource name: '{negative_criterion.resource_name}'")


if __name__ == "__main__":
    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    googleads_client = GoogleAdsClient.load_from_storage(version="v8")

    parser = argparse.ArgumentParser(
        description=(
            "Adds various types of negative criteria as exclusions at the "
            "customer level. These criteria will be applied to all campaignsi "
            "for the given customer."
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
    args = parser.parse_args()

    try:
        main(
            googleads_client, args.customer_id,
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
