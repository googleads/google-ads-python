# -*- coding: utf-8 -*-
# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import proto  # type: ignore

from google.ads.googleads.v8.common.types import ad_type_infos
from google.ads.googleads.v8.common.types import criteria


__protobuf__ = proto.module(
    package="google.ads.googleads.v8.services",
    marshal="google.ads.googleads.v8",
    manifest={
        "SuggestSmartCampaignBudgetOptionsRequest",
        "SmartCampaignSuggestionInfo",
        "SuggestSmartCampaignBudgetOptionsResponse",
        "SuggestSmartCampaignAdRequest",
        "SuggestSmartCampaignAdResponse",
    },
)


class SuggestSmartCampaignBudgetOptionsRequest(proto.Message):
    r"""Request message for
    [SmartCampaignSuggestService.SuggestSmartCampaignBudgets][].

    Attributes:
        customer_id (str):
            Required. The ID of the customer whose budget
            options are to be suggested.
        campaign (str):
            Required. The resource name of the campaign
            to get suggestion for.
        suggestion_info (google.ads.googleads.v8.services.types.SmartCampaignSuggestionInfo):
            Required. Information needed to get budget
            options
    """

    customer_id = proto.Field(proto.STRING, number=1,)
    campaign = proto.Field(proto.STRING, number=2, oneof="suggestion_data",)
    suggestion_info = proto.Field(
        proto.MESSAGE,
        number=3,
        oneof="suggestion_data",
        message="SmartCampaignSuggestionInfo",
    )


class SmartCampaignSuggestionInfo(proto.Message):
    r"""Information needed to get suggestion for Smart Campaign. More
    information provided will help the system to derive better
    suggestions.

    Attributes:
        final_url (str):
            Optional. Landing page URL of the campaign.
        language_code (str):
            Optional. The two letter advertising language
            for the Smart campaign to be constructed,
            default to 'en' if not set.
        ad_schedules (Sequence[google.ads.googleads.v8.common.types.AdScheduleInfo]):
            Optional. The business ad schedule.
        keyword_themes (Sequence[google.ads.googleads.v8.common.types.KeywordThemeInfo]):
            Optional. Smart campaign keyword themes. This
            field may greatly improve suggestion accuracy
            and we recommend always setting it if possible.
        business_context (google.ads.googleads.v8.services.types.SmartCampaignSuggestionInfo.BusinessContext):
            Optional. Context describing the business to
            advertise.
        business_location_id (int):
            Optional. The ID of the Google My Business (GMB) Location.
            The location ID can be fetched by GMB API with its form:
            accounts/{accountId}/locations/{locationId}. The last
            {locationId} component from the GMB API represents the
            business_location_id. See the [Google My Business API]
            (https://developers.google.com/my-business/reference/rest/v4/accounts.locations)
        location_list (google.ads.googleads.v8.services.types.SmartCampaignSuggestionInfo.LocationList):
            Optional. The targeting geo location by
            locations.
        proximity (google.ads.googleads.v8.common.types.ProximityInfo):
            Optional. The targeting geo location by
            proximity.
    """

    class LocationList(proto.Message):
        r"""A list of locations.
        Attributes:
            locations (Sequence[google.ads.googleads.v8.common.types.LocationInfo]):
                Required. Locations.
        """

        locations = proto.RepeatedField(
            proto.MESSAGE, number=1, message=criteria.LocationInfo,
        )

    class BusinessContext(proto.Message):
        r"""A context that describes a business.
        Attributes:
            business_name (str):
                Optional. The name of the business.
        """

        business_name = proto.Field(proto.STRING, number=1,)

    final_url = proto.Field(proto.STRING, number=1,)
    language_code = proto.Field(proto.STRING, number=3,)
    ad_schedules = proto.RepeatedField(
        proto.MESSAGE, number=6, message=criteria.AdScheduleInfo,
    )
    keyword_themes = proto.RepeatedField(
        proto.MESSAGE, number=7, message=criteria.KeywordThemeInfo,
    )
    business_context = proto.Field(
        proto.MESSAGE,
        number=8,
        oneof="business_setting",
        message=BusinessContext,
    )
    business_location_id = proto.Field(
        proto.INT64, number=2, oneof="business_setting",
    )
    location_list = proto.Field(
        proto.MESSAGE, number=4, oneof="geo_target", message=LocationList,
    )
    proximity = proto.Field(
        proto.MESSAGE,
        number=5,
        oneof="geo_target",
        message=criteria.ProximityInfo,
    )


