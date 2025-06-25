#!/usr/bin/env python
# Copyright 2025 Google LLC
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
"""This example illustrates how to generate audience insights."""

import argparse
import argparse
import sys

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException


def main(client, customer_id, custom_name):
    """The main method that creates all necessary entities for the example.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.
        custom_name: custom name to define audience.
    """
    location_id = "2840"  # US
    product_name = "Google"
    user_interest_category = "92948"  # Technology
    # Initialize appropriate services.
    audience_insights_service = client.get_service("AudienceInsightsService")
    googleads_service = client.get_service("GoogleAdsService")

    audience_composition_insights(
        client,
        audience_insights_service,
        googleads_service,
        customer_id,
        location_id,
        user_interest_category,
        custom_name,
    )
    generate_suggested_targeting_insights(
        client,
        audience_insights_service,
        googleads_service,
        customer_id,
        location_id,
        custom_name,
    )
    list_audience_insights_attributes(
        client,
        audience_insights_service,
        customer_id,
        product_name,
        custom_name,
    )


# [START composition_insights]
def audience_composition_insights(
    client,
    audience_insights_service,
    googleads_service,
    customer_id,
    location_id,
    user_interest,
    custom_name,
):
    """Returns a collection of attributes represented in an audience of interest.

        Please refere here for more:
        https://developers.google.com/google-ads/api/data/codes-formats

    Args:
        client: an initialized GoogleAdsClient instance.
        audience_insights_service: an initialized AudienceInsightsService
          instance.
        googleads_service: an initialized GoogleAds Service instance.
        customer_id: The customer ID for the audience insights service.
        location_id: The location ID for the audience of interest.
        user_interest: The criterion ID of the category.
        custom_name: custom defined name.
    """
    request = client.get_type("GenerateAudienceCompositionInsightsRequest")
    request.customer_id = customer_id

    insights_info = client.get_type("InsightsAudienceAttributeGroup")
    attributes = client.get_type("AudienceInsightsAttribute")
    attributes.user_interest.user_interest_category = (
        googleads_service.user_interest_path(customer_id, user_interest)
    )

    insights_info.attributes.append(attributes)
    request.audience.topic_audience_combinations.append(insights_info)

    location_info = client.get_type("LocationInfo")
    location_info.geo_target_constant = (
        googleads_service.geo_target_constant_path(location_id)
    )
    request.audience.country_locations.append(location_info)

    request.customer_insights_group = custom_name
    request.dimensions = (
        "AFFINITY_USER_INTEREST",
        "IN_MARKET_USER_INTEREST",
        "YOUTUBE_CHANNEL",
    )
    response = audience_insights_service.generate_audience_composition_insights(
        request=request
    )
    print(response)
    # [END composition_insights]


# [START targeted_insights]
def generate_suggested_targeting_insights(
    client,
    audience_insights_service,
    googleads_service,
    customer_id,
    location_id,
    custom_name,
):
    """Returns a collection of targeting insights (e.g.targetable audiences)
        that are relevant to the requested audience.

    Args:
        client: an initialized GoogleAdsClient instance.
        audience_insights_service: an initialized AudienceInsightsService
          instance.
        googleads_service: an initialized GoogleAds Service instance.
        customer_id: The customer ID for the audience insights service.
        location_id: The location ID for the audience of interest.
        custom_name: custom defined name.
    """
    request = client.get_type("GenerateSuggestedTargetingInsightsRequest")

    request.customer_id = customer_id
    request.customer_insights_group = custom_name

    audience_definition = request.audience_definition
    location_info = client.get_type("LocationInfo")
    location_info.geo_target_constant = (
        googleads_service.geo_target_constant_path(location_id)
    )
    audience_definition.audience.country_locations.append(location_info)

    request.audience_definition = audience_definition
    response = audience_insights_service.generate_suggested_targeting_insights(
        request=request
    )
    print(response)
    # [END targeted_insights]


# [START insights_attributes]
def list_audience_insights_attributes(
    client, audience_insights_service, customer_id, product_name, custom_name
):
    """Searches for audience attributes that can be used to generate insights.

    Args:
        client: an initialized GoogleAdsClient instance.
        audience_insights_service: an initialized AudienceInsightsService
          instance.
        customer_id: The customer ID for the audience insights service.
        product_name: The brand/product for which insights are expected.
        custom_name: custom defined name.
    """
    request = client.get_type("ListAudienceInsightsAttributesRequest")

    request.customer_id = customer_id
    request.query_text = product_name
    category_dimension = client.enums.AudienceInsightsDimensionEnum.CATEGORY
    kg_dimension = client.enums.AudienceInsightsDimensionEnum.KNOWLEDGE_GRAPH
    request.dimensions = [category_dimension, kg_dimension]
    request.customer_insights_group = custom_name
    response = audience_insights_service.list_audience_insights_attributes(
        request=request
    )
    for attribute in response.attributes:
        if attribute.dimension == 3:
            print(attribute.attribute.entity.knowledge_graph_machine_id)
            # [END insights_attributes]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create audience insights.")

    # The following argument(s) should be provided to run the example.
    parser.add_argument(
        "-c",
        "--customer_id",
        type=str,
        required=True,
        help="The Google Ads customer ID.",
    )

    parser.add_argument(
        "-n",
        "--custom_name",
        type=str,
        required=True,
        help="Custom name to indentify audiences",
    )
    parser.add_argument
    args = parser.parse_args()

    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    googleads_client = GoogleAdsClient.load_from_storage(version="v20")

    try:
        main(googleads_client, args.customer_id, args.custom_name)
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
