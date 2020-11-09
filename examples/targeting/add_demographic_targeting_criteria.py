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

import google.ads.google_ads.client


def main(client, customer_id, ad_group_id):
    ad_group_service = client.get_service("AdGroupService", version="v6")
    ad_group_criterion_service = client.get_service(
        "AdGroupCriterionService", version="v6"
    )

    ad_group_resource_name = ad_group_service.ad_group_path(
        customer_id, ad_group_id
    )
    # Create a positive ad group criterion for the gender MALE.
    gender_ad_group_criterion_operation = client.get_type(
        "AdGroupCriterionOperation", version="v6"
    )
    gender_ad_group_criterion = gender_ad_group_criterion_operation.create
    gender_ad_group_criterion.ad_group = ad_group_resource_name
    gender_ad_group_criterion.gender.type = client.get_type(
        "GenderTypeEnum"
    ).MALE

    # Create a negative ad group criterion for age range of 18 to 24.
    age_range_ad_group_criterion_operation = client.get_type(
        "AdGroupCriterionOperation", version="v6"
    )
    age_range_ad_group_criterion = age_range_ad_group_criterion_operation.create
    age_range_ad_group_criterion.ad_group = ad_group_resource_name
    age_range_ad_group_criterion.negative = True
    age_range_ad_group_criterion.age_range.type = client.get_type(
        "AgeRangeTypeEnum"
    ).AGE_RANGE_18_24

    # Add two ad group criteria
    try:
        ad_group_criterion_response = ad_group_criterion_service.mutate_ad_group_criteria(
            customer_id,
            [
                gender_ad_group_criterion_operation,
                age_range_ad_group_criterion_operation,
            ],
        )
    except google.ads.google_ads.errors.GoogleAdsException as ex:
        print(
            'Request with ID "%s" failed with status "%s" and includes the '
            "following errors:" % (ex.request_id, ex.error.code().name)
        )
        for error in ex.failure.errors:
            print('\tError with message "%s".' % error.message)
            if error.location:
                for field_path_element in error.location.field_path_elements:
                    print("\t\tOn field: %s" % field_path_element.field_name)
        sys.exit(1)

    for result in ad_group_criterion_response.results:
        print("Created keyword {}.".format(result.resource_name))


if __name__ == "__main__":
    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    google_ads_client = (
        google.ads.google_ads.client.GoogleAdsClient.load_from_storage()
    )

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

    main(google_ads_client, args.customer_id, args.ad_group_id)