class SuggestSmartCampaignBudgetOptionsResponse(proto.Message):
    r"""Response message for
    [SmartCampaignSuggestService.SuggestSmartCampaignBudgets][].
    Depending on whether the system could suggest the options, either
    all of the options or none of them might be returned.

    Attributes:
        low (google.ads.googleads.v8.services.types.SuggestSmartCampaignBudgetOptionsResponse.BudgetOption):
            Optional. The lowest budget option.
        recommended (google.ads.googleads.v8.services.types.SuggestSmartCampaignBudgetOptionsResponse.BudgetOption):
            Optional. The recommended budget option.
        high (google.ads.googleads.v8.services.types.SuggestSmartCampaignBudgetOptionsResponse.BudgetOption):
            Optional. The highest budget option.
    """

    class Metrics(proto.Message):
        r"""Performance metrics for a given budget option.
        Attributes:
            min_daily_clicks (int):
                The estimated min daily clicks.
            max_daily_clicks (int):
                The estimated max daily clicks.
        """

        min_daily_clicks = proto.Field(proto.INT64, number=1,)
        max_daily_clicks = proto.Field(proto.INT64, number=2,)

    class BudgetOption(proto.Message):
        r"""Smart Campaign budget option.
        Attributes:
            daily_amount_micros (int):
                The amount of the budget, in the local
                currency for the account. Amount is specified in
                micros, where one million is equivalent to one
                currency unit.
            metrics (google.ads.googleads.v8.services.types.SuggestSmartCampaignBudgetOptionsResponse.Metrics):
                Metrics pertaining to the suggested budget,
                could be empty if there is not enough
                information to derive the estimates.
        """

        daily_amount_micros = proto.Field(proto.INT64, number=1,)
        metrics = proto.Field(
            proto.MESSAGE,
            number=2,
            message="SuggestSmartCampaignBudgetOptionsResponse.Metrics",
        )

    low = proto.Field(
        proto.MESSAGE, number=1, optional=True, message=BudgetOption,
    )
    recommended = proto.Field(
        proto.MESSAGE, number=2, optional=True, message=BudgetOption,
    )
    high = proto.Field(
        proto.MESSAGE, number=3, optional=True, message=BudgetOption,
    )


class SuggestSmartCampaignAdRequest(proto.Message):
    r"""Request message for
    [SmartCampaignSuggestService.SuggestSmartCampaignAd][google.ads.googleads.v8.services.SmartCampaignSuggestService.SuggestSmartCampaignAd].

    Attributes:
        customer_id (str):
            Required. The ID of the customer.
        suggestion_info (google.ads.googleads.v8.services.types.SmartCampaignSuggestionInfo):
            Required. Inputs used to suggest a Smart campaign ad.
            Required fields: final_url, language_code, keyword_themes.
            Optional but recommended fields to improve the quality of
            the suggestion: business_setting and geo_target.
    """

    customer_id = proto.Field(proto.STRING, number=1,)
    suggestion_info = proto.Field(
        proto.MESSAGE, number=2, message="SmartCampaignSuggestionInfo",
    )


class SuggestSmartCampaignAdResponse(proto.Message):
    r"""Response message for
    [SmartCampaignSuggestService.SuggestSmartCampaignAd][google.ads.googleads.v8.services.SmartCampaignSuggestService.SuggestSmartCampaignAd].

    Attributes:
        ad_info (google.ads.googleads.v8.common.types.SmartCampaignAdInfo):
            Optional. Ad info includes 3 creative
            headlines and 2 creative descriptions.
    """

    ad_info = proto.Field(
        proto.MESSAGE, number=1, message=ad_type_infos.SmartCampaignAdInfo,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
