#!/usr/bin/env python
# Copyright 2021 Google LLC
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
"""This example shows how to create a Smart campaign.

More details on Smart campaigns can be found here:
https://support.google.com/google-ads/answer/7652860
"""

import argparse
import sys
from typing import List, Optional
from uuid import uuid4

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
from google.ads.googleads.v22.common.types.ad_asset import AdTextAsset
from google.ads.googleads.v22.common.types.ad_type_infos import (
    SmartCampaignAdInfo,
)
from google.ads.googleads.v22.common.types.criteria import (
    AdScheduleInfo,
    KeywordThemeInfo,
    LocationInfo,
)
from google.ads.googleads.v22.resources.types.ad_group import AdGroup
from google.ads.googleads.v22.resources.types.ad_group_ad import AdGroupAd
from google.ads.googleads.v22.resources.types.campaign import Campaign
from google.ads.googleads.v22.resources.types.campaign_budget import (
    CampaignBudget,
)
from google.ads.googleads.v22.resources.types.campaign_criterion import (
    CampaignCriterion,
)
from google.ads.googleads.v22.resources.types.keyword_theme_constant import (
    KeywordThemeConstant,
)
from google.ads.googleads.v22.resources.types.smart_campaign_setting import (
    SmartCampaignSetting,
)
from google.ads.googleads.v22.services.types.ad_group_ad_service import (
    AdGroupAdOperation,
)
from google.ads.googleads.v22.services.types.ad_group_service import (
    AdGroupOperation,
)
from google.ads.googleads.v22.services.types.campaign_budget_service import (
    CampaignBudgetOperation,
)
from google.ads.googleads.v22.services.types.campaign_criterion_service import (
    CampaignCriterionOperation,
)
from google.ads.googleads.v22.services.services.campaign_service import (
    CampaignServiceClient,
)
from google.ads.googleads.v22.enums.types.minute_of_hour import (
    MinuteOfHourEnum,
)
from google.ads.googleads.v22.services.types.campaign_service import (
    CampaignOperation,
)
from google.ads.googleads.v22.services.services.google_ads_service import (
    GoogleAdsServiceClient,
)
from google.ads.googleads.v22.services.types.google_ads_service import (
    MutateGoogleAdsResponse,
    MutateOperation,
    MutateOperationResponse,
)
from google.ads.googleads.v22.services.services.keyword_theme_constant_service import (
    KeywordThemeConstantServiceClient,
)
from google.ads.googleads.v22.services.types.keyword_theme_constant_service import (
    SuggestKeywordThemeConstantsRequest,
    SuggestKeywordThemeConstantsResponse,
)
from google.ads.googleads.v22.services.services.smart_campaign_suggest_service import (
    SmartCampaignSuggestServiceClient,
)
from google.ads.googleads.v22.services.types.smart_campaign_suggest_service import (
    SmartCampaignSuggestionInfo,
    SuggestKeywordThemesResponse,
    SuggestKeywordThemesRequest,
    SuggestSmartCampaignAdResponse,
    SuggestSmartCampaignAdRequest,
    SuggestSmartCampaignBudgetOptionsResponse,
    SuggestSmartCampaignBudgetOptionsRequest,
)
from google.ads.googleads.v22.services.types.smart_campaign_setting_service import (
    SmartCampaignSettingOperation,
)
from google.api_core import protobuf_helpers

# Geo target constant for New York City.
_GEO_TARGET_CONSTANT = "1023191"
# Country code is a two-letter ISO-3166 code, for a list of all codes see:
# https://developers.google.com/google-ads/api/reference/data/codes-formats#expandable-16
_COUNTRY_CODE = "US"
# For a list of all language codes, see:
# https://developers.google.com/google-ads/api/reference/data/codes-formats#expandable-7
_LANGUAGE_CODE = "en"
_LANDING_PAGE_URL = "http://www.example.com"
_PHONE_NUMBER = "800-555-0100"
_BUDGET_TEMPORARY_ID = "-1"
_SMART_CAMPAIGN_TEMPORARY_ID = "-2"
_AD_GROUP_TEMPORARY_ID = "-3"
# These define the minimum number of headlines and descriptions that are
# required to create an AdGroupAd in a Smart campaign.
_REQUIRED_NUM_HEADLINES = 3
_REQUIRED_NUM_DESCRIPTIONS = 2


