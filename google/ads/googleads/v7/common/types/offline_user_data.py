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

from google.ads.googleads.v7.enums.types import (
    user_identifier_source as gage_user_identifier_source,
)


__protobuf__ = proto.module(
    package="google.ads.googleads.v7.common",
    marshal="google.ads.googleads.v7",
    manifest={
        "OfflineUserAddressInfo",
        "UserIdentifier",
        "TransactionAttribute",
        "StoreAttribute",
        "UserData",
        "UserAttribute",
        "CustomerMatchUserListMetadata",
        "StoreSalesMetadata",
        "StoreSalesThirdPartyMetadata",
    },
)


class OfflineUserAddressInfo(proto.Message):
    r"""Address identifier of offline data.
    Attributes:
        hashed_first_name (str):
            First name of the user, which is hashed as
            SHA-256 after normalized (Lowercase all
            characters; Remove any extra spaces before,
            after, and in between).
        hashed_last_name (str):
            Last name of the user, which is hashed as
            SHA-256 after normalized (lower case only and no
            punctuation).
        city (str):
            City of the address. Only accepted for Store
            Sales Direct data.
        state (str):
            State code of the address. Only accepted for
            Store Sales Direct data.
        country_code (str):
            2-letter country code in ISO-3166-1 alpha-2
            of the user's address.
        postal_code (str):
            Postal code of the user's address.
    """

    hashed_first_name = proto.Field(proto.STRING, number=7, optional=True,)
    hashed_last_name = proto.Field(proto.STRING, number=8, optional=True,)
    city = proto.Field(proto.STRING, number=9, optional=True,)
    state = proto.Field(proto.STRING, number=10, optional=True,)
    country_code = proto.Field(proto.STRING, number=11, optional=True,)
    postal_code = proto.Field(proto.STRING, number=12, optional=True,)


class UserIdentifier(proto.Message):
    r"""Hashed user identifying information.
    Attributes:
        user_identifier_source (google.ads.googleads.v7.enums.types.UserIdentifierSourceEnum.UserIdentifierSource):
            Source of the user identifier when the upload
            is from Store Sales third party partners.
        hashed_email (str):
            Hashed email address using SHA-256 hash
            function after normalization.
        hashed_phone_number (str):
            Hashed phone number using SHA-256 hash
            function after normalization (E164 standard).
        mobile_id (str):
            Mobile device ID (advertising ID/IDFA).
        third_party_user_id (str):
            Advertiser-assigned user ID for Customer
            Match upload, or third-party-assigned user ID
            for SSD.
        address_info (google.ads.googleads.v7.common.types.OfflineUserAddressInfo):
            Address information.
    """

    user_identifier_source = proto.Field(
        proto.ENUM,
        number=6,
        enum=gage_user_identifier_source.UserIdentifierSourceEnum.UserIdentifierSource,
    )
    hashed_email = proto.Field(proto.STRING, number=7, oneof="identifier",)
    hashed_phone_number = proto.Field(
        proto.STRING, number=8, oneof="identifier",
    )
    mobile_id = proto.Field(proto.STRING, number=9, oneof="identifier",)
    third_party_user_id = proto.Field(
        proto.STRING, number=10, oneof="identifier",
    )
    address_info = proto.Field(
        proto.MESSAGE,
        number=5,
        oneof="identifier",
        message="OfflineUserAddressInfo",
    )


class TransactionAttribute(proto.Message):
    r"""Attribute of the store sales transaction.
    Attributes:
        transaction_date_time (str):
            Timestamp when transaction occurred. Required. The format is
            "YYYY-MM-DD HH:MM:SS[+/-HH:MM]", where [+/-HH:MM] is an
            optional timezone offset from UTC. If the offset is absent,
            the API will use the account's timezone as default.
            Examples: "2018-03-05 09:15:00" or "2018-02-01
            14:34:30+03:00".
        transaction_amount_micros (float):
            Transaction amount in micros. Required.
        currency_code (str):
            Transaction currency code. ISO 4217 three-
            etter code is used. Required.
        conversion_action (str):
            The resource name of conversion action to
            report conversions to. Required.
        order_id (str):
            Transaction order id.
            Accessible only to customers on the allow-list.
        store_attribute (google.ads.googleads.v7.common.types.StoreAttribute):
            Store attributes of the transaction.
            Accessible only to customers on the allow-list.
        custom_value (str):
            Value of the custom variable for each
            transaction. Accessible only to customers on the
            allow-list.
    """

    transaction_date_time = proto.Field(proto.STRING, number=8, optional=True,)
    transaction_amount_micros = proto.Field(
        proto.DOUBLE, number=9, optional=True,
    )
    currency_code = proto.Field(proto.STRING, number=10, optional=True,)
    conversion_action = proto.Field(proto.STRING, number=11, optional=True,)
    order_id = proto.Field(proto.STRING, number=12, optional=True,)
    store_attribute = proto.Field(
        proto.MESSAGE, number=6, message="StoreAttribute",
    )
    custom_value = proto.Field(proto.STRING, number=13, optional=True,)


class StoreAttribute(proto.Message):
    r"""Store attributes of the transaction.
    Attributes:
        store_code (str):
            Store code from
            https://support.google.com/business/answer/3370250#storecode
    """

    store_code = proto.Field(proto.STRING, number=2, optional=True,)


