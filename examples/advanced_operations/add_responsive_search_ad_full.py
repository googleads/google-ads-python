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
"""
This example shows how to create a complete Responsive Search ad.

Includes creation of: budget, campaign, ad group, ad group ad,
keywords, and geo targeting.

More details on Responsive Search ads can be found here:
https://support.google.com/google-ads/answer/7684791
"""

import argparse
import sys
import uuid
from typing import List, Optional

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
from google.ads.googleads.v22.common.types.ad_asset import AdTextAsset
from google.ads.googleads.v22.enums.types.served_asset_field_type import (
    ServedAssetFieldTypeEnum,
)
from google.ads.googleads.v22.resources.types.ad_group import AdGroup
from google.ads.googleads.v22.resources.types.ad_group_ad import AdGroupAd
from google.ads.googleads.v22.resources.types.ad_group_criterion import (
    AdGroupCriterion,
)
from google.ads.googleads.v22.resources.types.campaign import Campaign
from google.ads.googleads.v22.resources.types.campaign_budget import (
    CampaignBudget,
)
from google.ads.googleads.v22.resources.types.campaign_criterion import (
    CampaignCriterion,
)
from google.ads.googleads.v22.resources.types.customer_customizer import (
    CustomerCustomizer,
)
from google.ads.googleads.v22.resources.types.customizer_attribute import (
    CustomizerAttribute,
)
from google.ads.googleads.v22.services.services.ad_group_ad_service import (
    AdGroupAdServiceClient,
)
from google.ads.googleads.v22.services.services.ad_group_criterion_service import (
    AdGroupCriterionServiceClient,
)
from google.ads.googleads.v22.services.services.ad_group_service import (
    AdGroupServiceClient,
)
from google.ads.googleads.v22.services.services.campaign_budget_service import (
    CampaignBudgetServiceClient,
)
from google.ads.googleads.v22.services.services.campaign_criterion_service import (
    CampaignCriterionServiceClient,
)
from google.ads.googleads.v22.services.services.campaign_service import (
    CampaignServiceClient,
)
from google.ads.googleads.v22.services.services.customer_customizer_service import (
    CustomerCustomizerServiceClient,
)
from google.ads.googleads.v22.services.services.customizer_attribute_service import (
    CustomizerAttributeServiceClient,
)
from google.ads.googleads.v22.services.services.geo_target_constant_service import (
    GeoTargetConstantServiceClient,
)
from google.ads.googleads.v22.services.types.geo_target_constant_service import (
    SuggestGeoTargetConstantsRequest,
    SuggestGeoTargetConstantsResponse,
)
from google.ads.googleads.v22.services.types.ad_group_ad_service import (
    AdGroupAdOperation,
    MutateAdGroupAdsResponse,
)
from google.ads.googleads.v22.services.types.ad_group_criterion_service import (
    AdGroupCriterionOperation,
    MutateAdGroupCriteriaResponse,
)
from google.ads.googleads.v22.services.types.ad_group_service import (
    AdGroupOperation,
    MutateAdGroupsResponse,
)
from google.ads.googleads.v22.services.types.campaign_budget_service import (
    CampaignBudgetOperation,
    MutateCampaignBudgetsResponse,
)
from google.ads.googleads.v22.services.types.campaign_criterion_service import (
    CampaignCriterionOperation,
    MutateCampaignCriteriaResponse,
)
from google.ads.googleads.v22.services.types.campaign_service import (
    CampaignOperation,
    MutateCampaignsResponse,
)
from google.ads.googleads.v22.services.types.customer_customizer_service import (
    CustomerCustomizerOperation,
    MutateCustomerCustomizersResponse,
)
from google.ads.googleads.v22.services.types.customizer_attribute_service import (
    CustomizerAttributeOperation,
    MutateCustomizerAttributesResponse,
)

# Keywords from user.
KEYWORD_TEXT_EXACT = "example of exact match"
KEYWORD_TEXT_PHRASE = "example of phrase match"
KEYWORD_TEXT_BROAD = "example of broad match"

# Geo targeting from user.
GEO_LOCATION_1 = "Buenos aires"
GEO_LOCATION_2 = "San Isidro"
GEO_LOCATION_3 = "Mar del Plata"