def main(
    client: GoogleAdsClient,
    customer_id: str,
    keyword_text: Optional[str],
    free_form_keyword_text: Optional[str],
    business_profile_location: Optional[str],
    business_name: Optional[str],
) -> None:
    """The main method that creates all necessary entities for the example.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.
        keyword_text: a keyword used for generating keyword themes.
        free_form_keyword_text: a keyword used to create a free-form keyword
          theme.
        business_profile_location: the ID of a Business Profile location.
        business_name: the name of a Business Profile.
    """
    # [START add_smart_campaign_12]
    # The SmartCampaignSuggestionInfo object acts as the basis for many of the
    # entities necessary to create a Smart campaign. It will be reused a number
    # of times to retrieve suggestions for keyword themes, budget amount,
    # ad creatives, and campaign criteria.
    suggestion_info: SmartCampaignSuggestionInfo = (
        get_smart_campaign_suggestion_info(
            client, business_profile_location, business_name
        )
    )

    # After creating a SmartCampaignSuggestionInfo object we first use it to
    # generate a list of keyword themes using the SuggestKeywordThemes method
    # on the SmartCampaignSuggestService. It is strongly recommended that you
    # use this strategy for generating keyword themes.
    keyword_themes: List[SuggestKeywordThemesResponse.KeywordTheme] = (
        get_keyword_theme_suggestions(client, customer_id, suggestion_info)
    )

    # If a keyword text is given, retrieve keyword theme constant suggestions
    # from the KeywordThemeConstantService, map them to KeywordThemes, and
    # append them to the existing list. This logic should ideally only be used
    # if the suggestions from the get_keyword_theme_suggestions function are
    # insufficient.
    if keyword_text:
        keyword_themes.extend(
            get_keyword_text_auto_completions(client, keyword_text)
        )

    # Map the KeywordThemes retrieved by the previous two steps to
    # KeywordThemeInfo instances.
    keyword_theme_infos: List[KeywordThemeInfo] = (
        map_keyword_themes_to_keyword_infos(client, keyword_themes)
    )

    # If a free-form keyword text is given we create a KeywordThemeInfo instance
    # from it and add it to the existing list.
    if free_form_keyword_text:
        keyword_theme_infos.append(
            get_free_form_keyword_theme_info(client, free_form_keyword_text)
        )

    # Now add the generated keyword themes to the suggestion info instance.
    suggestion_info.keyword_themes.extend(keyword_theme_infos)
    # [END add_smart_campaign_12]

    # Retrieve a budget amount suggestion.
    suggested_budget_amount: int = get_budget_suggestion(
        client, customer_id, suggestion_info
    )

    # Retrieve Smart campaign ad creative suggestions.
    ad_suggestions: SmartCampaignAdInfo = get_ad_suggestions(
        client, customer_id, suggestion_info
    )

    # [START add_smart_campaign_7]
    # The below methods create and return MutateOperations that we later
    # provide to the GoogleAdsService.Mutate method in order to create the
    # entities in a single request. Since the entities for a Smart campaign
    # are closely tied to one-another it's considered a best practice to
    # create them in a single Mutate request so they all complete successfully
    # or fail entirely, leaving no orphaned entities. See:
    # https://developers.google.com/google-ads/api/docs/mutating/overview
    campaign_budget_operation: MutateOperation = (
        create_campaign_budget_operation(
            client, customer_id, suggested_budget_amount
        )
    )
    smart_campaign_operation: MutateOperation = create_smart_campaign_operation(
        client, customer_id
    )
    smart_campaign_setting_operation: MutateOperation = (
        create_smart_campaign_setting_operation(
            client, customer_id, business_profile_location, business_name
        )
    )
    campaign_criterion_operations: List[MutateOperation] = (
        create_campaign_criterion_operations(
            client, customer_id, keyword_theme_infos, suggestion_info
        )
    )
    ad_group_operation: MutateOperation = create_ad_group_operation(
        client, customer_id
    )
    ad_group_ad_operation: MutateOperation = create_ad_group_ad_operation(
        client, customer_id, ad_suggestions
    )

    googleads_service: GoogleAdsServiceClient = client.get_service(
        "GoogleAdsService"
    )

    # Send the operations into a single Mutate request.
    response: MutateGoogleAdsResponse = googleads_service.mutate(
        customer_id=customer_id,
        mutate_operations=[
            # It's important to create these entities in this order because
            # they depend on each other, for example the SmartCampaignSetting
            # and ad group depend on the campaign, and the ad group ad depends
            # on the ad group.
            campaign_budget_operation,
            smart_campaign_operation,
            smart_campaign_setting_operation,
            # Expand the list of campaign criterion operations into the list of
            # other mutate operations
            *campaign_criterion_operations,
            ad_group_operation,
            ad_group_ad_operation,
        ],
    )

    print_response_details(response)
    # [END add_smart_campaign_7]


