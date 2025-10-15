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
"""This code example generates a video ads reach forecast."""

import argparse
import math
import sys

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
from google.ads.googleads.v22.enums.types.reach_plan_age_range import (
    ReachPlanAgeRangeEnum,
)
from google.ads.googleads.v22.enums.types.gender_type import GenderTypeEnum
from google.ads.googleads.v22.enums.types.device import DeviceEnum
from google.ads.googleads.v22.common.types.criteria import (
    GenderInfo,
    DeviceInfo,
)
from google.ads.googleads.v22.services.services.reach_plan_service.client import (
    ReachPlanServiceClient,
)
from google.ads.googleads.v22.services.types.reach_plan_service import (
    ListPlannableLocationsResponse,
    PlannableLocation,
    ListPlannableProductsResponse,
    ProductMetadata,
    GenerateReachForecastRequest,
    GenerateReachForecastResponse,
    ReachForecast,
    PlannedProductReachForecast,
    PlannedProduct,
)

ONE_MILLION = 1.0e6


def main(client: GoogleAdsClient, customer_id: str):
    """The main method that creates all necessary entities for the example.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.
    """
    # You can review a list of valid location IDs by visiting:
    # https://developers.google.com/google-ads/api/reference/data/geotargets
    # or by calling the ListPlannableLocations method on ReachPlanService.
    location_id = "2840"  # US
    currency_code = "USD"
    budget = 500000

    show_plannable_locations(client)
    show_plannable_products(client, location_id)
    forecast_manual_mix(client, customer_id, location_id, currency_code, budget)


def show_plannable_locations(client: GoogleAdsClient):
    """Shows map of plannable locations to their IDs.

    Args:
        client: an initialized GoogleAdsClient instance.
    """
    reach_plan_service: ReachPlanServiceClient = client.get_service(
        "ReachPlanService"
    )
    response: ListPlannableLocationsResponse = (
        reach_plan_service.list_plannable_locations()
    )

    print("Plannable Locations")
    print("Name,\tId,\tParentCountryId")
    location: PlannableLocation
    for location in response.plannable_locations:
        print(
            f"'{location.name}',\t{location.id},\t{location.parent_country_id}"
        )


# [START forecast_reach_2]
def show_plannable_products(client: GoogleAdsClient, location_id: str):
    """Lists plannable products for a given location.

    Args:
        client: an initialized GoogleAdsClient instance.
        location_id: The location ID to plan for.
    """
    reach_plan_service: ReachPlanServiceClient = client.get_service(
        "ReachPlanService"
    )
    response: ListPlannableProductsResponse = (
        reach_plan_service.list_plannable_products(
            plannable_location_id=location_id
        )
    )
    print(f"Plannable Products for Location ID {location_id}")

    product_metadata: ProductMetadata
    for product_metadata in response.product_metadata:
        print(
            f"{product_metadata.plannable_product_code} : "
            f"{product_metadata.plannable_product_name}"
        )

        print("Age Ranges:")
        age_range: ReachPlanAgeRangeEnum
        for age_range in product_metadata.plannable_targeting.age_ranges:
            print(f"\t- {age_range.name}")

        print("Genders:")
        gender: GenderInfo
        for gender in product_metadata.plannable_targeting.genders:
            print(f"\t- {gender.type_.name}")

        print("Devices:")
        device: DeviceInfo
        for device in product_metadata.plannable_targeting.devices:
            print(f"\t- {device.type_.name}")
        # [END forecast_reach_2]