# LOCALE and COUNTRY_CODE are used for geo targeting.
# LOCALE is using ISO 639-1 format. If an invalid LOCALE is given,
# 'es' is used by default.
LOCALE = "es"

# A list of country codes can be referenced here:
# https://developers.google.com/google-ads/api/reference/data/geotargets
COUNTRY_CODE = "AR"


def main(
    client: GoogleAdsClient,
    customer_id: str,
    customizer_attribute_name: Optional[str] = None,
) -> None:
    """
    The main method that creates all necessary entities for the example.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.
        customizer_attribute_name: The name of the customizer attribute to be
            created
    """
    if customizer_attribute_name:
        customizer_attribute_resource_name: str = create_customizer_attribute(
            client, customer_id, customizer_attribute_name
        )

        link_customizer_attribute_to_customer(
            client, customer_id, customizer_attribute_resource_name
        )

    # Create a budget, which can be shared by multiple campaigns.
    campaign_budget: str = create_campaign_budget(client, customer_id)

    campaign_resource_name: str = create_campaign(
        client, customer_id, campaign_budget
    )

    ad_group_resource_name: str = create_ad_group(
        client, customer_id, campaign_resource_name
    )

    create_ad_group_ad(
        client, customer_id, ad_group_resource_name, customizer_attribute_name
    )

    add_keywords(client, customer_id, ad_group_resource_name)

    add_geo_targeting(client, customer_id, campaign_resource_name)


def create_customizer_attribute(
    client: GoogleAdsClient, customer_id: str, customizer_attribute_name: str
) -> str:
    """Creates a customizer attribute with the given customizer attribute name.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.
        customizer_attribute_name: the name for the customizer attribute.

    Returns:
        A resource name for a customizer attribute.
    """
    # Create a customizer attribute operation for creating a customizer
    # attribute.
    operation: CustomizerAttributeOperation = client.get_type(
        "CustomizerAttributeOperation"
    )
    # Create a customizer attribute with the specified name.
    customizer_attribute: CustomizerAttribute = operation.create
    customizer_attribute.name = customizer_attribute_name
    # Specify the type to be 'PRICE' so that we can dynamically customize the
    # part of the ad's description that is a price of a product/service we
    # advertise.
    customizer_attribute.type_ = client.enums.CustomizerAttributeTypeEnum.PRICE

    # Issue a mutate request to add the customizer attribute and prints its
    # information.
    customizer_attribute_service: CustomizerAttributeServiceClient = (
        client.get_service("CustomizerAttributeService")
    )
    response: MutateCustomizerAttributesResponse = (
        customizer_attribute_service.mutate_customizer_attributes(
            customer_id=customer_id, operations=[operation]
        )
    )
    resource_name: str = response.results[0].resource_name

    print(f"Added a customizer attribute with resource name: '{resource_name}'")

    return resource_name


def link_customizer_attribute_to_customer(
    client: GoogleAdsClient,
    customer_id: str,
    customizer_attribute_resource_name: str,
) -> None:
    """Links the customizer attribute to the customer.

    Args:
        client: an initialized GoogleAdsClient instance.
            customer_id: a client customer ID.
        customizer_attribute_resource_name: a resource name for  customizer
            attribute.
    """
    # Create a customer customizer operation.
    operation: CustomerCustomizerOperation = client.get_type(
        "CustomerCustomizerOperation"
    )
    # Create a customer customizer with the value to be used in the responsive
    # search ad.
    customer_customizer: CustomerCustomizer = operation.create
    customer_customizer.customizer_attribute = (
        customizer_attribute_resource_name
    )
    customer_customizer.value.type_ = (
        client.enums.CustomizerAttributeTypeEnum.PRICE
    )
    # The ad customizer will dynamically replace the placeholder with this value
    # when the ad serves.
    customer_customizer.value.string_value = "100USD"

    customer_customizer_service: CustomerCustomizerServiceClient = (
        client.get_service("CustomerCustomizerService")
    )
    # Issue a mutate request to create the customer customizer and prints its
    # information.
    response: MutateCustomerCustomizersResponse = (
        customer_customizer_service.mutate_customer_customizers(
            customer_id=customer_id, operations=[operation]
        )
    )
    resource_name: str = response.results[0].resource_name

    print(
        f"Added a customer customizer to the customer with resource name: '{resource_name}'"
    )


