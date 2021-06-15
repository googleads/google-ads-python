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
from uuid import uuid4

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException

from google.api_core import protobuf_helpers

_DEFAULT_KEYWORD = "travel"

# Geo target constant for New York City.
_GEO_TARGET_CONSTANT = "1023191"
# Country code is a two-letter ISO-3166 code, for a list of all codes see:
# https://developers.google.com/google-ads/api/reference/data/codes-formats#expandable-16
_COUNTRY_CODE = "US"
# For a list of all language codes, see:
# https://developers.google.com/google-ads/api/reference/data/codes-formats#expandable-7
_LANGUAGE_CODE = "en"
_LANDING_PAGE_URL = "http://www.example.com"
_PHONE_NUMBER = "555-555-5555"
_BUDGET_TEMPORARY_ID = "-1"
_SMART_CAMPAIGN_TEMPORARY_ID = "-2"
_AD_GROUP_TEMPORARY_ID = "-3"


def main(
    client, customer_id, keyword_text, business_location_id, business_name
):
    """The main method that creates all necessary entities for the example.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.
        keyword_text: a keyword used for generating keyword themes.
        business_location_id: the ID of a Google My Business location.
        business_name: the name of a Google My Business.
    """
    keyword_theme_constants = _get_keyword_theme_constants(client, keyword_text)
    keyword_theme_infos = _map_keyword_theme_constants_to_infos(
        client, keyword_theme_constants
    )
    suggested_budget_amount = _get_budget_suggestion(
        client, customer_id, business_location_id, keyword_theme_infos,
    )
    # [START add_smart_campaign_7]
    # The below methods create and return MutateOperations that we later
    # provide to the GoogleAdsService.Mutate method in order to create the
    # entities in a single request. Since the entities for a Smart campaign
    # are closely tied to one-another it's considered a best practice to
    # create them in a single Mutate request so they all complete successfully
    # or fail entirely, leaving no orphaned entities. See:
    # https://developers.google.com/google-ads/api/docs/mutating/overview
    campaign_budget_operation = _create_campaign_budget_operation(
        client, customer_id, suggested_budget_amount
    )
    smart_campaign_operation = _create_smart_campaign_operation(
        client, customer_id
    )
    smart_campaign_setting_operation = _create_smart_campaign_setting_operation(
        client, customer_id, business_location_id, business_name
    )
    campaign_criterion_operations = _create_campaign_criterion_operations(
        client, customer_id, keyword_theme_infos
    )
    ad_group_operation = _create_ad_group_operation(client, customer_id)
    ad_group_ad_operation = _create_ad_group_ad_operation(client, customer_id)

    googleads_service = client.get_service("GoogleAdsService")

    # Send the operations into a single Mutate request.
    response = googleads_service.mutate(
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

    _print_response_details(response)
    # [END add_smart_campaign_7]


# [START add_smart_campaign]
def _get_keyword_theme_constants(client, keyword_text):
    """Retrieves KeywordThemeConstants for the given criteria.

    Args:
        client: an initialized GoogleAdsClient instance.
        keyword_text: a keyword used for generating keyword themes.

    Returns:
        a list of KeywordThemeConstants.
    """
    keyword_theme_constant_service = client.get_service(
        "KeywordThemeConstantService"
    )
    request = client.get_type("SuggestKeywordThemeConstantsRequest")
    request.query_text = keyword_text
    request.country_code = _COUNTRY_CODE
    request.language_code = _LANGUAGE_CODE

    response = keyword_theme_constant_service.suggest_keyword_theme_constants(
        request=request
    )

    print(
        f"Retrieved {len(response.keyword_theme_constants)} keyword theme "
        f"constants using the keyword: '{keyword_text}'"
    )
    return response.keyword_theme_constants
    # [END add_smart_campaign]


# [START add_smart_campaign_1]
def _get_budget_suggestion(
    client, customer_id, business_location_id, keyword_theme_infos,
):
    """Retrieves a suggested budget amount for a new budget.

    Using the SmartCampaignSuggestService to determine a daily budget for new
    and existing Smart campaigns is highly recommended because it helps the
    campaigns achieve optimal performance.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.
        business_location_id: the ID of a Google My Business location.
        keyword_theme_infos: a list of KeywordThemeInfos.

    Returns:
        a daily budget amount in micros.
    """
    sc_suggest_service = client.get_service("SmartCampaignSuggestService")
    request = client.get_type("SuggestSmartCampaignBudgetOptionsRequest")
    request.customer_id = customer_id
    # You can retrieve suggestions for an existing campaign by setting the
    # "campaign" field of the request equal to the resource name of a campaign
    # and leaving the rest of the request fields below unset:
    # request.campaign = INSERT_CAMPAIGN_RESOURCE_NAME_HERE

    # Since these suggestions are for a new campaign, we're going to
    # use the suggestion_info field instead.
    suggestion_info = request.suggestion_info

    # Add the URL of the campaign's landing page.
    suggestion_info.final_url = _LANDING_PAGE_URL

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
    location = client.get_type("LocationInfo")
    # Set the location to the resource name of the given geo target constant.
    location.geo_target_constant = client.get_service(
        "GeoTargetConstantService"
    ).geo_target_constant_path(_GEO_TARGET_CONSTANT)
    # Add the LocationInfo object to the list of locations on the
    # suggestion_info object. You have the option of providing multiple
    # locations when using location-based suggestions.
    suggestion_info.location_list.locations.append(location)

    # Add the KeywordThemeInfo objects to the SuggestionInfo object.
    suggestion_info.keyword_themes.extend(keyword_theme_infos)

    # If provided, add the GMB location ID.
    if business_location_id:
        suggestion_info.business_location_id = business_location_id

    # Add a schedule detailing which days of the week the business is open.
    # This schedule describes a schedule in which the business is open on
    # Mondays from 9am to 5pm.
    ad_schedule_info = client.get_type("AdScheduleInfo")
    # Set the day of this schedule as Monday.
    ad_schedule_info.day_of_week = client.get_type(
        "DayOfWeekEnum"
    ).DayOfWeek.MONDAY
    # Set the start hour to 9am.
    ad_schedule_info.start_hour = 9
    # Set the end hour to 5pm.
    ad_schedule_info.end_hour = 17
    # Set the start and end minute of zero, for example: 9:00 and 5:00.
    zero_minute_of_hour = client.get_type("MinuteOfHourEnum").MinuteOfHour.ZERO
    ad_schedule_info.start_minute = zero_minute_of_hour
    ad_schedule_info.end_minute = zero_minute_of_hour
    suggestion_info.ad_schedules.append(ad_schedule_info)

    # Issue a request to retrieve a budget suggestion.
    response = sc_suggest_service.suggest_smart_campaign_budget_options(
        request=request
    )

    # Three tiers of options will be returned, a "low", "high" and
    # "recommended". Here we will use the "recommended" option. The amount is
    # specified in micros, where one million is equivalent to one currency unit.
    recommendation = response.recommended
    print(
        f"A daily budget amount of {recommendation.daily_amount_micros} micros "
        "was suggested, garnering an estimated minimum of "
        f"{recommendation.metrics.min_daily_clicks} clicks and an estimated "
        f"maximum of {recommendation.metrics.max_daily_clicks} per day."
    )

    return recommendation.daily_amount_micros
    # [END add_smart_campaign_1]


def _map_keyword_theme_constants_to_infos(client, keyword_theme_constants):
    """Maps a list of KeywordThemeConstants to KeywordThemeInfos.

    Args:
        client: an initialized GoogleAdsClient instance.
        keyword_theme_constants: a list of KeywordThemeConstants.

    Returns:
        a list of KeywordThemeInfos.
    """
    infos = []
    for constant in keyword_theme_constants:
        info = client.get_type("KeywordThemeInfo")
        info.keyword_theme_constant = constant.resource_name
        infos.append(info)

    return infos


# [START add_smart_campaign_2]
def _create_campaign_budget_operation(
    client, customer_id, suggested_budget_amount
):
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
    mutate_operation = client.get_type("MutateOperation")
    campaign_budget_operation = mutate_operation.campaign_budget_operation
    campaign_budget = campaign_budget_operation.create
    campaign_budget.name = f"Smart campaign budget #{uuid4()}"
    # A budget used for Smart campaigns must have the type SMART_CAMPAIGN.
    # Note that the field name "type_" is an implementation detail in Python,
    # the field's actual name is "type".
    campaign_budget.type_ = client.get_type(
        "BudgetTypeEnum"
    ).BudgetType.SMART_CAMPAIGN
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
def _create_smart_campaign_operation(client, customer_id):
    """Creates a MutateOperation that creates a new Smart campaign.

    A temporary ID will be assigned to this campaign so that it can
    be referenced by other objects being created in the same Mutate request.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.

    Returns:
        a MutateOperation that creates a campaign.
    """
    mutate_operation = client.get_type("MutateOperation")
    campaign = mutate_operation.campaign_operation.create
    campaign.name = f"Smart campaign #{uuid4()}"
    # Set the campaign status as PAUSED. The campaign is the only entity in
    # the mutate request that should have its' status set.
    campaign.status = client.get_type(
        "CampaignStatusEnum"
    ).CampaignStatus.PAUSED
    # Campaign.AdvertisingChannelType is required to be SMART.
    campaign.advertising_channel_type = client.get_type(
        "AdvertisingChannelTypeEnum"
    ).AdvertisingChannelType.SMART
    # Campaign.AdvertisingChannelSubType is required to be SMART_CAMPAIGN.
    campaign.advertising_channel_sub_type = client.get_type(
        "AdvertisingChannelSubTypeEnum"
    ).AdvertisingChannelSubType.SMART_CAMPAIGN
    # Assign the resource name with a temporary ID.
    campaign_service = client.get_service("CampaignService")
    campaign.resource_name = campaign_service.campaign_path(
        customer_id, _SMART_CAMPAIGN_TEMPORARY_ID
    )
    # Set the budget using the given budget resource name.
    campaign.campaign_budget = campaign_service.campaign_budget_path(
        customer_id, _BUDGET_TEMPORARY_ID
    )

    return mutate_operation
    # [END add_smart_campaign_3]


# [START add_smart_campaign_4]
def _create_smart_campaign_setting_operation(
    client, customer_id, business_location_id, business_name
):
    """Creates a MutateOperation to create a new SmartCampaignSetting.

    SmartCampaignSettings are unique in that they only support UPDATE
    operations, which are used to update and create them. Below we will
    use a temporary ID in the resource name to associate it with the
    campaign created in the previous step.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.
        business_location_id: the ID of a Google My Business location.
        business_name: the name of a Google My Business.

    Returns:
        a MutateOperation that creates a SmartCampaignSetting.
    """
    mutate_operation = client.get_type("MutateOperation")
    smart_campaign_setting = (
        mutate_operation.smart_campaign_setting_operation.update
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

    # It's required that either a business location ID or a business name is
    # added to the SmartCampaignSetting.
    if business_location_id:
        smart_campaign_setting.business_location_id = business_location_id
    else:
        smart_campaign_setting.business_name = business_name

    # Set the update mask on the operation. This is required since the smart
    # campaign setting is created in an UPDATE operation. Here the update
    # mask will be a list of all the fields that were set on the
    # SmartCampaignSetting.
    client.copy_from(
        mutate_operation.smart_campaign_setting_operation.update_mask,
        protobuf_helpers.field_mask(None, smart_campaign_setting._pb),
    )

    return mutate_operation
    # [END add_smart_campaign_4]


# [START add_smart_campaign_8]
def _create_campaign_criterion_operations(
    client, customer_id, keyword_theme_infos
):
    """Creates a list of MutateOperations that create new campaign criteria.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.
        keyword_theme_infos: a list of KeywordThemeInfos.

    Returns:
        a list of MutateOperations that create new campaign criteria.
    """
    campaign_service = client.get_service("CampaignService")

    operations = []
    for info in keyword_theme_infos:
        mutate_operation = client.get_type("MutateOperation")
        campaign_criterion = (
            mutate_operation.campaign_criterion_operation.create
        )
        # Set the campaign ID to a temporary ID.
        campaign_criterion.campaign = campaign_service.campaign_path(
            customer_id, _SMART_CAMPAIGN_TEMPORARY_ID
        )
        # Set the criterion type to KEYWORD_THEME.
        campaign_criterion.type_ = client.get_type(
            "CriterionTypeEnum"
        ).CriterionType.KEYWORD_THEME
        # Set the keyword theme to the given KeywordThemeInfo.
        campaign_criterion.keyword_theme = info
        # Add the mutate operation to the list of other operations.
        operations.append(mutate_operation)

    return operations
    # [END add_smart_campaign_8]


# [START add_smart_campaign_5]
def _create_ad_group_operation(client, customer_id):
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
    mutate_operation = client.get_type("MutateOperation")
    ad_group = mutate_operation.ad_group_operation.create
    # Set the ad group ID to a temporary ID.
    ad_group.resource_name = client.get_service("AdGroupService").ad_group_path(
        customer_id, _AD_GROUP_TEMPORARY_ID
    )
    ad_group.name = f"Smart campaign ad group #{uuid4()}"
    # Set the campaign ID to a temporary ID.
    ad_group.campaign = client.get_service("CampaignService").campaign_path(
        customer_id, _SMART_CAMPAIGN_TEMPORARY_ID
    )
    # The ad group type must be set to SMART_CAMPAIGN_ADS.
    ad_group.type_ = client.get_type(
        "AdGroupTypeEnum"
    ).AdGroupType.SMART_CAMPAIGN_ADS

    return mutate_operation
    # [END add_smart_campaign_5]


# [START add_smart_campaign_6]
def _create_ad_group_ad_operation(client, customer_id):
    """Creates a MutateOperation that creates a new ad group ad.

    A temporary ID will be used in the ad group resource name for this
    ad group ad to associate it with the ad group created in earlier steps.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.

    Returns:
        a MutateOperation that creates a new ad group ad.
    """
    mutate_operation = client.get_type("MutateOperation")
    ad_group_ad = mutate_operation.ad_group_ad_operation.create
    # Set the ad group ID to a temporary ID.
    ad_group_ad.ad_group = client.get_service("AdGroupService").ad_group_path(
        customer_id, _AD_GROUP_TEMPORARY_ID
    )
    # Set the type to SMART_CAMPAIGN_AD.
    ad_group_ad.ad.type_ = client.get_type(
        "AdTypeEnum"
    ).AdType.SMART_CAMPAIGN_AD
    ad = ad_group_ad.ad.smart_campaign_ad
    # At most, three headlines can be specified for a Smart campaign ad.
    headline_1 = client.get_type("AdTextAsset")
    headline_1.text = "Headline number one"
    headline_2 = client.get_type("AdTextAsset")
    headline_2.text = "Headline number two"
    headline_3 = client.get_type("AdTextAsset")
    headline_3.text = "Headline number three"
    ad.headlines.extend([headline_1, headline_2, headline_3])
    # At most, two descriptions can be specified for a Smart campaign ad.
    description_1 = client.get_type("AdTextAsset")
    description_1.text = "Description number one"
    description_2 = client.get_type("AdTextAsset")
    description_2.text = "Description number two"
    ad.descriptions.extend([description_1, description_2])

    return mutate_operation
    # [END add_smart_campaign_6]


def _print_response_details(response):
    """Prints the details of a MutateGoogleAdsResponse.

    Parses the "response" oneof field name and uses it to extract the new
    entity's name and resource name.

    Args:
        response: a MutateGoogleAdsResponse object.
    """
    # Parse the Mutate response to print details about the entities that
    # were created by the request.
    for result in response.mutate_operation_responses:
        resource_type = "unrecognized"
        resource_name = "not found"

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
    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    googleads_client = GoogleAdsClient.load_from_storage(version="v8")

    parser = argparse.ArgumentParser(description=("Creates a Smart campaign."))
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
        default=_DEFAULT_KEYWORD,
        help=(
            "A keyword text used to generate a set of keyword themes, which "
            "are used to improve the budget suggestion and performance of "
            f"the Smart campaign. Default value is '{_DEFAULT_KEYWORD}'."
        ),
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "-b",
        "--business_location_id",
        type=str,
        help=(
            "The ID of a Google My Business (GMB) location. This is required "
            "if a business name is not provided. It can be retrieved using the "
            "GMB API, for details see: "
            "https://developers.google.com/my-business/reference/rest/v4/accounts.locations"
        ),
    )
    group.add_argument(
        "-n",
        "--business_name",
        type=str,
        help=(
            "The name of a Google My Business (GMB) business. This is required "
            "if a business location ID is not provided."
        ),
    )

    args = parser.parse_args()

    try:
        main(
            googleads_client,
            args.customer_id,
            args.keyword_text,
            args.business_location_id,
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
