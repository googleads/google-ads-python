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
"""This example adds campaign targeting criteria."""


import argparse
import sys

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException


def main(client, customer_id, campaign_id, keyword_text, location_id):
    campaign_criterion_service = client.get_service("CampaignCriterionService")

    operations = [
        _create_location_op(client, customer_id, campaign_id, location_id),
        _create_negative_keyword_op(
            client, customer_id, campaign_id, keyword_text
        ),
        _create_proximity_op(client, customer_id, campaign_id),
    ]

    campaign_criterion_response = campaign_criterion_service.mutate_campaign_criteria(
        customer_id=customer_id, operations=operations
    )

    for result in campaign_criterion_response.results:
        print(f'Added campaign criterion "{result.resource_name}".')


# [START add_campaign_targeting_criteria]
def _create_location_op(client, customer_id, campaign_id, location_id):
    campaign_service = client.get_service("CampaignService")
    geo_target_constant_service = client.get_service("GeoTargetConstantService")

    # Create the campaign criterion.
    campaign_criterion_operation = client.get_type("CampaignCriterionOperation")
    campaign_criterion = campaign_criterion_operation.create
    campaign_criterion.campaign = campaign_service.campaign_path(
        customer_id, campaign_id
    )

    # Besides using location_id, you can also search by location names from
    # GeoTargetConstantService.suggest_geo_target_constants() and directly
    # apply GeoTargetConstant.resource_name here. An example can be found
    # in get_geo_target_constant_by_names.py.
    campaign_criterion.location.geo_target_constant = geo_target_constant_service.geo_target_constant_path(
        location_id
    )

    return campaign_criterion_operation
    # [END add_campaign_targeting_criteria]


def _create_negative_keyword_op(client, customer_id, campaign_id, keyword_text):
    campaign_service = client.get_service("CampaignService")

    # Create the campaign criterion.
    campaign_criterion_operation = client.get_type("CampaignCriterionOperation")
    campaign_criterion = campaign_criterion_operation.create
    campaign_criterion.campaign = campaign_service.campaign_path(
        customer_id, campaign_id
    )
    campaign_criterion.negative = True
    criterion_keyword = campaign_criterion.keyword
    criterion_keyword.text = keyword_text
    criterion_keyword.match_type = client.get_type(
        "KeywordMatchTypeEnum"
    ).KeywordMatchType.BROAD

    return campaign_criterion_operation


# [START add_campaign_targeting_criteria_1]
def _create_proximity_op(client, customer_id, campaign_id):
    campaign_service = client.get_service("CampaignService")

    # Create the campaign criterion.
    campaign_criterion_operation = client.get_type("CampaignCriterionOperation")
    campaign_criterion = campaign_criterion_operation.create
    campaign_criterion.campaign = campaign_service.campaign_path(
        customer_id, campaign_id
    )
    campaign_criterion.proximity.address.street_address = "38 avenue de l'Opera"
    campaign_criterion.proximity.address.city_name = "Paris"
    campaign_criterion.proximity.address.postal_code = "75002"
    campaign_criterion.proximity.address.country_code = "FR"
    campaign_criterion.proximity.radius = 10
    # Default is kilometers.
    campaign_criterion.proximity.radius_units = client.get_type(
        "ProximityRadiusUnitsEnum"
    ).ProximityRadiusUnits.MILES

    return campaign_criterion_operation
    # [END add_campaign_targeting_criteria_1]


if __name__ == "__main__":
    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    googleads_client = GoogleAdsClient.load_from_storage(version="v8")

    parser = argparse.ArgumentParser(
        description=(
            "Adds campaign targeting criteria for the specified "
            "campaign under the given customer ID."
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
        "-i", "--campaign_id", type=str, required=True, help="The campaign ID."
    )
    parser.add_argument(
        "-k",
        "--keyword_text",
        type=str,
        required=True,
        help="The keyword text to be added to the campaign.",
    )
    parser.add_argument(
        "-l",
        "--location_id",
        type=str,
        required=False,
        default="21167",  # New York
        help=(
            "A location criterion ID, this field is optional. If not "
            "specified, will default to New York. For more information on "
            "determining this value, see: "
            "https://developers.google.com/google-ads/api/reference/data/geotargets"
        ),
    )
    args = parser.parse_args()

    try:
        main(
            googleads_client,
            args.customer_id,
            args.campaign_id,
            args.keyword_text,
            args.location_id,
        )
    except GoogleAdsException as ex:
        print(
            f'Request with ID "{ex.request_id}" failed with status '
            f'"{ex.error.code().name}" and includes the following errors:'
        )
        for error in ex.failure.errors:
            print(f'	Error with message "{error.message}".')
            if error.location:
                for field_path_element in error.location.field_path_elements:
                    print(f"\t\tOn field: {field_path_element.field_name}")
        sys.exit(1)
