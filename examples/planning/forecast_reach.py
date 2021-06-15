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
"""This code example generates a video ads reach forecast.
"""


import argparse
import math
import sys

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException


ONE_MILLION = 1.0e6


def main(client, customer_id):
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

    _show_plannable_locations(client)
    _show_plannable_products(client, location_id)
    _forecast_manual_mix(
        client, customer_id, location_id, currency_code, budget
    )
    _forecast_suggested_mix(
        client, customer_id, location_id, currency_code, budget
    )


def _show_plannable_locations(client):
    """Shows map of plannable locations to their IDs.

    Args:
        client: an initialized GoogleAdsClient instance.
    """
    reach_plan_service = client.get_service("ReachPlanService")
    response = reach_plan_service.list_plannable_locations()

    print("Plannable Locations")
    print("Name,\tId,\tParentCountryId")
    for location in response.plannable_locations:
        print(
            f"'{location.name}',\t{location.id},\t{location.parent_country_id}"
        )


# [START forecast_reach_2]
def _show_plannable_products(client, location_id):
    """Lists plannable products for a given location.

    Args:
        client: an initialized GoogleAdsClient instance.
        location_id: The location ID to plan for.
    """
    reach_plan_service = client.get_service("ReachPlanService")
    response = reach_plan_service.list_plannable_products(
        plannable_location_id=location_id
    )
    print(f"Plannable Products for Location ID {location_id}")

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
def _request_reach_curve(
    client, customer_id, product_mix, location_id, currency_code
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
    request = client.get_type("GenerateReachForecastRequest")
    request.customer_id = customer_id
    # Valid durations are between 1 and 90 days.
    request.campaign_duration.duration_in_days = 28
    request.currency_code = currency_code
    request.cookie_frequency_cap = 0
    request.min_effective_frequency = 1
    request.planned_products = product_mix

    request.targeting.plannable_location_id = location_id
    request.targeting.age_range = client.get_type(
        "ReachPlanAgeRangeEnum"
    ).ReachPlanAgeRange.AGE_RANGE_18_65_UP

    # Add gender targeting to the request.
    for gender_type in [
        client.get_type("GenderTypeEnum").GenderType.FEMALE,
        client.get_type("GenderTypeEnum").GenderType.MALE,
    ]:
        gender = client.get_type("GenderInfo")
        gender.type_ = gender_type
        request.targeting.genders.append(gender)

    # Add device targeting to the request.
    for device_type in [
        client.get_type("DeviceEnum").Device.DESKTOP,
        client.get_type("DeviceEnum").Device.MOBILE,
        client.get_type("DeviceEnum").Device.TABLET,
    ]:
        device = client.get_type("DeviceInfo")
        device.type_ = device_type
        request.targeting.devices.append(device)

    reach_plan_service = client.get_service("ReachPlanService")
    response = reach_plan_service.generate_reach_forecast(request=request)

    print(
        "Currency, Cost, On-Target Reach, On-Target Imprs, Total Reach,"
        " Total Imprs, Products"
    )
    for point in response.reach_curve.reach_forecasts:
        product_splits = []
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
def _forecast_manual_mix(
    client, customer_id, location_id, currency_code, budget
):
    """Pulls a forecast for product mix created manually.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: The customer ID for the reach forecast.
        product_mix: The product mix for the reach forecast.
        location_id: The location ID to plan for.
        currency_code: Three-character ISO 4217 currency code.
        budget: Budget to allocate to the plan.
    """
    product_mix = []
    trueview_allocation = 0.15
    bumper_allocation = 1 - trueview_allocation
    product_splits = [
        ("TRUEVIEW_IN_STREAM", trueview_allocation),
        ("BUMPER", bumper_allocation),
    ]
    for product, split in product_splits:
        planned_product = client.get_type("PlannedProduct")
        planned_product.plannable_product_code = product
        planned_product.budget_micros = math.trunc(budget * ONE_MILLION * split)
        product_mix.append(planned_product)

    _request_reach_curve(
        client, customer_id, product_mix, location_id, currency_code
    )
    # [END forecast_reach_3]


# [START forecast_reach_1]
def _forecast_suggested_mix(
    client, customer_id, location_id, currency_code, budget
):
    """Pulls a forecast for a product mix based on your set of preferences.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: The customer ID for the reach forecast.
        product_mix: The product mix for the reach forecast.
        location_id: The location ID to plan for.
        currency_code: Three-character ISO 4217 currency code.
        budget: Budget to allocate to the plan.
    """
    preferences = client.get_type("Preferences")
    preferences.has_guaranteed_price = True
    preferences.starts_with_sound = True
    preferences.is_skippable = False
    preferences.top_content_only = True
    preferences.ad_length = client.get_type(
        "ReachPlanAdLengthEnum"
    ).ReachPlanAdLength.FIFTEEN_OR_TWENTY_SECONDS

    reach_plan_service = client.get_service("ReachPlanService")
    request = client.get_type("GenerateProductMixIdeasRequest")
    request.customer_id = customer_id
    request.plannable_location_id = location_id
    request.preferences = preferences
    request.currency_code = currency_code
    request.budget_micros = int(budget * ONE_MILLION)
    mix_response = reach_plan_service.generate_product_mix_ideas(
        request=request
    )

    product_mix = []
    for product in mix_response.product_allocation:
        planned_product = client.get_type("PlannedProduct")
        planned_product.plannable_product_code = product.plannable_product_code
        planned_product.budget_micros = product.budget_micros
        product_mix.append(planned_product)

    _request_reach_curve(
        client, customer_id, product_mix, location_id, currency_code
    )
    # [END forecast_reach_1]


if __name__ == "__main__":
    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    googleads_client = GoogleAdsClient.load_from_storage(version="v8")

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