# [START add_smart_campaign_11]
def get_keyword_theme_suggestions(
    client: GoogleAdsClient,
    customer_id: str,
    suggestion_info: SmartCampaignSuggestionInfo,
) -> List[SuggestKeywordThemesResponse.KeywordTheme]:
    """Retrieves KeywordThemes using the given suggestion info.

    Here we use the SuggestKeywordThemes method, which uses all of the business
    details included in the given SmartCampaignSuggestionInfo instance to
    generate keyword theme suggestions. This is the recommended way to
    generate keyword themes because it uses detailed information about your
    business, its location, and website content to generate keyword themes.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.
        suggestion_info: a SmartCampaignSuggestionInfo instance with details
          about the business being advertised.

    Returns:
        a list of KeywordThemes.
    """
    smart_campaign_suggest_service: SmartCampaignSuggestServiceClient = (
        client.get_service("SmartCampaignSuggestService")
    )
    request: SuggestKeywordThemesRequest = client.get_type(
        "SuggestKeywordThemesRequest"
    )
    request.customer_id = customer_id
    request.suggestion_info = suggestion_info

    response: SuggestKeywordThemesResponse = (
        smart_campaign_suggest_service.suggest_keyword_themes(request=request)
    )

    print(
        f"Retrieved {len(response.keyword_themes)} keyword theme suggestions "
        "from the SuggestKeywordThemes method."
    )
    return response.keyword_themes
    # [END add_smart_campaign_11]


# [START add_smart_campaign]
def get_keyword_text_auto_completions(
    client: GoogleAdsClient, keyword_text: str
) -> List[SuggestKeywordThemesResponse.KeywordTheme]:
    """Retrieves KeywordThemeConstants for the given keyword text.

    These KeywordThemeConstants are derived from autocomplete data for the
    given keyword text. They are mapped to KeywordThemes before being returned.

    Args:
        client: an initialized GoogleAdsClient instance.
        keyword_text: a keyword used for generating keyword themes.

    Returns:
        a list of KeywordThemes.
    """
    keyword_theme_constant_service: KeywordThemeConstantServiceClient = (
        client.get_service("KeywordThemeConstantService")
    )
    request: SuggestKeywordThemeConstantsRequest = client.get_type(
        "SuggestKeywordThemeConstantsRequest"
    )
    request.query_text = keyword_text
    request.country_code = _COUNTRY_CODE
    request.language_code = _LANGUAGE_CODE

    response: SuggestKeywordThemeConstantsResponse = (
        keyword_theme_constant_service.suggest_keyword_theme_constants(
            request=request
        )
    )

    print(
        f"Retrieved {len(response.keyword_theme_constants)} keyword theme "
        f"constants using the keyword: '{keyword_text}'"
    )

    # Map the keyword theme constants to KeywordTheme instances for consistency
    # with the response from SmartCampaignSuggestService.SuggestKeywordThemes.
    keyword_themes: List[SuggestKeywordThemesResponse.KeywordTheme] = []
    keyword_theme_constant: KeywordThemeConstant
    for keyword_theme_constant in response.keyword_theme_constants:
        # Note that the SuggestKeywordThemesResponse.KeywordTheme is a nested
        # type and not the same as the top-level KeywordTheme message.
        keyword_theme: SuggestKeywordThemesResponse.KeywordTheme = (
            client.get_type("SuggestKeywordThemesResponse").KeywordTheme()
        )
        keyword_theme.keyword_theme_constant = keyword_theme_constant
        keyword_themes.append(keyword_theme)

    return keyword_themes
    # [END add_smart_campaign]


# [START add_smart_campaign_13]
def get_free_form_keyword_theme_info(
    client: GoogleAdsClient, free_form_keyword_text: str
) -> KeywordThemeInfo:
    """Creates a KeywordThemeInfo using the given free-form keyword text.

    Args:
        client: an initialized GoogleAdsClient instance.
        free_form_keyword_text: a keyword used to create a free-form keyword
          theme.

    Returns:
        a KeywordThemeInfo instance.
    """
    info: KeywordThemeInfo = client.get_type("KeywordThemeInfo")
    info.free_form_keyword_theme = free_form_keyword_text
    return info
    # [END add_smart_campaign_13]


def map_keyword_themes_to_keyword_infos(
    client: GoogleAdsClient,
    keyword_themes: List[SuggestKeywordThemesResponse.KeywordTheme],
) -> List[KeywordThemeInfo]:
    """Maps a list of KeywordThemes to KeywordThemeInfos.

    Args:
        client: an initialized GoogleAdsClient instance.
        keyword_themes: a list of KeywordThemes.

    Returns:
        a list of KeywordThemeInfos.
    """
    infos: List[KeywordThemeInfo] = []
    keyword_theme: SuggestKeywordThemesResponse.KeywordTheme
    for keyword_theme in keyword_themes:
        info: KeywordThemeInfo = client.get_type("KeywordThemeInfo")
        # Check if the keyword_theme_constant field is set.
        if "keyword_theme_constant" in keyword_theme:
            info.keyword_theme_constant = (
                keyword_theme.keyword_theme_constant.resource_name
            )
            infos.append(info)
        # Check if the free_form_keyword_theme field is set.
        elif "free_form_keyword_theme" in keyword_theme:
            info.free_form_keyword_theme = keyword_theme.free_form_keyword_theme
            infos.append(info)
        else:
            raise ValueError(
                f"A malformed KeywordTheme was encountered: {keyword_theme}"
            )

    return infos