def create_ad_text_asset(
    client: GoogleAdsClient,
    text: str,
    pinned_field: Optional[
        ServedAssetFieldTypeEnum.ServedAssetFieldType
    ] = None,
) -> AdTextAsset:
    """Create an AdTextAsset.

    Args:
        client: an initialized GoogleAdsClient instance.
        text: text for headlines and descriptions.
        pinned_field: to pin a text asset so it always shows in the ad.

    Returns:
        An AdTextAsset.
    """
    ad_text_asset: AdTextAsset = client.get_type("AdTextAsset")
    ad_text_asset.text = text
    if pinned_field:
        ad_text_asset.pinned_field = pinned_field
    return ad_text_asset


def create_ad_text_asset_with_customizer(
    client: GoogleAdsClient, customizer_attribute_resource_name: str
) -> AdTextAsset:
    """Create an AdTextAsset.
    Args:
        client: an initialized GoogleAdsClient instance.
        customizer_attribute_resource_name: The resource name of the customizer attribute.

    Returns:
        An AdTextAsset.
    """
    ad_text_asset: AdTextAsset = client.get_type("AdTextAsset")

    # Create this particular description using the ad customizer. Visit
    # https://developers.google.com/google-ads/api/docs/ads/customize-responsive-search-ads#ad_customizers_in_responsive_search_ads
    # for details about the placeholder format. The ad customizer replaces the
    # placeholder with the value we previously created and linked to the
    # customer using CustomerCustomizer.
    ad_text_asset.text = (
        f"Just {{CUSTOMIZER.{customizer_attribute_resource_name}:10USD}}"
    )

    return ad_text_asset


def create_campaign_budget(client: GoogleAdsClient, customer_id: str) -> str:
    """Creates campaign budget resource.

    Args:
      client: an initialized GoogleAdsClient instance.
      customer_id: a client customer ID.

    Returns:
      Campaign budget resource name.
    """
    # Create a budget, which can be shared by multiple campaigns.
    campaign_budget_service: CampaignBudgetServiceClient = client.get_service(
        "CampaignBudgetService"
    )
    campaign_budget_operation: CampaignBudgetOperation = client.get_type(
        "CampaignBudgetOperation"
    )
    campaign_budget: CampaignBudget = campaign_budget_operation.create
    campaign_budget.name = f"Campaign budget {uuid.uuid4()}"
    campaign_budget.delivery_method = (
        client.enums.BudgetDeliveryMethodEnum.STANDARD
    )
    campaign_budget.amount_micros = 500000

    # Add budget.
    campaign_budget_response: MutateCampaignBudgetsResponse = (
        campaign_budget_service.mutate_campaign_budgets(
            customer_id=customer_id, operations=[campaign_budget_operation]
        )
    )

    return campaign_budget_response.results[0].resource_name


def create_campaign(
    client: GoogleAdsClient, customer_id: str, campaign_budget: str
) -> str:
    """Creates campaign resource.

    Args:
      client: an initialized GoogleAdsClient instance.
      customer_id: a client customer ID.
      campaign_budget: a budget resource name.

    Returns:
      Campaign resource name.
    """
    campaign_service: CampaignServiceClient = client.get_service(
        "CampaignService"
    )
    campaign_operation: CampaignOperation = client.get_type("CampaignOperation")
    campaign: Campaign = campaign_operation.create
    campaign.name = f"Testing RSA via API {uuid.uuid4()}"
    campaign.advertising_channel_type = (
        client.enums.AdvertisingChannelTypeEnum.SEARCH
    )

    # Recommendation: Set the campaign to PAUSED when creating it to prevent
    # the ads from immediately serving. Set to ENABLED once you've added
    # targeting and the ads are ready to serve.
    campaign.status = client.enums.CampaignStatusEnum.PAUSED

    # Set the bidding strategy and budget.
    # The bidding strategy for Maximize Clicks is TargetSpend.
    # The target_spend_micros is deprecated so don't put any value.
    # See other bidding strategies you can select in the link below.
    # https://developers.google.com/google-ads/api/reference/rpc/latest/Campaign#campaign_bidding_strategy
    campaign.target_spend.target_spend_micros = 0
    campaign.campaign_budget = campaign_budget

    # Set the campaign network options.
    campaign.network_settings.target_google_search = True
    campaign.network_settings.target_search_network = True
    campaign.network_settings.target_partner_search_network = False
    # Enable Display Expansion on Search campaigns. For more details see:
    # https://support.google.com/google-ads/answer/7193800
    campaign.network_settings.target_content_network = True

    # # Optional: Set the start date.
    # start_time = datetime.date.today() + datetime.timedelta(days=1)
    # campaign.start_date = datetime.date.strftime(start_time, _DATE_FORMAT)

    # # Optional: Set the end date.
    # end_time = start_time + datetime.timedelta(weeks=4)
    # campaign.end_date = datetime.date.strftime(end_time, _DATE_FORMAT)

    # Add the campaign.
    campaign_response: MutateCampaignsResponse = (
        campaign_service.mutate_campaigns(
            customer_id=customer_id, operations=[campaign_operation]
        )
    )
    resource_name: str = campaign_response.results[0].resource_name
    print(f"Created campaign {resource_name}.")
    return resource_name


