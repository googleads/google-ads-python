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
"""This example creates a keyword plan.

Keyword plans can be reused for retrieving forecast metrics and historic
metrics.
"""


import argparse
import sys
import uuid

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException


# [START add_keyword_plan]
def main(client, customer_id):
    """Adds a keyword plan, campaign, ad group, etc. to the customer account.

    Also handles errors from the API and prints them.

    Args:
        client: An initialized instance of GoogleAdsClient
        customer_id: A str of the customer_id to use in requests.
    """
    _add_keyword_plan(client, customer_id)


def _add_keyword_plan(client, customer_id):
    """Adds a keyword plan, campaign, ad group, etc. to the customer account.

    Args:
        client: An initialized instance of GoogleAdsClient
        customer_id: A str of the customer_id to use in requests.

    Raises:
        GoogleAdsException: If an error is returned from the API.
    """
    keyword_plan = _create_keyword_plan(client, customer_id)
    keyword_plan_campaign = _create_keyword_plan_campaign(
        client, customer_id, keyword_plan
    )
    keyword_plan_ad_group = _create_keyword_plan_ad_group(
        client, customer_id, keyword_plan_campaign
    )
    _create_keyword_plan_ad_group_keywords(
        client, customer_id, keyword_plan_ad_group
    )
    _create_keyword_plan_negative_campaign_keywords(
        client, customer_id, keyword_plan_campaign
    )


def _create_keyword_plan(client, customer_id):
    """Adds a keyword plan to the given customer account.

    Args:
        client: An initialized instance of GoogleAdsClient
        customer_id: A str of the customer_id to use in requests.

    Returns:
        A str of the resource_name for the newly created keyword plan.

    Raises:
        GoogleAdsException: If an error is returned from the API.
    """
    keyword_plan_service = client.get_service("KeywordPlanService")
    operation = client.get_type("KeywordPlanOperation")
    keyword_plan = operation.create

    keyword_plan.name = f"Keyword plan for traffic estimate {uuid.uuid4()}"

    forecast_interval = client.get_type(
        "KeywordPlanForecastIntervalEnum"
    ).KeywordPlanForecastInterval.NEXT_QUARTER
    keyword_plan.forecast_period.date_interval = forecast_interval

    response = keyword_plan_service.mutate_keyword_plans(
        customer_id=customer_id, operations=[operation]
    )
    resource_name = response.results[0].resource_name

    print(f"Created keyword plan with resource name: {resource_name}")

    return resource_name


def _create_keyword_plan_campaign(client, customer_id, keyword_plan):
    """Adds a keyword plan campaign to the given keyword plan.

    Args:
        client: An initialized instance of GoogleAdsClient
        customer_id: A str of the customer_id to use in requests.
        keyword_plan: A str of the keyword plan resource_name this keyword plan
            campaign should be attributed to.create_keyword_plan.

    Returns:
        A str of the resource_name for the newly created keyword plan campaign.

    Raises:
        GoogleAdsException: If an error is returned from the API.
    """
    keyword_plan_campaign_service = client.get_service(
        "KeywordPlanCampaignService"
    )
    operation = client.get_type("KeywordPlanCampaignOperation")
    keyword_plan_campaign = operation.create

    keyword_plan_campaign.name = f"Keyword plan campaign {uuid.uuid4()}"
    keyword_plan_campaign.cpc_bid_micros = 1000000
    keyword_plan_campaign.keyword_plan = keyword_plan

    network = client.get_type(
        "KeywordPlanNetworkEnum"
    ).KeywordPlanNetwork.GOOGLE_SEARCH
    keyword_plan_campaign.keyword_plan_network = network

    geo_target = client.get_type("KeywordPlanGeoTarget")
    # Constant for U.S. Other geo target constants can be referenced here:
    # https://developers.google.com/google-ads/api/reference/data/geotargets
    geo_target.geo_target_constant = "geoTargetConstants/2840"
    keyword_plan_campaign.geo_targets.append(geo_target)

    # Constant for English
    language = "languageConstants/1000"
    keyword_plan_campaign.language_constants.append(language)

    response = keyword_plan_campaign_service.mutate_keyword_plan_campaigns(
        customer_id=customer_id, operations=[operation]
    )

    resource_name = response.results[0].resource_name

    print(f"Created keyword plan campaign with resource name: {resource_name}")

    return resource_name


def _create_keyword_plan_ad_group(client, customer_id, keyword_plan_campaign):
    """Adds a keyword plan ad group to the given keyword plan campaign.

    Args:
        client: An initialized instance of GoogleAdsClient
        customer_id: A str of the customer_id to use in requests.
        keyword_plan_campaign: A str of the keyword plan campaign resource_name
            this keyword plan ad group should be attributed to.

    Returns:
        A str of the resource_name for the newly created keyword plan ad group.

    Raises:
        GoogleAdsException: If an error is returned from the API.
    """
    operation = client.get_type("KeywordPlanAdGroupOperation")
    keyword_plan_ad_group = operation.create

    keyword_plan_ad_group.name = f"Keyword plan ad group {uuid.uuid4()}"
    keyword_plan_ad_group.cpc_bid_micros = 2500000
    keyword_plan_ad_group.keyword_plan_campaign = keyword_plan_campaign

    keyword_plan_ad_group_service = client.get_service(
        "KeywordPlanAdGroupService"
    )
    response = keyword_plan_ad_group_service.mutate_keyword_plan_ad_groups(
        customer_id=customer_id, operations=[operation]
    )

    resource_name = response.results[0].resource_name

    print(f"Created keyword plan ad group with resource name: {resource_name}")

    return resource_name


