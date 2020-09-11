#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
"""This example creates a search campaign with the help of Google Ads API only.

This code example is the last in a series of code examples that shows how to
create a Search campaign using the AdWords API, and then migrate it to the
Google Ads API one functionality at a time. See other examples in this directory
for code examples in various stages of migration.

This code example represents the final state, where all the functionality -
create a campaign budget, a Search campaign, ad groups, keywords and expanded
text ads have been migrated to using the Google Ads API. The AdWords API is not
used.
"""

import argparse
import datetime
import sys
import uuid

from google.ads.google_ads.client import GoogleAdsClient
from google.ads.google_ads.errors import GoogleAdsException

# Number of ads being added/updated in this code example.
NUMBER_OF_ADS = 5
# The list of keywords being added in this code example.
KEYWORDS_TO_ADD = ["mars cruise", "space hotel"]
PAGE_SIZE = 1000


def create_campaign_budget(client, customer_id):
    """Creates a new campaign budget and returns it.

    Args:
        client: A google.ads.google_ads.client.GoogleAdsClient instance.
        customer_id: (str) Customer ID associated with the account.

    Returns:
        An instance of google.ads.google_ads.v5.types.CampaignBudget for the
            newly created Budget.
    """
    campaign_service = client.get_service("CampaignBudgetService", version="v5")
    operation = client.get_type("CampaignBudgetOperation", version="v5")
    criterion = operation.create
    criterion.name = "Interplanetary Cruise Budget #{}".format(uuid.uuid4())
    criterion.delivery_method = client.get_type(
        "BudgetDeliveryMethodEnum", version="v5"
    ).STANDARD
    criterion.amount_micros = 500000
    response = campaign_service.mutate_campaign_budgets(
        customer_id, [operation]
    )
    campaign_budget_resource_name = response.results[0].resource_name
    new_campaign_budget = get_campaign_budget(
        client, customer_id, campaign_budget_resource_name
    )
    print("Added budget named {}".format(new_campaign_budget.name))
    return new_campaign_budget


def get_campaign_budget(client, customer_id, resource_name):
    """Retrieves a google.ads.google_ads.v5.types.CampaignBudget instance.

    Args:
        client: A google.ads.google_ads.client.GoogleAdsClient instance.
        customer_id: (str) Customer ID associated with the account.
        resource_name: (str) Resource name associated with the newly created
            campaign.

    Returns:
        An instance of google.ads.google_ads.v5.types.CampaignBudget for the
            newly created Budget.
    """
    ga_service = client.get_service("GoogleAdsService", version="v5")
    query = f"""
        SELECT
          campaign_budget.id,
          campaign_budget.name,
          campaign_budget.resource_name
        FROM campaign_budget
        WHERE campaign_budget.resource_name = '{resource_name}'"""

    response = ga_service.search(customer_id, query, PAGE_SIZE)
    budget = list(response)[0].campaign_budget
    return budget


def create_campaign(client, customer_id, campaign_budget):
    """Creates a new campaign and returns it.

    Args:
        client: A google.ads.google_ads.client.GoogleAdsClient instance.
        customer_id: (str) Customer ID associated with the account.
        campaign_budget: A google.ads.google_ads.v5.types.CampaignBudget
            instance.

    Returns:
        A google.ads.google_ads.client.GoogleAdsClient message class instance.
    """
    operation = client.get_type("CampaignOperation", version="v5")
    campaign = operation.create
    campaign_service = client.get_service("CampaignService", version="v5")
    campaign.name = "Interplanetary Cruise#{}".format(uuid.uuid4())
    campaign.advertising_channel_type = client.get_type(
        "AdvertisingChannelTypeEnum", version="v5"
    ).SEARCH
    # Recommendation: Set the campaign to PAUSED when creating it to stop the
    # ads from immediately serving. Set to ENABLED once you've added
    # targeting and the ads are ready to serve.
    campaign.status = client.get_type("CampaignStatusEnum", version="v5").PAUSED
    campaign.manual_cpc.enhanced_cpc_enabled = True
    campaign.campaign_budget = campaign_budget.resource_name
    campaign.network_settings.target_google_search = True
    campaign.network_settings.target_search_network = True
    campaign.network_settings.target_content_network = False
    campaign.network_settings.target_partner_search_network = False
    campaign.start_date = (
        datetime.datetime.now() + datetime.timedelta(1)
    ).strftime("%Y%m%d")
    campaign.end_date = (
        datetime.datetime.now() + datetime.timedelta(365)
    ).strftime("%Y%m%d")
    response = campaign_service.mutate_campaigns(customer_id, [operation])
    campaign_resource_name = response.results[0].resource_name
    new_campaign = get_campaign(client, customer_id, campaign_resource_name)
    print("Added campaign named {}".format(new_campaign.name))
    return new_campaign


