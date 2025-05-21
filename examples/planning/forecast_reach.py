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
from typing import Dict, List, Tuple, Any

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
from google.ads.googleads.v19.common.types import (
    CampaignDuration,  # Added
    DeviceInfo,
    GenderInfo,
    PlannedProduct,
    SurfaceTargeting,  # Added
)
from google.ads.googleads.v19.enums.types import (
    DeviceEnum,
    GenderTypeEnum,
    ReachPlanAgeRangeEnum,
    ReachPlanSurfaceEnum,  # Added
)
from google.ads.googleads.v19.resources.types import (
    PlannableLocation,
    ProductMetadata,
)
from google.ads.googleads.v19.services.types import (
    GenerateReachForecastRequest,
    GenerateReachForecastResponse,
    ListPlannableLocationsResponse,
    ListPlannableProductsResponse,
    PlannedProductReachForecast,  # Added
    ReachForecast,  # Added
    ReachPlanService,
)

ONE_MILLION: float = 1.0e6


def main(
    client: GoogleAdsClient,
    customer_id: str,
    location_id: str,
    currency_code: str,
    campaign_budget: int,
    cookie_life_span: int,
) -> None:
    """The main method that creates all necessary entities for the example.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.
        location_id: The location ID to plan for.
        currency_code: Three-character ISO 4217 currency code.
        campaign_budget: Budget to allocate to the plan (in micros).
        cookie_life_span: The cookie life span for the reach forecast.
    """
    show_plannable_locations(client)
    show_plannable_products(client, location_id)
    forecast_manual_mix(
        client,
        customer_id,
        location_id,
        currency_code,
        campaign_budget,
        cookie_life_span,
    )