def create_ad_group(
    client: GoogleAdsClient,
    customer_id: str,
    campaign_resource_name: str,
) -> str:
    """Creates ad group.

    Args:
      client: an initialized GoogleAdsClient instance.
      customer_id: a client customer ID.
      campaign_resource_name: a campaign resource name.

    Returns:
      Ad group ID.
    """
    ad_group_service: AdGroupServiceClient = client.get_service(
        "AdGroupService"
    )

    ad_group_operation: AdGroupOperation = client.get_type("AdGroupOperation")
    ad_group: AdGroup = ad_group_operation.create
    ad_group.name = f"Testing RSA via API {uuid.uuid4()}"
    ad_group.status = client.enums.AdGroupStatusEnum.ENABLED
    ad_group.campaign = campaign_resource_name
    ad_group.type_ = client.enums.AdGroupTypeEnum.SEARCH_STANDARD

    # If you want to set up a max CPC bid uncomment line below.
    # ad_group.cpc_bid_micros = 10000000

    # Add the ad group.
    ad_group_response: MutateAdGroupsResponse = (
        ad_group_service.mutate_ad_groups(
            customer_id=customer_id, operations=[ad_group_operation]
        )
    )
    ad_group_resource_name: str = ad_group_response.results[0].resource_name
    print(f"Created ad group {ad_group_resource_name}.")
    return ad_group_resource_name


def create_ad_group_ad(
    client: GoogleAdsClient,
    customer_id: str,
    ad_group_resource_name: str,
    customizer_attribute_name: Optional[str],
) -> None:
    """Creates ad group ad.

    Args:
      client: an initialized GoogleAdsClient instance.
      customer_id: a client customer ID.
      ad_group_resource_name: an ad group resource name.
      customizer_attribute_name: (optional) If present, indicates the resource
        name of the customizer attribute to use in one of the descriptions

    Returns:
      None.
    """
    ad_group_ad_service: AdGroupAdServiceClient = client.get_service(
        "AdGroupAdService"
    )

    ad_group_ad_operation: AdGroupAdOperation = client.get_type(
        "AdGroupAdOperation"
    )
    ad_group_ad: AdGroupAd = ad_group_ad_operation.create
    ad_group_ad.status = client.enums.AdGroupAdStatusEnum.ENABLED
    ad_group_ad.ad_group = ad_group_resource_name

    # Set responsive search ad info.
    # https://developers.google.com/google-ads/api/reference/rpc/latest/ResponsiveSearchAdInfo

    # The list of possible final URLs after all cross-domain redirects for the ad.
    ad_group_ad.ad.final_urls.append("https://www.example.com/")

    # Set a pinning to always choose this asset for HEADLINE_1. Pinning is
    # optional; if no pinning is set, then headlines and descriptions will be
    # rotated and the ones that perform best will be used more often.

    # Headline 1
    served_asset_enum: ServedAssetFieldTypeEnum = (
        client.enums.ServedAssetFieldTypeEnum
    )
    pinned_headline: AdTextAsset = create_ad_text_asset(
        client, "Headline 1 testing", served_asset_enum
    )

    # Headline 2 and 3
    ad_group_ad.ad.responsive_search_ad.headlines.extend(
        [
            pinned_headline,
            create_ad_text_asset(client, "Headline 2 testing"),
            create_ad_text_asset(client, "Headline 3 testing"),
        ]
    )

    # Description 1 and 2
    description_1: AdTextAsset = create_ad_text_asset(client, "Desc 1 testing")
    description_2: Optional[AdTextAsset] = None

    if customizer_attribute_name:
        description_2 = create_ad_text_asset_with_customizer(
            client, customizer_attribute_name
        )
    else:
        description_2 = create_ad_text_asset(client, "Desc 2 testing")

    ad_group_ad.ad.responsive_search_ad.descriptions.extend(
        [description_1, description_2]
    )

    # Paths
    # First and second part of text that can be appended to the URL in the ad.
    # If you use the examples below, the ad will show
    # https://www.example.com/all-inclusive/deals
    ad_group_ad.ad.responsive_search_ad.path1 = "all-inclusive"
    ad_group_ad.ad.responsive_search_ad.path2 = "deals"

    # Send a request to the server to add a responsive search ad.
    ad_group_ad_response: MutateAdGroupAdsResponse = (
        ad_group_ad_service.mutate_ad_group_ads(
            customer_id=customer_id, operations=[ad_group_ad_operation]
        )
    )

    for result in ad_group_ad_response.results:
        print(
            f"Created responsive search ad with resource name "
            f'"{result.resource_name}".'
        )