def get_campaign(client, customer_id, campaign_resource_name):
    """Retrieves a google.ads.google_ads.v5.types.Campaign instance.

    Args:
        client: A google.ads.google_ads.client.GoogleAdsClient instance.
        customer_id: (str) Customer ID associated with the account.
        campaign_resource_name: (str) Resource name associated with the newly
            created campaign budget.

    Returns:
        A google.ads.google_ads.client.GoogleAdsClient message class instance.
    """
    ga_service = client.get_service("GoogleAdsService", version="v5")
    query = f"""
        SELECT campaign.id, campaign.name, campaign.resource_name
        FROM campaign
        WHERE campaign.resource_name = '{campaign_resource_name}'"""

    response = ga_service.search(customer_id, query, PAGE_SIZE)
    campaign = list(response)[0].campaign
    return campaign


def create_ad_group(client, customer_id, campaign):
    """Creates a new ad group and returns it.

    Args:
        client: A google.ads.google_ads.client.GoogleAdsClient instance.
        customer_id: (str) Customer ID associated with the account.
        campaign: A google.ads.google_ads.v5.types.Campaign instance.

    Returns:
        An instance of the google.ads.google_ads.v5.types.AdGroup message class
            of the newly created ad group.
    """
    operation = client.get_type("AdGroupOperation", version="v5")
    adgroup = operation.create
    adgroup_service = client.get_service("AdGroupService", version="v5")
    adgroup.name = "Earth to Mars Cruises #{}".format(uuid.uuid4())
    adgroup.campaign = campaign.resource_name
    adgroup.status = client.get_type("AdGroupStatusEnum", version="v5").ENABLED
    adgroup.type = client.get_type(
        "AdGroupTypeEnum", version="v5"
    ).SEARCH_STANDARD
    adgroup.cpc_bid_micros = 10000000
    response = adgroup_service.mutate_ad_groups(customer_id, [operation])
    ad_group_resource_name = response.results[0].resource_name
    ad_group = get_ad_group(client, customer_id, ad_group_resource_name)
    print("Added AdGroup named {}".format(ad_group.name))
    return ad_group


def get_ad_group(client, customer_id, ad_group_resource_name):
    """Retrieves a google.ads.google_ads.v5.types.AdGroup instance.

    Args:
        client: A google.ads.google_ads.client.GoogleAdsClient instance.
        customer_id: (str) Customer ID associated with the account.
        ad_group_resource_name: (str) Resource name associated with the newly
            created Ad group.

    Returns:
        An instance of the google.ads.google_ads.v5.types.AdGroup message class
            of the newly created ad group.
    """
    ga_service = client.get_service("GoogleAdsService", version="v5")
    query = f"""
        SELECT ad_group.id, ad_group.name, ad_group.resource_name
        FROM ad_group
        WHERE ad_group.resource_name = '{ad_group_resource_name}'"""

    response = ga_service.search(customer_id, query, PAGE_SIZE)
    ad_group = list(response)[0].ad_group
    return ad_group