# [START add_smart_campaign_9]
def get_smart_campaign_suggestion_info(
    client: GoogleAdsClient,
    business_profile_location: Optional[str],
    business_name: Optional[str],
) -> SmartCampaignSuggestionInfo:
    """Builds a SmartCampaignSuggestionInfo object with business details.

    The details are used by the SmartCampaignSuggestService to suggest a
    budget amount as well as creatives for the ad.

    Note that when retrieving ad creative suggestions it's required that the
    "final_url", "language_code" and "keyword_themes" fields are set on the
    SmartCampaignSuggestionInfo instance.

    Args:
        client: an initialized GoogleAdsClient instance.
        business_profile_location: the resource name of a Business Profile
          location.
        business_name: the name of a Business Profile.

    Returns:
        A SmartCampaignSuggestionInfo instance.
    """
    suggestion_info: SmartCampaignSuggestionInfo = client.get_type(
        "SmartCampaignSuggestionInfo"
    )

    # Add the URL of the campaign's landing page.
    suggestion_info.final_url = _LANDING_PAGE_URL

    # Add the language code for the campaign.
    suggestion_info.language_code = _LANGUAGE_CODE

    # Construct location information using the given geo target constant. It's
    # also possible to provide a geographic proximity using the "proximity"
    # field on suggestion_info, for example:
    #
    # suggestion_info.proximity.address.post_code = INSERT_POSTAL_CODE
    # suggestion_info.proximity.address.province_code = INSERT_PROVINCE_CODE
    # suggestion_info.proximity.address.country_code = INSERT_COUNTRY_CODE
    # suggestion_info.proximity.address.province_name = INSERT_PROVINCE_NAME
    # suggestion_info.proximity.address.street_address = INSERT_STREET_ADDRESS
    # suggestion_info.proximity.address.street_address2 = INSERT_STREET_ADDRESS_2
    # suggestion_info.proximity.address.city_name = INSERT_CITY_NAME
    # suggestion_info.proximity.radius = INSERT_RADIUS
    # suggestion_info.proximity.radius_units = RADIUS_UNITS
    #
    # For more information on proximities see:
    # https://developers.google.com/google-ads/api/reference/rpc/latest/ProximityInfo
    location: LocationInfo = client.get_type("LocationInfo")
    # Set the location to the resource name of the given geo target constant.
    location.geo_target_constant = client.get_service(
        "GeoTargetConstantService"
    ).geo_target_constant_path(_GEO_TARGET_CONSTANT)
    # Add the LocationInfo object to the list of locations on the
    # suggestion_info object. You have the option of providing multiple
    # locations when using location-based suggestions.
    suggestion_info.location_list.locations.append(location)

    # Set either of the business_profile_location or business_name, depending on
    # whichever is provided.
    if business_profile_location:
        suggestion_info.business_profile_location = business_profile_location
    else:
        suggestion_info.business_context.business_name = business_name

    # Add a schedule detailing which days of the week the business is open.
    # This schedule describes a schedule in which the business is open on
    # Mondays from 9am to 5pm.
    ad_schedule_info: AdScheduleInfo = client.get_type("AdScheduleInfo")
    # Set the day of this schedule as Monday.
    ad_schedule_info.day_of_week = client.enums.DayOfWeekEnum.MONDAY
    # Set the start hour to 9am.
    ad_schedule_info.start_hour = 9
    # Set the end hour to 5pm.
    ad_schedule_info.end_hour = 17
    # Set the start and end minute of zero, for example: 9:00 and 5:00.
    zero_minute_of_hour: MinuteOfHourEnum.MinuteOfHour = (
        client.enums.MinuteOfHourEnum.ZERO
    )
    ad_schedule_info.start_minute = zero_minute_of_hour
    ad_schedule_info.end_minute = zero_minute_of_hour
    suggestion_info.ad_schedules.append(ad_schedule_info)

    return suggestion_info
    # [END add_smart_campaign_9]


