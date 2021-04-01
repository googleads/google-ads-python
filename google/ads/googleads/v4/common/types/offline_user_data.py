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


from google.protobuf import wrappers_pb2 as wrappers  # type: ignore


__protobuf__ = proto.module(
    package="google.ads.googleads.v4.common",
    marshal="google.ads.googleads.v4",
    manifest={
        "OfflineUserAddressInfo",
        "UserIdentifier",
        "TransactionAttribute",
        "StoreAttribute",
        "UserData",
        "CustomerMatchUserListMetadata",
        "StoreSalesMetadata",
        "StoreSalesThirdPartyMetadata",
    },
)


class OfflineUserAddressInfo(proto.Message):
    r"""Address identifier of offline data.

    Attributes:
        hashed_first_name (google.protobuf.wrappers_pb2.StringValue):
            First name of the user, which is hashed as
            SHA-256 after normalized (Lowercase all
            characters; Remove any extra spaces before,
            after, and in between).
        hashed_last_name (google.protobuf.wrappers_pb2.StringValue):
            Last name of the user, which is hashed as
            SHA-256 after normalized (lower case only and no
            punctuation).
        city (google.protobuf.wrappers_pb2.StringValue):
            City of the address. Only accepted for Store
            Sales Direct data.
        state (google.protobuf.wrappers_pb2.StringValue):
            State code of the address. Only accepted for
            Store Sales Direct data.
        country_code (google.protobuf.wrappers_pb2.StringValue):
            2-letter country code in ISO-3166-1 alpha-2
            of the user's address.
        postal_code (google.protobuf.wrappers_pb2.StringValue):
            Postal code of the user's address.
    """

    hashed_first_name = proto.Field(
        proto.MESSAGE, number=1, message=wrappers.StringValue,
    )
    hashed_last_name = proto.Field(
        proto.MESSAGE, number=2, message=wrappers.StringValue,
    )
    city = proto.Field(proto.MESSAGE, number=3, message=wrappers.StringValue,)
    state = proto.Field(proto.MESSAGE, number=4, message=wrappers.StringValue,)
    country_code = proto.Field(
        proto.MESSAGE, number=5, message=wrappers.StringValue,
    )
    postal_code = proto.Field(
        proto.MESSAGE, number=6, message=wrappers.StringValue,
    )