def create_text_ads(client, customer_id, ad_group):
    """Creates new text ads in a given ad group.

    Args:
        client: A google.ads.google_ads.client.GoogleAdsClient instance.
        customer_id: (str) Customer ID associated with the account.
        ad_group: A google.ads.google_ads.v5.types.AdGroup instance.
    """
    operations = []
    for i in range(0, NUMBER_OF_ADS):
        operation = client.get_type("AdGroupAdOperation", version="v5")
        ad_group_operation = operation.create
        ad_group_operation.ad_group = ad_group.resource_name
        ad_group_operation.status = client.get_type(
            "AdGroupAdStatusEnum", version="v5"
        ).PAUSED
        ad_group_operation.ad.expanded_text_ad.headline_part1 = (
            f"Cruise to Mars #{str(uuid.uuid4())[:4]}"
        )
        ad_group_operation.ad.expanded_text_ad.headline_part2 = (
            "Best Space Cruise Line"
        )
        ad_group_operation.ad.expanded_text_ad.description = (
            "Buy your tickets now!"
        )
        ad_group_operation.ad.final_urls.append("http://www.example.com")
        operations.append(operation)

    adgroup_service = client.get_service("AdGroupAdService", version="v5")
    ad_group_ad_response = adgroup_service.mutate_ad_group_ads(
        customer_id, operations
    )
    new_ad_resource_names = []
    for i in range(NUMBER_OF_ADS):
        new_ad_resource_names.append(
            ad_group_ad_response.results[i].resource_name
        )

    new_ads = get_ads(client, customer_id, new_ad_resource_names)
    for i in range(len(new_ads)):
        print(
            "Created expanded text ad with ID {}, status {} and "
            "headline {}.{}".format(
                new_ads[i].ad.id,
                new_ads[i].status,
                new_ads[i].ad.expanded_text_ad.headline_part1,
                new_ads[i].ad.expanded_text_ad.headline_part2,
            )
        )


def get_ads(client, customer_id, new_ad_resource_names):
    """Retrieves a google.ads.google_ads.v5.types.AdGroupAd instance.

    Args:
        client: A google.ads.google_ads.client.GoogleAdsClient instanc  e.
        customer_id: (str) Customer ID associated with the account.
        new_ad_resource_names: (str) Resource name associated with the Ad group.

    Returns:
        An instance of the google.ads.google_ads.v5.types.AdGroupAd message
            class of the newly created ad group ad.
    """

    def formatter(given_string):
        """Assigns ' ' to names of resources.

        This produces a formatted string that can be used within an IN clause.
        Args:
            given_string: (str) The string to be formatted.
        Returns:
            The formatted string.
        """
        results = []
        for i in given_string:
            results.append(repr(i))
        return ",".join(results)

    resource_names = formatter(new_ad_resource_names)

    ga_service = client.get_service("GoogleAdsService", version="v5")
    query = f"""
        SELECT
          ad_group_ad.ad.id,
          ad_group_ad.ad.expanded_text_ad.headline_part1,
          ad_group_ad.ad.expanded_text_ad.headline_part2,
          ad_group_ad.status, ad_group_ad.ad.final_urls,
          ad_group_ad.resource_name
        FROM ad_group_ad
        WHERE ad_group_ad.resource_name IN ({resource_names})"""

    response = ga_service.search(customer_id, query, PAGE_SIZE)
    response = iter(response)
    ads = []

    while response:
        try:
            current_row = next(response)
            ads.append(current_row.ad_group_ad)
        except StopIteration:
            break

    return ads


