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


def _show_plannable_locations(client):
    """Shows map of plannable locations to their IDs.

    Args:
      client: A google.ads.google_ads.client.GoogleAdsClient instance.
    """
    reach_plan_service = client.get_service("ReachPlanService", version="v6")
    response = reach_plan_service.list_plannable_locations()

    print("Plannable Locations")
    print("Name,\tId,\tParentCountryId")
    for location in response.plannable_locations:
        print(
            '"{}",\t{},\t{}'.format(
                location.name, location.id, location.parent_country_id,
            )
        )


# [START forecast_reach_2]
def _show_plannable_products(client, location_id):
    """Lists plannable products for a given location.

    Args:
      client: A google.ads.google_ads.client.GoogleAdsClient instance.
      location_id: Location ID to plan for. You can get a valid loction ID from
        https://developers.google.com/adwords/api/docs/appendix/geotargeting or
        by calling ListPlannableLocations on the ReachPlanService.
    """
    reach_plan_service = client.get_service("ReachPlanService", version="v6")
    response = reach_plan_service.list_plannable_products(
        plannable_location_id=location_id
    )

    print(f"Plannable Products for Location ID {location_id}")

    age_range_enum = client.get_type("ReachPlanAgeRangeEnum", version="v6")
    gender_type_enum = client.get_type("GenderTypeEnum", version="v6")
    device_enum = client.get_type("DeviceEnum", version="v6")

    for product_metadata in response.product_metadata:
        print(
            f"{product_metadata.plannable_product_code} : "
            f"{product_metadata.plannable_product_name}"
        )

        print("Age Ranges:")
        for age_range in product_metadata.plannable_targeting.age_ranges:
            print(f"\t- {age_range_enum.ReachPlanAgeRange.Name(age_range)}")

        print("Genders:")
        for gender in product_metadata.plannable_targeting.genders:
            print(f"\t- {gender_type_enum.GenderType.Name(gender.type)}")

        print("Devices:")
        for device in product_metadata.plannable_targeting.devices:
            print(f"\t- {device_enum.Device.Name(device.type)}")
            # [END forecast_reach_2]


# [START forecast_reach]
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
        "GenerateReachForecastRequest", version="v6"
    )

    reach_request.customer_id = customer_id

    # Valid durations are between 1 and 90 days.
    campaign_duration = reach_request.campaign_duration
    campaign_duration.duration_in_days = 28

    targeting = reach_request.targeting
    targeting.plannable_location_id = location_id
    targeting.age_range = client.get_type(
        "ReachPlanAgeRangeEnum", version="v6"
    ).AGE_RANGE_18_65_UP

    genders = targeting.genders
    gender_types = [
        client.get_type("GenderTypeEnum", version="v6").FEMALE,
        client.get_type("GenderTypeEnum", version="v6").MALE,
    ]
    for gender_type in gender_types:
        gender = client.get_type("GenderInfo", version="v6")
        gender.type = gender_type
        genders.append(gender)

    devices = targeting.devices
    device_types = [
        client.get_type("DeviceEnum", version="v6").DESKTOP,
        client.get_type("DeviceEnum", version="v6").MOBILE,
        client.get_type("DeviceEnum", version="v6").TABLET,
    ]
    for device_type in device_types:
        device = client.get_type("DeviceInfo", version="v6")
        device.type = device_type
        devices.append(device)

    reach_plan_service = client.get_service("ReachPlanService", version="v6")

    # See the docs for defaults and valid ranges:
    # https://developers.google.com/google-ads/api/reference/rpc/latest/GenerateReachForecastRequest
    response = reach_plan_service.generate_reach_forecast(
        customer_id,
        campaign_duration,
        product_mix,
        currency_code=currency_code,
        cookie_frequency_cap=0,
        min_effective_frequency=1,
        targeting=targeting,
    )

    print(
        "Currency, Cost, On-Target Reach, On-Target Imprs, Total Reach, "
        " Total Imprs, Products"
    )
    for point in response.reach_curve.reach_forecasts:
        print(
            [
                currency_code,
                point.cost_micros / ONE_MILLION,
                point.forecast.on_target_reach,
                point.forecast.on_target_impressions,
                point.forecast.total_reach,
                point.forecast.total_impressions,
                [
                    {p.plannable_product_code: p.cost_micros / ONE_MILLION}
                    for p in point.planned_product_reach_forecasts
                ],
            ]
        )
        # [END forecast_reach]


# [START forecast_reach_3]
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
        planned_product = client.get_type("PlannedProduct", version="v6")
        planned_product.plannable_product_code = product
        planned_product.budget_micros = math.trunc(budget * ONE_MILLION * split)
        product_mix.append(planned_product)

    _request_reach_curve(
        client, customer_id, product_mix, location_id, currency_code
    )
    # [END forecast_reach_3]


# [START forecast_reach_1]
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
    preferences = client.get_type("Preferences", version="v6")
    preferences.has_guaranteed_price = True
    preferences.starts_with_sound = True
    preferences.is_skippable = False
    preferences.top_content_only = True
    preferences.ad_length = client.get_type(
        "ReachPlanAdLengthEnum", version="v6"
    ).FIFTEEN_OR_TWENTY_SECONDS

    reach_plan_service = client.get_service("ReachPlanService", version="v6")
    mix_response = reach_plan_service.generate_product_mix_ideas(
        customer_id=customer_id,
        plannable_location_id=location_id,
        preferences=preferences,
        currency_code=currency_code,
        budget_micros=math.trunc(budget * ONE_MILLION),
    )

    product_mix = []
    for product in mix_response.product_allocation:
        planned_product = client.get_type("PlannedProduct", version="v6")
        planned_product.plannable_product_code = product.plannable_product_code
        planned_product.budget_micros = product.budget_micros
        product_mix.append(planned_product)

    _request_reach_curve(
        client, customer_id, product_mix, location_id, currency_code
    )
    # [END forecast_reach_1]


def main(client, customer_id):
    # location_id: Location ID to plan for. You can get a valid loction ID from
    # https://developers.google.com/adwords/api/docs/appendix/geotargeting or by
    # calling ListPlannableLocations on the ReachPlanService.
    location_id = "2840"  # US
    currency_code = "USD"
    budget = 500000

    try:
        _show_plannable_locations(client)
        _show_plannable_products(client, location_id)
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