class UserIdentifier(proto.Message):
    r"""Hashed user identifying information.

    Attributes:
        hashed_email (google.protobuf.wrappers_pb2.StringValue):
            Hashed email address using SHA-256 hash
            function after normalization.
        hashed_phone_number (google.protobuf.wrappers_pb2.StringValue):
            Hashed phone number using SHA-256 hash
            function after normalization (E164 standard).
        mobile_id (google.protobuf.wrappers_pb2.StringValue):
            Mobile device ID (advertising ID/IDFA).
        third_party_user_id (google.protobuf.wrappers_pb2.StringValue):
            Advertiser-assigned user ID for Customer
            Match upload, or third-party-assigned user ID
            for SSD.
        address_info (google.ads.googleads.v4.common.types.OfflineUserAddressInfo):
            Address information.
    """

    hashed_email = proto.Field(
        proto.MESSAGE,
        number=1,
        oneof="identifier",
        message=wrappers.StringValue,
    )
    hashed_phone_number = proto.Field(
        proto.MESSAGE,
        number=2,
        oneof="identifier",
        message=wrappers.StringValue,
    )
    mobile_id = proto.Field(
        proto.MESSAGE,
        number=3,
        oneof="identifier",
        message=wrappers.StringValue,
    )
    third_party_user_id = proto.Field(
        proto.MESSAGE,
        number=4,
        oneof="identifier",
        message=wrappers.StringValue,
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
        transaction_date_time (google.protobuf.wrappers_pb2.StringValue):
            Timestamp when transaction occurred.
            Required. The format is "YYYY-MM-DD HH:MM:SS".
            Examples: "2018-03-05 09:15:00" or "2018-02-01
            14:34:30".
        transaction_amount_micros (google.protobuf.wrappers_pb2.DoubleValue):
            Transaction amount in micros. Required.
        currency_code (google.protobuf.wrappers_pb2.StringValue):
            Transaction currency code. ISO 4217 three-
            etter code is used. Required.
        conversion_action (google.protobuf.wrappers_pb2.StringValue):
            The resource name of conversion action to
            report conversions to. Required.
        order_id (google.protobuf.wrappers_pb2.StringValue):
            Transaction order id.
            Accessible only to customers on the allow-list.
        store_attribute (google.ads.googleads.v4.common.types.StoreAttribute):
            Store attributes of the transaction.
            Accessible only to customers on the allow-list.
        custom_value (google.protobuf.wrappers_pb2.StringValue):
            Value of the custom variable for each
            transaction. Accessible only to customers on the
            allow-list.
    """

    transaction_date_time = proto.Field(
        proto.MESSAGE, number=1, message=wrappers.StringValue,
    )
    transaction_amount_micros = proto.Field(
        proto.MESSAGE, number=2, message=wrappers.DoubleValue,
    )
    currency_code = proto.Field(
        proto.MESSAGE, number=3, message=wrappers.StringValue,
    )
    conversion_action = proto.Field(
        proto.MESSAGE, number=4, message=wrappers.StringValue,
    )
    order_id = proto.Field(
        proto.MESSAGE, number=5, message=wrappers.StringValue,
    )
    store_attribute = proto.Field(
        proto.MESSAGE, number=6, message="StoreAttribute",
    )
    custom_value = proto.Field(
        proto.MESSAGE, number=7, message=wrappers.StringValue,
    )


class StoreAttribute(proto.Message):
    r"""Store attributes of the transaction.

    Attributes:
        store_code (google.protobuf.wrappers_pb2.StringValue):
            Store code from
            https://support.google.com/business/answer/3370250#storecode
    """

    store_code = proto.Field(
        proto.MESSAGE, number=1, message=wrappers.StringValue,
    )


class UserData(proto.Message):
    r"""User data holding user identifiers and attributes.

    Attributes:
        user_identifiers (Sequence[google.ads.googleads.v4.common.types.UserIdentifier]):
            User identification info. Required.
        transaction_attribute (google.ads.googleads.v4.common.types.TransactionAttribute):
            Additional transactions/attributes associated
            with the user. Required when updating store
            sales data.
    """

    user_identifiers = proto.RepeatedField(
        proto.MESSAGE, number=1, message="UserIdentifier",
    )
    transaction_attribute = proto.Field(
        proto.MESSAGE, number=2, message="TransactionAttribute",
    )


class CustomerMatchUserListMetadata(proto.Message):
    r"""Metadata for customer match user list.

    Attributes:
        user_list (google.protobuf.wrappers_pb2.StringValue):
            The resource name of remarketing list to update data.
            Required for job of CUSTOMER_MATCH_USER_LIST type.
    """

    user_list = proto.Field(
        proto.MESSAGE, number=1, message=wrappers.StringValue,
    )


class StoreSalesMetadata(proto.Message):
    r"""Metadata for Store Sales Direct.

    Attributes:
        loyalty_fraction (google.protobuf.wrappers_pb2.DoubleValue):
            This is the fraction of all transactions that
            are identifiable (i.e., associated with any form
            of customer information). Required.
            The fraction needs to be between 0 and 1
            (excluding 0).
        transaction_upload_fraction (google.protobuf.wrappers_pb2.DoubleValue):
            This is the ratio of sales being uploaded
            compared to the overall sales that can be
            associated with a customer. Required. The
            fraction needs to be between 0 and 1 (excluding
            0). For example, if you upload half the sales
            that you are able to associate with a customer,
            this would be 0.5.
        custom_key (google.protobuf.wrappers_pb2.StringValue):
            Name of the store sales custom variable key.
            A predefined key that can be applied to the
            transaction and then later used for custom
            segmentation in reporting.
            Accessible only to customers on the allow-list.
        third_party_metadata (google.ads.googleads.v4.common.types.StoreSalesThirdPartyMetadata):
            Metadata for a third party Store Sales
            upload.
    """

    loyalty_fraction = proto.Field(
        proto.MESSAGE, number=1, message=wrappers.DoubleValue,
    )
    transaction_upload_fraction = proto.Field(
        proto.MESSAGE, number=2, message=wrappers.DoubleValue,
    )
    custom_key = proto.Field(
        proto.MESSAGE, number=4, message=wrappers.StringValue,
    )
    third_party_metadata = proto.Field(
        proto.MESSAGE, number=3, message="StoreSalesThirdPartyMetadata",
    )


class StoreSalesThirdPartyMetadata(proto.Message):
    r"""Metadata for a third party Store Sales.
    This product is only for customers on the allow-list. Please
    contact your Google business development representative for
    details on the upload configuration.

    Attributes:
        advertiser_upload_date_time (google.protobuf.wrappers_pb2.StringValue):
            Time the advertiser uploaded the data to the
            partner. Required. The format is "YYYY-MM-DD
            HH:MM:SS". Examples: "2018-03-05 09:15:00" or
            "2018-02-01 14:34:30".
        valid_transaction_fraction (google.protobuf.wrappers_pb2.DoubleValue):
            The fraction of transactions that are valid.
            Invalid transactions may include invalid formats
            or values. Required.
            The fraction needs to be between 0 and 1
            (excluding 0).
        partner_match_fraction (google.protobuf.wrappers_pb2.DoubleValue):
            The fraction of valid transactions that are
            matched to a third party assigned user ID on the
            partner side. Required.
            The fraction needs to be between 0 and 1
            (excluding 0).
        partner_upload_fraction (google.protobuf.wrappers_pb2.DoubleValue):
            The fraction of valid transactions that are
            uploaded by the partner to Google.
            Required.
            The fraction needs to be between 0 and 1
            (excluding 0).
        bridge_map_version_id (google.protobuf.wrappers_pb2.StringValue):
            Version of partner IDs to be used for
            uploads. Required.
        partner_id (google.protobuf.wrappers_pb2.Int64Value):
            ID of the third party partner updating the
            transaction feed.
    """

    advertiser_upload_date_time = proto.Field(
        proto.MESSAGE, number=1, message=wrappers.StringValue,
    )
    valid_transaction_fraction = proto.Field(
        proto.MESSAGE, number=2, message=wrappers.DoubleValue,
    )
    partner_match_fraction = proto.Field(
        proto.MESSAGE, number=3, message=wrappers.DoubleValue,
    )
    partner_upload_fraction = proto.Field(
        proto.MESSAGE, number=4, message=wrappers.DoubleValue,
    )
    bridge_map_version_id = proto.Field(
        proto.MESSAGE, number=5, message=wrappers.StringValue,
    )
    partner_id = proto.Field(
        proto.MESSAGE, number=6, message=wrappers.Int64Value,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
