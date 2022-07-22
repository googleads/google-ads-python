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
"""This example shows use of the validate_only header when creating an ad.

Here we use a responsive search ad, but this approach can be used for any ad
type. No objects will be created in the given customer account, but exceptions
will still be thrown.
"""


import argparse
import sys

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException


def main(client, customer_id, ad_group_id):
    ad_group_ad_operation = client.get_type("AdGroupAdOperation")
    ad_group_ad = ad_group_ad_operation.create
    ad_group_service = client.get_service("AdGroupService")
    ad_group_ad.ad_group = ad_group_service.ad_group_path(
        customer_id, ad_group_id
    )
    ad_group_ad.status = client.enums.AdGroupAdStatusEnum.PAUSED
    ad_group_ad.ad.final_urls.append("http://www.example.com/")

    # Create a responsive search ad.
    headline_1 = client.get_type("AdTextAsset")
    headline_1.text = "Visit the Red Planet in style."
    headline_1.pinned_field = client.enums.ServedAssetFieldTypeEnum.HEADLINE_1
    ad_group_ad.ad.responsive_search_ad.headlines.append(headline_1)

    headline_2 = client.get_type("AdTextAsset")
    headline_2.text = "An interplanetary adventure"
    ad_group_ad.ad.responsive_search_ad.headlines.append(headline_2)

    # Adds a headline that will trigger a policy violation to demonstrate
    # error handling.
    headline_3 = client.get_type("AdTextAsset")
    headline_3.text = "Low-gravity fun for everyone!!"
    ad_group_ad.ad.responsive_search_ad.headlines.append(headline_3)

    description_1 = client.get_type("AdTextAsset")
    description_1.text = "Luxury Cruise to Mars"
    ad_group_ad.ad.responsive_search_ad.descriptions.append(description_1)

    description_2 = client.get_type("AdTextAsset")
    description_2.text = "Book your ticket now"
    ad_group_ad.ad.responsive_search_ad.descriptions.append(description_2)

    ad_group_ad_service = client.get_service("AdGroupAdService")
    # Attempt the mutate with validate_only=True.
    try:
        request = client.get_type("MutateAdGroupAdsRequest")
        request.customer_id = customer_id
        request.operations.append(ad_group_ad_operation)
        request.partial_failure = False
        request.validate_only = True
        # This request will trigger a POLICY_FINDING error, which is handled
        # in the below except block.
        ad_group_ad_service.mutate_ad_group_ads(request=request)
    except GoogleAdsException as ex:
        print(
            f'Request with ID "{ex.request_id}" failed with status '
            f'"{ex.error.code().name}".'
        )
        print(
            "There may have been validation error(s) while adding responsive "
            "search ad."
        )
        policy_error_enum = client.get_type(
            "PolicyFindingErrorEnum"
        ).PolicyFindingError.POLICY_FINDING

        count = 1
        for error in ex.failure.errors:
            # Note: Policy violation errors are returned as PolicyFindingErrors.
            # For additional details, see
            # https://developers.google.com/google-ads/api/docs/policy-exemption/overview
            if error.error_code.policy_finding_error == policy_error_enum:
                if error.details.policy_finding_details:
                    details = (
                        error.details.policy_finding_details.policy_topic_entries
                    )
                    for entry in details:
                        print(f"{count}) Policy topic entry: \n{entry}\n")
                count += 1
            else:
                print(
                    f"\tNon-policy finding error with message "
                    f'"{error.message}".'
                )
                if error.location:
                    for (
                        field_path_element
                    ) in error.location.field_path_elements:
                        print(f"\t\tOn field: {field_path_element.field_name}")
                sys.exit(1)


if __name__ == "__main__":
    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    googleads_client = GoogleAdsClient.load_from_storage(version="v11")

    parser = argparse.ArgumentParser(
        description=(
            "Shows how to use the validate_only header to validate a "
            "responsive search ad. No objects will be created, but exceptions "
            "will still be thrown."
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
        "-a", "--ad_group_id", type=str, required=True, help="The Ad Group ID."
    )
    args = parser.parse_args()

    main(googleads_client, args.customer_id, args.ad_group_id)
