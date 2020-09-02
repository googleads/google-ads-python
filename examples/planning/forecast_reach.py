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

from google.ads.google_ads.client import GoogleAdsClient
from google.ads.google_ads.errors import GoogleAdsException


ONE_MILLION = 1.0e6


def _string_value(client, value):
    """Converts a value to a protocol buffer string wrapper.

    Args:
      client: A google.ads.google_ads.client.GoogleAdsClient instance.
      value: A string value to wrap.

    Returns:
      An instance of google.protobuf.wrappers_pb2.StringValue with its "value"
      property updates with the given value.
    """
    string_val = client.get_type("StringValue", version="v5")
    string_val.value = value
    return string_val


def _int_32_value(client, value):
    """Converts a value to a protocol buffer Int32 wrapper.

    Args:
      client: A google.ads.google_ads.client.GoogleAdsClient instance.
      value: A number to wrap, truncated to the nearest integer.

    Returns:
      An instance of google.protobuf.wrappers_pb2.Int32Value with its "value"
      property updates with the given value.
    """
    int_32_val = client.get_type("Int32Value", version="v5")
    int_32_val.value = math.trunc(value)
    return int_32_val


def _int_64_value(client, value):
    """Converts a value to a protocol buffer Int64 wrapper.

    Args:
      client: A google.ads.google_ads.client.GoogleAdsClient instance.
      value: A number to wrap, truncated to the nearest integer.

    Returns:
      An instance of google.protobuf.wrappers_pb2.Int64Value with its "value"
      property updates with the given value.
    """
    int_64_val = client.get_type("Int64Value", version="v5")
    int_64_val.value = math.trunc(value)
    return int_64_val


def show_plannable_locations(client):
    """Shows map of plannable locations to their IDs.

    Args:
      client: A google.ads.google_ads.client.GoogleAdsClient instance.
    """
    reach_plan_service = client.get_service("ReachPlanService", version="v5")
    response = reach_plan_service.list_plannable_locations()

    print("Plannable Locations")
    print("Name,\tId,\tParentCountryId")
    for location in response.plannable_locations:
        print(
            '"{}",\t{},\t{}'.format(
                location.name.value,
                location.id.value,
                location.parent_country_id.value,
            )
        )


def show_plannable_products(client, location_id):
    """Lists plannable products for a given location.

    Args:
      client: A google.ads.google_ads.client.GoogleAdsClient instance.
      location_id: Location ID to plan for. You can get a valid loction ID from
        https://developers.google.com/adwords/api/docs/appendix/geotargeting or
        by calling ListPlannableLocations on the ReachPlanService.
    """
    reach_plan_service = client.get_service("ReachPlanService", version="v5")
    response = reach_plan_service.list_plannable_products(
        plannable_location_id=_string_value(client, location_id)
    )
    print("Plannable Products for Location ID {}".format(location_id))
    print(response)


def _request_reach_curve(
    client, customer_id, product_mix, location_id, currency_code
):
    """Creates a sample request for a given product mix.

    Args:
      client: A google.ads.google_ads.client.GoogleAdsClient instance.
      customer_id: The customer ID for the reach forecast.
      product_mix: The product mix for the reach forecast.
      location_id: Location ID to plan for. You can get a valid loction ID from
        https://developers.google.com/adwords/api/docs/appendix/geotargeting or
        by calling ListPlannableLocations on the ReachPlanService.
      currency_code: Three-character ISO 4217 currency code.
    """
    reach_request = client.get_type(
        "GenerateReachForecastRequest", version="v5"
    )

    reach_request.customer_id = customer_id

    # Valid durations are between 1 and 90 days.
    campaign_duration = reach_request.campaign_duration
    campaign_duration.duration_in_days.value = 28

    targeting = reach_request.targeting
    targeting.plannable_location_id.value = location_id
    targeting.age_range = client.get_type(
        "ReachPlanAgeRangeEnum", version="v5"
    ).AGE_RANGE_18_65_UP

    genders = targeting.genders
    gender_types = [
        client.get_type("GenderTypeEnum", version="v5").FEMALE,
        client.get_type("GenderTypeEnum", version="v5").MALE,
    ]
    for gender_type in gender_types:
        gender = client.get_type("GenderInfo", version="v5")
        gender.type = gender_type
        genders.append(gender)

    devices = targeting.devices
    device_types = [
        client.get_type("DeviceEnum", version="v5").DESKTOP,
        client.get_type("DeviceEnum", version="v5").MOBILE,
        client.get_type("DeviceEnum", version="v5").TABLET,
    ]
    for device_type in device_types:
        device = client.get_type("DeviceInfo", version="v5")
        device.type = device_type
        devices.append(device)

    reach_plan_service = client.get_service("ReachPlanService", version="v5")

    # See the docs for defaults and valid ranges:
    # https://developers.google.com/google-ads/api/reference/rpc/latest/GenerateReachForecastRequest
    response = reach_plan_service.generate_reach_forecast(
        customer_id,
        campaign_duration,
        product_mix,
        currency_code=_string_value(client, currency_code),
        cookie_frequency_cap=_int_32_value(client, 0),
        min_effective_frequency=_int_32_value(client, 1),
        targeting=targeting,
    )

    print(
        "Currency, Cost, On-Target Reach, On-Target Imprs, Total Reach,"
        " Total Imprs, Products"
    )
    for point in response.reach_curve.reach_forecasts:
        product_splits = []
        for p in point.forecasted_product_allocations:
            product_splits.append(
                {
                    p.plannable_product_code.value: p.budget_micros.value
                    / ONE_MILLION
                }
            )
        print(
            [
                currency_code,
                point.cost_micros.value / ONE_MILLION,
                point.forecast.on_target_reach.value,
                point.forecast.on_target_impressions.value,
                point.forecast.total_reach.value,
                point.forecast.total_impressions.value,
                product_splits,
            ]
        )