# [START add_smart_campaign_1]
def get_budget_suggestion(
    client: GoogleAdsClient,
    customer_id: str,
    suggestion_info: SmartCampaignSuggestionInfo,
) -> int:
    """Retrieves a suggested budget amount for a new budget.

    Using the SmartCampaignSuggestService to determine a daily budget for new
    and existing Smart campaigns is highly recommended because it helps the
    campaigns achieve optimal performance.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.
        suggestion_info: a SmartCampaignSuggestionInfo instance with details
          about the business being advertised.

    Returns:
        a daily budget amount in micros.
    """
    sc_suggest_service: SmartCampaignSuggestServiceClient = client.get_service(
        "SmartCampaignSuggestService"
    )
    request: SuggestSmartCampaignBudgetOptionsRequest = client.get_type(
        "SuggestSmartCampaignBudgetOptionsRequest"
    )
    request.customer_id = customer_id
    # You can retrieve suggestions for an existing campaign by setting the
    # "campaign" field of the request equal to the resource name of a campaign
    # and leaving the rest of the request fields below unset:
    # request.campaign = INSERT_CAMPAIGN_RESOURCE_NAME_HERE

    # Since these suggestions are for a new campaign, we're going to
    # use the suggestion_info field instead.
    request.suggestion_info = suggestion_info

    # Issue a request to retrieve a budget suggestion.
    response: SuggestSmartCampaignBudgetOptionsResponse = (
        sc_suggest_service.suggest_smart_campaign_budget_options(
            request=request
        )
    )

    # Three tiers of options will be returned, a "low", "high" and
    # "recommended". Here we will use the "recommended" option. The amount is
    # specified in micros, where one million is equivalent to one currency unit.
    recommendation: SuggestSmartCampaignBudgetOptionsResponse.BudgetOption = (
        response.recommended
    )
    print(
        f"A daily budget amount of {recommendation.daily_amount_micros} micros "
        "was suggested, garnering an estimated minimum of "
        f"{recommendation.metrics.min_daily_clicks} clicks and an estimated "
        f"maximum of {recommendation.metrics.max_daily_clicks} per day."
    )

    return recommendation.daily_amount_micros
    # [END add_smart_campaign_1]


# [START add_smart_campaign_10]
def get_ad_suggestions(
    client: GoogleAdsClient,
    customer_id: str,
    suggestion_info: SmartCampaignSuggestionInfo,
) -> SmartCampaignAdInfo:
    """Retrieves creative suggestions for a Smart campaign ad.

    Using the SmartCampaignSuggestService to suggest creatives for new and
    existing Smart campaigns is highly recommended because it helps the
    campaigns achieve optimal performance.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.
        suggestion_info: a SmartCampaignSuggestionInfo instance with details
          about the business being advertised.

    Returns:
        a SmartCampaignAdInfo instance with suggested headlines and
            descriptions.
    """
    sc_suggest_service: SmartCampaignSuggestServiceClient = client.get_service(
        "SmartCampaignSuggestService"
    )
    request: SuggestSmartCampaignAdRequest = client.get_type(
        "SuggestSmartCampaignAdRequest"
    )
    request.customer_id = customer_id

    # Unlike the SuggestSmartCampaignBudgetOptions method, it's only possible
    # to use suggestion_info to retrieve ad creative suggestions.
    request.suggestion_info = suggestion_info

    # Issue a request to retrieve ad creative suggestions.
    response: SuggestSmartCampaignAdResponse = (
        sc_suggest_service.suggest_smart_campaign_ad(request=request)
    )

    # The SmartCampaignAdInfo object in the response contains a list of up to
    # three headlines and two descriptions. Note that some of the suggestions
    # may have empty strings as text. Before setting these on the ad you should
    # review them and filter out any empty values.
    ad_suggestions: SmartCampaignAdInfo = response.ad_info

    print("The following headlines were suggested:")
    headline: AdTextAsset
    for headline in ad_suggestions.headlines:
        print(f"\t{headline.text or '<None>'}")

    print("And the following descriptions were suggested:")
    description: AdTextAsset
    for description in ad_suggestions.descriptions:
        print(f"\t{description.text or '<None>'}")

    return ad_suggestions
    # [END add_smart_campaign_10]


# [START add_smart_campaign_2]
def create_campaign_budget_operation(
    client: GoogleAdsClient, customer_id: str, suggested_budget_amount: int
) -> MutateOperation:
    """Creates a MutateOperation that creates a new CampaignBudget.

    A temporary ID will be assigned to this campaign budget so that it can be
    referenced by other objects being created in the same Mutate request.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.
        suggested_budget_amount: a numeric daily budget amount in micros.

    Returns:
        a MutateOperation that creates a CampaignBudget.
    """
    mutate_operation: MutateOperation = client.get_type("MutateOperation")
    campaign_budget_operation: CampaignBudgetOperation = (
        mutate_operation.campaign_budget_operation
    )
    campaign_budget: CampaignBudget = campaign_budget_operation.create
    campaign_budget.name = f"Smart campaign budget #{uuid4()}"
    # A budget used for Smart campaigns must have the type SMART_CAMPAIGN.
    # Note that the field name "type_" is an implementation detail in Python,
    # the field's actual name is "type".
    campaign_budget.type_ = client.enums.BudgetTypeEnum.SMART_CAMPAIGN
    # The suggested budget amount from the SmartCampaignSuggestService is
    # a daily budget. We don't need to specify that here, because the budget
    # period already defaults to DAILY.
    campaign_budget.amount_micros = suggested_budget_amount
    # Set a temporary ID in the budget's resource name so it can be referenced
    # by the campaign in later steps.
    campaign_budget.resource_name = client.get_service(
        "CampaignBudgetService"
    ).campaign_budget_path(customer_id, _BUDGET_TEMPORARY_ID)

    return mutate_operation
    # [END add_smart_campaign_2]


