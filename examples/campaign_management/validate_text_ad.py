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
"""This example shows use of the validateOnly header for an expanded text ad.

No objects will be created, but exceptions will still be thrown.
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
    ad_group_ad.status = client.get_type(
        "AdGroupAdStatusEnum"
    ).AdGroupAdStatus.PAUSED

    # Create an expanded text ad.
    ad_group_ad.ad.expanded_text_ad.description = "Luxury Cruise to Mars"
    ad_group_ad.ad.expanded_text_ad.headline_part1 = (
        "Visit the Red Planet in style."
    )
    # Adds a headline that will trigger a policy violation to demonstrate error
    # handling.
    ad_group_ad.ad.expanded_text_ad.headline_part2 = (
        "Low-gravity fun for everyone!!"
    )
    ad_group_ad.ad.final_urls.append("http://www.example.com/")

    ad_group_ad_service = client.get_service("AdGroupAdService")
    # Attempt the mutate with validate_only=True.
    try:
        request = client.get_type("MutateAdGroupAdsRequest")
        request.customer_id = customer_id
        request.operations.append(ad_group_ad_operation)
        request.partial_failure = False
        request.validate_only = True
        response = ad_group_ad_service.mutate_ad_group_ads(request=request)
        print('"Expanded text ad validated successfully.')
    except GoogleAdsException as ex:
        # This will be hit if there is a validation error from the server.
        print(
            f'Request with ID "{ex.request_id}" failed with status '
            f'"{ex.error.code().name}".'
        )
        print(
            "There may have been validation error(s) while adding expanded "
            "text ad."
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
    googleads_client = GoogleAdsClient.load_from_storage(version="v8")

    parser = argparse.ArgumentParser(
        description="Shows how to use the ValidateOnly header."
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
