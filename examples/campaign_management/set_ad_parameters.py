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

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException


def main(client, customer_id, ad_group_id, criterion_id):
    """Demonstrates how to set ad parameters on an ad group criterion.

    Args:
        client: An initialized GoogleAdsClient instance.
        customer_id: A client customer ID str.
        ad_group_id: An ad group ID str.
        criterion_id: A criterion ID str.
    """
    ad_group_criterion_service = client.get_service("AdGroupCriterionService")
    # Gets the resource name of the ad group criterion to be used.
    resource_name = ad_group_criterion_service.ad_group_criterion_path(
        customer_id, ad_group_id, criterion_id
    )

    operations = [
        _create_ad_parameter(client, resource_name, 1, "100"),
        _create_ad_parameter(client, resource_name, 2, "$40"),
    ]

    ad_parameter_service = client.get_service("AdParameterService")

    # Add the ad parameter.
    try:
        response = ad_parameter_service.mutate_ad_parameters(
            customer_id=customer_id, operations=operations
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

        for result in response.results:
            print(
                "Set ad parameter with resource_name: "
                f"{result.resource_name}"
            )


def _create_ad_parameter(
    client, resource_name, parameter_index, insertion_text
):
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

    Returns: A new AdParamterOperation message class instance.
    """
    ad_param_operation = client.get_type("AdParameterOperation")
    ad_param = ad_param_operation.create
    ad_param.ad_group_criterion = resource_name
    ad_param.parameter_index = parameter_index
    ad_param.insertion_text = insertion_text
    return ad_param_operation


if __name__ == "__main__":
    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    googleads_client = GoogleAdsClient.load_from_storage(version="v8")

    # Initializes a command line argument parser.
    parser = argparse.ArgumentParser(
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
    args = parser.parse_args()

    main(
        googleads_client, args.customer_id, args.ad_group_id, args.criterion_id
    )
