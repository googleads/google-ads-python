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
"""This example sets ad parameters for an ad group criterion."""


import argparse
import sys
from typing import List

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
from google.ads.googleads.v22.services.services.ad_group_criterion_service import (
    AdGroupCriterionServiceClient,
)
from google.ads.googleads.v22.services.services.ad_parameter_service import (
    AdParameterServiceClient,
)
from google.ads.googleads.v22.services.types.ad_parameter_service import (
    AdParameterOperation,
    MutateAdParametersResponse,
)
from google.ads.googleads.v22.resources.types.ad_parameter import AdParameter


def main(
    client: GoogleAdsClient,
    customer_id: str,
    ad_group_id: str,
    criterion_id: str,
) -> None:
    """Demonstrates how to set ad parameters on an ad group criterion.

    Args:
        client: An initialized GoogleAdsClient instance.
        customer_id: A client customer ID str.
        ad_group_id: An ad group ID str.
        criterion_id: A criterion ID str.
    """
    ad_group_criterion_service: AdGroupCriterionServiceClient = (
        client.get_service("AdGroupCriterionService")
    )
    # Gets the resource name of the ad group criterion to be used.
    resource_name: str = ad_group_criterion_service.ad_group_criterion_path(
        customer_id, ad_group_id, criterion_id
    )

    operations: List[AdParameterOperation] = [
        create_ad_parameter(client, resource_name, 1, "100"),
        create_ad_parameter(client, resource_name, 2, "$40"),
    ]

    ad_parameter_service: AdParameterServiceClient = client.get_service(
        "AdParameterService"
    )

    # Add the ad parameter.
    try:
        response: MutateAdParametersResponse = (
            ad_parameter_service.mutate_ad_parameters(
                customer_id=customer_id, operations=operations
            )
        )
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
    else:
        print(f"Set {len(response.results)} ad parameters:")

        for res in response.results:
            # res: MutateAdParameterResult = res <- Removed type hint
            print(
                "Set ad parameter with resource_name: " f"{res.resource_name}"
            )


def create_ad_parameter(
    client: GoogleAdsClient,
    resource_name: str,
    parameter_index: int,
    insertion_text: str,
) -> AdParameterOperation:
    """Creates a new ad parameter create operation and returns it.

    There can be a maximum of two ad parameters per ad group criterion, one
    with "parameter_index" = 1 and another with "parameter_index" = 2.

    Restrictions apply to the value of the "insertion_text". For more
    information, see the field documentation in the AdParameter class located
    here: https://developers.google.com/google-ads/api/fields/latest/ad_parameter#ad_parameterinsertion_text

    Args:
        client: An initialized GoogleAdsClient instance.
        resource_name: The resource name of the ad group criterion.
        parameter_index: The unique index int of this ad parameter..
        insertion_text: A numeric str value to insert into the ad text.

    Returns: A new AdParameterOperation message class instance.
    """
    ad_param_operation: AdParameterOperation = client.get_type(
        "AdParameterOperation"
    )
    ad_param: AdParameter = ad_param_operation.create
    ad_param.ad_group_criterion = resource_name
    ad_param.parameter_index = parameter_index
    ad_param.insertion_text = insertion_text
    return ad_param_operation


if __name__ == "__main__":
    # Initializes a command line argument parser.
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description="Adds an ad group for specified customer and campaign id."
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
        "-k",
        "--criterion_id",
        type=str,
        required=True,
        help="The criterion ID.",
    )
    args: argparse.Namespace = parser.parse_args()

    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    googleads_client: GoogleAdsClient = GoogleAdsClient.load_from_storage(
        version="v22"
    )

    main(
        googleads_client, args.customer_id, args.ad_group_id, args.criterion_id
    )