def add_keywords(
    client: GoogleAdsClient, customer_id: str, ad_group_resource_name: str
) -> None:
    """Creates keywords.

    Creates 3 keyword match types: EXACT, PHRASE, and BROAD.

    EXACT: ads may show on searches that ARE the same meaning as your keyword.
    PHRASE: ads may show on searches that INCLUDE the meaning of your keyword.
    BROAD: ads may show on searches that RELATE to your keyword.
    For smart bidding, BROAD is the recommended one.

    Args:
      client: an initialized GoogleAdsClient instance.
      customer_id: a client customer ID.
      ad_group_resource_name: an ad group resource name.
    """
    ad_group_criterion_service: AdGroupCriterionServiceClient = (
        client.get_service("AdGroupCriterionService")
    )

    operations: List[AdGroupCriterionOperation] = []
    # Create keyword 1.
    ad_group_criterion_operation: AdGroupCriterionOperation = client.get_type(
        "AdGroupCriterionOperation"
    )
    ad_group_criterion: AdGroupCriterion = ad_group_criterion_operation.create
    ad_group_criterion.ad_group = ad_group_resource_name
    ad_group_criterion.status = client.enums.AdGroupCriterionStatusEnum.ENABLED
    ad_group_criterion.keyword.text = KEYWORD_TEXT_EXACT
    ad_group_criterion.keyword.match_type = (
        client.enums.KeywordMatchTypeEnum.EXACT
    )

    # Uncomment the below line if you want to change this keyword to a negative target.
    # ad_group_criterion.negative = True

    # Optional repeated field
    # ad_group_criterion.final_urls.append('https://www.example.com')

    # Add operation
    operations.append(ad_group_criterion_operation)

    # Create keyword 2.
    ad_group_criterion_operation: AdGroupCriterionOperation = client.get_type(
        "AdGroupCriterionOperation"
    )
    ad_group_criterion: AdGroupCriterion = ad_group_criterion_operation.create
    ad_group_criterion.ad_group = ad_group_resource_name
    ad_group_criterion.status = client.enums.AdGroupCriterionStatusEnum.ENABLED
    ad_group_criterion.keyword.text = KEYWORD_TEXT_PHRASE
    ad_group_criterion.keyword.match_type = (
        client.enums.KeywordMatchTypeEnum.PHRASE
    )

    # Uncomment the below line if you want to change this keyword to a negative target.
    # ad_group_criterion.negative = True

    # Optional repeated field
    # ad_group_criterion.final_urls.append('https://www.example.com')

    # Add operation
    operations.append(ad_group_criterion_operation)

    # Create keyword 3.
    ad_group_criterion_operation: AdGroupCriterionOperation = client.get_type(
        "AdGroupCriterionOperation"
    )
    ad_group_criterion: AdGroupCriterion = ad_group_criterion_operation.create
    ad_group_criterion.ad_group = ad_group_resource_name
    ad_group_criterion.status = client.enums.AdGroupCriterionStatusEnum.ENABLED
    ad_group_criterion.keyword.text = KEYWORD_TEXT_BROAD
    ad_group_criterion.keyword.match_type = (
        client.enums.KeywordMatchTypeEnum.BROAD
    )

    # Uncomment the below line if you want to change this keyword to a negative target.
    # ad_group_criterion.negative = True

    # Optional repeated field
    # ad_group_criterion.final_urls.append('https://www.example.com')

    # Add operation
    operations.append(ad_group_criterion_operation)

    # Add keywords
    ad_group_criterion_response: MutateAdGroupCriteriaResponse = (
        ad_group_criterion_service.mutate_ad_group_criteria(
            customer_id=customer_id,
            operations=operations,
        )
    )
    for result in ad_group_criterion_response.results:
        print("Created keyword " f"{result.resource_name}.")


