# -*- coding: utf-8 -*-
# Copyright 2025 Google LLC
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
from __future__ import annotations


import proto  # type: ignore


__protobuf__ = proto.module(
    package="google.ads.googleads.v20.errors",
    marshal="google.ads.googleads.v20",
    manifest={
        "ExtensionFeedItemErrorEnum",
    },
)


class ExtensionFeedItemErrorEnum(proto.Message):
    r"""Container for enum describing possible extension feed item
    error.

    """

    class ExtensionFeedItemError(proto.Enum):
        r"""Enum describing possible extension feed item errors.

        Values:
            UNSPECIFIED (0):
                Enum unspecified.
            UNKNOWN (1):
                The received error code is not known in this
                version.
            VALUE_OUT_OF_RANGE (2):
                Value is not within the accepted range.
            URL_LIST_TOO_LONG (3):
                Url list is too long.
            CANNOT_HAVE_RESTRICTION_ON_EMPTY_GEO_TARGETING (4):
                Cannot have a geo targeting restriction
                without having geo targeting.
            CANNOT_SET_WITH_FINAL_URLS (5):
                Cannot simultaneously set sitelink field with
                final urls.
            CANNOT_SET_WITHOUT_FINAL_URLS (6):
                Must set field with final urls.
            INVALID_PHONE_NUMBER (7):
                Phone number for a call extension is invalid.
            PHONE_NUMBER_NOT_SUPPORTED_FOR_COUNTRY (8):
                Phone number for a call extension is not
                supported for the given country code.
            CARRIER_SPECIFIC_SHORT_NUMBER_NOT_ALLOWED (9):
                A carrier specific number in short format is
                not allowed for call extensions.
            PREMIUM_RATE_NUMBER_NOT_ALLOWED (10):
                Premium rate numbers are not allowed for call
                extensions.
            DISALLOWED_NUMBER_TYPE (11):
                Phone number type for a call extension is not
                allowed. For example, personal number is not
                allowed for a call extension in most regions.
            INVALID_DOMESTIC_PHONE_NUMBER_FORMAT (12):
                Phone number for a call extension does not
                meet domestic format requirements.
            VANITY_PHONE_NUMBER_NOT_ALLOWED (13):
                Vanity phone numbers (for example, those
                including letters) are not allowed for call
                extensions.
            INVALID_CALL_CONVERSION_ACTION (14):
                Call conversion action provided for a call
                extension is invalid.
            CUSTOMER_NOT_ON_ALLOWLIST_FOR_CALLTRACKING (47):
                For a call extension, the customer is not on
                the allow-list for call tracking.
            CALLTRACKING_NOT_SUPPORTED_FOR_COUNTRY (16):
                Call tracking is not supported for the given
                country for a call extension.
            CUSTOMER_CONSENT_FOR_CALL_RECORDING_REQUIRED (17):
                Customer hasn't consented for call recording,
                which is required for creating/updating call
                feed items. See
                https://support.google.com/google-ads/answer/7412639.
            INVALID_APP_ID (18):
                App id provided for an app extension is
                invalid.
            QUOTES_IN_REVIEW_EXTENSION_SNIPPET (19):
                Quotation marks present in the review text
                for a review extension.
            HYPHENS_IN_REVIEW_EXTENSION_SNIPPET (20):
                Hyphen character present in the review text
                for a review extension.
            REVIEW_EXTENSION_SOURCE_INELIGIBLE (21):
                A denylisted review source name or url was
                provided for a review extension.
            SOURCE_NAME_IN_REVIEW_EXTENSION_TEXT (22):
                Review source name should not be found in the
                review text.
            INCONSISTENT_CURRENCY_CODES (23):
                Inconsistent currency codes.
            PRICE_EXTENSION_HAS_DUPLICATED_HEADERS (24):
                Price extension cannot have duplicated
                headers.
            PRICE_ITEM_HAS_DUPLICATED_HEADER_AND_DESCRIPTION (25):
                Price item cannot have duplicated header and
                description.
            PRICE_EXTENSION_HAS_TOO_FEW_ITEMS (26):
                Price extension has too few items.
            PRICE_EXTENSION_HAS_TOO_MANY_ITEMS (27):
                Price extension has too many items.
            UNSUPPORTED_VALUE (28):
                The input value is not currently supported.
            UNSUPPORTED_VALUE_IN_SELECTED_LANGUAGE (29):
                The input value is not currently supported in
                the selected language of an extension.
            INVALID_DEVICE_PREFERENCE (30):
                Unknown or unsupported device preference.
            INVALID_SCHEDULE_END (31):
                Invalid feed item schedule end time (for
                example, endHour = 24 and endMinute != 0).
            DATE_TIME_MUST_BE_IN_ACCOUNT_TIME_ZONE (32):
                Date time zone does not match the account's
                time zone.
            INVALID_SNIPPETS_HEADER (33):
                Invalid structured snippet header.
            CANNOT_OPERATE_ON_REMOVED_FEED_ITEM (34):
                Cannot operate on removed feed item.
            PHONE_NUMBER_NOT_SUPPORTED_WITH_CALLTRACKING_FOR_COUNTRY (35):
                Phone number not supported when call tracking
                enabled for country.
            CONFLICTING_CALL_CONVERSION_SETTINGS (36):
                Cannot set call_conversion_action while
                call_conversion_tracking_enabled is set to true.
            EXTENSION_TYPE_MISMATCH (37):
                The type of the input extension feed item
                doesn't match the existing extension feed item.
            EXTENSION_SUBTYPE_REQUIRED (38):
                The oneof field extension for example,
                subtype of extension feed item is required.
            EXTENSION_TYPE_UNSUPPORTED (39):
                The referenced feed item is not mapped to a
                supported extension type.
            CANNOT_OPERATE_ON_FEED_WITH_MULTIPLE_MAPPINGS (40):
                Cannot operate on a Feed with more than one
                active FeedMapping.
            CANNOT_OPERATE_ON_FEED_WITH_KEY_ATTRIBUTES (41):
                Cannot operate on a Feed that has key
                attributes.
            INVALID_PRICE_FORMAT (42):
                Input price is not in a valid format.
            PROMOTION_INVALID_TIME (43):
                The promotion time is invalid.
            TOO_MANY_DECIMAL_PLACES_SPECIFIED (44):
                This field has too many decimal places
                specified.
            CONCRETE_EXTENSION_TYPE_REQUIRED (45):
                Concrete sub type of ExtensionFeedItem is
                required for this operation.
            SCHEDULE_END_NOT_AFTER_START (46):
                Feed item schedule end time must be after
                start time.
        """

        UNSPECIFIED = 0
        UNKNOWN = 1
        VALUE_OUT_OF_RANGE = 2
        URL_LIST_TOO_LONG = 3
        CANNOT_HAVE_RESTRICTION_ON_EMPTY_GEO_TARGETING = 4
        CANNOT_SET_WITH_FINAL_URLS = 5
        CANNOT_SET_WITHOUT_FINAL_URLS = 6
        INVALID_PHONE_NUMBER = 7
        PHONE_NUMBER_NOT_SUPPORTED_FOR_COUNTRY = 8
        CARRIER_SPECIFIC_SHORT_NUMBER_NOT_ALLOWED = 9
        PREMIUM_RATE_NUMBER_NOT_ALLOWED = 10
        DISALLOWED_NUMBER_TYPE = 11
        INVALID_DOMESTIC_PHONE_NUMBER_FORMAT = 12
        VANITY_PHONE_NUMBER_NOT_ALLOWED = 13
        INVALID_CALL_CONVERSION_ACTION = 14
        CUSTOMER_NOT_ON_ALLOWLIST_FOR_CALLTRACKING = 47
        CALLTRACKING_NOT_SUPPORTED_FOR_COUNTRY = 16
        CUSTOMER_CONSENT_FOR_CALL_RECORDING_REQUIRED = 17
        INVALID_APP_ID = 18
        QUOTES_IN_REVIEW_EXTENSION_SNIPPET = 19
        HYPHENS_IN_REVIEW_EXTENSION_SNIPPET = 20
        REVIEW_EXTENSION_SOURCE_INELIGIBLE = 21
        SOURCE_NAME_IN_REVIEW_EXTENSION_TEXT = 22
        INCONSISTENT_CURRENCY_CODES = 23
        PRICE_EXTENSION_HAS_DUPLICATED_HEADERS = 24
        PRICE_ITEM_HAS_DUPLICATED_HEADER_AND_DESCRIPTION = 25
        PRICE_EXTENSION_HAS_TOO_FEW_ITEMS = 26
        PRICE_EXTENSION_HAS_TOO_MANY_ITEMS = 27
        UNSUPPORTED_VALUE = 28
        UNSUPPORTED_VALUE_IN_SELECTED_LANGUAGE = 29
        INVALID_DEVICE_PREFERENCE = 30
        INVALID_SCHEDULE_END = 31
        DATE_TIME_MUST_BE_IN_ACCOUNT_TIME_ZONE = 32
        INVALID_SNIPPETS_HEADER = 33
        CANNOT_OPERATE_ON_REMOVED_FEED_ITEM = 34
        PHONE_NUMBER_NOT_SUPPORTED_WITH_CALLTRACKING_FOR_COUNTRY = 35
        CONFLICTING_CALL_CONVERSION_SETTINGS = 36
        EXTENSION_TYPE_MISMATCH = 37
        EXTENSION_SUBTYPE_REQUIRED = 38
        EXTENSION_TYPE_UNSUPPORTED = 39
        CANNOT_OPERATE_ON_FEED_WITH_MULTIPLE_MAPPINGS = 40
        CANNOT_OPERATE_ON_FEED_WITH_KEY_ATTRIBUTES = 41
        INVALID_PRICE_FORMAT = 42
        PROMOTION_INVALID_TIME = 43
        TOO_MANY_DECIMAL_PLACES_SPECIFIED = 44
        CONCRETE_EXTENSION_TYPE_REQUIRED = 45
        SCHEDULE_END_NOT_AFTER_START = 46


__all__ = tuple(sorted(__protobuf__.manifest))