def show_plannable_locations(client: GoogleAdsClient) -> None:
    """Shows map of plannable locations to their IDs.

    Args:
        client: an initialized GoogleAdsClient instance.
    """
    reach_plan_service: ReachPlanService = client.get_service(
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
def show_plannable_products(
    client: GoogleAdsClient, location_id: str
) -> None:
    """Lists plannable products for a given location.

    Args:
        client: an initialized GoogleAdsClient instance.
        location_id: The location ID to plan for.
    """
    reach_plan_service: ReachPlanService = client.get_service(
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
        for age_range in product_metadata.plannable_targeting.age_ranges:
            print(f"\t- {age_range.name}")

        print("Genders:")
        for gender in product_metadata.plannable_targeting.genders:
            print(f"\t- {gender.type_.name}")

        print("Devices:")
        for device in product_metadata.plannable_targeting.devices:
            print(f"\t- {device.type_.name}")
        # [END forecast_reach_2]


# [START forecast_reach]
def request_reach_curve(
    client: GoogleAdsClient,
    customer_id: str,
    product_mix: List[PlannedProduct],
    location_id: str,
    currency_code: str,
) -> None:
    """Creates a sample request for a given product mix.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: The customer ID for the reach forecast.
        product_mix: The product mix for the reach forecast.
        location_id: The location ID to plan for.
        currency_code: Three-character ISO 4217 currency code.
        cookie_life_span: The cookie life span for the reach forecast.
    """
    # See the docs for defaults and valid ranges:
    # https://developers.google.com/google-ads/api/reference/rpc/latest/GenerateReachForecastRequest
    request: GenerateReachForecastRequest = client.get_type(
        "GenerateReachForecastRequest"
    )
    request.customer_id = customer_id
    # Valid durations are between 1 and 90 days.
    campaign_duration: CampaignDuration = request.campaign_duration
    campaign_duration.duration_in_days = 28
    request.currency_code = currency_code
    request.cookie_frequency_cap = cookie_life_span
    request.min_effective_frequency = 1
    request.planned_products.extend(product_mix)

    request.targeting.plannable_location_id = location_id
    request.targeting.age_range = (
        client.enums.ReachPlanAgeRangeEnum.AGE_RANGE_18_65_UP
    )

    # Add gender targeting to the request.
    gender_type_enum: GenderTypeEnum = client.enums.GenderTypeEnum
    for gender_type_value in [
        gender_type_enum.FEMALE,
        gender_type_enum.MALE,
    ]:
        gender: GenderInfo = client.get_type("GenderInfo")
        gender.type_ = gender_type_value
        request.targeting.genders.append(gender)

    # Add device targeting to the request.
    device_enum_type: DeviceEnum = client.enums.DeviceEnum
    for device_type_value in [
        device_enum_type.DESKTOP,
        device_enum_type.MOBILE,
        device_enum_type.TABLET,
    ]:
        device: DeviceInfo = client.get_type("DeviceInfo")
        device.type_ = device_type_value
        request.targeting.devices.append(device)

    reach_plan_service: ReachPlanService = client.get_service(
        "ReachPlanService"
    )
    response: GenerateReachForecastResponse = (
        reach_plan_service.generate_reach_forecast(request=request)
    )

    print(
        "Currency, Cost, On-Target Reach, On-Target Imprs, Total Reach,"
        " Total Imprs, Products"
    )
    reach_forecast: ReachForecast
    for reach_forecast in response.reach_curve.reach_forecasts:
        product_splits: List[Dict[str, float]] = []
        forecast: PlannedProductReachForecast
        for forecast in reach_forecast.planned_product_reach_forecasts:
            product_splits.append(
                {forecast.plannable_product_code: forecast.cost_micros / ONE_MILLION}
            )
        print(
            [
                currency_code,
                reach_forecast.cost_micros / ONE_MILLION,
                reach_forecast.forecast.on_target_reach,
                reach_forecast.forecast.on_target_impressions,
                reach_forecast.forecast.total_reach,
                reach_forecast.forecast.total_impressions,
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
    campaign_budget: int,  # Renamed from budget to campaign_budget
    cookie_life_span: int, # Added cookie_life_span
) -> None:
    """Pulls a forecast for product mix created manually.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: The customer ID for the reach forecast.
        location_id: The location ID to plan for.
        currency_code: Three-character ISO 4217 currency code.
        campaign_budget: Budget to allocate to the plan (in micros).
        cookie_life_span: The cookie life span for the reach forecast.
    """
    product_mix: List[PlannedProduct] = []
    trueview_allocation: float = 0.15
    bumper_allocation: float = 1 - trueview_allocation
    product_splits: List[Tuple[str, float]] = [
        ("TRUEVIEW_IN_STREAM", trueview_allocation),
        ("BUMPER", bumper_allocation),
    ]
    product_code_str: str
    split_float: float
    for product_code_str, split_float in product_splits:
        target_product: PlannedProduct = client.get_type("PlannedProduct")
        target_product.plannable_product_code = product_code_str
        # campaign_budget is already in micros
        target_product.budget_micros = math.trunc(
            campaign_budget * split_float
        )
        product_mix.append(target_product)

    request_reach_curve(
        client, customer_id, product_mix, location_id, currency_code, cookie_life_span
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
    # Adding new arguments as per the type hint for main
    parser.add_argument(
        "-l",
        "--location_id",
        type=str,
        default="2840",  # Default to US
        help="The location ID to plan for.",
    )
    parser.add_argument(
        "-cc",
        "--currency_code",
        type=str,
        default="USD",
        help="The three-character ISO 4217 currency code.",
    )
    parser.add_argument(
        "-b",
        "--campaign_budget",
        type=int,
        default=500000,  # Default budget in micros
        help="The campaign budget in micros.",
    )
    parser.add_argument(
        "-s",
        "--cookie_life_span",
        type=int,
        default=0, # Default as per original request.cookie_frequency_cap
        help="The cookie life span for the reach forecast.",
    )
    args = parser.parse_args()

    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    googleads_client: GoogleAdsClient = GoogleAdsClient.load_from_storage(
        version="v19"
    )

    try:
        # Passing all arguments to main now
        main(
            googleads_client,
            args.customer_id,
            args.location_id,
            args.currency_code,
            args.campaign_budget,
            args.cookie_life_span,
        )
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
