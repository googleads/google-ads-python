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
import sys
from typing import Any

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
from google.ads.googleads.v22.enums.types import (
    AudienceInsightsDimensionEnum,
)
from google.ads.googleads.v22.services.services.audience_insights_service import (
    AudienceInsightsServiceClient,
)
from google.ads.googleads.v22.services.services.google_ads_service import (
    GoogleAdsServiceClient,
)
from google.ads.googleads.v22.services.types.audience_insights_service import (
    GenerateAudienceCompositionInsightsRequest,
    GenerateAudienceCompositionInsightsResponse,
    GenerateSuggestedTargetingInsightsRequest,
    GenerateSuggestedTargetingInsightsResponse,
    InsightsAudienceAttributeGroup,
    ListAudienceInsightsAttributesRequest,
    ListAudienceInsightsAttributesResponse,
)
from google.ads.googleads.v22.common.types import (
    AudienceInsightsAttribute,
    LocationInfo,
)


def main(client: GoogleAdsClient, customer_id: str, custom_name: str) -> None:
    """The main method that creates all necessary entities for the example.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.
        custom_name: custom name to define audience.
    """
    location_id: str = "2840"  # US
    product_name: str = "Google"
    user_interest_category: str = "92948"  # Technology
    # Initialize appropriate services.
    audience_insights_service: AudienceInsightsServiceClient = (
        client.get_service("AudienceInsightsService")
    )
    googleads_service: GoogleAdsServiceClient = client.get_service(
        "GoogleAdsService"
    )

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
    client: GoogleAdsClient,
    audience_insights_service: AudienceInsightsServiceClient,
    googleads_service: GoogleAdsServiceClient,
    customer_id: str,
    location_id: str,
    user_interest: str,
    custom_name: str,
) -> None:
    """Returns a collection of attributes represented in an audience of interest.

        Please refer here for more:
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
    request: GenerateAudienceCompositionInsightsRequest = client.get_type(
        "GenerateAudienceCompositionInsightsRequest"
    )
    request.customer_id = customer_id

    insights_info: InsightsAudienceAttributeGroup = client.get_type(
        "InsightsAudienceAttributeGroup"
    )
    attributes: AudienceInsightsAttribute = client.get_type(
        "AudienceInsightsAttribute"
    )
    attributes.user_interest.user_interest_category = (
        googleads_service.user_interest_path(customer_id, user_interest)
    )

    insights_info.attributes.append(attributes)
    request.audience.topic_audience_combinations.append(insights_info)

    location_info: LocationInfo = client.get_type("LocationInfo")
    location_info.geo_target_constant = (
        googleads_service.geo_target_constant_path(location_id)
    )
    request.audience.country_locations.append(location_info)

    request.customer_insights_group = custom_name
    request.dimensions = [
        client.enums.AudienceInsightsDimensionEnum.AFFINITY_USER_INTEREST,
        client.enums.AudienceInsightsDimensionEnum.IN_MARKET_USER_INTEREST,
        client.enums.AudienceInsightsDimensionEnum.YOUTUBE_CHANNEL,
    ]
    response: GenerateAudienceCompositionInsightsResponse = (
        audience_insights_service.generate_audience_composition_insights(
            request=request
        )
    )
    print(response)
    # [END composition_insights]


# [START targeted_insights]
def generate_suggested_targeting_insights(
    client: GoogleAdsClient,
    audience_insights_service: AudienceInsightsServiceClient,
    googleads_service: GoogleAdsServiceClient,
    customer_id: str,
    location_id: str,
    custom_name: str,
) -> None:
    """Returns a collection of targeting insights (e.g. target-able audiences)
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
    request: GenerateSuggestedTargetingInsightsRequest = client.get_type(
        "GenerateSuggestedTargetingInsightsRequest"
    )

    request.customer_id = customer_id
    request.customer_insights_group = custom_name

    audience_definition: Any = request.audience_definition
    location_info: LocationInfo = client.get_type("LocationInfo")
    location_info.geo_target_constant = (
        googleads_service.geo_target_constant_path(location_id)
    )
    audience_definition.audience.country_locations.append(location_info)

    request.audience_definition = audience_definition
    response: GenerateSuggestedTargetingInsightsResponse = (
        audience_insights_service.generate_suggested_targeting_insights(
            request=request
        )
    )
    print(response)
    # [END targeted_insights]


# [START insights_attributes]
def list_audience_insights_attributes(
    client: GoogleAdsClient,
    audience_insights_service: AudienceInsightsServiceClient,
    customer_id: str,
    product_name: str,
    custom_name: str,
) -> None:
    """Searches for audience attributes that can be used to generate insights.

    Args:
        client: an initialized GoogleAdsClient instance.
        audience_insights_service: an initialized AudienceInsightsService
          instance.
        customer_id: The customer ID for the audience insights service.
        product_name: The brand/product for which insights are expected.
        custom_name: custom defined name.
    """
    request: ListAudienceInsightsAttributesRequest = client.get_type(
        "ListAudienceInsightsAttributesRequest"
    )

    request.customer_id = customer_id
    request.query_text = product_name
    category_dimension: (
        AudienceInsightsDimensionEnum.AudienceInsightsDimension
    ) = client.enums.AudienceInsightsDimensionEnum.CATEGORY
    kg_dimension: AudienceInsightsDimensionEnum.AudienceInsightsDimension = (
        client.enums.AudienceInsightsDimensionEnum.KNOWLEDGE_GRAPH
    )
    request.dimensions = [category_dimension, kg_dimension]
    request.customer_insights_group = custom_name
    response: ListAudienceInsightsAttributesResponse = (
        audience_insights_service.list_audience_insights_attributes(
            request=request
        )
    )
    for attribute in response.attributes:
        if (
            attribute.dimension
            == client.enums.AudienceInsightsDimensionEnum.KNOWLEDGE_GRAPH
        ):
            print(attribute.attribute.entity.knowledge_graph_machine_id)
            # [END insights_attributes]


if __name__ == "__main__":
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description="Create audience insights."
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
        "-n",
        "--custom_name",
        type=str,
        required=True,
        help="Custom name to identify audiences",
    )
    parser.add_argument
    args: argparse.Namespace = parser.parse_args()

    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    googleads_client: GoogleAdsClient = GoogleAdsClient.load_from_storage(
        version="v22"
    )

    try:
        main(googleads_client, args.customer_id, args.custom_name)
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