# [START add_smart_campaign_3]
def create_smart_campaign_operation(
    client: GoogleAdsClient, customer_id: str
) -> MutateOperation:
    """Creates a MutateOperation that creates a new Smart campaign.

    A temporary ID will be assigned to this campaign so that it can
    be referenced by other objects being created in the same Mutate request.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.

    Returns:
        a MutateOperation that creates a campaign.
    """
    mutate_operation: MutateOperation = client.get_type("MutateOperation")
    campaign_operation: CampaignOperation = mutate_operation.campaign_operation
    campaign: Campaign = campaign_operation.create
    campaign.name = f"Smart campaign #{uuid4()}"
    # Set the campaign status as PAUSED. The campaign is the only entity in
    # the mutate request that should have its' status set.
    campaign.status = client.enums.CampaignStatusEnum.PAUSED
    # Campaign.AdvertisingChannelType is required to be SMART.
    campaign.advertising_channel_type = (
        client.enums.AdvertisingChannelTypeEnum.SMART
    )
    # Campaign.AdvertisingChannelSubType is required to be SMART_CAMPAIGN.
    campaign.advertising_channel_sub_type = (
        client.enums.AdvertisingChannelSubTypeEnum.SMART_CAMPAIGN
    )
    # Assign the resource name with a temporary ID.
    campaign.resource_name = client.get_service(
        "CampaignService"
    ).campaign_path(customer_id, _SMART_CAMPAIGN_TEMPORARY_ID)
    # Set the budget using the given budget resource name.
    campaign.campaign_budget = client.get_service(
        "CampaignBudgetService"
    ).campaign_budget_path(customer_id, _BUDGET_TEMPORARY_ID)

    # Declare whether or not this campaign serves political ads targeting the
    # EU. Valid values are:
    #   CONTAINS_EU_POLITICAL_ADVERTISING
    #   DOES_NOT_CONTAIN_EU_POLITICAL_ADVERTISING
    campaign.contains_eu_political_advertising = (
        client.enums.EuPoliticalAdvertisingStatusEnum.DOES_NOT_CONTAIN_EU_POLITICAL_ADVERTISING
    )

    return mutate_operation
    # [END add_smart_campaign_3]


# [START add_smart_campaign_4]
def create_smart_campaign_setting_operation(
    client: GoogleAdsClient,
    customer_id: str,
    business_profile_location: Optional[str],
    business_name: Optional[str],
) -> MutateOperation:
    """Creates a MutateOperation to create a new SmartCampaignSetting.

    SmartCampaignSettings are unique in that they only support UPDATE
    operations, which are used to update and create them. Below we will
    use a temporary ID in the resource name to associate it with the
    campaign created in the previous step.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.
        business_profile_location: the resource name of a Business Profile
          location.
        business_name: the name of a Business Profile.

    Returns:
        a MutateOperation that creates a SmartCampaignSetting.
    """
    mutate_operation: MutateOperation = client.get_type("MutateOperation")
    smart_campaign_setting_operation: SmartCampaignSettingOperation = (
        mutate_operation.smart_campaign_setting_operation
    )
    smart_campaign_setting: SmartCampaignSetting = (
        smart_campaign_setting_operation.update
    )
    # Set a temporary ID in the campaign setting's resource name to associate it
    # with the campaign created in the previous step.
    smart_campaign_setting.resource_name = client.get_service(
        "SmartCampaignSettingService"
    ).smart_campaign_setting_path(customer_id, _SMART_CAMPAIGN_TEMPORARY_ID)

    # Below we configure the SmartCampaignSetting using many of the same
    # details used to generate a budget suggestion.
    smart_campaign_setting.phone_number.country_code = _COUNTRY_CODE
    smart_campaign_setting.phone_number.phone_number = _PHONE_NUMBER
    smart_campaign_setting.final_url = _LANDING_PAGE_URL
    smart_campaign_setting.advertising_language_code = _LANGUAGE_CODE

    # Set either of the business_profile_location or business_name, depending on
    # whichever is provided.
    if business_profile_location:
        smart_campaign_setting.business_profile_location = (
            business_profile_location
        )
    else:
        smart_campaign_setting.business_name = business_name

    # Set the update mask on the operation. This is required since the smart
    # campaign setting is created in an UPDATE operation. Here the update
    # mask will be a list of all the fields that were set on the
    # SmartCampaignSetting.
    client.copy_from(
        smart_campaign_setting_operation.update_mask,
        protobuf_helpers.field_mask(None, smart_campaign_setting._pb),
    )

    return mutate_operation
    # [END add_smart_campaign_4]


