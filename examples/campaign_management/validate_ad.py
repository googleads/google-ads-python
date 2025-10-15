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
from typing import List

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
from google.ads.googleads.v22.services.types.ad_group_ad_service import (
    AdGroupAdOperation,
    MutateAdGroupAdsRequest,
)
from google.ads.googleads.v22.resources.types.ad_group_ad import AdGroupAd
from google.ads.googleads.v22.services.services.ad_group_service import (
    AdGroupServiceClient,
)
from google.ads.googleads.v22.common.types.ad_type_infos import AdTextAsset
from google.ads.googleads.v22.services.services.ad_group_ad_service import (
    AdGroupAdServiceClient,
)
from google.ads.googleads.v22.errors.types.policy_finding_error import (
    PolicyFindingErrorEnum,
)
from google.ads.googleads.v22.common.types.policy import PolicyTopicEntry


def main(client: GoogleAdsClient, customer_id: str, ad_group_id: str) -> None:
    ad_group_ad_operation: AdGroupAdOperation = client.get_type(
        "AdGroupAdOperation"
    )
    ad_group_ad: AdGroupAd = ad_group_ad_operation.create
    ad_group_service: AdGroupServiceClient = client.get_service(
        "AdGroupService"
    )
    ad_group_ad.ad_group = ad_group_service.ad_group_path(
        customer_id, ad_group_id
    )
    ad_group_ad.status = client.enums.AdGroupAdStatusEnum.PAUSED
    ad_group_ad.ad.final_urls.append("http://www.example.com/")

    # Create a responsive search ad.
    headline_1: AdTextAsset = client.get_type("AdTextAsset")
    headline_1.text = "Visit the Red Planet in style."
    headline_1.pinned_field = client.enums.ServedAssetFieldTypeEnum.HEADLINE_1
    ad_group_ad.ad.responsive_search_ad.headlines.append(headline_1)

    headline_2: AdTextAsset = client.get_type("AdTextAsset")
    headline_2.text = "An interplanetary adventure"
    ad_group_ad.ad.responsive_search_ad.headlines.append(headline_2)

    # Adds a headline that will trigger a policy violation to demonstrate
    # error handling.
    headline_3: AdTextAsset = client.get_type("AdTextAsset")
    headline_3.text = "Low-gravity fun for everyone!!"
    ad_group_ad.ad.responsive_search_ad.headlines.append(headline_3)

    description_1: AdTextAsset = client.get_type("AdTextAsset")
    description_1.text = "Luxury Cruise to Mars"
    ad_group_ad.ad.responsive_search_ad.descriptions.append(description_1)

    description_2: AdTextAsset = client.get_type("AdTextAsset")
    description_2.text = "Book your ticket now"
    ad_group_ad.ad.responsive_search_ad.descriptions.append(description_2)

    ad_group_ad_service: AdGroupAdServiceClient = client.get_service(
        "AdGroupAdService"
    )
    # Attempt the mutate with validate_only=True.
    try:
        request: MutateAdGroupAdsRequest = client.get_type(
            "MutateAdGroupAdsRequest"
        )
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
        policy_error_enum: PolicyFindingErrorEnum.PolicyFindingError = (
            client.get_type(
                "PolicyFindingErrorEnum"
            ).PolicyFindingError.POLICY_FINDING
        )

        count: int = 1
        for err in ex.failure.errors:
            # err: GoogleAdsError = err <- Removed type hint
            # Note: Policy violation errors are returned as PolicyFindingErrors.
            # For additional details, see
            # https://developers.google.com/google-ads/api/docs/policy-exemption/overview
            if err.error_code.policy_finding_error == policy_error_enum:
                if err.details.policy_finding_details:
                    details: List[PolicyTopicEntry] = (
                        err.details.policy_finding_details.policy_topic_entries
                    )
                    for pol_entry in details:
                        # pol_entry: PolicyTopicEntry = pol_entry <- Removed type hint
                        print(f"{count}) Policy topic entry: \n{pol_entry}\n")
                count += 1
            else:
                print(
                    f"\tNon-policy finding error with message "
                    f'"{err.message}".'
                )
                if err.location:
                    for field_path_element in err.location.field_path_elements:
                        print(f"\t\tOn field: {field_path_element.field_name}")
                sys.exit(1)


if __name__ == "__main__":
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
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
    args: argparse.Namespace = parser.parse_args()

    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    googleads_client: GoogleAdsClient = GoogleAdsClient.load_from_storage(
        version="v22"
    )

    main(googleads_client, args.customer_id, args.ad_group_id)