def add_geo_targeting(
    client: GoogleAdsClient, customer_id: str, campaign_resource_name: str
) -> None:
    """Creates geo targets.

    Args:
      client: an initialized GoogleAdsClient instance.
      customer_id: a client customer ID.
      campaign_resource_name: an campaign resource name.

    Returns:
      None.
    """
    geo_target_constant_service: GeoTargetConstantServiceClient = (
        client.get_service("GeoTargetConstantService")
    )

    # Search by location names from
    # GeoTargetConstantService.suggest_geo_target_constants() and directly
    # apply GeoTargetConstant.resource_name.
    gtc_request: SuggestGeoTargetConstantsRequest = client.get_type(
        "SuggestGeoTargetConstantsRequest"
    )
    gtc_request.locale = LOCALE
    gtc_request.country_code = COUNTRY_CODE

    # The location names to get suggested geo target constants.
    gtc_request.location_names.names.extend(
        [GEO_LOCATION_1, GEO_LOCATION_2, GEO_LOCATION_3]
    )

    results: SuggestGeoTargetConstantsResponse = (
        geo_target_constant_service.suggest_geo_target_constants(gtc_request)
    )

    operations: List[CampaignCriterionOperation] = []
    for suggestion in results.geo_target_constant_suggestions:
        print(
            "geo_target_constant: "
            f"{suggestion.geo_target_constant.resource_name} "
            f"is found in LOCALE ({suggestion.locale}) "
            f"with reach ({suggestion.reach}) "
            f"from search term ({suggestion.search_term})."
        )
        # Create the campaign criterion for location targeting.
        campaign_criterion_operation: CampaignCriterionOperation = (
            client.get_type("CampaignCriterionOperation")
        )
        campaign_criterion: CampaignCriterion = (
            campaign_criterion_operation.create
        )
        campaign_criterion.campaign = campaign_resource_name
        campaign_criterion.location.geo_target_constant = (
            suggestion.geo_target_constant.resource_name
        )
        operations.append(campaign_criterion_operation)

    campaign_criterion_service: CampaignCriterionServiceClient = (
        client.get_service("CampaignCriterionService")
    )
    campaign_criterion_response: MutateCampaignCriteriaResponse = (
        campaign_criterion_service.mutate_campaign_criteria(
            customer_id=customer_id, operations=[*operations]
        )
    )

    for result in campaign_criterion_response.results:
        print(f'Added campaign criterion "{result.resource_name}".')


if __name__ == "__main__":
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description=("Creates a Responsive Search Ad for specified customer.")
    )
    # The following argument(s) should be provided to run the example.
    parser.add_argument(
        "-c",
        "--customer_id",
        type=str,
        required=True,
        help="The Google Ads customer ID.",
    )

    # The name of the customizer attribute used in the ad customizer, which
    # must be unique for a given customer account. To run this example multiple
    # times, specify a unique value as a command line argument. Note that there is
    # a limit for the number of enabled customizer attributes in one account
    # For more details visit:
    # https://developers.google.com/google-ads/api/docs/ads/customize-responsive-search-ads#rules_and_limitations
    parser.add_argument(
        "-n",
        "--customizer_attribute_name",
        type=str,
        default=None,
        help=(
            "The name of the customizer attribute to be created. The name must "
            "be unique across a client account, so be sure not to use "
            "the same value more than once."
        ),
    )

    args: argparse.Namespace = parser.parse_args()

    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    googleads_client: GoogleAdsClient = GoogleAdsClient.load_from_storage(
        version="v22"
    )

    try:
        main(
            googleads_client,
            args.customer_id,
            args.customizer_attribute_name,
        )
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