class UserData(proto.Message):
    r"""User data holding user identifiers and attributes.
    Attributes:
        user_identifiers (Sequence[google.ads.googleads.v7.common.types.UserIdentifier]):
            User identification info. Required.
        transaction_attribute (google.ads.googleads.v7.common.types.TransactionAttribute):
            Additional transactions/attributes associated
            with the user. Required when updating store
            sales data.
        user_attribute (google.ads.googleads.v7.common.types.UserAttribute):
            Additional attributes associated with the
            user. Required when updating customer match
            attributes. These have an expiration of 540
            days.
    """

    user_identifiers = proto.RepeatedField(
        proto.MESSAGE, number=1, message="UserIdentifier",
    )
    transaction_attribute = proto.Field(
        proto.MESSAGE, number=2, message="TransactionAttribute",
    )
    user_attribute = proto.Field(
        proto.MESSAGE, number=3, message="UserAttribute",
    )


class UserAttribute(proto.Message):
    r"""User attribute, can only be used with CUSTOMER_MATCH_WITH_ATTRIBUTES
    job type.

    Attributes:
        lifetime_value_micros (int):
            Advertiser defined lifetime value for the
            user.
        lifetime_value_bucket (int):
            Advertiser defined lifetime value bucket for
            the user. The valid range for a lifetime value
            bucket is from 1 (low) to 10 (high), except for
            remove operation where 0 will also be accepted.
    """

    lifetime_value_micros = proto.Field(proto.INT64, number=1, optional=True,)
    lifetime_value_bucket = proto.Field(proto.INT32, number=2, optional=True,)


class CustomerMatchUserListMetadata(proto.Message):
    r"""Metadata for customer match user list.
    Attributes:
        user_list (str):
            The resource name of remarketing list to update data.
            Required for job of CUSTOMER_MATCH_USER_LIST type.
    """

    user_list = proto.Field(proto.STRING, number=2, optional=True,)


class StoreSalesMetadata(proto.Message):
    r"""Metadata for Store Sales Direct.
    Attributes:
        loyalty_fraction (float):
            This is the fraction of all transactions that
            are identifiable (i.e., associated with any form
            of customer information). Required.
            The fraction needs to be between 0 and 1
            (excluding 0).
        transaction_upload_fraction (float):
            This is the ratio of sales being uploaded
            compared to the overall sales that can be
            associated with a customer. Required. The
            fraction needs to be between 0 and 1 (excluding
            0). For example, if you upload half the sales
            that you are able to associate with a customer,
            this would be 0.5.
        custom_key (str):
            Name of the store sales custom variable key.
            A predefined key that can be applied to the
            transaction and then later used for custom
            segmentation in reporting.
            Accessible only to customers on the allow-list.
        third_party_metadata (google.ads.googleads.v7.common.types.StoreSalesThirdPartyMetadata):
            Metadata for a third party Store Sales
            upload.
    """

    loyalty_fraction = proto.Field(proto.DOUBLE, number=5, optional=True,)
    transaction_upload_fraction = proto.Field(
        proto.DOUBLE, number=6, optional=True,
    )
    custom_key = proto.Field(proto.STRING, number=7, optional=True,)
    third_party_metadata = proto.Field(
        proto.MESSAGE, number=3, message="StoreSalesThirdPartyMetadata",
    )


class StoreSalesThirdPartyMetadata(proto.Message):
    r"""Metadata for a third party Store Sales.
    This product is only for customers on the allow-list. Please
    contact your Google business development representative for
    details on the upload configuration.

    Attributes:
        advertiser_upload_date_time (str):
            Time the advertiser uploaded the data to the
            partner. Required. The format is "YYYY-MM-DD
            HH:MM:SS". Examples: "2018-03-05 09:15:00" or
            "2018-02-01 14:34:30".
        valid_transaction_fraction (float):
            The fraction of transactions that are valid.
            Invalid transactions may include invalid formats
            or values. Required.
            The fraction needs to be between 0 and 1
            (excluding 0).
        partner_match_fraction (float):
            The fraction of valid transactions that are
            matched to a third party assigned user ID on the
            partner side. Required.
            The fraction needs to be between 0 and 1
            (excluding 0).
        partner_upload_fraction (float):
            The fraction of valid transactions that are
            uploaded by the partner to Google.
            Required.
            The fraction needs to be between 0 and 1
            (excluding 0).
        bridge_map_version_id (str):
            Version of partner IDs to be used for
            uploads. Required.
        partner_id (int):
            ID of the third party partner updating the
            transaction feed.
    """

    advertiser_upload_date_time = proto.Field(
        proto.STRING, number=7, optional=True,
    )
    valid_transaction_fraction = proto.Field(
        proto.DOUBLE, number=8, optional=True,
    )
    partner_match_fraction = proto.Field(proto.DOUBLE, number=9, optional=True,)
    partner_upload_fraction = proto.Field(
        proto.DOUBLE, number=10, optional=True,
    )
    bridge_map_version_id = proto.Field(proto.STRING, number=11, optional=True,)
    partner_id = proto.Field(proto.INT64, number=12, optional=True,)


__all__ = tuple(sorted(__protobuf__.manifest))