# [START add_smart_campaign_8]
def create_campaign_criterion_operations(
    client: GoogleAdsClient,
    customer_id: str,
    keyword_theme_infos: List[KeywordThemeInfo],
    suggestion_info: SmartCampaignSuggestionInfo,
) -> List[MutateOperation]:
    """Creates a list of MutateOperations that create new campaign criteria.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.
        keyword_theme_infos: a list of KeywordThemeInfos.
        suggestion_info: A SmartCampaignSuggestionInfo instance.

    Returns:
        a list of MutateOperations that create new campaign criteria.
    """
    campaign_service: CampaignServiceClient = client.get_service(
        "CampaignService"
    )

    operations: List[MutateOperation] = []
    info: KeywordThemeInfo
    for info in keyword_theme_infos:
        mutate_operation: MutateOperation = client.get_type("MutateOperation")
        campaign_criterion_operation: CampaignCriterionOperation = (
            mutate_operation.campaign_criterion_operation
        )
        campaign_criterion: CampaignCriterion = (
            campaign_criterion_operation.create
        )
        # Set the campaign ID to a temporary ID.
        campaign_criterion.campaign = campaign_service.campaign_path(
            customer_id, _SMART_CAMPAIGN_TEMPORARY_ID
        )
        # Set the keyword theme to the given KeywordThemeInfo.
        campaign_criterion.keyword_theme.CopyFrom(info)
        # Add the mutate operation to the list of other operations.
        operations.append(mutate_operation)

    # Create a location criterion for each location in the suggestion info
    # object to add corresponding location targeting to the Smart campaign
    location_info: LocationInfo
    for location_info in suggestion_info.location_list.locations:
        mutate_operation: MutateOperation = client.get_type("MutateOperation")
        campaign_criterion_operation: CampaignCriterionOperation = (
            mutate_operation.campaign_criterion_operation
        )
        campaign_criterion: CampaignCriterion = (
            campaign_criterion_operation.create
        )
        # Set the campaign ID to a temporary ID.
        campaign_criterion.campaign = campaign_service.campaign_path(
            customer_id, _SMART_CAMPAIGN_TEMPORARY_ID
        )
        # Set the location to the given location.
        campaign_criterion.location.CopyFrom(location_info)
        # Add the mutate operation to the list of other operations.
        operations.append(mutate_operation)

    return operations
    # [END add_smart_campaign_8]


# [START add_smart_campaign_5]
def create_ad_group_operation(
    client: GoogleAdsClient, customer_id: str
) -> MutateOperation:
    """Creates a MutateOperation that creates a new ad group.

    A temporary ID will be used in the campaign resource name for this
    ad group to associate it with the Smart campaign created in earlier steps.
    A temporary ID will also be used for its own resource name so that we can
    associate an ad group ad with it later in the process.

    Only one ad group can be created for a given Smart campaign.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.

    Returns:
        a MutateOperation that creates a new ad group.
    """
    mutate_operation: MutateOperation = client.get_type("MutateOperation")
    ad_group_operation: AdGroupOperation = mutate_operation.ad_group_operation
    ad_group: AdGroup = ad_group_operation.create
    # Set the ad group ID to a temporary ID.
    ad_group.resource_name = client.get_service("AdGroupService").ad_group_path(
        customer_id, _AD_GROUP_TEMPORARY_ID
    )
    ad_group.name = f"Smart campaign ad group #{uuid4()}"
    # Set the campaign ID to a temporary ID.
    ad_group.campaign = client.get_service("CampaignService").campaign_path(
        customer_id, _BUDGET_TEMPORARY_ID
    )
    # The ad group type must be set to SMART_CAMPAIGN_ADS.
    ad_group.type_ = client.enums.AdGroupTypeEnum.SMART_CAMPAIGN_ADS

    return mutate_operation
    # [END add_smart_campaign_5]