def create_keywords(client, customer_id, ad_group, keywords_to_add):
    """Creates new keywords on a given ad group.

    Args:
        client: A google.ads.google_ads.client.GoogleAdsClient instance.
        customer_id: (str) Customer ID associated with the account.
        ad_group: A google.ads.google_ads.v5.types.AdGroup instance.
        keywords_to_add: keywords_to_add: (list) A list of keywords which are to
            be added to a given ad group.
    """
    ad_group_criterion_operations = []
    for keyword in keywords_to_add:
        operation = client.get_type("AdGroupCriterionOperation", version="v5")
        ad_group_criterion_operation = operation.create
        ad_group_criterion_operation.ad_group = ad_group.resource_name
        ad_group_criterion_operation.status = client.get_type(
            "AdGroupCriterionStatusEnum", version="v5"
        ).ENABLED
        ad_group_criterion_operation.keyword.text = keyword
        ad_group_criterion_operation.keyword.match_type = client.get_type(
            "KeywordMatchTypeEnum", version="v5"
        ).EXACT
        ad_group_criterion_operations.append(operation)

    ad_group_criterion_service_client = client.get_service(
        "AdGroupCriterionService", version="v5"
    )
    ad_group_criterion_response = ad_group_criterion_service_client.mutate_ad_group_criteria(
        customer_id, ad_group_criterion_operations
    )
    new_ad_resource_names = []

    for i in range(len(keywords_to_add)):
        new_ad_resource_names.append(
            ad_group_criterion_response.results[i].resource_name
        )

    new_keywords = get_keywords(client, customer_id, new_ad_resource_names)
    for i in range(len(new_keywords)):
        print(
            "Keyword with text {}, id = {} and "
            "match type {} was created".format(
                new_keywords[i].keyword.text,
                new_keywords[i].criterion_id,
                new_keywords[i].keyword.match_type,
            )
        )


def get_keywords(client, customer_id, keyword_resource_names):
    """Retrieves a google.ads.google_ads.v5.types.AdGroupCriterion instance.

    Args:
        client: A google.ads.google_ads.client.GoogleAdsClient instance.
        customer_id: (str) Customer ID associated with the account.
        keyword_resource_names: (str) Resource name associated with the newly
            created ad group criterion.

    Returns:
        An instance of the google.ads.google_ads.v5.types.AdGroupCriterion
            message class of the newly created ad group criterion.
    """

    def formatter(given_string):
        """Assigns ' ' to names of resources.

        This produces a formatted string that can be used within an IN clause.
        Args:
            given_string: (str) The string to be formatted.
        Returns:
            The formatted string.
        """
        results = []
        for i in given_string:
            results.append(repr(i))
        return ",".join(results)

    resource_names = formatter(keyword_resource_names)
    ga_service = client.get_service("GoogleAdsService", version="v5")
    query = f"""
        SELECT
          ad_group.id,
          ad_group.status,
          ad_group_criterion.criterion_id,
          ad_group_criterion.keyword.text,
          ad_group_criterion.keyword.match_type
        FROM ad_group_criterion
        WHERE
          ad_group_criterion.type = 'KEYWORD'
          AND ad_group.status = 'ENABLED'
          AND ad_group_criterion.status IN ('ENABLED', 'PAUSED')
          AND ad_group_criterion.resource_name IN ({resource_names})"""

    response = ga_service.search(customer_id, query, PAGE_SIZE)
    response = iter(response)
    keywords = []

    while True:
        try:
            current_row = next(response)
            keywords.append(current_row.ad_group_criterion)
        except StopIteration:
            break

    return keywords


if __name__ == "__main__":
    # Initialize client object.
    # It will read the config file. The default file path is the Home Directory.
    google_ads_client = GoogleAdsClient.load_from_storage()

    parser = argparse.ArgumentParser(
        description="Lists all campaigns for specified customer."
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
        budget = create_campaign_budget(google_ads_client, args.customer_id)
        campaign = create_campaign(google_ads_client, args.customer_id, budget)
        ad_group = create_ad_group(
            google_ads_client, args.customer_id, campaign
        )
        create_text_ads(google_ads_client, args.customer_id, ad_group)
        create_keywords(
            google_ads_client, args.customer_id, ad_group, KEYWORDS_TO_ADD
        )
    except GoogleAdsException as ex:
        print(
            f"Request with ID '{ex.request_id}' failed with status "
            f"'{ex.error.code().name}' and includes the following errors:"
        )
        for error in ex.failure.errors:
            print(f"\tError with message '{error.message}'.")
            if error.location:
                for field_path_element in error.location.field_path_elements:
                    print(f"\t\tOn field: {field_path_element.field_name}")
        sys.exit(1)
