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
"""This example adds demographic target criteria to an ad group, one as
positive ad group criterion and one as negative ad group criterion. To
create ad groups, run add_ad_groups.py."""


import argparse
import sys

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException


def main(client, customer_id, ad_group_id):
    ad_group_service = client.get_service("AdGroupService")
    ad_group_criterion_service = client.get_service("AdGroupCriterionService")

    ad_group_resource_name = ad_group_service.ad_group_path(
        customer_id, ad_group_id
    )
    # Create a positive ad group criterion for the gender MALE.
    gender_ad_group_criterion_operation = client.get_type(
        "AdGroupCriterionOperation"
    )
    gender_ad_group_criterion = gender_ad_group_criterion_operation.create
    gender_ad_group_criterion.ad_group = ad_group_resource_name
    gender_ad_group_criterion.gender.type_ = client.get_type(
        "GenderTypeEnum"
    ).GenderType.MALE

    # Create a negative ad group criterion for age range of 18 to 24.
    age_range_ad_group_criterion_operation = client.get_type(
        "AdGroupCriterionOperation"
    )
    age_range_ad_group_criterion = age_range_ad_group_criterion_operation.create
    age_range_ad_group_criterion.ad_group = ad_group_resource_name
    age_range_ad_group_criterion.negative = True
    age_range_ad_group_criterion.age_range.type_ = client.get_type(
        "AgeRangeTypeEnum"
    ).AgeRangeType.AGE_RANGE_18_24

    # Add two ad group criteria
    ad_group_criterion_response = ad_group_criterion_service.mutate_ad_group_criteria(
        customer_id=customer_id,
        operations=[
            gender_ad_group_criterion_operation,
            age_range_ad_group_criterion_operation,
        ],
    )

    for result in ad_group_criterion_response.results:
        print("Created keyword {}.".format(result.resource_name))


if __name__ == "__main__":
    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    googleads_client = GoogleAdsClient.load_from_storage(version="v8")

    parser = argparse.ArgumentParser(
        description=(
            "Adds demographic targeting criteria to the provided"
            " ad group, for the specified customer."
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
        "-a", "--ad_group_id", type=str, required=True, help="The ad group ID."
    )
    args = parser.parse_args()

    try:
        main(googleads_client, args.customer_id, args.ad_group_id)
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