# [START add_smart_campaign_6]
def create_ad_group_ad_operation(
    client: GoogleAdsClient,
    customer_id: str,
    ad_suggestions: SmartCampaignAdInfo,
) -> MutateOperation:
    """Creates a MutateOperation that creates a new ad group ad.

    A temporary ID will be used in the ad group resource name for this
    ad group ad to associate it with the ad group created in earlier steps.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.
        ad_suggestions: a SmartCampaignAdInfo object with ad creative
          suggestions.

    Returns:
        a MutateOperation that creates a new ad group ad.
    """
    mutate_operation: MutateOperation = client.get_type("MutateOperation")
    ad_group_ad_operation: AdGroupAdOperation = (
        mutate_operation.ad_group_ad_operation
    )
    ad_group_ad: AdGroupAd = ad_group_ad_operation.create
    # Set the ad group ID to a temporary ID.
    ad_group_ad.ad_group = client.get_service("AdGroupService").ad_group_path(
        customer_id, _AD_GROUP_TEMPORARY_ID
    )
    # Set the type to SMART_CAMPAIGN_AD.
    ad_group_ad.ad.type_ = client.enums.AdTypeEnum.SMART_CAMPAIGN_AD
    ad: SmartCampaignAdInfo = ad_group_ad.ad.smart_campaign_ad

    # The SmartCampaignAdInfo object includes headlines and descriptions
    # retrieved from the SmartCampaignSuggestService.SuggestSmartCampaignAd
    # method. It's recommended that users review and approve or update these
    # creatives before they're set on the ad. It's possible that some or all of
    # these assets may contain empty texts, which should not be set on the ad
    # and instead should be replaced with meaningful texts from the user. Below
    # we just accept the creatives that were suggested while filtering out empty
    # assets. If no headlines or descriptions were suggested, then we manually
    # add some, otherwise this operation will generate an INVALID_ARGUMENT
    # error. Individual workflows will likely vary here.
    ad.headlines.extend(
        [asset for asset in ad_suggestions.headlines if asset.text]
    )
    num_missing_headlines: int = _REQUIRED_NUM_HEADLINES - len(ad.headlines)

    # If there are fewer headlines than are required, we manually add additional
    # headlines to make up for the difference.
    for i in range(num_missing_headlines):
        headline: AdTextAsset = client.get_type("AdTextAsset")
        headline.text = f"placeholder headline {i}"
        ad.headlines.append(headline)

    ad.descriptions.extend(
        asset for asset in ad_suggestions.descriptions if asset.text
    )
    num_missing_descriptions: int = _REQUIRED_NUM_DESCRIPTIONS - len(
        ad.descriptions
    )

    # If there are fewer descriptions than are required, we manually add
    # additional descriptions to make up for the difference.
    for i in range(num_missing_descriptions):
        description: AdTextAsset = client.get_type("AdTextAsset")
        description.text = f"placeholder description {i}"
        ad.descriptions.append(description)

    return mutate_operation
    # [END add_smart_campaign_6]


def print_response_details(response: MutateGoogleAdsResponse) -> None:
    """Prints the details of a MutateGoogleAdsResponse.

    Parses the "response" oneof field name and uses it to extract the new
    entity's name and resource name.

    Args:
        response: a MutateGoogleAdsResponse object.
    """
    # Parse the Mutate response to print details about the entities that
    # were created by the request.
    result: MutateOperationResponse
    for result in response.mutate_operation_responses:
        resource_type: str = "unrecognized"
        resource_name: str = "not found"

        if result._pb.HasField("campaign_budget_result"):
            resource_type = "CampaignBudget"
            resource_name = result.campaign_budget_result.resource_name
        elif result._pb.HasField("campaign_result"):
            resource_type = "Campaign"
            resource_name = result.campaign_result.resource_name
        elif result._pb.HasField("smart_campaign_setting_result"):
            resource_type = "SmartCampaignSettingResult"
            resource_name = result.smart_campaign_setting_result.resource_name
        elif result._pb.HasField("campaign_criterion_result"):
            resource_type = "CampaignCriterion"
            resource_name = result.campaign_criterion_result.resource_name
        elif result._pb.HasField("ad_group_result"):
            resource_type = "AdGroup"
            resource_name = result.ad_group_result.resource_name
        elif result._pb.HasField("ad_group_ad_result"):
            resource_type = "AdGroupAd"
            resource_name = result.ad_group_ad_result.resource_name

        print(
            f"Created a(n) {resource_type} with "
            f"resource_name: '{resource_name}'."
        )


if __name__ == "__main__":
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description=("Creates a Smart campaign.")
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
        "-k",
        "--keyword_text",
        type=str,
        required=False,
        help=(
            "A keyword text used to retrieve keyword theme constant "
            "suggestions from the KeywordThemeConstantService. These keyword "
            "theme suggestions are generated using auto-completion data for "
            "the given text and may help improve the performance of "
            "the Smart campaign."
        ),
    )
    parser.add_argument(
        "-f",
        "--free_form_keyword_text",
        type=str,
        required=False,
        help=(
            "A keyword text used to create a freeform keyword theme, which is "
            "entirely user-specified and not derived from any suggestion "
            "service. Using free-form keyword themes is typically not "
            "recommended because they are less effective than suggested "
            "keyword themes, however they are useful in situations where a "
            "very specific term needs to be targeted."
        ),
    )
    group: argparse._MutuallyExclusiveGroup = (
        parser.add_mutually_exclusive_group(required=True)
    )
    group.add_argument(
        "-b",
        "--business_profile_location",
        type=str,
        help=(
            "Optional: Specify the resource name of a Business Profile location. This"
            "is required if a business name is not provided. It can be retrieved"
            "using the Business Profile API, see:"
            "https://developers.google.com/my-business/reference/businessinformation/rest/v1/accounts.locations"
            "or from the Business Profile UI (https://support.google.com/business/answer/10737668)."
        ),
    )
    group.add_argument(
        "-n",
        "--business_name",
        type=str,
        help=(
            "The name of a Business Profile business. This is required "
            "if a business profile location is not provided."
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
            args.keyword_text,
            args.free_form_keyword_text,
            args.business_profile_location,
            args.business_name,
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