# [START forecast_reach]
def request_reach_curve(
    client: GoogleAdsClient,
    customer_id: str,
    product_mix: list[PlannedProduct],
    location_id: str,
    currency_code: str,
):
    """Creates a sample request for a given product mix.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: The customer ID for the reach forecast.
        product_mix: The product mix for the reach forecast.
        location_id: The location ID to plan for.
        currency_code: Three-character ISO 4217 currency code.
    """
    # See the docs for defaults and valid ranges:
    # https://developers.google.com/google-ads/api/reference/rpc/latest/GenerateReachForecastRequest
    request: GenerateReachForecastRequest = client.get_type(
        "GenerateReachForecastRequest"
    )
    request.customer_id = customer_id
    # Valid durations are between 1 and 90 days.
    request.campaign_duration.duration_in_days = 28
    request.currency_code = currency_code
    request.cookie_frequency_cap = 0
    request.min_effective_frequency = 1
    request.planned_products = product_mix

    request.targeting.plannable_location_id = location_id
    request.targeting.age_range = (
        client.enums.ReachPlanAgeRangeEnum.AGE_RANGE_18_65_UP
    )

    # Add gender targeting to the request.
    gender_type: GenderTypeEnum
    for gender_type in [
        client.enums.GenderTypeEnum.FEMALE,
        client.enums.GenderTypeEnum.MALE,
    ]:
        gender: GenderInfo = client.get_type("GenderInfo")
        gender.type_ = gender_type
        request.targeting.genders.append(gender)

    # Add device targeting to the request.
    device_type: DeviceEnum
    for device_type in [
        client.enums.DeviceEnum.DESKTOP,
        client.enums.DeviceEnum.MOBILE,
        client.enums.DeviceEnum.TABLET,
    ]:
        device: DeviceInfo = client.get_type("DeviceInfo")
        device.type_ = device_type
        request.targeting.devices.append(device)

    reach_plan_service: ReachPlanServiceClient = client.get_service(
        "ReachPlanService"
    )
    response: GenerateReachForecastResponse = (
        reach_plan_service.generate_reach_forecast(request=request)
    )

    print(
        "Currency, Cost, On-Target Reach, On-Target Imprs, Total Reach,"
        " Total Imprs, Products"
    )
    point: ReachForecast
    for point in response.reach_curve.reach_forecasts:
        product_splits = []
        p: PlannedProductReachForecast
        for p in point.planned_product_reach_forecasts:
            product_splits.append(
                {p.plannable_product_code: p.cost_micros / ONE_MILLION}
            )
        print(
            [
                currency_code,
                point.cost_micros / ONE_MILLION,
                point.forecast.on_target_reach,
                point.forecast.on_target_impressions,
                point.forecast.total_reach,
                point.forecast.total_impressions,
                product_splits,
            ]
        )
        # [END forecast_reach]


# [START forecast_reach_3]
def forecast_manual_mix(
    client: GoogleAdsClient,
    customer_id: str,
    location_id: str,
    currency_code: str,
    budget: int,
):
    """Pulls a forecast for product mix created manually.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: The customer ID for the reach forecast.
        location_id: The location ID to plan for.
        currency_code: Three-character ISO 4217 currency code.
        budget: Budget to allocate to the plan.
    """
    product_mix: list[PlannedProduct] = []
    trueview_allocation = 0.15
    bumper_allocation = 1 - trueview_allocation
    product_splits = [
        ("TRUEVIEW_IN_STREAM", trueview_allocation),
        ("BUMPER", bumper_allocation),
    ]
    product: str
    split: float
    for product, split in product_splits:
        planned_product: PlannedProduct = client.get_type("PlannedProduct")
        planned_product.plannable_product_code = product
        planned_product.budget_micros = math.trunc(budget * ONE_MILLION * split)
        product_mix.append(planned_product)

    request_reach_curve(
        client, customer_id, product_mix, location_id, currency_code
    )
    # [END forecast_reach_3]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generates video ads reach forecast."
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

    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    googleads_client = GoogleAdsClient.load_from_storage(version="v22")

    try:
        main(googleads_client, args.customer_id)
    except GoogleAdsException as ex:
        print(
            'Request with ID "{}" failed with status "%s" and includes the '
            "following errors:".format(ex.request_id, ex.error.code().name)
        )
        for error in ex.failure.errors:
            print('\tError with message "{}".'.format(error.message))
            if error.location:
                for field_path_element in error.location.field_path_elements:
                    print(
                        "\t\tOn field: {}".format(field_path_element.field_name)
                    )
        sys.exit(1)
