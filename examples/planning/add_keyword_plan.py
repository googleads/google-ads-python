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

from google.ads.google_ads.client import GoogleAdsClient
from google.ads.google_ads.errors import GoogleAdsException


def main(client, customer_id):
    """Adds a keyword plan, campaign, ad group, etc. to the customer account

    Also handles errors from the API and prints them.

    Args:
        client: An initialized instance of GoogleAdsClient
        customer_id: A str of the customer_id to use in requests.
    """
    try:
        add_keyword_plan(client, customer_id)
    except GoogleAdsException as ex:
        print('Request with ID "{}" failed with status "{}" and includes the '
              'following errors:'.format(ex.request_id, ex.error.code().name))
        for error in ex.failure.errors:
            print('\tError with message "{}".'.format(error.message))
            if error.location:
                for field_path_element in error.location.field_path_elements:
                    print('\t\tOn field: {}'.format(
                        field_path_element.field_name))
        sys.exit(1)


def add_keyword_plan(client, customer_id):
    """Adds a keyword plan, campaign, ad group, etc. to the customer account.

    Args:
        client: An initialized instance of GoogleAdsClient
        customer_id: A str of the customer_id to use in requests.

    Raises:
        GoogleAdsException: If an error is returned from the API.
    """
    keyword_plan = create_keyword_plan(client, customer_id)
    keyword_plan_campaign = create_keyword_plan_campaign(client, customer_id,
                                                         keyword_plan)
    keyword_plan_ad_group = create_keyword_plan_ad_group(client, customer_id,
                                                         keyword_plan_campaign)
    create_keyword_plan_keywords(client, customer_id, keyword_plan_ad_group)
    create_keyword_plan_negative_keywords(client, customer_id,
                                          keyword_plan_campaign)


def create_keyword_plan(client, customer_id):
    """Adds a keyword plan to the given customer account.

    Args:
        client: An initialized instance of GoogleAdsClient
        customer_id: A str of the customer_id to use in requests.

    Returns:
        A str of the resource_name for the newly created keyword plan.

    Raises:
        GoogleAdsException: If an error is returned from the API.
    """
    operation = client.get_type('KeywordPlanOperation', version='v3')
    keyword_plan = operation.create

    keyword_plan.name.value = ('Keyword plan for traffic estimate {}'.format(
        uuid.uuid4()))

    forecast_interval = client.get_type('KeywordPlanForecastIntervalEnum',
                                        version='v3').NEXT_QUARTER
    keyword_plan.forecast_period.date_interval = forecast_interval

    keyword_plan_service = client.get_service('KeywordPlanService',
                                              version='v3')
    response = keyword_plan_service.mutate_keyword_plans(customer_id,
                                                         [operation])
    resource_name = response.results[0].resource_name

    print('Created keyword plan with resource name: {}'.format(resource_name))

    return resource_name


def create_keyword_plan_campaign(client, customer_id, keyword_plan):
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
    operation = client.get_type('KeywordPlanCampaignOperation', version='v3')
    keyword_plan_campaign = operation.create

    keyword_plan_campaign.name.value = 'Keyword plan campaign {}'.format(
        uuid.uuid4())
    keyword_plan_campaign.cpc_bid_micros.value = 1000000
    keyword_plan_campaign.keyword_plan.value = keyword_plan

    keyword_plan_network = client.get_type('KeywordPlanNetworkEnum',
                                           version='v3')
    network = keyword_plan_network.GOOGLE_SEARCH
    keyword_plan_campaign.keyword_plan_network = network

    geo_target = client.get_type('KeywordPlanGeoTarget', version='v3')
    # Constant for U.S. Other geo target constants can be referenced here:
    # https://developers.google.com/adwords/api/docs/appendix/geotargeting
    geo_target.geo_target_constant.value = 'geoTargetConstants/2840'
    keyword_plan_campaign.geo_targets.extend([geo_target])

    language = client.get_type('StringValue', version='v3')
    # Constant for English
    language.value = 'languageConstants/1000'
    keyword_plan_campaign.language_constants.extend([language])

    keyword_plan_campaign_service = client.get_service(
        'KeywordPlanCampaignService', version='v3')
    response = keyword_plan_campaign_service.mutate_keyword_plan_campaigns(
        customer_id, [operation])

    resource_name = response.results[0].resource_name

    print('Created keyword plan campaign with resource name: {}'.format(
        resource_name))

    return resource_name


