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
"""This example pauses an ad."""


import argparse
import sys
from typing import List

from google.api_core import protobuf_helpers
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
from google.ads.googleads.v20.resources.types.ad_group_ad import AdGroupAd
from google.ads.googleads.v20.services.services.ad_group_ad_service import (
    AdGroupAdServiceClient,
)
from google.ads.googleads.v20.services.types.ad_group_ad_service import (
    AdGroupAdOperation,
    MutateAdGroupAdsResponse,
)


def main(
    client: GoogleAdsClient,
    customer_id: str,
    ad_group_id: str,
    ad_id: str,
) -> None:
    ad_group_ad_service: AdGroupAdServiceClient = client.get_service(
        "AdGroupAdService"
    )

    ad_group_ad_operation: AdGroupAdOperation = client.get_type(
        "AdGroupAdOperation"
    )

    ad_group_ad: AdGroupAd = ad_group_ad_operation.update
    ad_group_ad.resource_name = ad_group_ad_service.ad_group_ad_path(
        customer_id, ad_group_id, ad_id
    )
    ad_group_ad.status = client.enums.AdGroupAdStatusEnum.PAUSED
    client.copy_from(
        ad_group_ad_operation.update_mask,
        protobuf_helpers.field_mask(None, ad_group_ad._pb),
    )

    operations List[AdGroupAdOperation] = [ad_group_ad_operation]

    ad_group_ad_response: MutateAdGroupAdsResponse = (
        ad_group_ad_service.mutate_ad_group_ads(
            customer_id=customer_id,
            operations=operations,
        )
    )

    print(
        f"Paused ad group ad {ad_group_ad_response.results[0].resource_name}."
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=("Pauses an ad in the specified customer's ad group.")
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
    parser.add_argument(
        "-i", "--ad_id", type=str, required=True, help="The ad ID."
    )
    args: argparse.Namespace = parser.parse_args()

    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
<<<<<<< HEAD
    googleads_client: GoogleAdsClient = GoogleAdsClient.load_from_storage(
        version="v20"
    )
=======
<<<<<<< HEAD
    googleads_client = GoogleAdsClient.load_from_storage(version="v20")
=======
    googleads_client: GoogleAdsClient = GoogleAdsClient.load_from_storage(
        version="v20"
    )
>>>>>>> e9e91feee (I've added type hints and annotations to the Python files in your `examples/basic_operations` directory. This should make the code easier to read and also help with static analysis.)
>>>>>>> 6b1491771 (I've added type hints and annotations to the Python files in your `examples/basic_operations` directory. This should make the code easier to read and also help with static analysis.)

    try:
        main(googleads_client, args.customer_id, args.ad_group_id, args.ad_id)
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