def forecast_manual_mix(
    client, customer_id, location_id, currency_code, budget
):
    """Pulls a forecast for product mix created manually.

    Args:
      client: A google.ads.google_ads.client.GoogleAdsClient instance.
      customer_id: The customer ID for the reach forecast.
      location_id: Location ID to plan for. You can get a valid loction ID from
        https://developers.google.com/adwords/api/docs/appendix/geotargeting or
        by calling ListPlannableLocations on the ReachPlanService.
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
        planned_product = client.get_type("PlannedProduct", version="v5")
        planned_product.plannable_product_code.value = product
        planned_product.budget_micros.value = math.trunc(
            budget * ONE_MILLION * split
        )
        product_mix.append(planned_product)

    _request_reach_curve(
        client, customer_id, product_mix, location_id, currency_code
    )


def forecast_suggested_mix(
    client, customer_id, location_id, currency_code, budget
):
    """Pulls a forecast for a product mix based on your set of preferences.

    Args:
      client: A google.ads.google_ads.client.GoogleAdsClient instance.
      customer_id: The customer ID for the reach forecast.
      location_id: Location ID to plan for. You can get a valid loction ID from
        https://developers.google.com/adwords/api/docs/appendix/geotargeting or
        by calling ListPlannableLocations on the ReachPlanService.
      currency_code: Three-character ISO 4217 currency code.
      budget: Budget to allocate to the plan.
    """
    preferences = client.get_type("Preferences", version="v5")
    preferences.has_guaranteed_price.value = True
    preferences.starts_with_sound.value = True
    preferences.is_skippable.value = False
    preferences.top_content_only.value = True
    preferences.ad_length = client.get_type(
        "ReachPlanAdLengthEnum", version="v5"
    ).FIFTEEN_OR_TWENTY_SECONDS

    reach_plan_service = client.get_service("ReachPlanService", version="v5")
    mix_response = reach_plan_service.generate_product_mix_ideas(
        customer_id=customer_id,
        plannable_location_id=_string_value(client, location_id),
        preferences=preferences,
        currency_code=_string_value(client, currency_code),
        budget_micros=_int_64_value(client, budget * ONE_MILLION),
    )

    product_mix = []
    for product in mix_response.product_allocation:
        planned_product = client.get_type("PlannedProduct", version="v5")
        planned_product.plannable_product_code.value = (
            product.plannable_product_code.value
        )
        planned_product.budget_micros.value = product.budget_micros.value
        product_mix.append(planned_product)

    _request_reach_curve(
        client, customer_id, product_mix, location_id, currency_code
    )


def main(client, customer_id):
    # location_id: Location ID to plan for. You can get a valid loction ID from
    # https://developers.google.com/adwords/api/docs/appendix/geotargeting or by
    # calling ListPlannableLocations on the ReachPlanService.
    location_id = "2840"  # US
    currency_code = "USD"
    budget = 500000

    try:
        show_plannable_locations(client)
        show_plannable_products(client, location_id)
        forecast_manual_mix(
            client, customer_id, location_id, currency_code, budget
        )
        forecast_suggested_mix(
            client, customer_id, location_id, currency_code, budget
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


if __name__ == "__main__":
    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    google_ads_client = GoogleAdsClient.load_from_storage()

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

    main(google_ads_client, args.customer_id)
