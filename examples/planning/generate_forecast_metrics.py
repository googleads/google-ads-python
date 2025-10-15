#!/usr/bin/env python
# Copyright 2023 Google LLC
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
"""This example generates forecast metrics for keyword planning.

For more details see this guide:
https://developers.google.com/google-ads/api/docs/keyword-planning/generate-forecast-metrics
"""

import argparse
from datetime import datetime, timedelta
import sys

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
from google.ads.googleads.v22.common.types.criteria import (
    KeywordInfo,
)
from google.ads.googleads.v22.services.services.google_ads_service.client import (
    GoogleAdsServiceClient,
)
from google.ads.googleads.v22.services.services.keyword_plan_idea_service.client import (
    KeywordPlanIdeaServiceClient,
)
from google.ads.googleads.v22.services.types.keyword_plan_idea_service import (
    CampaignToForecast,
    CriterionBidModifier,
    ForecastAdGroup,
    BiddableKeyword,
    GenerateKeywordForecastMetricsRequest,
    GenerateKeywordForecastMetricsResponse,
)


# [START generate_forecast_metrics]
def main(client: GoogleAdsClient, customer_id: str):
    """The main method that creates all necessary entities for the example.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.
    """
    campaign_to_forecast: CampaignToForecast = create_campaign_to_forecast(
        client
    )
    generate_forecast_metrics(client, customer_id, campaign_to_forecast)


def create_campaign_to_forecast(client: GoogleAdsClient) -> CampaignToForecast:
    """Creates the campaign to forecast.

    A campaign to forecast lets you try out various configurations and keywords
    to find the best optimization for your future campaigns. Once you've found
    the best campaign configuration, create a serving campaign in your Google
    Ads account with similar values and keywords. For more details, see:
    https://support.google.com/google-ads/answer/3022575

    Args:
        client: an initialized GoogleAdsClient instance.

    Returns:
        An CampaignToForecast instance.
    """
    googleads_service: GoogleAdsServiceClient = client.get_service(
        "GoogleAdsService"
    )
    # Create a campaign to forecast.
    campaign_to_forecast: CampaignToForecast = client.get_type(
        "CampaignToForecast"
    )
    campaign_to_forecast.keyword_plan_network = (
        client.enums.KeywordPlanNetworkEnum.GOOGLE_SEARCH
    )

    # Set the bidding strategy.
    campaign_to_forecast.bidding_strategy.manual_cpc_bidding_strategy.max_cpc_bid_micros = (
        1000000
    )

    # For the list of geo target IDs, see:
    # https://developers.google.com/google-ads/api/reference/data/geotargets
    criterion_bid_modifier: CriterionBidModifier = client.get_type(
        "CriterionBidModifier"
    )
    # Geo target constant 2840 is for USA.
    criterion_bid_modifier.geo_target_constant = (
        googleads_service.geo_target_constant_path("2840")
    )
    campaign_to_forecast.geo_modifiers.append(criterion_bid_modifier)

    # For the list of language criteria IDs, see:
    # https://developers.google.com/google-ads/api/reference/data/codes-formats#languages
    # Language criteria 1000 is for English.
    campaign_to_forecast.language_constants.append(
        googleads_service.language_constant_path("1000")
    )

    # Create forecast ad groups based on themes such as creative relevance,
    # product category, or cost per click.
    forecast_ad_group: ForecastAdGroup = client.get_type("ForecastAdGroup")

    # Create and configure three BiddableKeyword instances.
    biddable_keyword_1: BiddableKeyword = client.get_type("BiddableKeyword")
    biddable_keyword_1.max_cpc_bid_micros = 2500000
    biddable_keyword_1.keyword.text = "mars cruise"
    biddable_keyword_1.keyword.match_type = (
        client.enums.KeywordMatchTypeEnum.BROAD
    )

    biddable_keyword_2: BiddableKeyword = client.get_type("BiddableKeyword")
    biddable_keyword_2.max_cpc_bid_micros = 1500000
    biddable_keyword_2.keyword.text = "cheap cruise"
    biddable_keyword_2.keyword.match_type = (
        client.enums.KeywordMatchTypeEnum.PHRASE
    )

    biddable_keyword_3: BiddableKeyword = client.get_type("BiddableKeyword")
    biddable_keyword_3.max_cpc_bid_micros = 1990000
    biddable_keyword_3.keyword.text = "cheap cruise"
    biddable_keyword_3.keyword.match_type = (
        client.enums.KeywordMatchTypeEnum.EXACT
    )

    # Add the biddable keywords to the forecast ad group.
    forecast_ad_group.biddable_keywords.extend(
        [biddable_keyword_1, biddable_keyword_2, biddable_keyword_3]
    )

    # Create and configure a negative keyword, then add it to the forecast ad
    # group.
    negative_keyword: KeywordInfo = client.get_type("KeywordInfo")
    negative_keyword.text = "moon walk"
    negative_keyword.match_type = client.enums.KeywordMatchTypeEnum.BROAD
    forecast_ad_group.negative_keywords.append(negative_keyword)

    campaign_to_forecast.ad_groups.append(forecast_ad_group)

    return campaign_to_forecast


def generate_forecast_metrics(
    client: GoogleAdsClient,
    customer_id: str,
    campaign_to_forecast: CampaignToForecast,
):
    """Generates forecast metrics and prints the results.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.
        campaign_to_forecast: a CampaignToForecast to generate metrics for.
    """
    keyword_plan_idea_service: KeywordPlanIdeaServiceClient = (
        client.get_service("KeywordPlanIdeaService")
    )
    request: GenerateKeywordForecastMetricsRequest = client.get_type(
        "GenerateKeywordForecastMetricsRequest"
    )
    request.customer_id = customer_id
    request.campaign = campaign_to_forecast
    # Set the forecast range. Repeat forecasts with different horizons to get a
    # holistic picture.
    # Set the forecast start date to tomorrow.
    tomorrow = datetime.now() + timedelta(days=1)
    request.forecast_period.start_date = tomorrow.strftime("%Y-%m-%d")
    # Set the forecast end date to 30 days from today.
    thirty_days_from_now = datetime.now() + timedelta(days=30)
    request.forecast_period.end_date = thirty_days_from_now.strftime("%Y-%m-%d")

    response: GenerateKeywordForecastMetricsResponse = (
        keyword_plan_idea_service.generate_keyword_forecast_metrics(
            request=request
        )
    )

    metrics = response.campaign_forecast_metrics
    print(f"Estimated daily clicks: {metrics.clicks}")
    print(f"Estimated daily impressions: {metrics.impressions}")
    print(f"Estimated daily average CPC: {metrics.average_cpc_micros}")
    # [END generate_forecast_metrics]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generates forecast metrics for keyword planning."
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
            f'Request with ID "{ex.request_id}" failed with status '
            f'"{ex.error.code().name}" and includes the following errors:'
        )
        for error in ex.failure.errors:
            print(f'Error with message "{error.message}".')
            if error.location:
                for field_path_element in error.location.field_path_elements:
                    print(f"\t\tOn field: {field_path_element.field_name}")
        sys.exit(1)