def create_keyword_plan_ad_group(client, customer_id, keyword_plan_campaign):
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
    operation = client.get_type('KeywordPlanAdGroupOperation', version='v3')
    keyword_plan_ad_group = operation.create

    keyword_plan_ad_group.name.value = 'Keyword plan ad group {}'.format(
        uuid.uuid4())
    keyword_plan_ad_group.cpc_bid_micros.value = 2500000
    keyword_plan_ad_group.keyword_plan_campaign.value = keyword_plan_campaign

    keyword_plan_ad_group_service = client.get_service(
        'KeywordPlanAdGroupService', version='v3')
    response = keyword_plan_ad_group_service.mutate_keyword_plan_ad_groups(
        customer_id, [operation])

    resource_name = response.results[0].resource_name

    print('Created keyword plan ad group with resource name: {}'.format(
        resource_name))

    return resource_name


def create_keyword_plan_keywords(client, customer_id, plan_ad_group):
    """Adds keyword plan keywords to the given keyword plan ad group.

    Args:
        client: An initialized instance of GoogleAdsClient
        customer_id: A str of the customer_id to use in requests.
        keyword_plan_ad_group: A str of the keyword plan ad group resource_name
            these keyword plan keywords should be attributed to.

    Raises:
        GoogleAdsException: If an error is returned from the API.
    """
    match_types = client.get_type('KeywordMatchTypeEnum', version='v3')

    keyword_plan_keyword1 = client.get_type('KeywordPlanKeyword', version='v3')
    keyword_plan_keyword1.text.value = 'mars cruise'
    keyword_plan_keyword1.cpc_bid_micros.value = 2000000
    keyword_plan_keyword1.match_type = match_types.BROAD
    keyword_plan_keyword1.keyword_plan_ad_group.value = plan_ad_group

    keyword_plan_keyword2 = client.get_type('KeywordPlanKeyword', version='v3')
    keyword_plan_keyword2.text.value = 'cheap cruise'
    keyword_plan_keyword2.cpc_bid_micros.value = 1500000
    keyword_plan_keyword2.match_type = match_types.PHRASE
    keyword_plan_keyword2.keyword_plan_ad_group.value = plan_ad_group

    keyword_plan_keyword3 = client.get_type('KeywordPlanKeyword', version='v3')
    keyword_plan_keyword3.text.value = 'jupiter cruise'
    keyword_plan_keyword3.cpc_bid_micros.value = 1990000
    keyword_plan_keyword3.match_type = match_types.EXACT
    keyword_plan_keyword3.keyword_plan_ad_group.value = plan_ad_group

    operations = []
    for keyword in [keyword_plan_keyword1,
                    keyword_plan_keyword2,
                    keyword_plan_keyword3]:
        operation = client.get_type('KeywordPlanKeywordOperation', version='v3')
        operation.create.CopyFrom(keyword)
        operations.append(operation)

    keyword_plan_keyword_service = client.get_service(
        'KeywordPlanKeywordService', version='v3')
    response = keyword_plan_keyword_service.mutate_keyword_plan_keywords(
        customer_id, operations)

    for result in response.results:
        print('Created keyword plan keyword with resource name: {}'.format(
            result.resource_name))


def create_keyword_plan_negative_keywords(client, customer_id, plan_campaign):
    """Adds a keyword plan negative keyword to the given keyword plan campaign.

    Args:
        client: An initialized instance of GoogleAdsClient
        customer_id: A str of the customer_id to use in requests.
        keyword_plan_campaign: A str of the keyword plan campaign resource_name
            this keyword plan negative keyword should be attributed to.

    Raises:
        GoogleAdsException: If an error is returned from the API.
    """
    match_types = client.get_type('KeywordMatchTypeEnum', version='v3')
    operation = client.get_type('KeywordPlanNegativeKeywordOperation',
                                version='v3')
    keyword_plan_negative_keyword = operation.create

    keyword_plan_negative_keyword.text.value = 'moon walk'
    keyword_plan_negative_keyword.match_type = match_types.BROAD
    keyword_plan_negative_keyword.keyword_plan_campaign.value = plan_campaign

    keyword_plan_negative_keyword_service = client.get_service(
        'KeywordPlanNegativeKeywordService', version='v3')
    response = (keyword_plan_negative_keyword_service
                    .mutate_keyword_plan_negative_keywords(
                        customer_id, [operation]))

    print('Created keyword plan negative keyword with resource name: {}'.format(
        response.results[0].resource_name))


if __name__ == '__main__':
    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    google_ads_client = GoogleAdsClient.load_from_storage()

    parser = argparse.ArgumentParser(
        description='Creates a keyword plan for specified customer.')
    # The following argument(s) should be provided to run the example.
    parser.add_argument('-c', '--customer_id', type=str,
                        required=True, help='The Google Ads customer ID.')
    args = parser.parse_args()

    main(google_ads_client, args.customer_id)