def _create_keyword_plan_ad_group_keywords(client, customer_id, plan_ad_group):
    """Adds keyword plan ad group keywords to the given keyword plan ad group.

    Args:
        client: An initialized instance of GoogleAdsClient
        customer_id: A str of the customer_id to use in requests.
        plan_ad_group: A str of the keyword plan ad group resource_name
            these keyword plan keywords should be attributed to.

    Raises:
        GoogleAdsException: If an error is returned from the API.
    """
    keyword_plan_ad_group_keyword_service = client.get_service(
        "KeywordPlanAdGroupKeywordService"
    )
    operation = client.get_type("KeywordPlanAdGroupKeywordOperation")
    operations = []

    operation = client.get_type("KeywordPlanAdGroupKeywordOperation")
    keyword_plan_ad_group_keyword1 = operation.create
    keyword_plan_ad_group_keyword1.text = "mars cruise"
    keyword_plan_ad_group_keyword1.cpc_bid_micros = 2000000
    keyword_plan_ad_group_keyword1.match_type = client.get_type(
        "KeywordMatchTypeEnum"
    ).KeywordMatchType.BROAD
    keyword_plan_ad_group_keyword1.keyword_plan_ad_group = plan_ad_group
    operations.append(operation)

    operation = client.get_type("KeywordPlanAdGroupKeywordOperation")
    keyword_plan_ad_group_keyword2 = operation.create
    keyword_plan_ad_group_keyword2.text = "cheap cruise"
    keyword_plan_ad_group_keyword2.cpc_bid_micros = 1500000
    keyword_plan_ad_group_keyword2.match_type = client.get_type(
        "KeywordMatchTypeEnum"
    ).KeywordMatchType.PHRASE
    keyword_plan_ad_group_keyword2.keyword_plan_ad_group = plan_ad_group
    operations.append(operation)

    operation = client.get_type("KeywordPlanAdGroupKeywordOperation")
    keyword_plan_ad_group_keyword3 = operation.create
    keyword_plan_ad_group_keyword3.text = "jupiter cruise"
    keyword_plan_ad_group_keyword3.cpc_bid_micros = 1990000
    keyword_plan_ad_group_keyword3.match_type = client.get_type(
        "KeywordMatchTypeEnum"
    ).KeywordMatchType.EXACT
    keyword_plan_ad_group_keyword3.keyword_plan_ad_group = plan_ad_group
    operations.append(operation)

    response = keyword_plan_ad_group_keyword_service.mutate_keyword_plan_ad_group_keywords(
        customer_id=customer_id, operations=operations
    )

    for result in response.results:
        print(
            "Created keyword plan ad group keyword with resource name: "
            f"{result.resource_name}"
        )


def _create_keyword_plan_negative_campaign_keywords(
    client, customer_id, plan_campaign
):
    """Adds a keyword plan negative campaign keyword to the given campaign.

    Args:
        client: An initialized instance of GoogleAdsClient
        customer_id: A str of the customer_id to use in requests.
        plan_campaign: A str of the keyword plan campaign resource_name
            this keyword plan negative keyword should be attributed to.

    Raises:
        GoogleAdsException: If an error is returned from the API.
    """
    keyword_plan_negative_keyword_service = client.get_service(
        "KeywordPlanCampaignKeywordService"
    )
    operation = client.get_type("KeywordPlanCampaignKeywordOperation")

    keyword_plan_campaign_keyword = operation.create
    keyword_plan_campaign_keyword.text = "moon walk"
    keyword_plan_campaign_keyword.match_type = client.get_type(
        "KeywordMatchTypeEnum"
    ).KeywordMatchType.BROAD
    keyword_plan_campaign_keyword.keyword_plan_campaign = plan_campaign
    keyword_plan_campaign_keyword.negative = True

    response = keyword_plan_negative_keyword_service.mutate_keyword_plan_campaign_keywords(
        customer_id=customer_id, operations=[operation]
    )

    print(
        "Created keyword plan campaign keyword with resource name: "
        f"{response.results[0].resource_name}"
    )
    # [END add_keyword_plan]


if __name__ == "__main__":
    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    googleads_client = GoogleAdsClient.load_from_storage(version="v8")

    parser = argparse.ArgumentParser(
        description="Creates a keyword plan for specified customer."
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
            f'Request with ID "{ex.request_id}" failed with status '
            f'"{ex.error.code().name}" and includes the following errors:'
        )
        for error in ex.failure.errors:
            print(f'	Error with message "{error.message}".')
            if error.location:
                for field_path_element in error.location.field_path_elements:
                    print(f"\t\tOn field: {field_path_element.field_name}")
        sys.exit(1)
