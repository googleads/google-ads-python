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


__protobuf__ = proto.module(
    package="google.ads.googleads.v8.resources",
    marshal="google.ads.googleads.v8",
    manifest={"SmartCampaignSetting",},
)


class SmartCampaignSetting(proto.Message):
    r"""Settings for configuring Smart campaigns.
    Attributes:
        resource_name (str):
            Immutable. The resource name of the Smart campaign setting.
            Smart campaign setting resource names have the form:

            ``customers/{customer_id}/smartCampaignSettings/{campaign_id}``
        campaign (str):
            Output only. The campaign to which these
            settings apply.
        phone_number (google.ads.googleads.v8.resources.types.SmartCampaignSetting.PhoneNumber):
            Phone number and country code.
        final_url (str):
            Landing page url given by user for this
            Campaign.
        advertising_language_code (str):
            The ISO-639-1 language code to advertise in.
        business_name (str):
            The name of the business.
        business_location_id (int):
            The ID of the Google My Business (GMB) Location. The
            location ID can be fetched by GMB API with its form:
            accounts/{accountId}/locations/{locationId}. The last
            {locationId} component from the GMB API represents the
            business_location_id. See the [Google My Business API]
            (https://developers.google.com/my-business/reference/rest/v4/accounts.locations)
    """

    class PhoneNumber(proto.Message):
        r"""Phone number and country code in smart campaign settings.
        Attributes:
            phone_number (str):
                Phone number of the smart campaign.
            country_code (str):
                Upper-case, two-letter country code as
                defined by ISO-3166.
        """

        phone_number = proto.Field(proto.STRING, number=1, optional=True,)
        country_code = proto.Field(proto.STRING, number=2, optional=True,)

    resource_name = proto.Field(proto.STRING, number=1,)
    campaign = proto.Field(proto.STRING, number=2,)
    phone_number = proto.Field(proto.MESSAGE, number=3, message=PhoneNumber,)
    final_url = proto.Field(proto.STRING, number=4,)
    advertising_language_code = proto.Field(proto.STRING, number=7,)
    business_name = proto.Field(
        proto.STRING, number=5, oneof="business_setting",
    )
    business_location_id = proto.Field(
        proto.INT64, number=6, oneof="business_setting",
    )


__all__ = tuple(sorted(__protobuf__.manifest))
