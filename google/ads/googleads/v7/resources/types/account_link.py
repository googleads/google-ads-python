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

from google.ads.googleads.v7.enums.types import account_link_status
from google.ads.googleads.v7.enums.types import linked_account_type
from google.ads.googleads.v7.enums.types import mobile_app_vendor


__protobuf__ = proto.module(
    package="google.ads.googleads.v7.resources",
    marshal="google.ads.googleads.v7",
    manifest={
        "AccountLink",
        "ThirdPartyAppAnalyticsLinkIdentifier",
        "DataPartnerLinkIdentifier",
        "GoogleAdsLinkIdentifier",
    },
)


class AccountLink(proto.Message):
    r"""Represents the data sharing connection between a Google Ads
    account and another account

    Attributes:
        resource_name (str):
            Immutable. Resource name of the account link. AccountLink
            resource names have the form:
            ``customers/{customer_id}/accountLinks/{account_link_id}``
        account_link_id (int):
            Output only. The ID of the link.
            This field is read only.
        status (google.ads.googleads.v7.enums.types.AccountLinkStatusEnum.AccountLinkStatus):
            The status of the link.
        type_ (google.ads.googleads.v7.enums.types.LinkedAccountTypeEnum.LinkedAccountType):
            Output only. The type of the linked account.
        third_party_app_analytics (google.ads.googleads.v7.resources.types.ThirdPartyAppAnalyticsLinkIdentifier):
            Immutable. A third party app analytics link.
        data_partner (google.ads.googleads.v7.resources.types.DataPartnerLinkIdentifier):
            Output only. Data partner link.
        google_ads (google.ads.googleads.v7.resources.types.GoogleAdsLinkIdentifier):
            Output only. Google Ads link.
    """

    resource_name = proto.Field(proto.STRING, number=1,)
    account_link_id = proto.Field(proto.INT64, number=8, optional=True,)
    status = proto.Field(
        proto.ENUM,
        number=3,
        enum=account_link_status.AccountLinkStatusEnum.AccountLinkStatus,
    )
    type_ = proto.Field(
        proto.ENUM,
        number=4,
        enum=linked_account_type.LinkedAccountTypeEnum.LinkedAccountType,
    )
    third_party_app_analytics = proto.Field(
        proto.MESSAGE,
        number=5,
        oneof="linked_account",
        message="ThirdPartyAppAnalyticsLinkIdentifier",
    )
    data_partner = proto.Field(
        proto.MESSAGE,
        number=6,
        oneof="linked_account",
        message="DataPartnerLinkIdentifier",
    )
    google_ads = proto.Field(
        proto.MESSAGE,
        number=7,
        oneof="linked_account",
        message="GoogleAdsLinkIdentifier",
    )


class ThirdPartyAppAnalyticsLinkIdentifier(proto.Message):
    r"""The identifiers of a Third Party App Analytics Link.
    Attributes:
        app_analytics_provider_id (int):
            Immutable. The ID of the app analytics
            provider. This field should not be empty when
            creating a new third party app analytics link.
            It is unable to be modified after the creation
            of the link.
        app_id (str):
            Immutable. A string that uniquely identifies
            a mobile application from which the data was
            collected to the Google Ads API. For iOS, the ID
            string is the 9 digit string that appears at the
            end of an App Store URL (e.g., "422689480" for
            "Gmail" whose App Store link is
            https://apps.apple.com/us/app/gmail-email-by-
            google/id422689480). For Android, the ID string
            is the application's package name (e.g.,
            "com.google.android.gm" for "Gmail" given Google
            Play link
            https://play.google.com/store/apps/details?id=com.google.android.gm)
            This field should not be empty when creating a
            new third party app analytics link. It is unable
            to be modified after the creation of the link.
        app_vendor (google.ads.googleads.v7.enums.types.MobileAppVendorEnum.MobileAppVendor):
            Immutable. The vendor of the app.
            This field should not be empty when creating a
            new third party app analytics link. It is unable
            to be modified after the creation of the link.
    """

    app_analytics_provider_id = proto.Field(
        proto.INT64, number=4, optional=True,
    )
    app_id = proto.Field(proto.STRING, number=5, optional=True,)
    app_vendor = proto.Field(
        proto.ENUM,
        number=3,
        enum=mobile_app_vendor.MobileAppVendorEnum.MobileAppVendor,
    )


class DataPartnerLinkIdentifier(proto.Message):
    r"""The identifier for Data Partner account.
    Attributes:
        data_partner_id (int):
            Immutable. The customer ID of the Data
            partner account. This field is required and
            should not be empty when creating a new data
            partner link. It is unable to be modified after
            the creation of the link.
    """

    data_partner_id = proto.Field(proto.INT64, number=1, optional=True,)


class GoogleAdsLinkIdentifier(proto.Message):
    r"""The identifier for Google Ads account.
    Attributes:
        customer (str):
            Immutable. The resource name of the Google
            Ads account. This field is required and should
            not be empty when creating a new Google Ads
            link. It is unable to be modified after the
            creation of the link.
    """

    customer = proto.Field(proto.STRING, number=3, optional=True,)


__all__ = tuple(sorted(__protobuf__.manifest))
