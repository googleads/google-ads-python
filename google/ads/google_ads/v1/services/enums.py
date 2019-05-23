# -*- coding: utf-8 -*-
#
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
"""Wrappers for protocol buffer enum types."""

import enum


class AccessReasonEnum(object):
    class AccessReason(enum.IntEnum):
        """
        Enum describing possible access reasons.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          OWNED (int): The resource is owned by the user.
          SHARED (int): The resource is shared to the user.
          LICENSED (int): The resource is licensed to the user.
          SUBSCRIBED (int): The user subscribed to the resource.
          AFFILIATED (int): The resource is accessible to the user.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        OWNED = 2
        SHARED = 3
        LICENSED = 4
        SUBSCRIBED = 5
        AFFILIATED = 6


class AccountBudgetProposalErrorEnum(object):
    class AccountBudgetProposalError(enum.IntEnum):
        """
        Enum describing possible account budget proposal errors.

        Attributes:
          UNSPECIFIED (int): Enum unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          FIELD_MASK_NOT_ALLOWED (int): The field mask must be empty for create/end/remove proposals.
          IMMUTABLE_FIELD (int): The field cannot be set because of the proposal type.
          REQUIRED_FIELD_MISSING (int): The field is required because of the proposal type.
          CANNOT_CANCEL_APPROVED_PROPOSAL (int): Proposals that have been approved cannot be cancelled.
          CANNOT_REMOVE_UNAPPROVED_BUDGET (int): Budgets that haven't been approved cannot be removed.
          CANNOT_REMOVE_RUNNING_BUDGET (int): Budgets that are currently running cannot be removed.
          CANNOT_END_UNAPPROVED_BUDGET (int): Budgets that haven't been approved cannot be truncated.
          CANNOT_END_INACTIVE_BUDGET (int): Only budgets that are currently running can be truncated.
          BUDGET_NAME_REQUIRED (int): All budgets must have names.
          CANNOT_UPDATE_OLD_BUDGET (int): Expired budgets cannot be edited after a sufficient amount of time has
          passed.
          CANNOT_END_IN_PAST (int): It is not permissible a propose a new budget that ends in the past.
          CANNOT_EXTEND_END_TIME (int): An expired budget cannot be extended to overlap with the running budget.
          PURCHASE_ORDER_NUMBER_REQUIRED (int): A purchase order number is required.
          PENDING_UPDATE_PROPOSAL_EXISTS (int): Budgets that have a pending update cannot be updated.
          MULTIPLE_BUDGETS_NOT_ALLOWED_FOR_UNAPPROVED_BILLING_SETUP (int): Cannot propose more than one budget when the corresponding billing setup
          hasn't been approved.
          CANNOT_UPDATE_START_TIME_FOR_STARTED_BUDGET (int): Cannot update the start time of a budget that has already started.
          SPENDING_LIMIT_LOWER_THAN_ACCRUED_COST_NOT_ALLOWED (int): Cannot update the spending limit of a budget with an amount lower than
          what has already been spent.
          UPDATE_IS_NO_OP (int): Cannot propose a budget update without actually changing any fields.
          END_TIME_MUST_FOLLOW_START_TIME (int): The end time must come after the start time.
          BUDGET_DATE_RANGE_INCOMPATIBLE_WITH_BILLING_SETUP (int): The budget's date range must fall within the date range of its billing
          setup.
          NOT_AUTHORIZED (int): The user is not authorized to mutate budgets for the given billing setup.
          INVALID_BILLING_SETUP (int): Mutates are not allowed for the given billing setup.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        FIELD_MASK_NOT_ALLOWED = 2
        IMMUTABLE_FIELD = 3
        REQUIRED_FIELD_MISSING = 4
        CANNOT_CANCEL_APPROVED_PROPOSAL = 5
        CANNOT_REMOVE_UNAPPROVED_BUDGET = 6
        CANNOT_REMOVE_RUNNING_BUDGET = 7
        CANNOT_END_UNAPPROVED_BUDGET = 8
        CANNOT_END_INACTIVE_BUDGET = 9
        BUDGET_NAME_REQUIRED = 10
        CANNOT_UPDATE_OLD_BUDGET = 11
        CANNOT_END_IN_PAST = 12
        CANNOT_EXTEND_END_TIME = 13
        PURCHASE_ORDER_NUMBER_REQUIRED = 14
        PENDING_UPDATE_PROPOSAL_EXISTS = 15
        MULTIPLE_BUDGETS_NOT_ALLOWED_FOR_UNAPPROVED_BILLING_SETUP = 16
        CANNOT_UPDATE_START_TIME_FOR_STARTED_BUDGET = 17
        SPENDING_LIMIT_LOWER_THAN_ACCRUED_COST_NOT_ALLOWED = 18
        UPDATE_IS_NO_OP = 19
        END_TIME_MUST_FOLLOW_START_TIME = 20
        BUDGET_DATE_RANGE_INCOMPATIBLE_WITH_BILLING_SETUP = 21
        NOT_AUTHORIZED = 22
        INVALID_BILLING_SETUP = 23


class AccountBudgetProposalStatusEnum(object):
    class AccountBudgetProposalStatus(enum.IntEnum):
        """
        The possible statuses of an AccountBudgetProposal.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          PENDING (int): The proposal is pending approval.
          APPROVED_HELD (int): The proposal has been approved but the corresponding billing setup
          has not.  This can occur for proposals that set up the first budget
          when signing up for billing or when performing a change of bill-to
          operation.
          APPROVED (int): The proposal has been approved.
          CANCELLED (int): The proposal has been cancelled by the user.
          REJECTED (int): The proposal has been rejected by the user, e.g. by rejecting an
          acceptance email.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        PENDING = 2
        APPROVED_HELD = 3
        APPROVED = 4
        CANCELLED = 5
        REJECTED = 6


class AccountBudgetProposalTypeEnum(object):
    class AccountBudgetProposalType(enum.IntEnum):
        """
        The possible types of an AccountBudgetProposal.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          CREATE (int): Identifies a request to create a new budget.
          UPDATE (int): Identifies a request to edit an existing budget.
          END (int): Identifies a request to end a budget that has already started.
          REMOVE (int): Identifies a request to remove a budget that hasn't started yet.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        CREATE = 2
        UPDATE = 3
        END = 4
        REMOVE = 5


class AccountBudgetStatusEnum(object):
    class AccountBudgetStatus(enum.IntEnum):
        """
        The possible statuses of an AccountBudget.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          PENDING (int): The account budget is pending approval.
          APPROVED (int): The account budget has been approved.
          CANCELLED (int): The account budget has been cancelled by the user.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        PENDING = 2
        APPROVED = 3
        CANCELLED = 4


class AdCustomizerErrorEnum(object):
    class AdCustomizerError(enum.IntEnum):
        """
        Enum describing possible ad customizer errors.

        Attributes:
          UNSPECIFIED (int): Enum unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          COUNTDOWN_INVALID_DATE_FORMAT (int): Invalid date argument in countdown function.
          COUNTDOWN_DATE_IN_PAST (int): Countdown end date is in the past.
          COUNTDOWN_INVALID_LOCALE (int): Invalid locale string in countdown function.
          COUNTDOWN_INVALID_START_DAYS_BEFORE (int): Days-before argument to countdown function is not positive.
          UNKNOWN_USER_LIST (int): A user list referenced in an IF function does not exist.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        COUNTDOWN_INVALID_DATE_FORMAT = 2
        COUNTDOWN_DATE_IN_PAST = 3
        COUNTDOWN_INVALID_LOCALE = 4
        COUNTDOWN_INVALID_START_DAYS_BEFORE = 5
        UNKNOWN_USER_LIST = 6


class AdCustomizerPlaceholderFieldEnum(object):
    class AdCustomizerPlaceholderField(enum.IntEnum):
        """
        Possible values for Ad Customizers placeholder fields.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          INTEGER (int): Data Type: INT64. Integer value to be inserted.
          PRICE (int): Data Type: STRING. Price value to be inserted.
          DATE (int): Data Type: DATE\_TIME. Date value to be inserted.
          STRING (int): Data Type: STRING. String value to be inserted.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        INTEGER = 2
        PRICE = 3
        DATE = 4
        STRING = 5


class AdErrorEnum(object):
    class AdError(enum.IntEnum):
        """
        Enum describing possible ad errors.

        Attributes:
          UNSPECIFIED (int): Enum unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          AD_CUSTOMIZERS_NOT_SUPPORTED_FOR_AD_TYPE (int): Ad customizers are not supported for ad type.
          APPROXIMATELY_TOO_LONG (int): Estimating character sizes the string is too long.
          APPROXIMATELY_TOO_SHORT (int): Estimating character sizes the string is too short.
          BAD_SNIPPET (int): There is a problem with the snippet.
          CANNOT_MODIFY_AD (int): Cannot modify an ad.
          CANNOT_SET_BUSINESS_NAME_IF_URL_SET (int): business name and url cannot be set at the same time
          CANNOT_SET_FIELD (int): The specified field is incompatible with this ad's type or settings.
          CANNOT_SET_FIELD_WITH_ORIGIN_AD_ID_SET (int): Cannot set field when originAdId is set.
          CANNOT_SET_FIELD_WITH_AD_ID_SET_FOR_SHARING (int): Cannot set field when an existing ad id is set for sharing.
          CANNOT_SET_ALLOW_FLEXIBLE_COLOR_FALSE (int): Cannot set allowFlexibleColor false if no color is provided by user.
          CANNOT_SET_COLOR_CONTROL_WHEN_NATIVE_FORMAT_SETTING (int): When user select native, no color control is allowed because we will
          always respect publisher color for native format serving.
          CANNOT_SET_URL (int): Cannot specify a url for the ad type
          CANNOT_SET_WITHOUT_FINAL_URLS (int): Cannot specify a tracking or mobile url without also setting final urls
          CANNOT_SET_WITH_FINAL_URLS (int): Cannot specify a legacy url and a final url simultaneously
          CANNOT_SET_WITH_URL_DATA (int): Cannot specify a urls in UrlData and in template fields simultaneously.
          CANNOT_USE_AD_SUBCLASS_FOR_OPERATOR (int): This operator cannot be used with a subclass of Ad.
          CUSTOMER_NOT_APPROVED_MOBILEADS (int): Customer is not approved for mobile ads.
          CUSTOMER_NOT_APPROVED_THIRDPARTY_ADS (int): Customer is not approved for 3PAS richmedia ads.
          CUSTOMER_NOT_APPROVED_THIRDPARTY_REDIRECT_ADS (int): Customer is not approved for 3PAS redirect richmedia (Ad Exchange) ads.
          CUSTOMER_NOT_ELIGIBLE (int): Not an eligible customer
          CUSTOMER_NOT_ELIGIBLE_FOR_UPDATING_BEACON_URL (int): Customer is not eligible for updating beacon url
          DIMENSION_ALREADY_IN_UNION (int): There already exists an ad with the same dimensions in the union.
          DIMENSION_MUST_BE_SET (int): Ad's dimension must be set before setting union dimension.
          DIMENSION_NOT_IN_UNION (int): Ad's dimension must be included in the union dimensions.
          DISPLAY_URL_CANNOT_BE_SPECIFIED (int): Display Url cannot be specified (applies to Ad Exchange Ads)
          DOMESTIC_PHONE_NUMBER_FORMAT (int): Telephone number contains invalid characters or invalid format. Please
          re-enter your number using digits (0-9), dashes (-), and parentheses
          only.
          EMERGENCY_PHONE_NUMBER (int): Emergency telephone numbers are not allowed. Please enter a valid
          domestic phone number to connect customers to your business.
          EMPTY_FIELD (int): A required field was not specified or is an empty string.
          FEED_ATTRIBUTE_MUST_HAVE_MAPPING_FOR_TYPE_ID (int): A feed attribute referenced in an ad customizer tag is not in the ad
          customizer mapping for the feed.
          FEED_ATTRIBUTE_MAPPING_TYPE_MISMATCH (int): The ad customizer field mapping for the feed attribute does not match the
          expected field type.
          ILLEGAL_AD_CUSTOMIZER_TAG_USE (int): The use of ad customizer tags in the ad text is disallowed. Details in
          trigger.
          ILLEGAL_TAG_USE (int): Tags of the form {PH\_x}, where x is a number, are disallowed in ad
          text.
          INCONSISTENT_DIMENSIONS (int): The dimensions of the ad are specified or derived in multiple ways and
          are not consistent.
          INCONSISTENT_STATUS_IN_TEMPLATE_UNION (int): The status cannot differ among template ads of the same union.
          INCORRECT_LENGTH (int): The length of the string is not valid.
          INELIGIBLE_FOR_UPGRADE (int): The ad is ineligible for upgrade.
          INVALID_AD_ADDRESS_CAMPAIGN_TARGET (int): User cannot create mobile ad for countries targeted in specified
          campaign.
          INVALID_AD_TYPE (int): Invalid Ad type. A specific type of Ad is required.
          INVALID_ATTRIBUTES_FOR_MOBILE_IMAGE (int): Headline, description or phone cannot be present when creating mobile
          image ad.
          INVALID_ATTRIBUTES_FOR_MOBILE_TEXT (int): Image cannot be present when creating mobile text ad.
          INVALID_CALL_TO_ACTION_TEXT (int): Invalid call to action text.
          INVALID_CHARACTER_FOR_URL (int): Invalid character in URL.
          INVALID_COUNTRY_CODE (int): Creative's country code is not valid.
          INVALID_EXPANDED_DYNAMIC_SEARCH_AD_TAG (int): Invalid use of Expanded Dynamic Search Ads tags ({lpurl} etc.)
          INVALID_INPUT (int): An input error whose real reason was not properly mapped (should not
          happen).
          INVALID_MARKUP_LANGUAGE (int): An invalid markup language was entered.
          INVALID_MOBILE_CARRIER (int): An invalid mobile carrier was entered.
          INVALID_MOBILE_CARRIER_TARGET (int): Specified mobile carriers target a country not targeted by the campaign.
          INVALID_NUMBER_OF_ELEMENTS (int): Wrong number of elements for given element type
          INVALID_PHONE_NUMBER_FORMAT (int): The format of the telephone number is incorrect. Please re-enter the
          number using the correct format.
          INVALID_RICH_MEDIA_CERTIFIED_VENDOR_FORMAT_ID (int): The certified vendor format id is incorrect.
          INVALID_TEMPLATE_DATA (int): The template ad data contains validation errors.
          INVALID_TEMPLATE_ELEMENT_FIELD_TYPE (int): The template field doesn't have have the correct type.
          INVALID_TEMPLATE_ID (int): Invalid template id.
          LINE_TOO_WIDE (int): After substituting replacement strings, the line is too wide.
          MISSING_AD_CUSTOMIZER_MAPPING (int): The feed referenced must have ad customizer mapping to be used in a
          customizer tag.
          MISSING_ADDRESS_COMPONENT (int): Missing address component in template element address field.
          MISSING_ADVERTISEMENT_NAME (int): An ad name must be entered.
          MISSING_BUSINESS_NAME (int): Business name must be entered.
          MISSING_DESCRIPTION1 (int): Description (line 2) must be entered.
          MISSING_DESCRIPTION2 (int): Description (line 3) must be entered.
          MISSING_DESTINATION_URL_TAG (int): The destination url must contain at least one tag (e.g. {lpurl})
          MISSING_LANDING_PAGE_URL_TAG (int): The tracking url template of ExpandedDynamicSearchAd must contain at
          least one tag. (e.g. {lpurl})
          MISSING_DIMENSION (int): A valid dimension must be specified for this ad.
          MISSING_DISPLAY_URL (int): A display URL must be entered.
          MISSING_HEADLINE (int): Headline must be entered.
          MISSING_HEIGHT (int): A height must be entered.
          MISSING_IMAGE (int): An image must be entered.
          MISSING_MARKETING_IMAGE_OR_PRODUCT_VIDEOS (int): Marketing image or product videos are required.
          MISSING_MARKUP_LANGUAGES (int): The markup language in which your site is written must be entered.
          MISSING_MOBILE_CARRIER (int): A mobile carrier must be entered.
          MISSING_PHONE (int): Phone number must be entered.
          MISSING_REQUIRED_TEMPLATE_FIELDS (int): Missing required template fields
          MISSING_TEMPLATE_FIELD_VALUE (int): Missing a required field value
          MISSING_TEXT (int): The ad must have text.
          MISSING_VISIBLE_URL (int): A visible URL must be entered.
          MISSING_WIDTH (int): A width must be entered.
          MULTIPLE_DISTINCT_FEEDS_UNSUPPORTED (int): Only 1 feed can be used as the source of ad customizer substitutions in a
          single ad.
          MUST_USE_TEMP_AD_UNION_ID_ON_ADD (int): TempAdUnionId must be use when adding template ads.
          TOO_LONG (int): The string has too many characters.
          TOO_SHORT (int): The string has too few characters.
          UNION_DIMENSIONS_CANNOT_CHANGE (int): Ad union dimensions cannot change for saved ads.
          UNKNOWN_ADDRESS_COMPONENT (int): Address component is not {country, lat, lng}.
          UNKNOWN_FIELD_NAME (int): Unknown unique field name
          UNKNOWN_UNIQUE_NAME (int): Unknown unique name (template element type specifier)
          UNSUPPORTED_DIMENSIONS (int): Unsupported ad dimension
          URL_INVALID_SCHEME (int): URL starts with an invalid scheme.
          URL_INVALID_TOP_LEVEL_DOMAIN (int): URL ends with an invalid top-level domain name.
          URL_MALFORMED (int): URL contains illegal characters.
          URL_NO_HOST (int): URL must contain a host name.
          URL_NOT_EQUIVALENT (int): URL not equivalent during upgrade.
          URL_HOST_NAME_TOO_LONG (int): URL host name too long to be stored as visible URL (applies to Ad
          Exchange ads)
          URL_NO_SCHEME (int): URL must start with a scheme.
          URL_NO_TOP_LEVEL_DOMAIN (int): URL should end in a valid domain extension, such as .com or .net.
          URL_PATH_NOT_ALLOWED (int): URL must not end with a path.
          URL_PORT_NOT_ALLOWED (int): URL must not specify a port.
          URL_QUERY_NOT_ALLOWED (int): URL must not contain a query.
          URL_SCHEME_BEFORE_EXPANDED_DYNAMIC_SEARCH_AD_TAG (int): A url scheme is not allowed in front of tag in tracking url template
          (e.g. http://{lpurl})
          USER_DOES_NOT_HAVE_ACCESS_TO_TEMPLATE (int): The user does not have permissions to create a template ad for the given
          template.
          INCONSISTENT_EXPANDABLE_SETTINGS (int): Expandable setting is inconsistent/wrong. For example, an AdX ad is
          invalid if it has a expandable vendor format but no expanding directions
          specified, or expanding directions is specified, but the vendor format is
          not expandable.
          INVALID_FORMAT (int): Format is invalid
          INVALID_FIELD_TEXT (int): The text of this field did not match a pattern of allowed values.
          ELEMENT_NOT_PRESENT (int): Template element is mising
          IMAGE_ERROR (int): Error occurred during image processing
          VALUE_NOT_IN_RANGE (int): The value is not within the valid range
          FIELD_NOT_PRESENT (int): Template element field is not present
          ADDRESS_NOT_COMPLETE (int): Address is incomplete
          ADDRESS_INVALID (int): Invalid address
          VIDEO_RETRIEVAL_ERROR (int): Error retrieving specified video
          AUDIO_ERROR (int): Error processing audio
          INVALID_YOUTUBE_DISPLAY_URL (int): Display URL is incorrect for YouTube PYV ads
          TOO_MANY_PRODUCT_IMAGES (int): Too many product Images in GmailAd
          TOO_MANY_PRODUCT_VIDEOS (int): Too many product Videos in GmailAd
          INCOMPATIBLE_AD_TYPE_AND_DEVICE_PREFERENCE (int): The device preference is not compatible with the ad type
          CALLTRACKING_NOT_SUPPORTED_FOR_COUNTRY (int): Call tracking is not supported for specified country.
          CARRIER_SPECIFIC_SHORT_NUMBER_NOT_ALLOWED (int): Carrier specific short number is not allowed.
          DISALLOWED_NUMBER_TYPE (int): Specified phone number type is disallowed.
          PHONE_NUMBER_NOT_SUPPORTED_FOR_COUNTRY (int): Phone number not supported for country.
          PHONE_NUMBER_NOT_SUPPORTED_WITH_CALLTRACKING_FOR_COUNTRY (int): Phone number not supported with call tracking enabled for country.
          PREMIUM_RATE_NUMBER_NOT_ALLOWED (int): Premium rate phone number is not allowed.
          VANITY_PHONE_NUMBER_NOT_ALLOWED (int): Vanity phone number is not allowed.
          INVALID_CALL_CONVERSION_TYPE_ID (int): Invalid call conversion type id.
          CANNOT_DISABLE_CALL_CONVERSION_AND_SET_CONVERSION_TYPE_ID (int): Cannot disable call conversion and set conversion type id.
          CANNOT_SET_PATH2_WITHOUT_PATH1 (int): Cannot set path2 without path1.
          MISSING_DYNAMIC_SEARCH_ADS_SETTING_DOMAIN_NAME (int): Missing domain name in campaign setting when adding expanded dynamic
          search ad.
          INCOMPATIBLE_WITH_RESTRICTION_TYPE (int): The associated ad is not compatible with restriction type.
          CUSTOMER_CONSENT_FOR_CALL_RECORDING_REQUIRED (int): Consent for call recording is required for creating/updating call only
          ads. Please see https://support.google.com/google-ads/answer/7412639.
          MISSING_IMAGE_OR_MEDIA_BUNDLE (int): Either an image or a media bundle is required in a display upload ad.
          PRODUCT_TYPE_NOT_SUPPORTED_IN_THIS_CAMPAIGN (int): The display upload product type is not supported in this campaign.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        AD_CUSTOMIZERS_NOT_SUPPORTED_FOR_AD_TYPE = 2
        APPROXIMATELY_TOO_LONG = 3
        APPROXIMATELY_TOO_SHORT = 4
        BAD_SNIPPET = 5
        CANNOT_MODIFY_AD = 6
        CANNOT_SET_BUSINESS_NAME_IF_URL_SET = 7
        CANNOT_SET_FIELD = 8
        CANNOT_SET_FIELD_WITH_ORIGIN_AD_ID_SET = 9
        CANNOT_SET_FIELD_WITH_AD_ID_SET_FOR_SHARING = 10
        CANNOT_SET_ALLOW_FLEXIBLE_COLOR_FALSE = 11
        CANNOT_SET_COLOR_CONTROL_WHEN_NATIVE_FORMAT_SETTING = 12
        CANNOT_SET_URL = 13
        CANNOT_SET_WITHOUT_FINAL_URLS = 14
        CANNOT_SET_WITH_FINAL_URLS = 15
        CANNOT_SET_WITH_URL_DATA = 17
        CANNOT_USE_AD_SUBCLASS_FOR_OPERATOR = 18
        CUSTOMER_NOT_APPROVED_MOBILEADS = 19
        CUSTOMER_NOT_APPROVED_THIRDPARTY_ADS = 20
        CUSTOMER_NOT_APPROVED_THIRDPARTY_REDIRECT_ADS = 21
        CUSTOMER_NOT_ELIGIBLE = 22
        CUSTOMER_NOT_ELIGIBLE_FOR_UPDATING_BEACON_URL = 23
        DIMENSION_ALREADY_IN_UNION = 24
        DIMENSION_MUST_BE_SET = 25
        DIMENSION_NOT_IN_UNION = 26
        DISPLAY_URL_CANNOT_BE_SPECIFIED = 27
        DOMESTIC_PHONE_NUMBER_FORMAT = 28
        EMERGENCY_PHONE_NUMBER = 29
        EMPTY_FIELD = 30
        FEED_ATTRIBUTE_MUST_HAVE_MAPPING_FOR_TYPE_ID = 31
        FEED_ATTRIBUTE_MAPPING_TYPE_MISMATCH = 32
        ILLEGAL_AD_CUSTOMIZER_TAG_USE = 33
        ILLEGAL_TAG_USE = 34
        INCONSISTENT_DIMENSIONS = 35
        INCONSISTENT_STATUS_IN_TEMPLATE_UNION = 36
        INCORRECT_LENGTH = 37
        INELIGIBLE_FOR_UPGRADE = 38
        INVALID_AD_ADDRESS_CAMPAIGN_TARGET = 39
        INVALID_AD_TYPE = 40
        INVALID_ATTRIBUTES_FOR_MOBILE_IMAGE = 41
        INVALID_ATTRIBUTES_FOR_MOBILE_TEXT = 42
        INVALID_CALL_TO_ACTION_TEXT = 43
        INVALID_CHARACTER_FOR_URL = 44
        INVALID_COUNTRY_CODE = 45
        INVALID_EXPANDED_DYNAMIC_SEARCH_AD_TAG = 47
        INVALID_INPUT = 48
        INVALID_MARKUP_LANGUAGE = 49
        INVALID_MOBILE_CARRIER = 50
        INVALID_MOBILE_CARRIER_TARGET = 51
        INVALID_NUMBER_OF_ELEMENTS = 52
        INVALID_PHONE_NUMBER_FORMAT = 53
        INVALID_RICH_MEDIA_CERTIFIED_VENDOR_FORMAT_ID = 54
        INVALID_TEMPLATE_DATA = 55
        INVALID_TEMPLATE_ELEMENT_FIELD_TYPE = 56
        INVALID_TEMPLATE_ID = 57
        LINE_TOO_WIDE = 58
        MISSING_AD_CUSTOMIZER_MAPPING = 59
        MISSING_ADDRESS_COMPONENT = 60
        MISSING_ADVERTISEMENT_NAME = 61
        MISSING_BUSINESS_NAME = 62
        MISSING_DESCRIPTION1 = 63
        MISSING_DESCRIPTION2 = 64
        MISSING_DESTINATION_URL_TAG = 65
        MISSING_LANDING_PAGE_URL_TAG = 66
        MISSING_DIMENSION = 67
        MISSING_DISPLAY_URL = 68
        MISSING_HEADLINE = 69
        MISSING_HEIGHT = 70
        MISSING_IMAGE = 71
        MISSING_MARKETING_IMAGE_OR_PRODUCT_VIDEOS = 72
        MISSING_MARKUP_LANGUAGES = 73
        MISSING_MOBILE_CARRIER = 74
        MISSING_PHONE = 75
        MISSING_REQUIRED_TEMPLATE_FIELDS = 76
        MISSING_TEMPLATE_FIELD_VALUE = 77
        MISSING_TEXT = 78
        MISSING_VISIBLE_URL = 79
        MISSING_WIDTH = 80
        MULTIPLE_DISTINCT_FEEDS_UNSUPPORTED = 81
        MUST_USE_TEMP_AD_UNION_ID_ON_ADD = 82
        TOO_LONG = 83
        TOO_SHORT = 84
        UNION_DIMENSIONS_CANNOT_CHANGE = 85
        UNKNOWN_ADDRESS_COMPONENT = 86
        UNKNOWN_FIELD_NAME = 87
        UNKNOWN_UNIQUE_NAME = 88
        UNSUPPORTED_DIMENSIONS = 89
        URL_INVALID_SCHEME = 90
        URL_INVALID_TOP_LEVEL_DOMAIN = 91
        URL_MALFORMED = 92
        URL_NO_HOST = 93
        URL_NOT_EQUIVALENT = 94
        URL_HOST_NAME_TOO_LONG = 95
        URL_NO_SCHEME = 96
        URL_NO_TOP_LEVEL_DOMAIN = 97
        URL_PATH_NOT_ALLOWED = 98
        URL_PORT_NOT_ALLOWED = 99
        URL_QUERY_NOT_ALLOWED = 100
        URL_SCHEME_BEFORE_EXPANDED_DYNAMIC_SEARCH_AD_TAG = 102
        USER_DOES_NOT_HAVE_ACCESS_TO_TEMPLATE = 103
        INCONSISTENT_EXPANDABLE_SETTINGS = 104
        INVALID_FORMAT = 105
        INVALID_FIELD_TEXT = 106
        ELEMENT_NOT_PRESENT = 107
        IMAGE_ERROR = 108
        VALUE_NOT_IN_RANGE = 109
        FIELD_NOT_PRESENT = 110
        ADDRESS_NOT_COMPLETE = 111
        ADDRESS_INVALID = 112
        VIDEO_RETRIEVAL_ERROR = 113
        AUDIO_ERROR = 114
        INVALID_YOUTUBE_DISPLAY_URL = 115
        TOO_MANY_PRODUCT_IMAGES = 116
        TOO_MANY_PRODUCT_VIDEOS = 117
        INCOMPATIBLE_AD_TYPE_AND_DEVICE_PREFERENCE = 118
        CALLTRACKING_NOT_SUPPORTED_FOR_COUNTRY = 119
        CARRIER_SPECIFIC_SHORT_NUMBER_NOT_ALLOWED = 120
        DISALLOWED_NUMBER_TYPE = 121
        PHONE_NUMBER_NOT_SUPPORTED_FOR_COUNTRY = 122
        PHONE_NUMBER_NOT_SUPPORTED_WITH_CALLTRACKING_FOR_COUNTRY = 123
        PREMIUM_RATE_NUMBER_NOT_ALLOWED = 124
        VANITY_PHONE_NUMBER_NOT_ALLOWED = 125
        INVALID_CALL_CONVERSION_TYPE_ID = 126
        CANNOT_DISABLE_CALL_CONVERSION_AND_SET_CONVERSION_TYPE_ID = 127
        CANNOT_SET_PATH2_WITHOUT_PATH1 = 128
        MISSING_DYNAMIC_SEARCH_ADS_SETTING_DOMAIN_NAME = 129
        INCOMPATIBLE_WITH_RESTRICTION_TYPE = 130
        CUSTOMER_CONSENT_FOR_CALL_RECORDING_REQUIRED = 131
        MISSING_IMAGE_OR_MEDIA_BUNDLE = 132
        PRODUCT_TYPE_NOT_SUPPORTED_IN_THIS_CAMPAIGN = 133


class AdGroupAdErrorEnum(object):
    class AdGroupAdError(enum.IntEnum):
        """
        Enum describing possible ad group ad errors.

        Attributes:
          UNSPECIFIED (int): Enum unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          AD_GROUP_AD_LABEL_DOES_NOT_EXIST (int): No link found between the adgroup ad and the label.
          AD_GROUP_AD_LABEL_ALREADY_EXISTS (int): The label has already been attached to the adgroup ad.
          AD_NOT_UNDER_ADGROUP (int): The specified ad was not found in the adgroup
          CANNOT_OPERATE_ON_REMOVED_ADGROUPAD (int): Removed ads may not be modified
          CANNOT_CREATE_DEPRECATED_ADS (int): An ad of this type is deprecated and cannot be created. Only deletions
          are permitted.
          CANNOT_CREATE_TEXT_ADS (int): Text ads are deprecated and cannot be created. Use expanded text ads
          instead.
          EMPTY_FIELD (int): A required field was not specified or is an empty string.
          RESOURCE_REFERENCED_IN_MULTIPLE_OPS (int): An ad may only be modified once per call
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        AD_GROUP_AD_LABEL_DOES_NOT_EXIST = 2
        AD_GROUP_AD_LABEL_ALREADY_EXISTS = 3
        AD_NOT_UNDER_ADGROUP = 4
        CANNOT_OPERATE_ON_REMOVED_ADGROUPAD = 5
        CANNOT_CREATE_DEPRECATED_ADS = 6
        CANNOT_CREATE_TEXT_ADS = 7
        EMPTY_FIELD = 8
        RESOURCE_REFERENCED_IN_MULTIPLE_OPS = 9


class AdGroupAdRotationModeEnum(object):
    class AdGroupAdRotationMode(enum.IntEnum):
        """
        The possible ad rotation modes of an ad group.

        Attributes:
          UNSPECIFIED (int): The ad rotation mode has not been specified.
          UNKNOWN (int): The received value is not known in this version.

          This is a response-only value.
          OPTIMIZE (int): Optimize ad group ads based on clicks or conversions.
          ROTATE_FOREVER (int): Rotate evenly forever.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        OPTIMIZE = 2
        ROTATE_FOREVER = 3


class AdGroupAdStatusEnum(object):
    class AdGroupAdStatus(enum.IntEnum):
        """
        The possible statuses of an AdGroupAd.

        Attributes:
          UNSPECIFIED (int): No value has been specified.
          UNKNOWN (int): The received value is not known in this version.

          This is a response-only value.
          ENABLED (int): The ad group ad is enabled.
          PAUSED (int): The ad group ad is paused.
          REMOVED (int): The ad group ad is removed.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        ENABLED = 2
        PAUSED = 3
        REMOVED = 4


class AdGroupBidModifierErrorEnum(object):
    class AdGroupBidModifierError(enum.IntEnum):
        """
        Enum describing possible ad group bid modifier errors.

        Attributes:
          UNSPECIFIED (int): Enum unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          CRITERION_ID_NOT_SUPPORTED (int): The criterion ID does not support bid modification.
          CANNOT_OVERRIDE_OPTED_OUT_CAMPAIGN_CRITERION_BID_MODIFIER (int): Cannot override the bid modifier for the given criterion ID if the parent
          campaign is opted out of the same criterion.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        CRITERION_ID_NOT_SUPPORTED = 2
        CANNOT_OVERRIDE_OPTED_OUT_CAMPAIGN_CRITERION_BID_MODIFIER = 3


class AdGroupCriterionApprovalStatusEnum(object):
    class AdGroupCriterionApprovalStatus(enum.IntEnum):
        """
        Enumerates AdGroupCriterion approval statuses.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): The value is unknown in this version.
          APPROVED (int): Approved.
          DISAPPROVED (int): Disapproved.
          PENDING_REVIEW (int): Pending Review.
          UNDER_REVIEW (int): Under review.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        APPROVED = 2
        DISAPPROVED = 3
        PENDING_REVIEW = 4
        UNDER_REVIEW = 5


class AdGroupCriterionErrorEnum(object):
    class AdGroupCriterionError(enum.IntEnum):
        """
        Enum describing possible ad group criterion errors.

        Attributes:
          UNSPECIFIED (int): Enum unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          AD_GROUP_CRITERION_LABEL_DOES_NOT_EXIST (int): No link found between the AdGroupCriterion and the label.
          AD_GROUP_CRITERION_LABEL_ALREADY_EXISTS (int): The label has already been attached to the AdGroupCriterion.
          CANNOT_ADD_LABEL_TO_NEGATIVE_CRITERION (int): Negative AdGroupCriterion cannot have labels.
          TOO_MANY_OPERATIONS (int): Too many operations for a single call.
          CANT_UPDATE_NEGATIVE (int): Negative ad group criteria are not updateable.
          CONCRETE_TYPE_REQUIRED (int): Concrete type of criterion (keyword v.s. placement) is required for ADD
          and SET operations.
          BID_INCOMPATIBLE_WITH_ADGROUP (int): Bid is incompatible with ad group's bidding settings.
          CANNOT_TARGET_AND_EXCLUDE (int): Cannot target and exclude the same criterion at once.
          ILLEGAL_URL (int): The URL of a placement is invalid.
          INVALID_KEYWORD_TEXT (int): Keyword text was invalid.
          INVALID_DESTINATION_URL (int): Destination URL was invalid.
          MISSING_DESTINATION_URL_TAG (int): The destination url must contain at least one tag (e.g. {lpurl})
          KEYWORD_LEVEL_BID_NOT_SUPPORTED_FOR_MANUALCPM (int): Keyword-level cpm bid is not supported
          INVALID_USER_STATUS (int): For example, cannot add a biddable ad group criterion that had been
          removed.
          CANNOT_ADD_CRITERIA_TYPE (int): Criteria type cannot be targeted for the ad group. Either the account is
          restricted to keywords only, the criteria type is incompatible with the
          campaign's bidding strategy, or the criteria type can only be applied to
          campaigns.
          CANNOT_EXCLUDE_CRITERIA_TYPE (int): Criteria type cannot be excluded for the ad group. Refer to the
          documentation for a specific criterion to check if it is excludable.
          CAMPAIGN_TYPE_NOT_COMPATIBLE_WITH_PARTIAL_FAILURE (int): Partial failure is not supported for shopping campaign mutate operations.
          OPERATIONS_FOR_TOO_MANY_SHOPPING_ADGROUPS (int): Operations in the mutate request changes too many shopping ad groups.
          Please split requests for multiple shopping ad groups across multiple
          requests.
          CANNOT_MODIFY_URL_FIELDS_WITH_DUPLICATE_ELEMENTS (int): Not allowed to modify url fields of an ad group criterion if there are
          duplicate elements for that ad group criterion in the request.
          CANNOT_SET_WITHOUT_FINAL_URLS (int): Cannot set url fields without also setting final urls.
          CANNOT_CLEAR_FINAL_URLS_IF_FINAL_MOBILE_URLS_EXIST (int): Cannot clear final urls if final mobile urls exist.
          CANNOT_CLEAR_FINAL_URLS_IF_FINAL_APP_URLS_EXIST (int): Cannot clear final urls if final app urls exist.
          CANNOT_CLEAR_FINAL_URLS_IF_TRACKING_URL_TEMPLATE_EXISTS (int): Cannot clear final urls if tracking url template exists.
          CANNOT_CLEAR_FINAL_URLS_IF_URL_CUSTOM_PARAMETERS_EXIST (int): Cannot clear final urls if url custom parameters exist.
          CANNOT_SET_BOTH_DESTINATION_URL_AND_FINAL_URLS (int): Cannot set both destination url and final urls.
          CANNOT_SET_BOTH_DESTINATION_URL_AND_TRACKING_URL_TEMPLATE (int): Cannot set both destination url and tracking url template.
          FINAL_URLS_NOT_SUPPORTED_FOR_CRITERION_TYPE (int): Final urls are not supported for this criterion type.
          FINAL_MOBILE_URLS_NOT_SUPPORTED_FOR_CRITERION_TYPE (int): Final mobile urls are not supported for this criterion type.
          INVALID_LISTING_GROUP_HIERARCHY (int): Ad group is invalid due to the listing groups it contains.
          LISTING_GROUP_UNIT_CANNOT_HAVE_CHILDREN (int): Listing group unit cannot have children.
          LISTING_GROUP_SUBDIVISION_REQUIRES_OTHERS_CASE (int): Subdivided listing groups must have an "others" case.
          LISTING_GROUP_REQUIRES_SAME_DIMENSION_TYPE_AS_SIBLINGS (int): Dimension type of listing group must be the same as that of its siblings.
          LISTING_GROUP_ALREADY_EXISTS (int): Listing group cannot be added to the ad group because it already exists.
          LISTING_GROUP_DOES_NOT_EXIST (int): Listing group referenced in the operation was not found in the ad group.
          LISTING_GROUP_CANNOT_BE_REMOVED (int): Recursive removal failed because listing group subdivision is being
          created or modified in this request.
          INVALID_LISTING_GROUP_TYPE (int): Listing group type is not allowed for specified ad group criterion type.
          LISTING_GROUP_ADD_MAY_ONLY_USE_TEMP_ID (int): Listing group in an ADD operation specifies a non temporary criterion id.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        AD_GROUP_CRITERION_LABEL_DOES_NOT_EXIST = 2
        AD_GROUP_CRITERION_LABEL_ALREADY_EXISTS = 3
        CANNOT_ADD_LABEL_TO_NEGATIVE_CRITERION = 4
        TOO_MANY_OPERATIONS = 5
        CANT_UPDATE_NEGATIVE = 6
        CONCRETE_TYPE_REQUIRED = 7
        BID_INCOMPATIBLE_WITH_ADGROUP = 8
        CANNOT_TARGET_AND_EXCLUDE = 9
        ILLEGAL_URL = 10
        INVALID_KEYWORD_TEXT = 11
        INVALID_DESTINATION_URL = 12
        MISSING_DESTINATION_URL_TAG = 13
        KEYWORD_LEVEL_BID_NOT_SUPPORTED_FOR_MANUALCPM = 14
        INVALID_USER_STATUS = 15
        CANNOT_ADD_CRITERIA_TYPE = 16
        CANNOT_EXCLUDE_CRITERIA_TYPE = 17
        CAMPAIGN_TYPE_NOT_COMPATIBLE_WITH_PARTIAL_FAILURE = 27
        OPERATIONS_FOR_TOO_MANY_SHOPPING_ADGROUPS = 28
        CANNOT_MODIFY_URL_FIELDS_WITH_DUPLICATE_ELEMENTS = 29
        CANNOT_SET_WITHOUT_FINAL_URLS = 30
        CANNOT_CLEAR_FINAL_URLS_IF_FINAL_MOBILE_URLS_EXIST = 31
        CANNOT_CLEAR_FINAL_URLS_IF_FINAL_APP_URLS_EXIST = 32
        CANNOT_CLEAR_FINAL_URLS_IF_TRACKING_URL_TEMPLATE_EXISTS = 33
        CANNOT_CLEAR_FINAL_URLS_IF_URL_CUSTOM_PARAMETERS_EXIST = 34
        CANNOT_SET_BOTH_DESTINATION_URL_AND_FINAL_URLS = 35
        CANNOT_SET_BOTH_DESTINATION_URL_AND_TRACKING_URL_TEMPLATE = 36
        FINAL_URLS_NOT_SUPPORTED_FOR_CRITERION_TYPE = 37
        FINAL_MOBILE_URLS_NOT_SUPPORTED_FOR_CRITERION_TYPE = 38
        INVALID_LISTING_GROUP_HIERARCHY = 39
        LISTING_GROUP_UNIT_CANNOT_HAVE_CHILDREN = 40
        LISTING_GROUP_SUBDIVISION_REQUIRES_OTHERS_CASE = 41
        LISTING_GROUP_REQUIRES_SAME_DIMENSION_TYPE_AS_SIBLINGS = 42
        LISTING_GROUP_ALREADY_EXISTS = 43
        LISTING_GROUP_DOES_NOT_EXIST = 44
        LISTING_GROUP_CANNOT_BE_REMOVED = 45
        INVALID_LISTING_GROUP_TYPE = 46
        LISTING_GROUP_ADD_MAY_ONLY_USE_TEMP_ID = 47


class AdGroupCriterionStatusEnum(object):
    class AdGroupCriterionStatus(enum.IntEnum):
        """
        The possible statuses of an AdGroupCriterion.

        Attributes:
          UNSPECIFIED (int): No value has been specified.
          UNKNOWN (int): The received value is not known in this version.

          This is a response-only value.
          ENABLED (int): The ad group criterion is enabled.
          PAUSED (int): The ad group criterion is paused.
          REMOVED (int): The ad group criterion is removed.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        ENABLED = 2
        PAUSED = 3
        REMOVED = 4


class AdGroupErrorEnum(object):
    class AdGroupError(enum.IntEnum):
        """
        Enum describing possible ad group errors.

        Attributes:
          UNSPECIFIED (int): Enum unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          DUPLICATE_ADGROUP_NAME (int): AdGroup with the same name already exists for the campaign.
          INVALID_ADGROUP_NAME (int): AdGroup name is not valid.
          ADVERTISER_NOT_ON_CONTENT_NETWORK (int): Advertiser is not allowed to target sites or set site bids that are not
          on the Google Search Network.
          BID_TOO_BIG (int): Bid amount is too big.
          BID_TYPE_AND_BIDDING_STRATEGY_MISMATCH (int): AdGroup bid does not match the campaign's bidding strategy.
          MISSING_ADGROUP_NAME (int): AdGroup name is required for Add.
          ADGROUP_LABEL_DOES_NOT_EXIST (int): No link found between the ad group and the label.
          ADGROUP_LABEL_ALREADY_EXISTS (int): The label has already been attached to the ad group.
          INVALID_CONTENT_BID_CRITERION_TYPE_GROUP (int): The CriterionTypeGroup is not supported for the content bid dimension.
          AD_GROUP_TYPE_NOT_VALID_FOR_ADVERTISING_CHANNEL_TYPE (int): The ad group type is not compatible with the campaign channel type.
          ADGROUP_TYPE_NOT_SUPPORTED_FOR_CAMPAIGN_SALES_COUNTRY (int): The ad group type is not supported in the country of sale of the
          campaign.
          CANNOT_ADD_ADGROUP_OF_TYPE_DSA_TO_CAMPAIGN_WITHOUT_DSA_SETTING (int): Ad groups of AdGroupType.SEARCH\_DYNAMIC\_ADS can only be added to
          campaigns that have DynamicSearchAdsSetting attached.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        DUPLICATE_ADGROUP_NAME = 2
        INVALID_ADGROUP_NAME = 3
        ADVERTISER_NOT_ON_CONTENT_NETWORK = 5
        BID_TOO_BIG = 6
        BID_TYPE_AND_BIDDING_STRATEGY_MISMATCH = 7
        MISSING_ADGROUP_NAME = 8
        ADGROUP_LABEL_DOES_NOT_EXIST = 9
        ADGROUP_LABEL_ALREADY_EXISTS = 10
        INVALID_CONTENT_BID_CRITERION_TYPE_GROUP = 11
        AD_GROUP_TYPE_NOT_VALID_FOR_ADVERTISING_CHANNEL_TYPE = 12
        ADGROUP_TYPE_NOT_SUPPORTED_FOR_CAMPAIGN_SALES_COUNTRY = 13
        CANNOT_ADD_ADGROUP_OF_TYPE_DSA_TO_CAMPAIGN_WITHOUT_DSA_SETTING = 14


class AdGroupFeedErrorEnum(object):
    class AdGroupFeedError(enum.IntEnum):
        """
        Enum describing possible ad group feed errors.

        Attributes:
          UNSPECIFIED (int): Enum unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          FEED_ALREADY_EXISTS_FOR_PLACEHOLDER_TYPE (int): An active feed already exists for this ad group and place holder type.
          CANNOT_CREATE_FOR_REMOVED_FEED (int): The specified feed is removed.
          ADGROUP_FEED_ALREADY_EXISTS (int): The AdGroupFeed already exists. UPDATE operation should be used to modify
          the existing AdGroupFeed.
          CANNOT_OPERATE_ON_REMOVED_ADGROUP_FEED (int): Cannot operate on removed AdGroupFeed.
          INVALID_PLACEHOLDER_TYPE (int): Invalid placeholder type.
          MISSING_FEEDMAPPING_FOR_PLACEHOLDER_TYPE (int): Feed mapping for this placeholder type does not exist.
          NO_EXISTING_LOCATION_CUSTOMER_FEED (int): Location AdGroupFeeds cannot be created unless there is a location
          CustomerFeed for the specified feed.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        FEED_ALREADY_EXISTS_FOR_PLACEHOLDER_TYPE = 2
        CANNOT_CREATE_FOR_REMOVED_FEED = 3
        ADGROUP_FEED_ALREADY_EXISTS = 4
        CANNOT_OPERATE_ON_REMOVED_ADGROUP_FEED = 5
        INVALID_PLACEHOLDER_TYPE = 6
        MISSING_FEEDMAPPING_FOR_PLACEHOLDER_TYPE = 7
        NO_EXISTING_LOCATION_CUSTOMER_FEED = 8


class AdGroupStatusEnum(object):
    class AdGroupStatus(enum.IntEnum):
        """
        The possible statuses of an ad group.

        Attributes:
          UNSPECIFIED (int): The status has not been specified.
          UNKNOWN (int): The received value is not known in this version.

          This is a response-only value.
          ENABLED (int): The ad group is enabled.
          PAUSED (int): The ad group is paused.
          REMOVED (int): The ad group is removed.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        ENABLED = 2
        PAUSED = 3
        REMOVED = 4


class AdGroupTypeEnum(object):
    class AdGroupType(enum.IntEnum):
        """
        Enum listing the possible types of an ad group.

        Attributes:
          UNSPECIFIED (int): The type has not been specified.
          UNKNOWN (int): The received value is not known in this version.

          This is a response-only value.
          SEARCH_STANDARD (int): The default ad group type for Search campaigns.
          DISPLAY_STANDARD (int): The default ad group type for Display campaigns.
          SHOPPING_PRODUCT_ADS (int): The ad group type for Shopping campaigns serving standard product ads.
          HOTEL_ADS (int): The default ad group type for Hotel campaigns.
          SHOPPING_SMART_ADS (int): The type for ad groups in Smart Shopping campaigns.
          VIDEO_BUMPER (int): Short unskippable in-stream video ads.
          VIDEO_TRUE_VIEW_IN_STREAM (int): TrueView (skippable) in-stream video ads.
          VIDEO_TRUE_VIEW_IN_DISPLAY (int): TrueView in-display video ads.
          VIDEO_NON_SKIPPABLE_IN_STREAM (int): Unskippable in-stream video ads.
          VIDEO_OUTSTREAM (int): Outstream video ads.
          SEARCH_DYNAMIC_ADS (int): Ad group type for Dynamic Search Ads ad groups.
          SHOPPING_COMPARISON_LISTING_ADS (int): The type for ad groups in Shopping Comparison Listing campaigns.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        SEARCH_STANDARD = 2
        DISPLAY_STANDARD = 3
        SHOPPING_PRODUCT_ADS = 4
        HOTEL_ADS = 6
        SHOPPING_SMART_ADS = 7
        VIDEO_BUMPER = 8
        VIDEO_TRUE_VIEW_IN_STREAM = 9
        VIDEO_TRUE_VIEW_IN_DISPLAY = 10
        VIDEO_NON_SKIPPABLE_IN_STREAM = 11
        VIDEO_OUTSTREAM = 12
        SEARCH_DYNAMIC_ADS = 13
        SHOPPING_COMPARISON_LISTING_ADS = 14


class AdNetworkTypeEnum(object):
    class AdNetworkType(enum.IntEnum):
        """
        Enumerates Google Ads network types.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): The value is unknown in this version.
          SEARCH (int): Google search.
          SEARCH_PARTNERS (int): Search partners.
          CONTENT (int): Display Network.
          YOUTUBE_SEARCH (int): YouTube Search.
          YOUTUBE_WATCH (int): YouTube Videos
          MIXED (int): Cross-network.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        SEARCH = 2
        SEARCH_PARTNERS = 3
        CONTENT = 4
        YOUTUBE_SEARCH = 5
        YOUTUBE_WATCH = 6
        MIXED = 7


class AdParameterErrorEnum(object):
    class AdParameterError(enum.IntEnum):
        """
        Enum describing possible ad parameter errors.

        Attributes:
          UNSPECIFIED (int): Enum unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          AD_GROUP_CRITERION_MUST_BE_KEYWORD (int): The ad group criterion must be a keyword criterion.
          INVALID_INSERTION_TEXT_FORMAT (int): The insertion text is invalid.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        AD_GROUP_CRITERION_MUST_BE_KEYWORD = 2
        INVALID_INSERTION_TEXT_FORMAT = 3


class AdServingOptimizationStatusEnum(object):
    class AdServingOptimizationStatus(enum.IntEnum):
        """
        Enum describing possible serving statuses.

        Attributes:
          UNSPECIFIED (int): No value has been specified.
          UNKNOWN (int): The received value is not known in this version.

          This is a response-only value.
          OPTIMIZE (int): Ad serving is optimized based on CTR for the campaign.
          CONVERSION_OPTIMIZE (int): Ad serving is optimized based on CTR \* Conversion for the campaign. If
          the campaign is not in the conversion optimizer bidding strategy, it
          will default to OPTIMIZED.
          ROTATE (int): Ads are rotated evenly for 90 days, then optimized for clicks.
          ROTATE_INDEFINITELY (int): Show lower performing ads more evenly with higher performing ads, and do
          not optimize.
          UNAVAILABLE (int): Ad serving optimization status is not available.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        OPTIMIZE = 2
        CONVERSION_OPTIMIZE = 3
        ROTATE = 4
        ROTATE_INDEFINITELY = 5
        UNAVAILABLE = 6


class AdSharingErrorEnum(object):
    class AdSharingError(enum.IntEnum):
        """
        Enum describing possible ad sharing errors.

        Attributes:
          UNSPECIFIED (int): Enum unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          AD_GROUP_ALREADY_CONTAINS_AD (int): Error resulting in attempting to add an Ad to an AdGroup that already
          contains the Ad.
          INCOMPATIBLE_AD_UNDER_AD_GROUP (int): Ad is not compatible with the AdGroup it is being shared with.
          CANNOT_SHARE_INACTIVE_AD (int): Cannot add AdGroupAd on inactive Ad.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        AD_GROUP_ALREADY_CONTAINS_AD = 2
        INCOMPATIBLE_AD_UNDER_AD_GROUP = 3
        CANNOT_SHARE_INACTIVE_AD = 4


class AdStrengthEnum(object):
    class AdStrength(enum.IntEnum):
        """
        Enum listing the possible ad strengths.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          PENDING (int): The ad strength is currently pending.
          NO_ADS (int): No ads could be generated.
          POOR (int): Poor strength.
          AVERAGE (int): Average strength.
          GOOD (int): Good strength.
          EXCELLENT (int): Excellent strength.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        PENDING = 2
        NO_ADS = 3
        POOR = 4
        AVERAGE = 5
        GOOD = 6
        EXCELLENT = 7


class AdTypeEnum(object):
    class AdType(enum.IntEnum):
        """
        The possible types of an ad.

        Attributes:
          UNSPECIFIED (int): No value has been specified.
          UNKNOWN (int): The received value is not known in this version.

          This is a response-only value.
          TEXT_AD (int): The ad is a text ad.
          EXPANDED_TEXT_AD (int): The ad is an expanded text ad.
          CALL_ONLY_AD (int): The ad is a call only ad.
          EXPANDED_DYNAMIC_SEARCH_AD (int): The ad is an expanded dynamic search ad.
          HOTEL_AD (int): The ad is a hotel ad.
          SHOPPING_SMART_AD (int): The ad is a Smart Shopping ad.
          SHOPPING_PRODUCT_AD (int): The ad is a standard Shopping ad.
          VIDEO_AD (int): The ad is a video ad.
          GMAIL_AD (int): This ad is a Gmail ad.
          IMAGE_AD (int): This ad is an Image ad.
          RESPONSIVE_SEARCH_AD (int): The ad is a responsive search ad.
          LEGACY_RESPONSIVE_DISPLAY_AD (int): The ad is a legacy responsive display ad.
          APP_AD (int): The ad is an app ad.
          LEGACY_APP_INSTALL_AD (int): The ad is a legacy app install ad.
          RESPONSIVE_DISPLAY_AD (int): The ad is a responsive display ad.
          HTML5_UPLOAD_AD (int): The ad is a display upload ad with the HTML5\_UPLOAD\_AD product type.
          DYNAMIC_HTML5_AD (int): The ad is a display upload ad with one of the DYNAMIC\_HTML5\_\* product
          types.
          APP_ENGAGEMENT_AD (int): The ad is an app engagement ad.
          SHOPPING_COMPARISON_LISTING_AD (int): The ad is a Shopping Comparison Listing ad.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        TEXT_AD = 2
        EXPANDED_TEXT_AD = 3
        CALL_ONLY_AD = 6
        EXPANDED_DYNAMIC_SEARCH_AD = 7
        HOTEL_AD = 8
        SHOPPING_SMART_AD = 9
        SHOPPING_PRODUCT_AD = 10
        VIDEO_AD = 12
        GMAIL_AD = 13
        IMAGE_AD = 14
        RESPONSIVE_SEARCH_AD = 15
        LEGACY_RESPONSIVE_DISPLAY_AD = 16
        APP_AD = 17
        LEGACY_APP_INSTALL_AD = 18
        RESPONSIVE_DISPLAY_AD = 19
        HTML5_UPLOAD_AD = 21
        DYNAMIC_HTML5_AD = 22
        APP_ENGAGEMENT_AD = 23
        SHOPPING_COMPARISON_LISTING_AD = 24


class AdvertisingChannelSubTypeEnum(object):
    class AdvertisingChannelSubType(enum.IntEnum):
        """
        Enum describing the different channel subtypes.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used as a return value only. Represents value unknown in this version.
          SEARCH_MOBILE_APP (int): Mobile app campaigns for Search.
          DISPLAY_MOBILE_APP (int): Mobile app campaigns for Display.
          SEARCH_EXPRESS (int): AdWords express campaigns for search.
          DISPLAY_EXPRESS (int): AdWords Express campaigns for display.
          SHOPPING_SMART_ADS (int): Smart Shopping campaigns.
          DISPLAY_GMAIL_AD (int): Gmail Ad campaigns.
          DISPLAY_SMART_CAMPAIGN (int): Smart display campaigns.
          VIDEO_OUTSTREAM (int): Video Outstream campaigns.
          VIDEO_ACTION (int): Video TrueView for Action campaigns.
          VIDEO_NON_SKIPPABLE (int): Video campaigns with non-skippable video ads.
          APP_CAMPAIGN (int): App Campaign that allows you to easily promote your Android or iOS app
          across Google's top properties including Search, Play, YouTube, and the
          Google Display Network.
          APP_CAMPAIGN_FOR_ENGAGEMENT (int): App Campaign for engagement, focused on driving re-engagement with the
          app across several of Google’s top properties including Search, YouTube,
          and the Google Display Network.
          SHOPPING_COMPARISON_LISTING_ADS (int): Shopping Comparison Listing campaigns.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        SEARCH_MOBILE_APP = 2
        DISPLAY_MOBILE_APP = 3
        SEARCH_EXPRESS = 4
        DISPLAY_EXPRESS = 5
        SHOPPING_SMART_ADS = 6
        DISPLAY_GMAIL_AD = 7
        DISPLAY_SMART_CAMPAIGN = 8
        VIDEO_OUTSTREAM = 9
        VIDEO_ACTION = 10
        VIDEO_NON_SKIPPABLE = 11
        APP_CAMPAIGN = 12
        APP_CAMPAIGN_FOR_ENGAGEMENT = 13
        SHOPPING_COMPARISON_LISTING_ADS = 15


class AdvertisingChannelTypeEnum(object):
    class AdvertisingChannelType(enum.IntEnum):
        """
        Enum describing the various advertising channel types.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          SEARCH (int): Search Network. Includes display bundled, and Search+ campaigns.
          DISPLAY (int): Google Display Network only.
          SHOPPING (int): Shopping campaigns serve on the shopping property
          and on google.com search results.
          HOTEL (int): Hotel Ads campaigns.
          VIDEO (int): Video campaigns.
          MULTI_CHANNEL (int): App Campaigns, and App Campaigns for Engagement, that run
          across multiple channels.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        SEARCH = 2
        DISPLAY = 3
        SHOPPING = 4
        HOTEL = 5
        VIDEO = 6
        MULTI_CHANNEL = 7


class AdxErrorEnum(object):
    class AdxError(enum.IntEnum):
        """
        Enum describing possible adx errors.

        Attributes:
          UNSPECIFIED (int): Enum unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          UNSUPPORTED_FEATURE (int): Attempt to use non-AdX feature by AdX customer.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        UNSUPPORTED_FEATURE = 2


class AffiliateLocationFeedRelationshipTypeEnum(object):
    class AffiliateLocationFeedRelationshipType(enum.IntEnum):
        """
        Possible values for a relationship type for an affiliate location feed.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          GENERAL_RETAILER (int): General retailer relationship.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        GENERAL_RETAILER = 2


class AffiliateLocationPlaceholderFieldEnum(object):
    class AffiliateLocationPlaceholderField(enum.IntEnum):
        """
        Possible values for Affiliate Location placeholder fields.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          BUSINESS_NAME (int): Data Type: STRING. The name of the business.
          ADDRESS_LINE_1 (int): Data Type: STRING. Line 1 of the business address.
          ADDRESS_LINE_2 (int): Data Type: STRING. Line 2 of the business address.
          CITY (int): Data Type: STRING. City of the business address.
          PROVINCE (int): Data Type: STRING. Province of the business address.
          POSTAL_CODE (int): Data Type: STRING. Postal code of the business address.
          COUNTRY_CODE (int): Data Type: STRING. Country code of the business address.
          PHONE_NUMBER (int): Data Type: STRING. Phone number of the business.
          LANGUAGE_CODE (int): Data Type: STRING. Language code of the business.
          CHAIN_ID (int): Data Type: INT64. ID of the chain.
          CHAIN_NAME (int): Data Type: STRING. Name of the chain.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        BUSINESS_NAME = 2
        ADDRESS_LINE_1 = 3
        ADDRESS_LINE_2 = 4
        CITY = 5
        PROVINCE = 6
        POSTAL_CODE = 7
        COUNTRY_CODE = 8
        PHONE_NUMBER = 9
        LANGUAGE_CODE = 10
        CHAIN_ID = 11
        CHAIN_NAME = 12


class AgeRangeTypeEnum(object):
    class AgeRangeType(enum.IntEnum):
        """
        The type of demographic age ranges (e.g. between 18 and 24 years old).

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          AGE_RANGE_18_24 (int): Between 18 and 24 years old.
          AGE_RANGE_25_34 (int): Between 25 and 34 years old.
          AGE_RANGE_35_44 (int): Between 35 and 44 years old.
          AGE_RANGE_45_54 (int): Between 45 and 54 years old.
          AGE_RANGE_55_64 (int): Between 55 and 64 years old.
          AGE_RANGE_65_UP (int): 65 years old and beyond.
          AGE_RANGE_UNDETERMINED (int): Undetermined age range.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        AGE_RANGE_18_24 = 503001
        AGE_RANGE_25_34 = 503002
        AGE_RANGE_35_44 = 503003
        AGE_RANGE_45_54 = 503004
        AGE_RANGE_55_64 = 503005
        AGE_RANGE_65_UP = 503006
        AGE_RANGE_UNDETERMINED = 503999


class AppCampaignAppStoreEnum(object):
    class AppCampaignAppStore(enum.IntEnum):
        """
        Enum describing app campaign app store.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          APPLE_APP_STORE (int): Apple app store.
          GOOGLE_APP_STORE (int): Google play.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        APPLE_APP_STORE = 2
        GOOGLE_APP_STORE = 3


class AppCampaignBiddingStrategyGoalTypeEnum(object):
    class AppCampaignBiddingStrategyGoalType(enum.IntEnum):
        """
        Goal type of App campaign BiddingStrategy.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          OPTIMIZE_INSTALLS_TARGET_INSTALL_COST (int): Aim to maximize the number of app installs. The cpa bid is the
          target cost per install.
          OPTIMIZE_IN_APP_CONVERSIONS_TARGET_INSTALL_COST (int): Aim to maximize the long term number of selected in-app conversions from
          app installs. The cpa bid is the target cost per install.
          OPTIMIZE_IN_APP_CONVERSIONS_TARGET_CONVERSION_COST (int): Aim to maximize the long term number of selected in-app conversions from
          app installs. The cpa bid is the target cost per in-app conversion. Note
          that the actual cpa may seem higher than the target cpa at first, since
          the long term conversions haven’t happened yet.
          OPTIMIZE_RETURN_ON_ADVERTISING_SPEND (int): Aim to maximize all conversions' value, i.e. install + selected in-app
          conversions while achieving or exceeding target return on advertising
          spend.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        OPTIMIZE_INSTALLS_TARGET_INSTALL_COST = 2
        OPTIMIZE_IN_APP_CONVERSIONS_TARGET_INSTALL_COST = 3
        OPTIMIZE_IN_APP_CONVERSIONS_TARGET_CONVERSION_COST = 4
        OPTIMIZE_RETURN_ON_ADVERTISING_SPEND = 5


class AppPaymentModelTypeEnum(object):
    class AppPaymentModelType(enum.IntEnum):
        """
        Enum describing possible app payment models.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          PAID (int): Represents paid-for apps.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        PAID = 30


class AppPlaceholderFieldEnum(object):
    class AppPlaceholderField(enum.IntEnum):
        """
        Possible values for App placeholder fields.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          STORE (int): Data Type: INT64. The application store that the target application
          belongs to. Valid values are: 1 = Apple iTunes Store; 2 = Google Play
          Store.
          ID (int): Data Type: STRING. The store-specific ID for the target application.
          LINK_TEXT (int): Data Type: STRING. The visible text displayed when the link is rendered
          in an ad.
          URL (int): Data Type: STRING. The destination URL of the in-app link.
          FINAL_URLS (int): Data Type: URL\_LIST. Final URLs for the in-app link when using Upgraded
          URLs.
          FINAL_MOBILE_URLS (int): Data Type: URL\_LIST. Final Mobile URLs for the in-app link when using
          Upgraded URLs.
          TRACKING_URL (int): Data Type: URL. Tracking template for the in-app link when using Upgraded
          URLs.
          FINAL_URL_SUFFIX (int): Data Type: STRING. Final URL suffix for the in-app link when using
          parallel tracking.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        STORE = 2
        ID = 3
        LINK_TEXT = 4
        URL = 5
        FINAL_URLS = 6
        FINAL_MOBILE_URLS = 7
        TRACKING_URL = 8
        FINAL_URL_SUFFIX = 9


class AppStoreEnum(object):
    class AppStore(enum.IntEnum):
        """
        App store type in an app extension.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          APPLE_ITUNES (int): Apple iTunes.
          GOOGLE_PLAY (int): Google Play.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        APPLE_ITUNES = 2
        GOOGLE_PLAY = 3


class AppUrlOperatingSystemTypeEnum(object):
    class AppUrlOperatingSystemType(enum.IntEnum):
        """
        Operating System

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          IOS (int): The Apple IOS operating system.
          ANDROID (int): The Android operating system.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        IOS = 2
        ANDROID = 3


class AssetErrorEnum(object):
    class AssetError(enum.IntEnum):
        """
        Enum describing possible asset errors.

        Attributes:
          UNSPECIFIED (int): Enum unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          CUSTOMER_NOT_WHITELISTED_FOR_ASSET_TYPE (int): The customer is not whitelisted for this asset type.
          DUPLICATE_ASSET (int): Assets are duplicated across operations.
          DUPLICATE_ASSET_NAME (int): The asset name is duplicated, either across operations or with an
          existing asset.
          ASSET_DATA_IS_MISSING (int): The Asset.asset\_data oneof is empty.
          CANNOT_MODIFY_ASSET_NAME (int): The asset has a name which is different from an existing duplicate that
          represents the same content.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        CUSTOMER_NOT_WHITELISTED_FOR_ASSET_TYPE = 2
        DUPLICATE_ASSET = 3
        DUPLICATE_ASSET_NAME = 4
        ASSET_DATA_IS_MISSING = 5
        CANNOT_MODIFY_ASSET_NAME = 6


class AssetTypeEnum(object):
    class AssetType(enum.IntEnum):
        """
        Enum describing possible types of asset.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          YOUTUBE_VIDEO (int): YouTube video asset.
          MEDIA_BUNDLE (int): Media bundle asset.
          IMAGE (int): Image asset.
          TEXT (int): Text asset.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        YOUTUBE_VIDEO = 2
        MEDIA_BUNDLE = 3
        IMAGE = 4
        TEXT = 5


class AttributionModelEnum(object):
    class AttributionModel(enum.IntEnum):
        """
        The attribution model that describes how to distribute credit for a
        particular conversion across potentially many prior interactions.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          EXTERNAL (int): Uses external attribution.
          GOOGLE_ADS_LAST_CLICK (int): Attributes all credit for a conversion to its last click.
          GOOGLE_SEARCH_ATTRIBUTION_FIRST_CLICK (int): Attributes all credit for a conversion to its first click using Google
          Search attribution.
          GOOGLE_SEARCH_ATTRIBUTION_LINEAR (int): Attributes credit for a conversion equally across all of its clicks using
          Google Search attribution.
          GOOGLE_SEARCH_ATTRIBUTION_TIME_DECAY (int): Attributes exponentially more credit for a conversion to its more recent
          clicks using Google Search attribution (half-life is 1 week).
          GOOGLE_SEARCH_ATTRIBUTION_POSITION_BASED (int): Attributes 40% of the credit for a conversion to its first and last
          clicks. Remaining 20% is evenly distributed across all other clicks. This
          uses Google Search attribution.
          GOOGLE_SEARCH_ATTRIBUTION_DATA_DRIVEN (int): Flexible model that uses machine learning to determine the appropriate
          distribution of credit among clicks using Google Search attribution.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        EXTERNAL = 100
        GOOGLE_ADS_LAST_CLICK = 101
        GOOGLE_SEARCH_ATTRIBUTION_FIRST_CLICK = 102
        GOOGLE_SEARCH_ATTRIBUTION_LINEAR = 103
        GOOGLE_SEARCH_ATTRIBUTION_TIME_DECAY = 104
        GOOGLE_SEARCH_ATTRIBUTION_POSITION_BASED = 105
        GOOGLE_SEARCH_ATTRIBUTION_DATA_DRIVEN = 106


class AuthenticationErrorEnum(object):
    class AuthenticationError(enum.IntEnum):
        """
        Enum describing possible authentication errors.

        Attributes:
          UNSPECIFIED (int): Enum unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          AUTHENTICATION_ERROR (int): Authentication of the request failed.
          CLIENT_CUSTOMER_ID_INVALID (int): Client Customer Id is not a number.
          CUSTOMER_NOT_FOUND (int): No customer found for the provided customer id.
          GOOGLE_ACCOUNT_DELETED (int): Client's Google Account is deleted.
          GOOGLE_ACCOUNT_COOKIE_INVALID (int): Google account login token in the cookie is invalid.
          GOOGLE_ACCOUNT_AUTHENTICATION_FAILED (int): A problem occurred during Google account authentication.
          GOOGLE_ACCOUNT_USER_AND_ADS_USER_MISMATCH (int): The user in the google account login token does not match the UserId in
          the cookie.
          LOGIN_COOKIE_REQUIRED (int): Login cookie is required for authentication.
          NOT_ADS_USER (int): User in the cookie is not a valid Ads user.
          OAUTH_TOKEN_INVALID (int): Oauth token in the header is not valid.
          OAUTH_TOKEN_EXPIRED (int): Oauth token in the header has expired.
          OAUTH_TOKEN_DISABLED (int): Oauth token in the header has been disabled.
          OAUTH_TOKEN_REVOKED (int): Oauth token in the header has been revoked.
          OAUTH_TOKEN_HEADER_INVALID (int): Oauth token HTTP header is malformed.
          LOGIN_COOKIE_INVALID (int): Login cookie is not valid.
          USER_ID_INVALID (int): User Id in the header is not a valid id.
          TWO_STEP_VERIFICATION_NOT_ENROLLED (int): An account administrator changed this account's authentication settings.
          To access this Google Ads account, enable 2-Step Verification in your
          Google account at https://www.google.com/landing/2step.
          ADVANCED_PROTECTION_NOT_ENROLLED (int): An account administrator changed this account's authentication settings.
          To access this Google Ads account, enable Advanced Protection in your
          Google account at https://landing.google.com/advancedprotection.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        AUTHENTICATION_ERROR = 2
        CLIENT_CUSTOMER_ID_INVALID = 5
        CUSTOMER_NOT_FOUND = 8
        GOOGLE_ACCOUNT_DELETED = 9
        GOOGLE_ACCOUNT_COOKIE_INVALID = 10
        GOOGLE_ACCOUNT_AUTHENTICATION_FAILED = 25
        GOOGLE_ACCOUNT_USER_AND_ADS_USER_MISMATCH = 12
        LOGIN_COOKIE_REQUIRED = 13
        NOT_ADS_USER = 14
        OAUTH_TOKEN_INVALID = 15
        OAUTH_TOKEN_EXPIRED = 16
        OAUTH_TOKEN_DISABLED = 17
        OAUTH_TOKEN_REVOKED = 18
        OAUTH_TOKEN_HEADER_INVALID = 19
        LOGIN_COOKIE_INVALID = 20
        USER_ID_INVALID = 22
        TWO_STEP_VERIFICATION_NOT_ENROLLED = 23
        ADVANCED_PROTECTION_NOT_ENROLLED = 24


class AuthorizationErrorEnum(object):
    class AuthorizationError(enum.IntEnum):
        """
        Enum describing possible authorization errors.

        Attributes:
          UNSPECIFIED (int): Enum unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          USER_PERMISSION_DENIED (int): User doesn't have permission to access customer. Note: If you're
          accessing a client customer, the manager's customer id must be set in the
          'login-customer-id' header. See
          https://developers.google.com/google-ads/api/docs/concepts/
          call-structure#login-customer-id
          DEVELOPER_TOKEN_NOT_WHITELISTED (int): The developer token is not whitelisted.
          DEVELOPER_TOKEN_PROHIBITED (int): The developer token is not allowed with the project sent in the request.
          PROJECT_DISABLED (int): The Google Cloud project sent in the request does not have permission to
          access the api.
          AUTHORIZATION_ERROR (int): Authorization of the client failed.
          ACTION_NOT_PERMITTED (int): The user does not have permission to perform this action
          (e.g., ADD, UPDATE, REMOVE) on the resource or call a method.
          INCOMPLETE_SIGNUP (int): Signup not complete.
          CUSTOMER_NOT_ENABLED (int): The customer can't be used because it isn't enabled.
          MISSING_TOS (int): The developer must sign the terms of service. They can be found here:
          ads.google.com/aw/apicenter
          DEVELOPER_TOKEN_NOT_APPROVED (int): The developer token is not approved. Non-approved developer tokens can
          only be used with test accounts.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        USER_PERMISSION_DENIED = 2
        DEVELOPER_TOKEN_NOT_WHITELISTED = 3
        DEVELOPER_TOKEN_PROHIBITED = 4
        PROJECT_DISABLED = 5
        AUTHORIZATION_ERROR = 6
        ACTION_NOT_PERMITTED = 7
        INCOMPLETE_SIGNUP = 8
        CUSTOMER_NOT_ENABLED = 24
        MISSING_TOS = 9
        DEVELOPER_TOKEN_NOT_APPROVED = 10


class BidModifierSourceEnum(object):
    class BidModifierSource(enum.IntEnum):
        """
        Enum describing possible bid modifier sources.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          CAMPAIGN (int): The bid modifier is specified at the campaign level, on the campaign
          level criterion.
          AD_GROUP (int): The bid modifier is specified (overridden) at the ad group level.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        CAMPAIGN = 2
        AD_GROUP = 3


class BiddingErrorEnum(object):
    class BiddingError(enum.IntEnum):
        """
        Enum describing possible bidding errors.

        Attributes:
          UNSPECIFIED (int): Enum unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          BIDDING_STRATEGY_TRANSITION_NOT_ALLOWED (int): Cannot transition to new bidding strategy.
          CANNOT_ATTACH_BIDDING_STRATEGY_TO_CAMPAIGN (int): Cannot attach bidding strategy to campaign.
          INVALID_ANONYMOUS_BIDDING_STRATEGY_TYPE (int): Bidding strategy is not supported or cannot be used as anonymous.
          INVALID_BIDDING_STRATEGY_TYPE (int): The type does not match the named strategy's type.
          INVALID_BID (int): The bid is invalid.
          BIDDING_STRATEGY_NOT_AVAILABLE_FOR_ACCOUNT_TYPE (int): Bidding strategy is not available for the account type.
          CONVERSION_TRACKING_NOT_ENABLED (int): Conversion tracking is not enabled for the campaign for VBB transition.
          NOT_ENOUGH_CONVERSIONS (int): Not enough conversions tracked for VBB transitions.
          CANNOT_CREATE_CAMPAIGN_WITH_BIDDING_STRATEGY (int): Campaign can not be created with given bidding strategy. It can be
          transitioned to the strategy, once eligible.
          CANNOT_TARGET_CONTENT_NETWORK_ONLY_WITH_CAMPAIGN_LEVEL_POP_BIDDING_STRATEGY (int): Cannot target content network only as campaign uses Page One Promoted
          bidding strategy.
          BIDDING_STRATEGY_NOT_SUPPORTED_WITH_AD_SCHEDULE (int): Budget Optimizer and Target Spend bidding strategies are not supported
          for campaigns with AdSchedule targeting.
          PAY_PER_CONVERSION_NOT_AVAILABLE_FOR_CUSTOMER (int): Pay per conversion is not available to all the customer, only few
          whitelisted customers can use this.
          PAY_PER_CONVERSION_NOT_ALLOWED_WITH_TARGET_CPA (int): Pay per conversion is not allowed with Target CPA.
          BIDDING_STRATEGY_NOT_ALLOWED_FOR_SEARCH_ONLY_CAMPAIGNS (int): Cannot set bidding strategy to Manual CPM for search network only
          campaigns.
          BIDDING_STRATEGY_NOT_SUPPORTED_IN_DRAFTS_OR_EXPERIMENTS (int): The bidding strategy is not supported for use in drafts or experiments.
          BIDDING_STRATEGY_TYPE_DOES_NOT_SUPPORT_PRODUCT_TYPE_ADGROUP_CRITERION (int): Bidding strategy type does not support product type ad group criterion.
          BID_TOO_SMALL (int): Bid amount is too small.
          BID_TOO_BIG (int): Bid amount is too big.
          BID_TOO_MANY_FRACTIONAL_DIGITS (int): Bid has too many fractional digit precision.
          INVALID_DOMAIN_NAME (int): Invalid domain name specified.
          NOT_COMPATIBLE_WITH_PAYMENT_MODE (int): The field is not compatible with the payment mode.
          NOT_COMPATIBLE_WITH_BUDGET_TYPE (int): The field is not compatible with the budget type.
          NOT_COMPATIBLE_WITH_BIDDING_STRATEGY_TYPE (int): The field is not compatible with the bidding strategy type.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        BIDDING_STRATEGY_TRANSITION_NOT_ALLOWED = 2
        CANNOT_ATTACH_BIDDING_STRATEGY_TO_CAMPAIGN = 7
        INVALID_ANONYMOUS_BIDDING_STRATEGY_TYPE = 10
        INVALID_BIDDING_STRATEGY_TYPE = 14
        INVALID_BID = 17
        BIDDING_STRATEGY_NOT_AVAILABLE_FOR_ACCOUNT_TYPE = 18
        CONVERSION_TRACKING_NOT_ENABLED = 19
        NOT_ENOUGH_CONVERSIONS = 20
        CANNOT_CREATE_CAMPAIGN_WITH_BIDDING_STRATEGY = 21
        CANNOT_TARGET_CONTENT_NETWORK_ONLY_WITH_CAMPAIGN_LEVEL_POP_BIDDING_STRATEGY = 23
        BIDDING_STRATEGY_NOT_SUPPORTED_WITH_AD_SCHEDULE = 24
        PAY_PER_CONVERSION_NOT_AVAILABLE_FOR_CUSTOMER = 25
        PAY_PER_CONVERSION_NOT_ALLOWED_WITH_TARGET_CPA = 26
        BIDDING_STRATEGY_NOT_ALLOWED_FOR_SEARCH_ONLY_CAMPAIGNS = 27
        BIDDING_STRATEGY_NOT_SUPPORTED_IN_DRAFTS_OR_EXPERIMENTS = 28
        BIDDING_STRATEGY_TYPE_DOES_NOT_SUPPORT_PRODUCT_TYPE_ADGROUP_CRITERION = 29
        BID_TOO_SMALL = 30
        BID_TOO_BIG = 31
        BID_TOO_MANY_FRACTIONAL_DIGITS = 32
        INVALID_DOMAIN_NAME = 33
        NOT_COMPATIBLE_WITH_PAYMENT_MODE = 34
        NOT_COMPATIBLE_WITH_BUDGET_TYPE = 35
        NOT_COMPATIBLE_WITH_BIDDING_STRATEGY_TYPE = 36


class BiddingSourceEnum(object):
    class BiddingSource(enum.IntEnum):
        """
        Indicates where a bid or target is defined. For example, an ad group
        criterion may define a cpc bid directly, or it can inherit its cpc bid from
        the ad group.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          CAMPAIGN_BIDDING_STRATEGY (int): Effective bid or target is inherited from campaign bidding strategy.
          AD_GROUP (int): The bid or target is defined on the ad group.
          AD_GROUP_CRITERION (int): The bid or target is defined on the ad group criterion.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        CAMPAIGN_BIDDING_STRATEGY = 5
        AD_GROUP = 6
        AD_GROUP_CRITERION = 7


class BiddingStrategyErrorEnum(object):
    class BiddingStrategyError(enum.IntEnum):
        """
        Enum describing possible bidding strategy errors.

        Attributes:
          UNSPECIFIED (int): Enum unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          DUPLICATE_NAME (int): Each bidding strategy must have a unique name.
          CANNOT_CHANGE_BIDDING_STRATEGY_TYPE (int): Bidding strategy type is immutable.
          CANNOT_REMOVE_ASSOCIATED_STRATEGY (int): Only bidding strategies not linked to campaigns, adgroups or adgroup
          criteria can be removed.
          BIDDING_STRATEGY_NOT_SUPPORTED (int): The specified bidding strategy is not supported.
          INCOMPATIBLE_BIDDING_STRATEGY_AND_BIDDING_STRATEGY_GOAL_TYPE (int): The bidding strategy is incompatible with the campaign's bidding
          strategy goal type.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        DUPLICATE_NAME = 2
        CANNOT_CHANGE_BIDDING_STRATEGY_TYPE = 3
        CANNOT_REMOVE_ASSOCIATED_STRATEGY = 4
        BIDDING_STRATEGY_NOT_SUPPORTED = 5
        INCOMPATIBLE_BIDDING_STRATEGY_AND_BIDDING_STRATEGY_GOAL_TYPE = 6


class BiddingStrategyStatusEnum(object):
    class BiddingStrategyStatus(enum.IntEnum):
        """
        The possible statuses of a BiddingStrategy.

        Attributes:
          UNSPECIFIED (int): No value has been specified.
          UNKNOWN (int): The received value is not known in this version.

          This is a response-only value.
          ENABLED (int): The bidding strategy is enabled.
          REMOVED (int): The bidding strategy is removed.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        ENABLED = 2
        REMOVED = 4


class BiddingStrategyTypeEnum(object):
    class BiddingStrategyType(enum.IntEnum):
        """
        Enum describing possible bidding strategy types.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          COMMISSION (int): Commission is an automatic bidding strategy in which the advertiser pays
          a certain portion of the conversion value.
          ENHANCED_CPC (int): Enhanced CPC is a bidding strategy that raises bids for clicks
          that seem more likely to lead to a conversion and lowers
          them for clicks where they seem less likely.
          MANUAL_CPC (int): Manual click based bidding where user pays per click.
          MANUAL_CPM (int): Manual impression based bidding
          where user pays per thousand impressions.
          MANUAL_CPV (int): A bidding strategy that pays a configurable amount per video view.
          MAXIMIZE_CONVERSIONS (int): A bidding strategy that automatically maximizes number of conversions
          given a daily budget.
          MAXIMIZE_CONVERSION_VALUE (int): An automated bidding strategy that automatically sets bids to maximize
          revenue while spending your budget.
          PAGE_ONE_PROMOTED (int): Page-One Promoted bidding scheme, which sets max cpc bids to
          target impressions on page one or page one promoted slots on google.com.
          PERCENT_CPC (int): Percent Cpc is bidding strategy where bids are a fraction of the
          advertised price for some good or service.
          TARGET_CPA (int): Target CPA is an automated bid strategy that sets bids
          to help get as many conversions as possible
          at the target cost-per-acquisition (CPA) you set.
          TARGET_CPM (int): Target CPM is an automated bid strategy that sets bids to help get
          as many impressions as possible at the target cost per one thousand
          impressions (CPM) you set.
          TARGET_IMPRESSION_SHARE (int): An automated bidding strategy that sets bids so that a certain percentage
          of search ads are shown at the top of the first page (or other targeted
          location).
          TARGET_OUTRANK_SHARE (int): Target Outrank Share is an automated bidding strategy that sets bids
          based on the target fraction of auctions where the advertiser
          should outrank a specific competitor.
          TARGET_ROAS (int): Target ROAS is an automated bidding strategy
          that helps you maximize revenue while averaging
          a specific target Return On Average Spend (ROAS).
          TARGET_SPEND (int): Target Spend is an automated bid strategy that sets your bids
          to help get as many clicks as possible within your budget.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        COMMISSION = 16
        ENHANCED_CPC = 2
        MANUAL_CPC = 3
        MANUAL_CPM = 4
        MANUAL_CPV = 13
        MAXIMIZE_CONVERSIONS = 10
        MAXIMIZE_CONVERSION_VALUE = 11
        PAGE_ONE_PROMOTED = 5
        PERCENT_CPC = 12
        TARGET_CPA = 6
        TARGET_CPM = 14
        TARGET_IMPRESSION_SHARE = 15
        TARGET_OUTRANK_SHARE = 7
        TARGET_ROAS = 8
        TARGET_SPEND = 9


class BillingSetupErrorEnum(object):
    class BillingSetupError(enum.IntEnum):
        """
        Enum describing possible billing setup errors.

        Attributes:
          UNSPECIFIED (int): Enum unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          CANNOT_USE_EXISTING_AND_NEW_ACCOUNT (int): Cannot use both an existing Payments account and a new Payments account
          when setting up billing.
          CANNOT_REMOVE_STARTED_BILLING_SETUP (int): Cannot cancel an APPROVED billing setup whose start time has passed.
          CANNOT_CHANGE_BILLING_TO_SAME_PAYMENTS_ACCOUNT (int): Cannot perform a Change of Bill-To (CBT) to the same Payments account.
          BILLING_SETUP_NOT_PERMITTED_FOR_CUSTOMER_STATUS (int): Billing Setups can only be used by customers with ENABLED or DRAFT
          status.
          INVALID_PAYMENTS_ACCOUNT (int): Billing Setups must either include a correctly formatted existing
          Payments account id, or a non-empty new Payments account name.
          BILLING_SETUP_NOT_PERMITTED_FOR_CUSTOMER_CATEGORY (int): Only billable and third-party customers can create billing setups.
          INVALID_START_TIME_TYPE (int): Billing Setup creations can only use NOW for start time type.
          THIRD_PARTY_ALREADY_HAS_BILLING (int): Billing Setups can only be created for a third-party customer if they do
          not already have a setup.
          BILLING_SETUP_IN_PROGRESS (int): Billing Setups cannot be created if there is already a pending billing in
          progress, ie. a billing known to Payments.
          NO_SIGNUP_PERMISSION (int): Billing Setups can only be created by customers who have permission to
          setup billings. Users can contact a representative for help setting up
          permissions.
          CHANGE_OF_BILL_TO_IN_PROGRESS (int): Billing Setups cannot be created if there is already a future-approved
          billing.
          PAYMENTS_PROFILE_NOT_FOUND (int): Billing Setup creation failed because Payments could not find the
          requested Payments profile.
          PAYMENTS_ACCOUNT_NOT_FOUND (int): Billing Setup creation failed because Payments could not find the
          requested Payments account.
          PAYMENTS_PROFILE_INELIGIBLE (int): Billing Setup creation failed because Payments considers requested
          Payments profile ineligible.
          PAYMENTS_ACCOUNT_INELIGIBLE (int): Billing Setup creation failed because Payments considers requested
          Payments account ineligible.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        CANNOT_USE_EXISTING_AND_NEW_ACCOUNT = 2
        CANNOT_REMOVE_STARTED_BILLING_SETUP = 3
        CANNOT_CHANGE_BILLING_TO_SAME_PAYMENTS_ACCOUNT = 4
        BILLING_SETUP_NOT_PERMITTED_FOR_CUSTOMER_STATUS = 5
        INVALID_PAYMENTS_ACCOUNT = 6
        BILLING_SETUP_NOT_PERMITTED_FOR_CUSTOMER_CATEGORY = 7
        INVALID_START_TIME_TYPE = 8
        THIRD_PARTY_ALREADY_HAS_BILLING = 9
        BILLING_SETUP_IN_PROGRESS = 10
        NO_SIGNUP_PERMISSION = 11
        CHANGE_OF_BILL_TO_IN_PROGRESS = 12
        PAYMENTS_PROFILE_NOT_FOUND = 13
        PAYMENTS_ACCOUNT_NOT_FOUND = 14
        PAYMENTS_PROFILE_INELIGIBLE = 15
        PAYMENTS_ACCOUNT_INELIGIBLE = 16


class BillingSetupStatusEnum(object):
    class BillingSetupStatus(enum.IntEnum):
        """
        The possible statuses of a BillingSetup.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          PENDING (int): The billing setup is pending approval.
          APPROVED_HELD (int): The billing setup has been approved but the corresponding first budget
          has not.  This can only occur for billing setups configured for monthly
          invoicing.
          APPROVED (int): The billing setup has been approved.
          CANCELLED (int): The billing setup was cancelled by the user prior to approval.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        PENDING = 2
        APPROVED_HELD = 3
        APPROVED = 4
        CANCELLED = 5


class BrandSafetySuitabilityEnum(object):
    class BrandSafetySuitability(enum.IntEnum):
        """
        3-Tier brand safety suitability control.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          EXPANDED_INVENTORY (int): This option lets you show ads across all inventory on YouTube and video
          partners that meet our standards for monetization. This option may be an
          appropriate choice for brands that want maximum access to the full
          breadth of videos eligible for ads, including, for example, videos that
          have strong profanity in the context of comedy or a documentary, or
          excessive violence as featured in video games.
          STANDARD_INVENTORY (int): This option lets you show ads across a wide range of content that's
          appropriate for most brands, such as popular music videos, documentaries,
          and movie trailers. The content you can show ads on is based on YouTube's
          advertiser-friendly content guidelines that take into account, for
          example, the strength or frequency of profanity, or the appropriateness
          of subject matter like sensitive events. Ads won't show, for example, on
          content with repeated strong profanity, strong sexual content, or graphic
          violence.
          LIMITED_INVENTORY (int): This option lets you show ads on a reduced range of content that's
          appropriate for brands with particularly strict guidelines around
          inappropriate language and sexual suggestiveness; above and beyond what
          YouTube's advertiser-friendly content guidelines address. The videos
          accessible in this sensitive category meet heightened requirements,
          especially for inappropriate language and sexual suggestiveness. For
          example, your ads will be excluded from showing on some of YouTube's most
          popular music videos and other pop culture content across YouTube and
          Google video partners.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        EXPANDED_INVENTORY = 2
        STANDARD_INVENTORY = 3
        LIMITED_INVENTORY = 4


class BudgetDeliveryMethodEnum(object):
    class BudgetDeliveryMethod(enum.IntEnum):
        """
        Possible delivery methods of a Budget.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          STANDARD (int): The budget server will throttle serving evenly across
          the entire time period.
          ACCELERATED (int): The budget server will not throttle serving,
          and ads will serve as fast as possible.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        STANDARD = 2
        ACCELERATED = 3


class BudgetPeriodEnum(object):
    class BudgetPeriod(enum.IntEnum):
        """
        Possible period of a Budget.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          DAILY (int): Daily budget.
          CUSTOM (int): Custom budget.
          FIXED_DAILY (int): Fixed daily budget.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        DAILY = 2
        CUSTOM = 3
        FIXED_DAILY = 4


class BudgetStatusEnum(object):
    class BudgetStatus(enum.IntEnum):
        """
        Possible statuses of a Budget.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          ENABLED (int): Budget is enabled.
          REMOVED (int): Budget is removed.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        ENABLED = 2
        REMOVED = 3


class BudgetTypeEnum(object):
    class BudgetType(enum.IntEnum):
        """
        Possible Budget types.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          STANDARD (int): Budget type for standard Google Ads usage.
          Caps daily spend at two times the specified budget amount.
          Full details: https://support.google.com/google-ads/answer/6385083
          HOTEL_ADS_COMMISSION (int): Budget type for Hotels Ads commission program. Full details:
          https://support.google.com/google-ads/answer/9243945

          This type is only supported by campaigns with
          AdvertisingChannelType.HOTEL, BiddingStrategyType.COMMISSION and
          PaymentMode.CONVERSION\_VALUE.
          FIXED_CPA (int): Budget type with a fixed cost-per-acquisition (conversion). Full
          details: https://support.google.com/google-ads/answer/7528254

          This type is only supported by campaigns with
          AdvertisingChannelType.DISPLAY (excluding
          AdvertisingChannelSubType.DISPLAY\_GMAIL),
          BiddingStrategyType.TARGET\_CPA and PaymentMode.CONVERSIONS.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        STANDARD = 2
        HOTEL_ADS_COMMISSION = 3
        FIXED_CPA = 4


class CallConversionReportingStateEnum(object):
    class CallConversionReportingState(enum.IntEnum):
        """
        Possible data types for a call conversion action state.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          DISABLED (int): Call conversion action is disabled.
          USE_ACCOUNT_LEVEL_CALL_CONVERSION_ACTION (int): Call conversion action will use call conversion type set at the
          account level.
          USE_RESOURCE_LEVEL_CALL_CONVERSION_ACTION (int): Call conversion action will use call conversion type set at the resource
          (call only ads/call extensions) level.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        DISABLED = 2
        USE_ACCOUNT_LEVEL_CALL_CONVERSION_ACTION = 3
        USE_RESOURCE_LEVEL_CALL_CONVERSION_ACTION = 4


class CallPlaceholderFieldEnum(object):
    class CallPlaceholderField(enum.IntEnum):
        """
        Possible values for Call placeholder fields.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          PHONE_NUMBER (int): Data Type: STRING. The advertiser's phone number to append to the ad.
          COUNTRY_CODE (int): Data Type: STRING. Uppercase two-letter country code of the advertiser's
          phone number.
          TRACKED (int): Data Type: BOOLEAN. Indicates whether call tracking is enabled. Default:
          true.
          CONVERSION_TYPE_ID (int): Data Type: INT64. The ID of an AdCallMetricsConversion object. This
          object contains the phoneCallDurationfield which is the minimum duration
          (in seconds) of a call to be considered a conversion.
          CONVERSION_REPORTING_STATE (int): Data Type: STRING. Indicates whether this call extension uses its own
          call conversion setting or follows the account level setting. Valid
          values are: USE\_ACCOUNT\_LEVEL\_CALL\_CONVERSION\_ACTION and
          USE\_RESOURCE\_LEVEL\_CALL\_CONVERSION\_ACTION.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        PHONE_NUMBER = 2
        COUNTRY_CODE = 3
        TRACKED = 4
        CONVERSION_TYPE_ID = 5
        CONVERSION_REPORTING_STATE = 6


class CalloutPlaceholderFieldEnum(object):
    class CalloutPlaceholderField(enum.IntEnum):
        """
        Possible values for Callout placeholder fields.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          CALLOUT_TEXT (int): Data Type: STRING. Callout text.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        CALLOUT_TEXT = 2


class CampaignBudgetErrorEnum(object):
    class CampaignBudgetError(enum.IntEnum):
        """
        Enum describing possible campaign budget errors.

        Attributes:
          UNSPECIFIED (int): Enum unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          CAMPAIGN_BUDGET_CANNOT_BE_SHARED (int): The campaign budget cannot be shared.
          CAMPAIGN_BUDGET_REMOVED (int): The requested campaign budget no longer exists.
          CAMPAIGN_BUDGET_IN_USE (int): The campaign budget is associated with at least one campaign, and so the
          campaign budget cannot be removed.
          CAMPAIGN_BUDGET_PERIOD_NOT_AVAILABLE (int): Customer is not whitelisted for this campaign budget period.
          CANNOT_MODIFY_FIELD_OF_IMPLICITLY_SHARED_CAMPAIGN_BUDGET (int): This field is not mutable on implicitly shared campaign budgets
          CANNOT_UPDATE_CAMPAIGN_BUDGET_TO_IMPLICITLY_SHARED (int): Cannot change explicitly shared campaign budgets back to implicitly
          shared ones.
          CANNOT_UPDATE_CAMPAIGN_BUDGET_TO_EXPLICITLY_SHARED_WITHOUT_NAME (int): An implicit campaign budget without a name cannot be changed to
          explicitly shared campaign budget.
          CANNOT_UPDATE_CAMPAIGN_BUDGET_TO_EXPLICITLY_SHARED (int): Cannot change an implicitly shared campaign budget to an explicitly
          shared one.
          CANNOT_USE_IMPLICITLY_SHARED_CAMPAIGN_BUDGET_WITH_MULTIPLE_CAMPAIGNS (int): Only explicitly shared campaign budgets can be used with multiple
          campaigns.
          DUPLICATE_NAME (int): A campaign budget with this name already exists.
          MONEY_AMOUNT_IN_WRONG_CURRENCY (int): A money amount was not in the expected currency.
          MONEY_AMOUNT_LESS_THAN_CURRENCY_MINIMUM_CPC (int): A money amount was less than the minimum CPC for currency.
          MONEY_AMOUNT_TOO_LARGE (int): A money amount was greater than the maximum allowed.
          NEGATIVE_MONEY_AMOUNT (int): A money amount was negative.
          NON_MULTIPLE_OF_MINIMUM_CURRENCY_UNIT (int): A money amount was not a multiple of a minimum unit.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        CAMPAIGN_BUDGET_CANNOT_BE_SHARED = 17
        CAMPAIGN_BUDGET_REMOVED = 2
        CAMPAIGN_BUDGET_IN_USE = 3
        CAMPAIGN_BUDGET_PERIOD_NOT_AVAILABLE = 4
        CANNOT_MODIFY_FIELD_OF_IMPLICITLY_SHARED_CAMPAIGN_BUDGET = 6
        CANNOT_UPDATE_CAMPAIGN_BUDGET_TO_IMPLICITLY_SHARED = 7
        CANNOT_UPDATE_CAMPAIGN_BUDGET_TO_EXPLICITLY_SHARED_WITHOUT_NAME = 8
        CANNOT_UPDATE_CAMPAIGN_BUDGET_TO_EXPLICITLY_SHARED = 9
        CANNOT_USE_IMPLICITLY_SHARED_CAMPAIGN_BUDGET_WITH_MULTIPLE_CAMPAIGNS = 10
        DUPLICATE_NAME = 11
        MONEY_AMOUNT_IN_WRONG_CURRENCY = 12
        MONEY_AMOUNT_LESS_THAN_CURRENCY_MINIMUM_CPC = 13
        MONEY_AMOUNT_TOO_LARGE = 14
        NEGATIVE_MONEY_AMOUNT = 15
        NON_MULTIPLE_OF_MINIMUM_CURRENCY_UNIT = 16


class CampaignCriterionErrorEnum(object):
    class CampaignCriterionError(enum.IntEnum):
        """
        Enum describing possible campaign criterion errors.

        Attributes:
          UNSPECIFIED (int): Enum unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          CONCRETE_TYPE_REQUIRED (int): Concrete type of criterion (keyword v.s. placement) is required for
          CREATE and UPDATE operations.
          INVALID_PLACEMENT_URL (int): Invalid placement URL.
          CANNOT_EXCLUDE_CRITERIA_TYPE (int): Criteria type can not be excluded for the campaign by the customer. like
          AOL account type cannot target site type criteria
          CANNOT_SET_STATUS_FOR_CRITERIA_TYPE (int): Cannot set the campaign criterion status for this criteria type.
          CANNOT_SET_STATUS_FOR_EXCLUDED_CRITERIA (int): Cannot set the campaign criterion status for an excluded criteria.
          CANNOT_TARGET_AND_EXCLUDE (int): Cannot target and exclude the same criterion.
          TOO_MANY_OPERATIONS (int): The mutate contained too many operations.
          OPERATOR_NOT_SUPPORTED_FOR_CRITERION_TYPE (int): This operator cannot be applied to a criterion of this type.
          SHOPPING_CAMPAIGN_SALES_COUNTRY_NOT_SUPPORTED_FOR_SALES_CHANNEL (int): The Shopping campaign sales country is not supported for
          ProductSalesChannel targeting.
          CANNOT_ADD_EXISTING_FIELD (int): The existing field can't be updated with CREATE operation. It can be
          updated with UPDATE operation only.
          CANNOT_UPDATE_NEGATIVE_CRITERION (int): Negative criteria are immutable, so updates are not allowed.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        CONCRETE_TYPE_REQUIRED = 2
        INVALID_PLACEMENT_URL = 3
        CANNOT_EXCLUDE_CRITERIA_TYPE = 4
        CANNOT_SET_STATUS_FOR_CRITERIA_TYPE = 5
        CANNOT_SET_STATUS_FOR_EXCLUDED_CRITERIA = 6
        CANNOT_TARGET_AND_EXCLUDE = 7
        TOO_MANY_OPERATIONS = 8
        OPERATOR_NOT_SUPPORTED_FOR_CRITERION_TYPE = 9
        SHOPPING_CAMPAIGN_SALES_COUNTRY_NOT_SUPPORTED_FOR_SALES_CHANNEL = 10
        CANNOT_ADD_EXISTING_FIELD = 11
        CANNOT_UPDATE_NEGATIVE_CRITERION = 12


class CampaignCriterionStatusEnum(object):
    class CampaignCriterionStatus(enum.IntEnum):
        """
        The possible statuses of a CampaignCriterion.

        Attributes:
          UNSPECIFIED (int): No value has been specified.
          UNKNOWN (int): The received value is not known in this version.

          This is a response-only value.
          ENABLED (int): The campaign criterion is enabled.
          PAUSED (int): The campaign criterion is paused.
          REMOVED (int): The campaign criterion is removed.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        ENABLED = 2
        PAUSED = 3
        REMOVED = 4


class CampaignDraftErrorEnum(object):
    class CampaignDraftError(enum.IntEnum):
        """
        Enum describing possible campaign draft errors.

        Attributes:
          UNSPECIFIED (int): Enum unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          DUPLICATE_DRAFT_NAME (int): A draft with this name already exists for this campaign.
          INVALID_STATUS_TRANSITION_FROM_REMOVED (int): The draft is removed and cannot be transitioned to another status.
          INVALID_STATUS_TRANSITION_FROM_PROMOTED (int): The draft has been promoted and cannot be transitioned to the specified
          status.
          INVALID_STATUS_TRANSITION_FROM_PROMOTE_FAILED (int): The draft has failed to be promoted and cannot be transitioned to the
          specified status.
          CUSTOMER_CANNOT_CREATE_DRAFT (int): This customer is not allowed to create drafts.
          CAMPAIGN_CANNOT_CREATE_DRAFT (int): This campaign is not allowed to create drafts.
          INVALID_DRAFT_CHANGE (int): This modification cannot be made on a draft.
          INVALID_STATUS_TRANSITION (int): The draft cannot be transitioned to the specified status from its
          current status.
          MAX_NUMBER_OF_DRAFTS_PER_CAMPAIGN_REACHED (int): The campaign has reached the maximum number of drafts that can be created
          for a campaign throughout its lifetime. No additional drafts can be
          created for this campaign. Removed drafts also count towards this limit.
          LIST_ERRORS_FOR_PROMOTED_DRAFT_ONLY (int): ListAsyncErrors was called without first promoting the draft.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        DUPLICATE_DRAFT_NAME = 2
        INVALID_STATUS_TRANSITION_FROM_REMOVED = 3
        INVALID_STATUS_TRANSITION_FROM_PROMOTED = 4
        INVALID_STATUS_TRANSITION_FROM_PROMOTE_FAILED = 5
        CUSTOMER_CANNOT_CREATE_DRAFT = 6
        CAMPAIGN_CANNOT_CREATE_DRAFT = 7
        INVALID_DRAFT_CHANGE = 8
        INVALID_STATUS_TRANSITION = 9
        MAX_NUMBER_OF_DRAFTS_PER_CAMPAIGN_REACHED = 10
        LIST_ERRORS_FOR_PROMOTED_DRAFT_ONLY = 11


class CampaignDraftStatusEnum(object):
    class CampaignDraftStatus(enum.IntEnum):
        """
        Possible statuses of a campaign draft.

        Attributes:
          UNSPECIFIED (int): The status has not been specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          PROPOSED (int): Initial state of the draft, the advertiser can start adding changes with
          no effect on serving.
          REMOVED (int): The campaign draft is removed.
          PROMOTING (int): Advertiser requested to promote draft's changes back into the original
          campaign. Advertiser can poll the long running operation returned by
          the promote action to see the status of the promotion.
          PROMOTED (int): The process to merge changes in the draft back to the original campaign
          has completed successfully.
          PROMOTE_FAILED (int): The promotion failed after it was partially applied. Promote cannot be
          attempted again safely, so the issue must be corrected in the original
          campaign.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        PROPOSED = 2
        REMOVED = 3
        PROMOTING = 5
        PROMOTED = 4
        PROMOTE_FAILED = 6


class CampaignErrorEnum(object):
    class CampaignError(enum.IntEnum):
        """
        Enum describing possible campaign errors.

        Attributes:
          UNSPECIFIED (int): Enum unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          CANNOT_TARGET_CONTENT_NETWORK (int): Cannot target content network.
          CANNOT_TARGET_SEARCH_NETWORK (int): Cannot target search network.
          CANNOT_TARGET_SEARCH_NETWORK_WITHOUT_GOOGLE_SEARCH (int): Cannot cover search network without google search network.
          CANNOT_TARGET_GOOGLE_SEARCH_FOR_CPM_CAMPAIGN (int): Cannot target Google Search network for a CPM campaign.
          CAMPAIGN_MUST_TARGET_AT_LEAST_ONE_NETWORK (int): Must target at least one network.
          CANNOT_TARGET_PARTNER_SEARCH_NETWORK (int): Only some Google partners are allowed to target partner search network.
          CANNOT_TARGET_CONTENT_NETWORK_ONLY_WITH_CRITERIA_LEVEL_BIDDING_STRATEGY (int): Cannot target content network only as campaign has criteria-level bidding
          strategy.
          CAMPAIGN_DURATION_MUST_CONTAIN_ALL_RUNNABLE_TRIALS (int): Cannot modify the start or end date such that the campaign duration would
          not contain the durations of all runnable trials.
          CANNOT_MODIFY_FOR_TRIAL_CAMPAIGN (int): Cannot modify dates, budget or campaign name of a trial campaign.
          DUPLICATE_CAMPAIGN_NAME (int): Trying to modify the name of an active or paused campaign, where the name
          is already assigned to another active or paused campaign.
          INCOMPATIBLE_CAMPAIGN_FIELD (int): Two fields are in conflicting modes.
          INVALID_CAMPAIGN_NAME (int): Campaign name cannot be used.
          INVALID_AD_SERVING_OPTIMIZATION_STATUS (int): Given status is invalid.
          INVALID_TRACKING_URL (int): Error in the campaign level tracking url.
          CANNOT_SET_BOTH_TRACKING_URL_TEMPLATE_AND_TRACKING_SETTING (int): Cannot set both tracking url template and tracking setting. An user has
          to clear legacy tracking setting in order to add tracking url template.
          MAX_IMPRESSIONS_NOT_IN_RANGE (int): The maximum number of impressions for Frequency Cap should be an integer
          greater than 0.
          TIME_UNIT_NOT_SUPPORTED (int): Only the Day, Week and Month time units are supported.
          INVALID_OPERATION_IF_SERVING_STATUS_HAS_ENDED (int): Operation not allowed on a campaign whose serving status has ended
          BUDGET_CANNOT_BE_SHARED (int): This budget is exclusively linked to a Campaign that is using experiments
          so it cannot be shared.
          CAMPAIGN_CANNOT_USE_SHARED_BUDGET (int): Campaigns using experiments cannot use a shared budget.
          CANNOT_CHANGE_BUDGET_ON_CAMPAIGN_WITH_TRIALS (int): A different budget cannot be assigned to a campaign when there are
          running or scheduled trials.
          CAMPAIGN_LABEL_DOES_NOT_EXIST (int): No link found between the campaign and the label.
          CAMPAIGN_LABEL_ALREADY_EXISTS (int): The label has already been attached to the campaign.
          MISSING_SHOPPING_SETTING (int): A ShoppingSetting was not found when creating a shopping campaign.
          INVALID_SHOPPING_SALES_COUNTRY (int): The country in shopping setting is not an allowed country.
          MISSING_UNIVERSAL_APP_CAMPAIGN_SETTING (int): A Campaign with channel sub type UNIVERSAL\_APP\_CAMPAIGN must have a
          UniversalAppCampaignSetting specified.
          ADVERTISING_CHANNEL_TYPE_NOT_AVAILABLE_FOR_ACCOUNT_TYPE (int): The requested channel type is not available according to the customer's
          account setting.
          INVALID_ADVERTISING_CHANNEL_SUB_TYPE (int): The AdvertisingChannelSubType is not a valid subtype of the primary
          channel type.
          AT_LEAST_ONE_CONVERSION_MUST_BE_SELECTED (int): At least one conversion must be selected.
          CANNOT_SET_AD_ROTATION_MODE (int): Setting ad rotation mode for a campaign is not allowed. Ad rotation mode
          at campaign is deprecated.
          CANNOT_MODIFY_START_DATE_IF_ALREADY_STARTED (int): Trying to change start date on a campaign that has started.
          CANNOT_SET_DATE_TO_PAST (int): Trying to modify a date into the past.
          MISSING_HOTEL_CUSTOMER_LINK (int): Hotel center id in the hotel setting does not match any customer links.
          INVALID_HOTEL_CUSTOMER_LINK (int): Hotel center id in the hotel setting must match an active customer link.
          MISSING_HOTEL_SETTING (int): Hotel setting was not found when creating a hotel ads campaign.
          CANNOT_USE_SHARED_CAMPAIGN_BUDGET_WHILE_PART_OF_CAMPAIGN_GROUP (int): A Campaign cannot use shared campaign budgets and be part of a campaign
          group.
          APP_NOT_FOUND (int): The app ID was not found.
          SHOPPING_ENABLE_LOCAL_NOT_SUPPORTED_FOR_CAMPAIGN_TYPE (int): Campaign.shopping\_setting.enable\_local is not supported for the
          specified campaign type.
          MERCHANT_NOT_ALLOWED_FOR_COMPARISON_LISTING_ADS (int): The merchant does not support the creation of campaigns for Shopping
          Comparison Listing Ads.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        CANNOT_TARGET_CONTENT_NETWORK = 3
        CANNOT_TARGET_SEARCH_NETWORK = 4
        CANNOT_TARGET_SEARCH_NETWORK_WITHOUT_GOOGLE_SEARCH = 5
        CANNOT_TARGET_GOOGLE_SEARCH_FOR_CPM_CAMPAIGN = 6
        CAMPAIGN_MUST_TARGET_AT_LEAST_ONE_NETWORK = 7
        CANNOT_TARGET_PARTNER_SEARCH_NETWORK = 8
        CANNOT_TARGET_CONTENT_NETWORK_ONLY_WITH_CRITERIA_LEVEL_BIDDING_STRATEGY = 9
        CAMPAIGN_DURATION_MUST_CONTAIN_ALL_RUNNABLE_TRIALS = 10
        CANNOT_MODIFY_FOR_TRIAL_CAMPAIGN = 11
        DUPLICATE_CAMPAIGN_NAME = 12
        INCOMPATIBLE_CAMPAIGN_FIELD = 13
        INVALID_CAMPAIGN_NAME = 14
        INVALID_AD_SERVING_OPTIMIZATION_STATUS = 15
        INVALID_TRACKING_URL = 16
        CANNOT_SET_BOTH_TRACKING_URL_TEMPLATE_AND_TRACKING_SETTING = 17
        MAX_IMPRESSIONS_NOT_IN_RANGE = 18
        TIME_UNIT_NOT_SUPPORTED = 19
        INVALID_OPERATION_IF_SERVING_STATUS_HAS_ENDED = 20
        BUDGET_CANNOT_BE_SHARED = 21
        CAMPAIGN_CANNOT_USE_SHARED_BUDGET = 22
        CANNOT_CHANGE_BUDGET_ON_CAMPAIGN_WITH_TRIALS = 23
        CAMPAIGN_LABEL_DOES_NOT_EXIST = 24
        CAMPAIGN_LABEL_ALREADY_EXISTS = 25
        MISSING_SHOPPING_SETTING = 26
        INVALID_SHOPPING_SALES_COUNTRY = 27
        MISSING_UNIVERSAL_APP_CAMPAIGN_SETTING = 30
        ADVERTISING_CHANNEL_TYPE_NOT_AVAILABLE_FOR_ACCOUNT_TYPE = 31
        INVALID_ADVERTISING_CHANNEL_SUB_TYPE = 32
        AT_LEAST_ONE_CONVERSION_MUST_BE_SELECTED = 33
        CANNOT_SET_AD_ROTATION_MODE = 34
        CANNOT_MODIFY_START_DATE_IF_ALREADY_STARTED = 35
        CANNOT_SET_DATE_TO_PAST = 36
        MISSING_HOTEL_CUSTOMER_LINK = 37
        INVALID_HOTEL_CUSTOMER_LINK = 38
        MISSING_HOTEL_SETTING = 39
        CANNOT_USE_SHARED_CAMPAIGN_BUDGET_WHILE_PART_OF_CAMPAIGN_GROUP = 40
        APP_NOT_FOUND = 41
        SHOPPING_ENABLE_LOCAL_NOT_SUPPORTED_FOR_CAMPAIGN_TYPE = 42
        MERCHANT_NOT_ALLOWED_FOR_COMPARISON_LISTING_ADS = 43


class CampaignExperimentErrorEnum(object):
    class CampaignExperimentError(enum.IntEnum):
        """
        Enum describing possible campaign experiment errors.

        Attributes:
          UNSPECIFIED (int): Enum unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          DUPLICATE_NAME (int): An active campaign or experiment with this name already exists.
          INVALID_TRANSITION (int): Experiment cannot be updated from the current state to the
          requested target state. For example, an experiment can only graduate
          if its status is ENABLED.
          CANNOT_CREATE_EXPERIMENT_WITH_SHARED_BUDGET (int): Cannot create an experiment from a campaign using an explicitly shared
          budget.
          CANNOT_CREATE_EXPERIMENT_FOR_REMOVED_BASE_CAMPAIGN (int): Cannot create an experiment for a removed base campaign.
          CANNOT_CREATE_EXPERIMENT_FOR_NON_PROPOSED_DRAFT (int): Cannot create an experiment from a draft, which has a status other than
          proposed.
          CUSTOMER_CANNOT_CREATE_EXPERIMENT (int): This customer is not allowed to create an experiment.
          CAMPAIGN_CANNOT_CREATE_EXPERIMENT (int): This campaign is not allowed to create an experiment.
          EXPERIMENT_DURATIONS_MUST_NOT_OVERLAP (int): Trying to set an experiment duration which overlaps with another
          experiment.
          EXPERIMENT_DURATION_MUST_BE_WITHIN_CAMPAIGN_DURATION (int): All non-removed experiments must start and end within their campaign's
          duration.
          CANNOT_MUTATE_EXPERIMENT_DUE_TO_STATUS (int): The experiment cannot be modified because its status is in a terminal
          state, such as REMOVED.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        DUPLICATE_NAME = 2
        INVALID_TRANSITION = 3
        CANNOT_CREATE_EXPERIMENT_WITH_SHARED_BUDGET = 4
        CANNOT_CREATE_EXPERIMENT_FOR_REMOVED_BASE_CAMPAIGN = 5
        CANNOT_CREATE_EXPERIMENT_FOR_NON_PROPOSED_DRAFT = 6
        CUSTOMER_CANNOT_CREATE_EXPERIMENT = 7
        CAMPAIGN_CANNOT_CREATE_EXPERIMENT = 8
        EXPERIMENT_DURATIONS_MUST_NOT_OVERLAP = 9
        EXPERIMENT_DURATION_MUST_BE_WITHIN_CAMPAIGN_DURATION = 10
        CANNOT_MUTATE_EXPERIMENT_DUE_TO_STATUS = 11


class CampaignExperimentStatusEnum(object):
    class CampaignExperimentStatus(enum.IntEnum):
        """
        Possible statuses of a campaign experiment.

        Attributes:
          UNSPECIFIED (int): The status has not been specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          INITIALIZING (int): The experiment campaign is being initialized.
          INITIALIZATION_FAILED (int): Initialization of the experiment campaign failed.
          ENABLED (int): The experiment campaign is fully initialized. The experiment is currently
          running, scheduled to run in the future or has ended based on its
          end date. An experiment with the status INITIALIZING will be updated to
          ENABLED when it is fully created.
          GRADUATED (int): The experiment campaign was graduated to a stand-alone
          campaign, existing independently of the experiment.
          REMOVED (int): The experiment is removed.
          PROMOTING (int): The experiment's changes are being applied to the original campaign.
          The long running operation returned by the promote method can be polled
          to see the status of the promotion.
          PROMOTION_FAILED (int): Promote of the experiment campaign failed.
          PROMOTED (int): The changes of the experiment are promoted to their original campaign.
          ENDED_MANUALLY (int): The experiment was ended manually. It did not end based on its end date.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        INITIALIZING = 2
        INITIALIZATION_FAILED = 8
        ENABLED = 3
        GRADUATED = 4
        REMOVED = 5
        PROMOTING = 6
        PROMOTION_FAILED = 9
        PROMOTED = 7
        ENDED_MANUALLY = 10


class CampaignExperimentTrafficSplitTypeEnum(object):
    class CampaignExperimentTrafficSplitType(enum.IntEnum):
        """
        Enum of strategies for splitting traffic between base and experiment
        campaigns in campaign experiment.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          RANDOM_QUERY (int): Traffic is randomly assigned to the base or experiment arm for each
          query, independent of previous assignments for the same user.
          COOKIE (int): Traffic is split using cookies to keep users in the same arm (base or
          experiment) of the experiment.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        RANDOM_QUERY = 2
        COOKIE = 3


class CampaignExperimentTypeEnum(object):
    class CampaignExperimentType(enum.IntEnum):
        """
        Indicates if this campaign is a normal campaign,
        a draft campaign, or an experiment campaign.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          BASE (int): This is a regular campaign.
          DRAFT (int): This is a draft version of a campaign.
          It has some modifications from a base campaign,
          but it does not serve or accrue metrics.
          EXPERIMENT (int): This is an experiment version of a campaign.
          It has some modifications from a base campaign,
          and a percentage of traffic is being diverted
          from the BASE campaign to this experiment campaign.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        BASE = 2
        DRAFT = 3
        EXPERIMENT = 4


class CampaignFeedErrorEnum(object):
    class CampaignFeedError(enum.IntEnum):
        """
        Enum describing possible campaign feed errors.

        Attributes:
          UNSPECIFIED (int): Enum unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          FEED_ALREADY_EXISTS_FOR_PLACEHOLDER_TYPE (int): An active feed already exists for this campaign and placeholder type.
          CANNOT_CREATE_FOR_REMOVED_FEED (int): The specified feed is removed.
          CANNOT_CREATE_ALREADY_EXISTING_CAMPAIGN_FEED (int): The CampaignFeed already exists. UPDATE should be used to modify the
          existing CampaignFeed.
          CANNOT_MODIFY_REMOVED_CAMPAIGN_FEED (int): Cannot update removed campaign feed.
          INVALID_PLACEHOLDER_TYPE (int): Invalid placeholder type.
          MISSING_FEEDMAPPING_FOR_PLACEHOLDER_TYPE (int): Feed mapping for this placeholder type does not exist.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        FEED_ALREADY_EXISTS_FOR_PLACEHOLDER_TYPE = 2
        CANNOT_CREATE_FOR_REMOVED_FEED = 4
        CANNOT_CREATE_ALREADY_EXISTING_CAMPAIGN_FEED = 5
        CANNOT_MODIFY_REMOVED_CAMPAIGN_FEED = 6
        INVALID_PLACEHOLDER_TYPE = 7
        MISSING_FEEDMAPPING_FOR_PLACEHOLDER_TYPE = 8


class CampaignServingStatusEnum(object):
    class CampaignServingStatus(enum.IntEnum):
        """
        Possible serving statuses of a campaign.

        Attributes:
          UNSPECIFIED (int): No value has been specified.
          UNKNOWN (int): The received value is not known in this version.

          This is a response-only value.
          SERVING (int): Serving.
          NONE (int): None.
          ENDED (int): Ended.
          PENDING (int): Pending.
          SUSPENDED (int): Suspended.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        SERVING = 2
        NONE = 3
        ENDED = 4
        PENDING = 5
        SUSPENDED = 6


class CampaignSharedSetErrorEnum(object):
    class CampaignSharedSetError(enum.IntEnum):
        """
        Enum describing possible campaign shared set errors.

        Attributes:
          UNSPECIFIED (int): Enum unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          SHARED_SET_ACCESS_DENIED (int): The shared set belongs to another customer and permission isn't granted.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        SHARED_SET_ACCESS_DENIED = 2


class CampaignSharedSetStatusEnum(object):
    class CampaignSharedSetStatus(enum.IntEnum):
        """
        Enum listing the possible campaign shared set statuses.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          ENABLED (int): The campaign shared set is enabled.
          REMOVED (int): The campaign shared set is removed and can no longer be used.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        ENABLED = 2
        REMOVED = 3


class CampaignStatusEnum(object):
    class CampaignStatus(enum.IntEnum):
        """
        Possible statuses of a campaign.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          ENABLED (int): Campaign is currently serving ads depending on budget information.
          PAUSED (int): Campaign has been paused by the user.
          REMOVED (int): Campaign has been removed.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        ENABLED = 2
        PAUSED = 3
        REMOVED = 4


class ChangeStatusErrorEnum(object):
    class ChangeStatusError(enum.IntEnum):
        """
        Enum describing possible change status errors.

        Attributes:
          UNSPECIFIED (int): Enum unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          START_DATE_TOO_OLD (int): The requested start date is too old.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        START_DATE_TOO_OLD = 3


class ChangeStatusOperationEnum(object):
    class ChangeStatusOperation(enum.IntEnum):
        """
        Status of the changed resource

        Attributes:
          UNSPECIFIED (int): No value has been specified.
          UNKNOWN (int): Used for return value only. Represents an unclassified resource unknown
          in this version.
          ADDED (int): The resource was created.
          CHANGED (int): The resource was modified.
          REMOVED (int): The resource was removed.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        ADDED = 2
        CHANGED = 3
        REMOVED = 4


class ChangeStatusResourceTypeEnum(object):
    class ChangeStatusResourceType(enum.IntEnum):
        """
        Enum listing the resource types support by the ChangeStatus resource.

        Attributes:
          UNSPECIFIED (int): No value has been specified.
          UNKNOWN (int): Used for return value only. Represents an unclassified resource unknown
          in this version.
          AD_GROUP (int): An AdGroup resource change.
          AD_GROUP_AD (int): An AdGroupAd resource change.
          AD_GROUP_CRITERION (int): An AdGroupCriterion resource change.
          CAMPAIGN (int): A Campaign resource change.
          CAMPAIGN_CRITERION (int): A CampaignCriterion resource change.
          FEED (int): A Feed resource change.
          FEED_ITEM (int): A FeedItem resource change.
          AD_GROUP_FEED (int): An AdGroupFeed resource change.
          CAMPAIGN_FEED (int): A CampaignFeed resource change.
          AD_GROUP_BID_MODIFIER (int): An AdGroupBidModifier resource change.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        AD_GROUP = 3
        AD_GROUP_AD = 4
        AD_GROUP_CRITERION = 5
        CAMPAIGN = 6
        CAMPAIGN_CRITERION = 7
        FEED = 9
        FEED_ITEM = 10
        AD_GROUP_FEED = 11
        CAMPAIGN_FEED = 12
        AD_GROUP_BID_MODIFIER = 13


class ClickTypeEnum(object):
    class ClickType(enum.IntEnum):
        """
        Enumerates Google Ads click types.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): The value is unknown in this version.
          APP_DEEPLINK (int): App engagement ad deep link.
          BREADCRUMBS (int): Breadcrumbs.
          BROADBAND_PLAN (int): Broadband Plan.
          CALL_TRACKING (int): Manually dialed phone calls.
          CALLS (int): Phone calls.
          CLICK_ON_ENGAGEMENT_AD (int): Click on engagement ad.
          GET_DIRECTIONS (int): Driving direction.
          LOCATION_EXPANSION (int): Get location details.
          LOCATION_FORMAT_CALL (int): Call.
          LOCATION_FORMAT_DIRECTIONS (int): Directions.
          LOCATION_FORMAT_IMAGE (int): Image(s).
          LOCATION_FORMAT_LANDING_PAGE (int): Go to landing page.
          LOCATION_FORMAT_MAP (int): Map.
          LOCATION_FORMAT_STORE_INFO (int): Go to store info.
          LOCATION_FORMAT_TEXT (int): Text.
          MOBILE_CALL_TRACKING (int): Mobile phone calls.
          OFFER_PRINTS (int): Print offer.
          OTHER (int): Other.
          PRODUCT_EXTENSION_CLICKS (int): Product plusbox offer.
          PRODUCT_LISTING_AD_CLICKS (int): Shopping - Product - Online.
          SITELINKS (int): Sitelink.
          STORE_LOCATOR (int): Show nearby locations.
          URL_CLICKS (int): Headline.
          VIDEO_APP_STORE_CLICKS (int): App store.
          VIDEO_CALL_TO_ACTION_CLICKS (int): Call-to-Action overlay.
          VIDEO_CARD_ACTION_HEADLINE_CLICKS (int): Cards.
          VIDEO_END_CAP_CLICKS (int): End cap.
          VIDEO_WEBSITE_CLICKS (int): Website.
          VISUAL_SITELINKS (int): Visual Sitelinks.
          WIRELESS_PLAN (int): Wireless Plan.
          PRODUCT_LISTING_AD_LOCAL (int): Shopping - Product - Local.
          PRODUCT_LISTING_AD_MULTICHANNEL_LOCAL (int): Shopping - Product - MultiChannel Local.
          PRODUCT_LISTING_AD_MULTICHANNEL_ONLINE (int): Shopping - Product - MultiChannel Online.
          PRODUCT_LISTING_ADS_COUPON (int): Shopping - Product - Coupon.
          PRODUCT_LISTING_AD_TRANSACTABLE (int): Shopping - Product - Sell on Google.
          PRODUCT_AD_APP_DEEPLINK (int): Shopping - Product - App engagement ad deep link.
          SHOWCASE_AD_CATEGORY_LINK (int): Shopping - Showcase - Category.
          SHOWCASE_AD_LOCAL_STOREFRONT_LINK (int): Shopping - Showcase - Local storefront.
          SHOWCASE_AD_ONLINE_PRODUCT_LINK (int): Shopping - Showcase - Online product.
          SHOWCASE_AD_LOCAL_PRODUCT_LINK (int): Shopping - Showcase - Local product.
          PROMOTION_EXTENSION (int): Promotion Extension.
          SWIPEABLE_GALLERY_AD_HEADLINE (int): Ad Headline.
          SWIPEABLE_GALLERY_AD_SWIPES (int): Swipes.
          SWIPEABLE_GALLERY_AD_SEE_MORE (int): See More.
          SWIPEABLE_GALLERY_AD_SITELINK_ONE (int): Sitelink 1.
          SWIPEABLE_GALLERY_AD_SITELINK_TWO (int): Sitelink 2.
          SWIPEABLE_GALLERY_AD_SITELINK_THREE (int): Sitelink 3.
          SWIPEABLE_GALLERY_AD_SITELINK_FOUR (int): Sitelink 4.
          SWIPEABLE_GALLERY_AD_SITELINK_FIVE (int): Sitelink 5.
          HOTEL_PRICE (int): Hotel price.
          PRICE_EXTENSION (int): Price Extension.
          HOTEL_BOOK_ON_GOOGLE_ROOM_SELECTION (int): Book on Google hotel room selection.
          SHOPPING_COMPARISON_LISTING (int): Shopping - Comparison Listing.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        APP_DEEPLINK = 2
        BREADCRUMBS = 3
        BROADBAND_PLAN = 4
        CALL_TRACKING = 5
        CALLS = 6
        CLICK_ON_ENGAGEMENT_AD = 7
        GET_DIRECTIONS = 8
        LOCATION_EXPANSION = 9
        LOCATION_FORMAT_CALL = 10
        LOCATION_FORMAT_DIRECTIONS = 11
        LOCATION_FORMAT_IMAGE = 12
        LOCATION_FORMAT_LANDING_PAGE = 13
        LOCATION_FORMAT_MAP = 14
        LOCATION_FORMAT_STORE_INFO = 15
        LOCATION_FORMAT_TEXT = 16
        MOBILE_CALL_TRACKING = 17
        OFFER_PRINTS = 18
        OTHER = 19
        PRODUCT_EXTENSION_CLICKS = 20
        PRODUCT_LISTING_AD_CLICKS = 21
        SITELINKS = 22
        STORE_LOCATOR = 23
        URL_CLICKS = 25
        VIDEO_APP_STORE_CLICKS = 26
        VIDEO_CALL_TO_ACTION_CLICKS = 27
        VIDEO_CARD_ACTION_HEADLINE_CLICKS = 28
        VIDEO_END_CAP_CLICKS = 29
        VIDEO_WEBSITE_CLICKS = 30
        VISUAL_SITELINKS = 31
        WIRELESS_PLAN = 32
        PRODUCT_LISTING_AD_LOCAL = 33
        PRODUCT_LISTING_AD_MULTICHANNEL_LOCAL = 34
        PRODUCT_LISTING_AD_MULTICHANNEL_ONLINE = 35
        PRODUCT_LISTING_ADS_COUPON = 36
        PRODUCT_LISTING_AD_TRANSACTABLE = 37
        PRODUCT_AD_APP_DEEPLINK = 38
        SHOWCASE_AD_CATEGORY_LINK = 39
        SHOWCASE_AD_LOCAL_STOREFRONT_LINK = 40
        SHOWCASE_AD_ONLINE_PRODUCT_LINK = 42
        SHOWCASE_AD_LOCAL_PRODUCT_LINK = 43
        PROMOTION_EXTENSION = 44
        SWIPEABLE_GALLERY_AD_HEADLINE = 45
        SWIPEABLE_GALLERY_AD_SWIPES = 46
        SWIPEABLE_GALLERY_AD_SEE_MORE = 47
        SWIPEABLE_GALLERY_AD_SITELINK_ONE = 48
        SWIPEABLE_GALLERY_AD_SITELINK_TWO = 49
        SWIPEABLE_GALLERY_AD_SITELINK_THREE = 50
        SWIPEABLE_GALLERY_AD_SITELINK_FOUR = 51
        SWIPEABLE_GALLERY_AD_SITELINK_FIVE = 52
        HOTEL_PRICE = 53
        PRICE_EXTENSION = 54
        HOTEL_BOOK_ON_GOOGLE_ROOM_SELECTION = 55
        SHOPPING_COMPARISON_LISTING = 56


class CollectionSizeErrorEnum(object):
    class CollectionSizeError(enum.IntEnum):
        """
        Enum describing possible collection size errors.

        Attributes:
          UNSPECIFIED (int): Enum unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          TOO_FEW (int): Too few.
          TOO_MANY (int): Too many.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        TOO_FEW = 2
        TOO_MANY = 3


class ContentLabelTypeEnum(object):
    class ContentLabelType(enum.IntEnum):
        """
        Enum listing the content label types supported by ContentLabel criterion.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          SEXUALLY_SUGGESTIVE (int): Sexually suggestive content.
          BELOW_THE_FOLD (int): Below the fold placement.
          PARKED_DOMAIN (int): Parked domain.
          GAME (int): Game.
          JUVENILE (int): Juvenile, gross & bizarre content.
          PROFANITY (int): Profanity & rough language.
          TRAGEDY (int): Death & tragedy.
          VIDEO (int): Video.
          VIDEO_RATING_DV_G (int): Content rating: G.
          VIDEO_RATING_DV_PG (int): Content rating: PG.
          VIDEO_RATING_DV_T (int): Content rating: T.
          VIDEO_RATING_DV_MA (int): Content rating: MA.
          VIDEO_NOT_YET_RATED (int): Content rating: not yet rated.
          EMBEDDED_VIDEO (int): Embedded video.
          LIVE_STREAMING_VIDEO (int): Live streaming video.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        SEXUALLY_SUGGESTIVE = 2
        BELOW_THE_FOLD = 3
        PARKED_DOMAIN = 4
        GAME = 5
        JUVENILE = 6
        PROFANITY = 7
        TRAGEDY = 8
        VIDEO = 9
        VIDEO_RATING_DV_G = 10
        VIDEO_RATING_DV_PG = 11
        VIDEO_RATING_DV_T = 12
        VIDEO_RATING_DV_MA = 13
        VIDEO_NOT_YET_RATED = 14
        EMBEDDED_VIDEO = 15
        LIVE_STREAMING_VIDEO = 16


class ContextErrorEnum(object):
    class ContextError(enum.IntEnum):
        """
        Enum describing possible context errors.

        Attributes:
          UNSPECIFIED (int): Enum unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          OPERATION_NOT_PERMITTED_FOR_CONTEXT (int): The operation is not allowed for the given context.
          OPERATION_NOT_PERMITTED_FOR_REMOVED_RESOURCE (int): The operation is not allowed for removed resources.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        OPERATION_NOT_PERMITTED_FOR_CONTEXT = 2
        OPERATION_NOT_PERMITTED_FOR_REMOVED_RESOURCE = 3


class ConversionActionCategoryEnum(object):
    class ConversionActionCategory(enum.IntEnum):
        """
        The category of conversions that are associated with a ConversionAction.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          DEFAULT (int): Default category.
          PAGE_VIEW (int): User visiting a page.
          PURCHASE (int): Purchase, sales, or "order placed" event.
          SIGNUP (int): Signup user action.
          LEAD (int): Lead-generating action.
          DOWNLOAD (int): Software download action (as for an app).
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        DEFAULT = 2
        PAGE_VIEW = 3
        PURCHASE = 4
        SIGNUP = 5
        LEAD = 6
        DOWNLOAD = 7


class ConversionActionCountingTypeEnum(object):
    class ConversionActionCountingType(enum.IntEnum):
        """
        Indicates how conversions for this action will be counted. For more
        information, see https://support.google.com/google-ads/answer/3438531.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          ONE_PER_CLICK (int): Count only one conversion per click.
          MANY_PER_CLICK (int): Count all conversions per click.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        ONE_PER_CLICK = 2
        MANY_PER_CLICK = 3


class ConversionActionErrorEnum(object):
    class ConversionActionError(enum.IntEnum):
        """
        Enum describing possible conversion action errors.

        Attributes:
          UNSPECIFIED (int): Enum unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          DUPLICATE_NAME (int): The specified conversion action name already exists.
          DUPLICATE_APP_ID (int): Another conversion action with the specified app id already exists.
          TWO_CONVERSION_ACTIONS_BIDDING_ON_SAME_APP_DOWNLOAD (int): Android first open action conflicts with Google play codeless download
          action tracking the same app.
          BIDDING_ON_SAME_APP_DOWNLOAD_AS_GLOBAL_ACTION (int): Android first open action conflicts with Google play codeless download
          action tracking the same app.
          DATA_DRIVEN_MODEL_WAS_NEVER_GENERATED (int): The attribution model cannot be set to DATA\_DRIVEN because a
          data-driven model has never been generated.
          DATA_DRIVEN_MODEL_EXPIRED (int): The attribution model cannot be set to DATA\_DRIVEN because the
          data-driven model is expired.
          DATA_DRIVEN_MODEL_STALE (int): The attribution model cannot be set to DATA\_DRIVEN because the
          data-driven model is stale.
          DATA_DRIVEN_MODEL_UNKNOWN (int): The attribution model cannot be set to DATA\_DRIVEN because the
          data-driven model is unavailable or the conversion action was newly
          added.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        DUPLICATE_NAME = 2
        DUPLICATE_APP_ID = 3
        TWO_CONVERSION_ACTIONS_BIDDING_ON_SAME_APP_DOWNLOAD = 4
        BIDDING_ON_SAME_APP_DOWNLOAD_AS_GLOBAL_ACTION = 5
        DATA_DRIVEN_MODEL_WAS_NEVER_GENERATED = 6
        DATA_DRIVEN_MODEL_EXPIRED = 7
        DATA_DRIVEN_MODEL_STALE = 8
        DATA_DRIVEN_MODEL_UNKNOWN = 9


class ConversionActionStatusEnum(object):
    class ConversionActionStatus(enum.IntEnum):
        """
        Possible statuses of a conversion action.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          ENABLED (int): Conversions will be recorded.
          REMOVED (int): Conversions will not be recorded.
          HIDDEN (int): Conversions will not be recorded and the conversion action will not
          appear in the UI.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        ENABLED = 2
        REMOVED = 3
        HIDDEN = 4


class ConversionActionTypeEnum(object):
    class ConversionActionType(enum.IntEnum):
        """
        Possible types of a conversion action.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          AD_CALL (int): Conversions that occur when a user clicks on an ad's call extension.
          CLICK_TO_CALL (int): Conversions that occur when a user on a mobile device clicks a phone
          number.
          GOOGLE_PLAY_DOWNLOAD (int): Conversions that occur when a user downloads a mobile app from the Google
          Play Store.
          GOOGLE_PLAY_IN_APP_PURCHASE (int): Conversions that occur when a user makes a purchase in an app through
          Android billing.
          UPLOAD_CALLS (int): Call conversions that are tracked by the advertiser and uploaded.
          UPLOAD_CLICKS (int): Conversions that are tracked by the advertiser and uploaded with
          attributed clicks.
          WEBPAGE (int): Conversions that occur on a webpage.
          WEBSITE_CALL (int): Conversions that occur when a user calls a dynamically-generated phone
          number from an advertiser's website.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        AD_CALL = 2
        CLICK_TO_CALL = 3
        GOOGLE_PLAY_DOWNLOAD = 4
        GOOGLE_PLAY_IN_APP_PURCHASE = 5
        UPLOAD_CALLS = 6
        UPLOAD_CLICKS = 7
        WEBPAGE = 8
        WEBSITE_CALL = 9


class ConversionAdjustmentTypeEnum(object):
    class ConversionAdjustmentType(enum.IntEnum):
        """
        The different actions advertisers can take to adjust the conversions that
        they already reported. Retractions negate a conversion. Restatements change
        the value of a conversion.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Represents value unknown in this version.
          RETRACTION (int): Negates a conversion so that its total value and count are both zero.
          RESTATEMENT (int): Changes the value of a conversion.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        RETRACTION = 2
        RESTATEMENT = 3


class ConversionAdjustmentUploadErrorEnum(object):
    class ConversionAdjustmentUploadError(enum.IntEnum):
        """
        Enum describing possible conversion adjustment upload errors.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): The received error code is not known in this version.
          TOO_RECENT_CONVERSION_ACTION (int): The specified conversion action was created too recently.
          Please try the upload again after 4-6 hours have passed since the
          conversion action was created.
          INVALID_CONVERSION_ACTION (int): No conversion action of a supported ConversionActionType that matches the
          provided information can be found for the customer.
          CONVERSION_ALREADY_RETRACTED (int): A retraction was already reported for this conversion.
          CONVERSION_NOT_FOUND (int): A conversion for the supplied combination of conversion
          action and conversion identifier could not be found.
          CONVERSION_EXPIRED (int): The specified conversion has already expired. Conversions expire after 55
          days, after which adjustments cannot be reported against them.
          ADJUSTMENT_PRECEDES_CONVERSION (int): The supplied adjustment date time precedes that of the original
          conversion.
          MORE_RECENT_RESTATEMENT_FOUND (int): A restatement with a more recent adjustment date time was already
          reported for this conversion.
          TOO_RECENT_CONVERSION (int): The conversion was created too recently.
          CANNOT_RESTATE_CONVERSION_ACTION_THAT_ALWAYS_USES_DEFAULT_CONVERSION_VALUE (int): Restatements cannot be reported for a conversion action that always uses
          the default value.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        TOO_RECENT_CONVERSION_ACTION = 2
        INVALID_CONVERSION_ACTION = 3
        CONVERSION_ALREADY_RETRACTED = 4
        CONVERSION_NOT_FOUND = 5
        CONVERSION_EXPIRED = 6
        ADJUSTMENT_PRECEDES_CONVERSION = 7
        MORE_RECENT_RESTATEMENT_FOUND = 8
        TOO_RECENT_CONVERSION = 9
        CANNOT_RESTATE_CONVERSION_ACTION_THAT_ALWAYS_USES_DEFAULT_CONVERSION_VALUE = 10


class ConversionAttributionEventTypeEnum(object):
    class ConversionAttributionEventType(enum.IntEnum):
        """
        The event type of conversions that are attributed to.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Represents value unknown in this version.
          IMPRESSION (int): The conversion is attributed to an impression.
          INTERACTION (int): The conversion is attributed to an interaction.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        IMPRESSION = 2
        INTERACTION = 3


class ConversionLagBucketEnum(object):
    class ConversionLagBucket(enum.IntEnum):
        """
        Enum representing the number of days between impression and conversion.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          LESS_THAN_ONE_DAY (int): Conversion lag bucket from 0 to 1 day. 0 day is included, 1 day is not.
          ONE_TO_TWO_DAYS (int): Conversion lag bucket from 1 to 2 days. 1 day is included, 2 days is not.
          TWO_TO_THREE_DAYS (int): Conversion lag bucket from 2 to 3 days. 2 days is included,
          3 days is not.
          THREE_TO_FOUR_DAYS (int): Conversion lag bucket from 3 to 4 days. 3 days is included,
          4 days is not.
          FOUR_TO_FIVE_DAYS (int): Conversion lag bucket from 4 to 5 days. 4 days is included,
          5 days is not.
          FIVE_TO_SIX_DAYS (int): Conversion lag bucket from 5 to 6 days. 5 days is included,
          6 days is not.
          SIX_TO_SEVEN_DAYS (int): Conversion lag bucket from 6 to 7 days. 6 days is included,
          7 days is not.
          SEVEN_TO_EIGHT_DAYS (int): Conversion lag bucket from 7 to 8 days. 7 days is included,
          8 days is not.
          EIGHT_TO_NINE_DAYS (int): Conversion lag bucket from 8 to 9 days. 8 days is included,
          9 days is not.
          NINE_TO_TEN_DAYS (int): Conversion lag bucket from 9 to 10 days. 9 days is included,
          10 days is not.
          TEN_TO_ELEVEN_DAYS (int): Conversion lag bucket from 10 to 11 days. 10 days is included,
          11 days is not.
          ELEVEN_TO_TWELVE_DAYS (int): Conversion lag bucket from 11 to 12 days. 11 days is included,
          12 days is not.
          TWELVE_TO_THIRTEEN_DAYS (int): Conversion lag bucket from 12 to 13 days. 12 days is included,
          13 days is not.
          THIRTEEN_TO_FOURTEEN_DAYS (int): Conversion lag bucket from 13 to 14 days. 13 days is included,
          14 days is not.
          FOURTEEN_TO_TWENTY_ONE_DAYS (int): Conversion lag bucket from 14 to 21 days. 14 days is included,
          21 days is not.
          TWENTY_ONE_TO_THIRTY_DAYS (int): Conversion lag bucket from 21 to 30 days. 21 days is included,
          30 days is not.
          THIRTY_TO_FORTY_FIVE_DAYS (int): Conversion lag bucket from 30 to 45 days. 30 days is included,
          45 days is not.
          FORTY_FIVE_TO_SIXTY_DAYS (int): Conversion lag bucket from 45 to 60 days. 45 days is included,
          60 days is not.
          SIXTY_TO_NINETY_DAYS (int): Conversion lag bucket from 60 to 90 days. 60 days is included,
          90 days is not.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        LESS_THAN_ONE_DAY = 2
        ONE_TO_TWO_DAYS = 3
        TWO_TO_THREE_DAYS = 4
        THREE_TO_FOUR_DAYS = 5
        FOUR_TO_FIVE_DAYS = 6
        FIVE_TO_SIX_DAYS = 7
        SIX_TO_SEVEN_DAYS = 8
        SEVEN_TO_EIGHT_DAYS = 9
        EIGHT_TO_NINE_DAYS = 10
        NINE_TO_TEN_DAYS = 11
        TEN_TO_ELEVEN_DAYS = 12
        ELEVEN_TO_TWELVE_DAYS = 13
        TWELVE_TO_THIRTEEN_DAYS = 14
        THIRTEEN_TO_FOURTEEN_DAYS = 15
        FOURTEEN_TO_TWENTY_ONE_DAYS = 16
        TWENTY_ONE_TO_THIRTY_DAYS = 17
        THIRTY_TO_FORTY_FIVE_DAYS = 18
        FORTY_FIVE_TO_SIXTY_DAYS = 19
        SIXTY_TO_NINETY_DAYS = 20


class ConversionOrAdjustmentLagBucketEnum(object):
    class ConversionOrAdjustmentLagBucket(enum.IntEnum):
        """
        Enum representing the number of days between the impression and the
        conversion or between the impression and adjustments to the conversion.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          CONVERSION_LESS_THAN_ONE_DAY (int): Conversion lag bucket from 0 to 1 day. 0 day is included, 1 day is not.
          CONVERSION_ONE_TO_TWO_DAYS (int): Conversion lag bucket from 1 to 2 days. 1 day is included, 2 days is not.
          CONVERSION_TWO_TO_THREE_DAYS (int): Conversion lag bucket from 2 to 3 days. 2 days is included,
          3 days is not.
          CONVERSION_THREE_TO_FOUR_DAYS (int): Conversion lag bucket from 3 to 4 days. 3 days is included,
          4 days is not.
          CONVERSION_FOUR_TO_FIVE_DAYS (int): Conversion lag bucket from 4 to 5 days. 4 days is included,
          5 days is not.
          CONVERSION_FIVE_TO_SIX_DAYS (int): Conversion lag bucket from 5 to 6 days. 5 days is included,
          6 days is not.
          CONVERSION_SIX_TO_SEVEN_DAYS (int): Conversion lag bucket from 6 to 7 days. 6 days is included,
          7 days is not.
          CONVERSION_SEVEN_TO_EIGHT_DAYS (int): Conversion lag bucket from 7 to 8 days. 7 days is included,
          8 days is not.
          CONVERSION_EIGHT_TO_NINE_DAYS (int): Conversion lag bucket from 8 to 9 days. 8 days is included,
          9 days is not.
          CONVERSION_NINE_TO_TEN_DAYS (int): Conversion lag bucket from 9 to 10 days. 9 days is included,
          10 days is not.
          CONVERSION_TEN_TO_ELEVEN_DAYS (int): Conversion lag bucket from 10 to 11 days. 10 days is included,
          11 days is not.
          CONVERSION_ELEVEN_TO_TWELVE_DAYS (int): Conversion lag bucket from 11 to 12 days. 11 days is included,
          12 days is not.
          CONVERSION_TWELVE_TO_THIRTEEN_DAYS (int): Conversion lag bucket from 12 to 13 days. 12 days is included,
          13 days is not.
          CONVERSION_THIRTEEN_TO_FOURTEEN_DAYS (int): Conversion lag bucket from 13 to 14 days. 13 days is included,
          14 days is not.
          CONVERSION_FOURTEEN_TO_TWENTY_ONE_DAYS (int): Conversion lag bucket from 14 to 21 days. 14 days is included,
          21 days is not.
          CONVERSION_TWENTY_ONE_TO_THIRTY_DAYS (int): Conversion lag bucket from 21 to 30 days. 21 days is included,
          30 days is not.
          CONVERSION_THIRTY_TO_FORTY_FIVE_DAYS (int): Conversion lag bucket from 30 to 45 days. 30 days is included,
          45 days is not.
          CONVERSION_FORTY_FIVE_TO_SIXTY_DAYS (int): Conversion lag bucket from 45 to 60 days. 45 days is included,
          60 days is not.
          CONVERSION_SIXTY_TO_NINETY_DAYS (int): Conversion lag bucket from 60 to 90 days. 60 days is included,
          90 days is not.
          ADJUSTMENT_LESS_THAN_ONE_DAY (int): Conversion adjustment lag bucket from 0 to 1 day. 0 day is included,
          1 day is not.
          ADJUSTMENT_ONE_TO_TWO_DAYS (int): Conversion adjustment lag bucket from 1 to 2 days. 1 day is included,
          2 days is not.
          ADJUSTMENT_TWO_TO_THREE_DAYS (int): Conversion adjustment lag bucket from 2 to 3 days. 2 days is included,
          3 days is not.
          ADJUSTMENT_THREE_TO_FOUR_DAYS (int): Conversion adjustment lag bucket from 3 to 4 days. 3 days is included,
          4 days is not.
          ADJUSTMENT_FOUR_TO_FIVE_DAYS (int): Conversion adjustment lag bucket from 4 to 5 days. 4 days is included,
          5 days is not.
          ADJUSTMENT_FIVE_TO_SIX_DAYS (int): Conversion adjustment lag bucket from 5 to 6 days. 5 days is included,
          6 days is not.
          ADJUSTMENT_SIX_TO_SEVEN_DAYS (int): Conversion adjustment lag bucket from 6 to 7 days. 6 days is included,
          7 days is not.
          ADJUSTMENT_SEVEN_TO_EIGHT_DAYS (int): Conversion adjustment lag bucket from 7 to 8 days. 7 days is included,
          8 days is not.
          ADJUSTMENT_EIGHT_TO_NINE_DAYS (int): Conversion adjustment lag bucket from 8 to 9 days. 8 days is included,
          9 days is not.
          ADJUSTMENT_NINE_TO_TEN_DAYS (int): Conversion adjustment lag bucket from 9 to 10 days. 9 days is included,
          10 days is not.
          ADJUSTMENT_TEN_TO_ELEVEN_DAYS (int): Conversion adjustment lag bucket from 10 to 11 days. 10 days is included,
          11 days is not.
          ADJUSTMENT_ELEVEN_TO_TWELVE_DAYS (int): Conversion adjustment lag bucket from 11 to 12 days. 11 days is included,
          12 days is not.
          ADJUSTMENT_TWELVE_TO_THIRTEEN_DAYS (int): Conversion adjustment lag bucket from 12 to 13 days. 12 days is included,
          13 days is not.
          ADJUSTMENT_THIRTEEN_TO_FOURTEEN_DAYS (int): Conversion adjustment lag bucket from 13 to 14 days. 13 days is included,
          14 days is not.
          ADJUSTMENT_FOURTEEN_TO_TWENTY_ONE_DAYS (int): Conversion adjustment lag bucket from 14 to 21 days. 14 days is included,
          21 days is not.
          ADJUSTMENT_TWENTY_ONE_TO_THIRTY_DAYS (int): Conversion adjustment lag bucket from 21 to 30 days. 21 days is included,
          30 days is not.
          ADJUSTMENT_THIRTY_TO_FORTY_FIVE_DAYS (int): Conversion adjustment lag bucket from 30 to 45 days. 30 days is included,
          45 days is not.
          ADJUSTMENT_FORTY_FIVE_TO_SIXTY_DAYS (int): Conversion adjustment lag bucket from 45 to 60 days. 45 days is included,
          60 days is not.
          ADJUSTMENT_SIXTY_TO_NINETY_DAYS (int): Conversion adjustment lag bucket from 60 to 90 days. 60 days is included,
          90 days is not.
          ADJUSTMENT_NINETY_TO_ONE_HUNDRED_AND_FORTY_FIVE_DAYS (int): Conversion adjustment lag bucket from 90 to 145 days. 90 days is
          included, 145 days is not.
          CONVERSION_UNKNOWN (int): Conversion lag bucket UNKNOWN. This is for dates before conversion lag
          bucket was available in Google Ads.
          ADJUSTMENT_UNKNOWN (int): Conversion adjustment lag bucket UNKNOWN. This is for dates before
          conversion adjustment lag bucket was available in Google Ads.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        CONVERSION_LESS_THAN_ONE_DAY = 2
        CONVERSION_ONE_TO_TWO_DAYS = 3
        CONVERSION_TWO_TO_THREE_DAYS = 4
        CONVERSION_THREE_TO_FOUR_DAYS = 5
        CONVERSION_FOUR_TO_FIVE_DAYS = 6
        CONVERSION_FIVE_TO_SIX_DAYS = 7
        CONVERSION_SIX_TO_SEVEN_DAYS = 8
        CONVERSION_SEVEN_TO_EIGHT_DAYS = 9
        CONVERSION_EIGHT_TO_NINE_DAYS = 10
        CONVERSION_NINE_TO_TEN_DAYS = 11
        CONVERSION_TEN_TO_ELEVEN_DAYS = 12
        CONVERSION_ELEVEN_TO_TWELVE_DAYS = 13
        CONVERSION_TWELVE_TO_THIRTEEN_DAYS = 14
        CONVERSION_THIRTEEN_TO_FOURTEEN_DAYS = 15
        CONVERSION_FOURTEEN_TO_TWENTY_ONE_DAYS = 16
        CONVERSION_TWENTY_ONE_TO_THIRTY_DAYS = 17
        CONVERSION_THIRTY_TO_FORTY_FIVE_DAYS = 18
        CONVERSION_FORTY_FIVE_TO_SIXTY_DAYS = 19
        CONVERSION_SIXTY_TO_NINETY_DAYS = 20
        ADJUSTMENT_LESS_THAN_ONE_DAY = 21
        ADJUSTMENT_ONE_TO_TWO_DAYS = 22
        ADJUSTMENT_TWO_TO_THREE_DAYS = 23
        ADJUSTMENT_THREE_TO_FOUR_DAYS = 24
        ADJUSTMENT_FOUR_TO_FIVE_DAYS = 25
        ADJUSTMENT_FIVE_TO_SIX_DAYS = 26
        ADJUSTMENT_SIX_TO_SEVEN_DAYS = 27
        ADJUSTMENT_SEVEN_TO_EIGHT_DAYS = 28
        ADJUSTMENT_EIGHT_TO_NINE_DAYS = 29
        ADJUSTMENT_NINE_TO_TEN_DAYS = 30
        ADJUSTMENT_TEN_TO_ELEVEN_DAYS = 31
        ADJUSTMENT_ELEVEN_TO_TWELVE_DAYS = 32
        ADJUSTMENT_TWELVE_TO_THIRTEEN_DAYS = 33
        ADJUSTMENT_THIRTEEN_TO_FOURTEEN_DAYS = 34
        ADJUSTMENT_FOURTEEN_TO_TWENTY_ONE_DAYS = 35
        ADJUSTMENT_TWENTY_ONE_TO_THIRTY_DAYS = 36
        ADJUSTMENT_THIRTY_TO_FORTY_FIVE_DAYS = 37
        ADJUSTMENT_FORTY_FIVE_TO_SIXTY_DAYS = 38
        ADJUSTMENT_SIXTY_TO_NINETY_DAYS = 39
        ADJUSTMENT_NINETY_TO_ONE_HUNDRED_AND_FORTY_FIVE_DAYS = 40
        CONVERSION_UNKNOWN = 41
        ADJUSTMENT_UNKNOWN = 42


class ConversionUploadErrorEnum(object):
    class ConversionUploadError(enum.IntEnum):
        """
        Enum describing possible conversion upload errors.

        Attributes:
          UNSPECIFIED (int): Enum unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          TOO_MANY_CONVERSIONS_IN_REQUEST (int): The request contained more than 2000 conversions.
          UNPARSEABLE_GCLID (int): The specified gclid could not be decoded.
          CONVERSION_PRECEDES_GCLID (int): The specified conversion\_date\_time is before the event time associated
          with the given gclid.
          EXPIRED_GCLID (int): The click associated with the given gclid is either too old to be
          imported or occurred outside of the click through lookback window for the
          specified conversion action.
          TOO_RECENT_GCLID (int): The click associated with the given gclid occurred too recently. Please
          try uploading again after 24 hours have passed since the click occurred.
          GCLID_NOT_FOUND (int): The click associated with the given gclid could not be found in the
          system. This can happen if Google Click IDs are collected for non Google
          Ads clicks.
          UNAUTHORIZED_CUSTOMER (int): The click associated with the given gclid is owned by a customer
          account that the uploading customer does not manage.
          INVALID_CONVERSION_ACTION (int): No upload eligible conversion action that matches the provided
          information can be found for the customer.
          TOO_RECENT_CONVERSION_ACTION (int): The specified conversion action was created too recently.
          Please try the upload again after 4-6 hours have passed since the
          conversion action was created.
          CONVERSION_TRACKING_NOT_ENABLED_AT_IMPRESSION_TIME (int): The click associated with the given gclid does not contain conversion
          tracking information.
          EXTERNAL_ATTRIBUTION_DATA_SET_FOR_NON_EXTERNALLY_ATTRIBUTED_CONVERSION_ACTION (int): The specified conversion action does not use an external attribution
          model, but external\_attribution\_data was set.
          EXTERNAL_ATTRIBUTION_DATA_NOT_SET_FOR_EXTERNALLY_ATTRIBUTED_CONVERSION_ACTION (int): The specified conversion action uses an external attribution model, but
          external\_attribution\_data or one of its contained fields was not set.
          Both external\_attribution\_credit and external\_attribution\_model must
          be set for externally attributed conversion actions.
          ORDER_ID_NOT_PERMITTED_FOR_EXTERNALLY_ATTRIBUTED_CONVERSION_ACTION (int): Order IDs are not supported for conversion actions which use an external
          attribution model.
          ORDER_ID_ALREADY_IN_USE (int): A conversion with the same order id and conversion action combination
          already exists in our system.
          DUPLICATE_ORDER_ID (int): The request contained two or more conversions with the same order id and
          conversion action combination.
          TOO_RECENT_CALL (int): The call occurred too recently. Please try uploading again after 24 hours
          have passed since the call occurred.
          EXPIRED_CALL (int): The click that initiated the call is too old for this conversion to be
          imported.
          CALL_NOT_FOUND (int): The call or the click leading to the call was not found.
          CONVERSION_PRECEDES_CALL (int): The specified conversion\_date\_time is before the
          call\_start\_date\_time.
          CONVERSION_TRACKING_NOT_ENABLED_AT_CALL_TIME (int): The click associated with the call does not contain conversion tracking
          information.
          UNPARSEABLE_CALLERS_PHONE_NUMBER (int): The caller’s phone number cannot be parsed. It should be formatted either
          as E.164 "+16502531234", International "+64 3-331 6005" or US national
          number "6502531234".
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        TOO_MANY_CONVERSIONS_IN_REQUEST = 2
        UNPARSEABLE_GCLID = 3
        CONVERSION_PRECEDES_GCLID = 4
        EXPIRED_GCLID = 5
        TOO_RECENT_GCLID = 6
        GCLID_NOT_FOUND = 7
        UNAUTHORIZED_CUSTOMER = 8
        INVALID_CONVERSION_ACTION = 9
        TOO_RECENT_CONVERSION_ACTION = 10
        CONVERSION_TRACKING_NOT_ENABLED_AT_IMPRESSION_TIME = 11
        EXTERNAL_ATTRIBUTION_DATA_SET_FOR_NON_EXTERNALLY_ATTRIBUTED_CONVERSION_ACTION = 12
        EXTERNAL_ATTRIBUTION_DATA_NOT_SET_FOR_EXTERNALLY_ATTRIBUTED_CONVERSION_ACTION = 13
        ORDER_ID_NOT_PERMITTED_FOR_EXTERNALLY_ATTRIBUTED_CONVERSION_ACTION = 14
        ORDER_ID_ALREADY_IN_USE = 15
        DUPLICATE_ORDER_ID = 16
        TOO_RECENT_CALL = 17
        EXPIRED_CALL = 18
        CALL_NOT_FOUND = 19
        CONVERSION_PRECEDES_CALL = 20
        CONVERSION_TRACKING_NOT_ENABLED_AT_CALL_TIME = 21
        UNPARSEABLE_CALLERS_PHONE_NUMBER = 22


class CountryCodeErrorEnum(object):
    class CountryCodeError(enum.IntEnum):
        """
        Enum describing country code errors.

        Attributes:
          UNSPECIFIED (int): Enum unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          INVALID_COUNTRY_CODE (int): The country code is invalid.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        INVALID_COUNTRY_CODE = 2


class CriterionCategoryChannelAvailabilityModeEnum(object):
    class CriterionCategoryChannelAvailabilityMode(enum.IntEnum):
        """
        Enum containing the possible CriterionCategoryChannelAvailabilityMode.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          ALL_CHANNELS (int): The category is available to campaigns of all channel types and subtypes.
          CHANNEL_TYPE_AND_ALL_SUBTYPES (int): The category is available to campaigns of a specific channel type,
          including all subtypes under it.
          CHANNEL_TYPE_AND_SUBSET_SUBTYPES (int): The category is available to campaigns of a specific channel type and
          subtype(s).
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        ALL_CHANNELS = 2
        CHANNEL_TYPE_AND_ALL_SUBTYPES = 3
        CHANNEL_TYPE_AND_SUBSET_SUBTYPES = 4


class CriterionCategoryLocaleAvailabilityModeEnum(object):
    class CriterionCategoryLocaleAvailabilityMode(enum.IntEnum):
        """
        Enum containing the possible CriterionCategoryLocaleAvailabilityMode.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          ALL_LOCALES (int): The category is available to campaigns of all locales.
          COUNTRY_AND_ALL_LANGUAGES (int): The category is available to campaigns within a list of countries,
          regardless of language.
          LANGUAGE_AND_ALL_COUNTRIES (int): The category is available to campaigns within a list of languages,
          regardless of country.
          COUNTRY_AND_LANGUAGE (int): The category is available to campaigns within a list of country, language
          pairs.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        ALL_LOCALES = 2
        COUNTRY_AND_ALL_LANGUAGES = 3
        LANGUAGE_AND_ALL_COUNTRIES = 4
        COUNTRY_AND_LANGUAGE = 5


class CriterionErrorEnum(object):
    class CriterionError(enum.IntEnum):
        """
        Enum describing possible criterion errors.

        Attributes:
          UNSPECIFIED (int): Enum unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          CONCRETE_TYPE_REQUIRED (int): Concrete type of criterion is required for CREATE and UPDATE operations.
          INVALID_EXCLUDED_CATEGORY (int): The category requested for exclusion is invalid.
          INVALID_KEYWORD_TEXT (int): Invalid keyword criteria text.
          KEYWORD_TEXT_TOO_LONG (int): Keyword text should be less than 80 chars.
          KEYWORD_HAS_TOO_MANY_WORDS (int): Keyword text has too many words.
          KEYWORD_HAS_INVALID_CHARS (int): Keyword text has invalid characters or symbols.
          INVALID_PLACEMENT_URL (int): Invalid placement URL.
          INVALID_USER_LIST (int): Invalid user list criterion.
          INVALID_USER_INTEREST (int): Invalid user interest criterion.
          INVALID_FORMAT_FOR_PLACEMENT_URL (int): Placement URL has wrong format.
          PLACEMENT_URL_IS_TOO_LONG (int): Placement URL is too long.
          PLACEMENT_URL_HAS_ILLEGAL_CHAR (int): Indicates the URL contains an illegal character.
          PLACEMENT_URL_HAS_MULTIPLE_SITES_IN_LINE (int): Indicates the URL contains multiple comma separated URLs.
          PLACEMENT_IS_NOT_AVAILABLE_FOR_TARGETING_OR_EXCLUSION (int): Indicates the domain is blacklisted.
          INVALID_TOPIC_PATH (int): Invalid topic path.
          INVALID_YOUTUBE_CHANNEL_ID (int): The YouTube Channel Id is invalid.
          INVALID_YOUTUBE_VIDEO_ID (int): The YouTube Video Id is invalid.
          YOUTUBE_VERTICAL_CHANNEL_DEPRECATED (int): Indicates the placement is a YouTube vertical channel, which is no longer
          supported.
          YOUTUBE_DEMOGRAPHIC_CHANNEL_DEPRECATED (int): Indicates the placement is a YouTube demographic channel, which is no
          longer supported.
          YOUTUBE_URL_UNSUPPORTED (int): YouTube urls are not supported in Placement criterion. Use YouTubeChannel
          and YouTubeVideo criterion instead.
          CANNOT_EXCLUDE_CRITERIA_TYPE (int): Criteria type can not be excluded by the customer, like AOL account type
          cannot target site type criteria.
          CANNOT_ADD_CRITERIA_TYPE (int): Criteria type can not be targeted.
          INVALID_PRODUCT_FILTER (int): Product filter in the product criteria has invalid characters. Operand
          and the argument in the filter can not have "==" or "&+".
          PRODUCT_FILTER_TOO_LONG (int): Product filter in the product criteria is translated to a string as
          operand1==argument1&+operand2==argument2, maximum allowed length for the
          string is 255 chars.
          CANNOT_EXCLUDE_SIMILAR_USER_LIST (int): Not allowed to exclude similar user list.
          CANNOT_ADD_CLOSED_USER_LIST (int): Not allowed to target a closed user list.
          CANNOT_ADD_DISPLAY_ONLY_LISTS_TO_SEARCH_ONLY_CAMPAIGNS (int): Not allowed to add display only UserLists to search only campaigns.
          CANNOT_ADD_DISPLAY_ONLY_LISTS_TO_SEARCH_CAMPAIGNS (int): Not allowed to add display only UserLists to search plus campaigns.
          CANNOT_ADD_DISPLAY_ONLY_LISTS_TO_SHOPPING_CAMPAIGNS (int): Not allowed to add display only UserLists to shopping campaigns.
          CANNOT_ADD_USER_INTERESTS_TO_SEARCH_CAMPAIGNS (int): Not allowed to add User interests to search only campaigns.
          CANNOT_SET_BIDS_ON_CRITERION_TYPE_IN_SEARCH_CAMPAIGNS (int): Not allowed to set bids for this criterion type in search campaigns
          CANNOT_ADD_URLS_TO_CRITERION_TYPE_FOR_CAMPAIGN_TYPE (int): Final URLs, URL Templates and CustomParameters cannot be set for the
          criterion types of Gender, AgeRange, UserList, Placement, MobileApp, and
          MobileAppCategory in search campaigns and shopping campaigns.
          INVALID_CUSTOM_AFFINITY (int): Invalid custom affinity criterion.
          INVALID_CUSTOM_INTENT (int): Invalid custom intent criterion.
          INVALID_IP_ADDRESS (int): IP address is not valid.
          INVALID_IP_FORMAT (int): IP format is not valid.
          INVALID_MOBILE_APP (int): Mobile application is not valid.
          INVALID_MOBILE_APP_CATEGORY (int): Mobile application category is not valid.
          INVALID_CRITERION_ID (int): The CriterionId does not exist or is of the incorrect type.
          CANNOT_TARGET_CRITERION (int): The Criterion is not allowed to be targeted.
          CANNOT_TARGET_OBSOLETE_CRITERION (int): The criterion is not allowed to be targeted as it is deprecated.
          CRITERION_ID_AND_TYPE_MISMATCH (int): The CriterionId is not valid for the type.
          INVALID_PROXIMITY_RADIUS (int): Distance for the radius for the proximity criterion is invalid.
          INVALID_PROXIMITY_RADIUS_UNITS (int): Units for the distance for the radius for the proximity criterion is
          invalid.
          INVALID_STREETADDRESS_LENGTH (int): Street address in the address is not valid.
          INVALID_CITYNAME_LENGTH (int): City name in the address is not valid.
          INVALID_REGIONCODE_LENGTH (int): Region code in the address is not valid.
          INVALID_REGIONNAME_LENGTH (int): Region name in the address is not valid.
          INVALID_POSTALCODE_LENGTH (int): Postal code in the address is not valid.
          INVALID_COUNTRY_CODE (int): Country code in the address is not valid.
          INVALID_LATITUDE (int): Latitude for the GeoPoint is not valid.
          INVALID_LONGITUDE (int): Longitude for the GeoPoint is not valid.
          PROXIMITY_GEOPOINT_AND_ADDRESS_BOTH_CANNOT_BE_NULL (int): The Proximity input is not valid. Both address and geoPoint cannot be
          null.
          INVALID_PROXIMITY_ADDRESS (int): The Proximity address cannot be geocoded to a valid lat/long.
          INVALID_USER_DOMAIN_NAME (int): User domain name is not valid.
          CRITERION_PARAMETER_TOO_LONG (int): Length of serialized criterion parameter exceeded size limit.
          AD_SCHEDULE_TIME_INTERVALS_OVERLAP (int): Time interval in the AdSchedule overlaps with another AdSchedule.
          AD_SCHEDULE_INTERVAL_CANNOT_SPAN_MULTIPLE_DAYS (int): AdSchedule time interval cannot span multiple days.
          AD_SCHEDULE_INVALID_TIME_INTERVAL (int): AdSchedule time interval specified is invalid, endTime cannot be earlier
          than startTime.
          AD_SCHEDULE_EXCEEDED_INTERVALS_PER_DAY_LIMIT (int): The number of AdSchedule entries in a day exceeds the limit.
          AD_SCHEDULE_CRITERION_ID_MISMATCHING_FIELDS (int): CriteriaId does not match the interval of the AdSchedule specified.
          CANNOT_BID_MODIFY_CRITERION_TYPE (int): Cannot set bid modifier for this criterion type.
          CANNOT_BID_MODIFY_CRITERION_CAMPAIGN_OPTED_OUT (int): Cannot bid modify criterion, since it is opted out of the campaign.
          CANNOT_BID_MODIFY_NEGATIVE_CRITERION (int): Cannot set bid modifier for a negative criterion.
          BID_MODIFIER_ALREADY_EXISTS (int): Bid Modifier already exists. Use SET operation to update.
          FEED_ID_NOT_ALLOWED (int): Feed Id is not allowed in these Location Groups.
          ACCOUNT_INELIGIBLE_FOR_CRITERIA_TYPE (int): The account may not use the requested criteria type. For example, some
          accounts are restricted to keywords only.
          CRITERIA_TYPE_INVALID_FOR_BIDDING_STRATEGY (int): The requested criteria type cannot be used with campaign or ad group
          bidding strategy.
          CANNOT_EXCLUDE_CRITERION (int): The Criterion is not allowed to be excluded.
          CANNOT_REMOVE_CRITERION (int): The criterion is not allowed to be removed. For example, we cannot remove
          any of the device criterion.
          PRODUCT_SCOPE_TOO_LONG (int): The combined length of product dimension values of the product scope
          criterion is too long.
          PRODUCT_SCOPE_TOO_MANY_DIMENSIONS (int): Product scope contains too many dimensions.
          PRODUCT_PARTITION_TOO_LONG (int): The combined length of product dimension values of the product partition
          criterion is too long.
          PRODUCT_PARTITION_TOO_MANY_DIMENSIONS (int): Product partition contains too many dimensions.
          INVALID_PRODUCT_DIMENSION (int): The product dimension is invalid (e.g. dimension contains illegal value,
          dimension type is represented with wrong class, etc). Product dimension
          value can not contain "==" or "&+".
          INVALID_PRODUCT_DIMENSION_TYPE (int): Product dimension type is either invalid for campaigns of this type or
          cannot be used in the current context. BIDDING\_CATEGORY\_Lx and
          PRODUCT\_TYPE\_Lx product dimensions must be used in ascending order of
          their levels: L1, L2, L3, L4, L5... The levels must be specified
          sequentially and start from L1. Furthermore, an "others" product
          partition cannot be subdivided with a dimension of the same type but of
          a higher level ("others" BIDDING\_CATEGORY\_L3 can be subdivided with
          BRAND but not with BIDDING\_CATEGORY\_L4).
          INVALID_PRODUCT_BIDDING_CATEGORY (int): Bidding categories do not form a valid path in the Shopping bidding
          category taxonomy.
          MISSING_SHOPPING_SETTING (int): ShoppingSetting must be added to the campaign before ProductScope
          criteria can be added.
          INVALID_MATCHING_FUNCTION (int): Matching function is invalid.
          LOCATION_FILTER_NOT_ALLOWED (int): Filter parameters not allowed for location groups targeting.
          INVALID_FEED_FOR_LOCATION_FILTER (int): Feed not found, or the feed is not an enabled location feed.
          LOCATION_FILTER_INVALID (int): Given location filter parameter is invalid for location groups targeting.
          CANNOT_ATTACH_CRITERIA_AT_CAMPAIGN_AND_ADGROUP (int): Criteria type cannot be associated with a campaign and its ad group(s)
          simultaneously.
          HOTEL_LENGTH_OF_STAY_OVERLAPS_WITH_EXISTING_CRITERION (int): Range represented by hotel length of stay's min nights and max nights
          overlaps with an existing criterion.
          HOTEL_ADVANCE_BOOKING_WINDOW_OVERLAPS_WITH_EXISTING_CRITERION (int): Range represented by hotel advance booking window's min days and max days
          overlaps with an existing criterion.
          FIELD_INCOMPATIBLE_WITH_NEGATIVE_TARGETING (int): The field is not allowed to be set when the negative field is set to
          true, e.g. we don't allow bids in negative ad group or campaign criteria.
          INVALID_WEBPAGE_CONDITION (int): The combination of operand and operator in webpage condition is invalid.
          INVALID_WEBPAGE_CONDITION_URL (int): The URL of webpage condition is invalid.
          WEBPAGE_CONDITION_URL_CANNOT_BE_EMPTY (int): The URL of webpage condition cannot be empty or contain white space.
          WEBPAGE_CONDITION_URL_UNSUPPORTED_PROTOCOL (int): The URL of webpage condition contains an unsupported protocol.
          WEBPAGE_CONDITION_URL_CANNOT_BE_IP_ADDRESS (int): The URL of webpage condition cannot be an IP address.
          WEBPAGE_CONDITION_URL_DOMAIN_NOT_CONSISTENT_WITH_CAMPAIGN_SETTING (int): The domain of the URL is not consistent with the domain in campaign
          setting.
          WEBPAGE_CONDITION_URL_CANNOT_BE_PUBLIC_SUFFIX (int): The URL of webpage condition cannot be a public suffix itself.
          WEBPAGE_CONDITION_URL_INVALID_PUBLIC_SUFFIX (int): The URL of webpage condition has an invalid public suffix.
          WEBPAGE_CONDITION_URL_VALUE_TRACK_VALUE_NOT_SUPPORTED (int): Value track parameter is not supported in webpage condition URL.
          WEBPAGE_CRITERION_URL_EQUALS_CAN_HAVE_ONLY_ONE_CONDITION (int): Only one URL-EQUALS webpage condition is allowed in a webpage
          criterion and it cannot be combined with other conditions.
          WEBPAGE_CRITERION_NOT_SUPPORTED_ON_NON_DSA_AD_GROUP (int): A webpage criterion cannot be added to a non-DSA ad group.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        CONCRETE_TYPE_REQUIRED = 2
        INVALID_EXCLUDED_CATEGORY = 3
        INVALID_KEYWORD_TEXT = 4
        KEYWORD_TEXT_TOO_LONG = 5
        KEYWORD_HAS_TOO_MANY_WORDS = 6
        KEYWORD_HAS_INVALID_CHARS = 7
        INVALID_PLACEMENT_URL = 8
        INVALID_USER_LIST = 9
        INVALID_USER_INTEREST = 10
        INVALID_FORMAT_FOR_PLACEMENT_URL = 11
        PLACEMENT_URL_IS_TOO_LONG = 12
        PLACEMENT_URL_HAS_ILLEGAL_CHAR = 13
        PLACEMENT_URL_HAS_MULTIPLE_SITES_IN_LINE = 14
        PLACEMENT_IS_NOT_AVAILABLE_FOR_TARGETING_OR_EXCLUSION = 15
        INVALID_TOPIC_PATH = 16
        INVALID_YOUTUBE_CHANNEL_ID = 17
        INVALID_YOUTUBE_VIDEO_ID = 18
        YOUTUBE_VERTICAL_CHANNEL_DEPRECATED = 19
        YOUTUBE_DEMOGRAPHIC_CHANNEL_DEPRECATED = 20
        YOUTUBE_URL_UNSUPPORTED = 21
        CANNOT_EXCLUDE_CRITERIA_TYPE = 22
        CANNOT_ADD_CRITERIA_TYPE = 23
        INVALID_PRODUCT_FILTER = 24
        PRODUCT_FILTER_TOO_LONG = 25
        CANNOT_EXCLUDE_SIMILAR_USER_LIST = 26
        CANNOT_ADD_CLOSED_USER_LIST = 27
        CANNOT_ADD_DISPLAY_ONLY_LISTS_TO_SEARCH_ONLY_CAMPAIGNS = 28
        CANNOT_ADD_DISPLAY_ONLY_LISTS_TO_SEARCH_CAMPAIGNS = 29
        CANNOT_ADD_DISPLAY_ONLY_LISTS_TO_SHOPPING_CAMPAIGNS = 30
        CANNOT_ADD_USER_INTERESTS_TO_SEARCH_CAMPAIGNS = 31
        CANNOT_SET_BIDS_ON_CRITERION_TYPE_IN_SEARCH_CAMPAIGNS = 32
        CANNOT_ADD_URLS_TO_CRITERION_TYPE_FOR_CAMPAIGN_TYPE = 33
        INVALID_CUSTOM_AFFINITY = 96
        INVALID_CUSTOM_INTENT = 97
        INVALID_IP_ADDRESS = 34
        INVALID_IP_FORMAT = 35
        INVALID_MOBILE_APP = 36
        INVALID_MOBILE_APP_CATEGORY = 37
        INVALID_CRITERION_ID = 38
        CANNOT_TARGET_CRITERION = 39
        CANNOT_TARGET_OBSOLETE_CRITERION = 40
        CRITERION_ID_AND_TYPE_MISMATCH = 41
        INVALID_PROXIMITY_RADIUS = 42
        INVALID_PROXIMITY_RADIUS_UNITS = 43
        INVALID_STREETADDRESS_LENGTH = 44
        INVALID_CITYNAME_LENGTH = 45
        INVALID_REGIONCODE_LENGTH = 46
        INVALID_REGIONNAME_LENGTH = 47
        INVALID_POSTALCODE_LENGTH = 48
        INVALID_COUNTRY_CODE = 49
        INVALID_LATITUDE = 50
        INVALID_LONGITUDE = 51
        PROXIMITY_GEOPOINT_AND_ADDRESS_BOTH_CANNOT_BE_NULL = 52
        INVALID_PROXIMITY_ADDRESS = 53
        INVALID_USER_DOMAIN_NAME = 54
        CRITERION_PARAMETER_TOO_LONG = 55
        AD_SCHEDULE_TIME_INTERVALS_OVERLAP = 56
        AD_SCHEDULE_INTERVAL_CANNOT_SPAN_MULTIPLE_DAYS = 57
        AD_SCHEDULE_INVALID_TIME_INTERVAL = 58
        AD_SCHEDULE_EXCEEDED_INTERVALS_PER_DAY_LIMIT = 59
        AD_SCHEDULE_CRITERION_ID_MISMATCHING_FIELDS = 60
        CANNOT_BID_MODIFY_CRITERION_TYPE = 61
        CANNOT_BID_MODIFY_CRITERION_CAMPAIGN_OPTED_OUT = 62
        CANNOT_BID_MODIFY_NEGATIVE_CRITERION = 63
        BID_MODIFIER_ALREADY_EXISTS = 64
        FEED_ID_NOT_ALLOWED = 65
        ACCOUNT_INELIGIBLE_FOR_CRITERIA_TYPE = 66
        CRITERIA_TYPE_INVALID_FOR_BIDDING_STRATEGY = 67
        CANNOT_EXCLUDE_CRITERION = 68
        CANNOT_REMOVE_CRITERION = 69
        PRODUCT_SCOPE_TOO_LONG = 70
        PRODUCT_SCOPE_TOO_MANY_DIMENSIONS = 71
        PRODUCT_PARTITION_TOO_LONG = 72
        PRODUCT_PARTITION_TOO_MANY_DIMENSIONS = 73
        INVALID_PRODUCT_DIMENSION = 74
        INVALID_PRODUCT_DIMENSION_TYPE = 75
        INVALID_PRODUCT_BIDDING_CATEGORY = 76
        MISSING_SHOPPING_SETTING = 77
        INVALID_MATCHING_FUNCTION = 78
        LOCATION_FILTER_NOT_ALLOWED = 79
        INVALID_FEED_FOR_LOCATION_FILTER = 98
        LOCATION_FILTER_INVALID = 80
        CANNOT_ATTACH_CRITERIA_AT_CAMPAIGN_AND_ADGROUP = 81
        HOTEL_LENGTH_OF_STAY_OVERLAPS_WITH_EXISTING_CRITERION = 82
        HOTEL_ADVANCE_BOOKING_WINDOW_OVERLAPS_WITH_EXISTING_CRITERION = 83
        FIELD_INCOMPATIBLE_WITH_NEGATIVE_TARGETING = 84
        INVALID_WEBPAGE_CONDITION = 85
        INVALID_WEBPAGE_CONDITION_URL = 86
        WEBPAGE_CONDITION_URL_CANNOT_BE_EMPTY = 87
        WEBPAGE_CONDITION_URL_UNSUPPORTED_PROTOCOL = 88
        WEBPAGE_CONDITION_URL_CANNOT_BE_IP_ADDRESS = 89
        WEBPAGE_CONDITION_URL_DOMAIN_NOT_CONSISTENT_WITH_CAMPAIGN_SETTING = 90
        WEBPAGE_CONDITION_URL_CANNOT_BE_PUBLIC_SUFFIX = 91
        WEBPAGE_CONDITION_URL_INVALID_PUBLIC_SUFFIX = 92
        WEBPAGE_CONDITION_URL_VALUE_TRACK_VALUE_NOT_SUPPORTED = 93
        WEBPAGE_CRITERION_URL_EQUALS_CAN_HAVE_ONLY_ONE_CONDITION = 94
        WEBPAGE_CRITERION_NOT_SUPPORTED_ON_NON_DSA_AD_GROUP = 95


class CriterionSystemServingStatusEnum(object):
    class CriterionSystemServingStatus(enum.IntEnum):
        """
        Enumerates criterion system serving statuses.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): The value is unknown in this version.
          ELIGIBLE (int): Eligible.
          RARELY_SERVED (int): Low search volume.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        ELIGIBLE = 2
        RARELY_SERVED = 3


class CriterionTypeEnum(object):
    class CriterionType(enum.IntEnum):
        """
        Enum describing possible criterion types.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          KEYWORD (int): Keyword. e.g. 'mars cruise'.
          PLACEMENT (int): Placement, aka Website. e.g. 'www.flowers4sale.com'
          MOBILE_APP_CATEGORY (int): Mobile application categories to target.
          MOBILE_APPLICATION (int): Mobile applications to target.
          DEVICE (int): Devices to target.
          LOCATION (int): Locations to target.
          LISTING_GROUP (int): Listing groups to target.
          AD_SCHEDULE (int): Ad Schedule.
          AGE_RANGE (int): Age range.
          GENDER (int): Gender.
          INCOME_RANGE (int): Income Range.
          PARENTAL_STATUS (int): Parental status.
          YOUTUBE_VIDEO (int): YouTube Video.
          YOUTUBE_CHANNEL (int): YouTube Channel.
          USER_LIST (int): User list.
          PROXIMITY (int): Proximity.
          TOPIC (int): A topic target on the display network (e.g. "Pets & Animals").
          LISTING_SCOPE (int): Listing scope to target.
          LANGUAGE (int): Language.
          IP_BLOCK (int): IpBlock.
          CONTENT_LABEL (int): Content Label for category exclusion.
          CARRIER (int): Carrier.
          USER_INTEREST (int): A category the user is interested in.
          WEBPAGE (int): Webpage criterion for dynamic search ads.
          OPERATING_SYSTEM_VERSION (int): Operating system version.
          APP_PAYMENT_MODEL (int): App payment model.
          MOBILE_DEVICE (int): Mobile device.
          CUSTOM_AFFINITY (int): Custom affinity.
          CUSTOM_INTENT (int): Custom intent.
          LOCATION_GROUP (int): Location group.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        KEYWORD = 2
        PLACEMENT = 3
        MOBILE_APP_CATEGORY = 4
        MOBILE_APPLICATION = 5
        DEVICE = 6
        LOCATION = 7
        LISTING_GROUP = 8
        AD_SCHEDULE = 9
        AGE_RANGE = 10
        GENDER = 11
        INCOME_RANGE = 12
        PARENTAL_STATUS = 13
        YOUTUBE_VIDEO = 14
        YOUTUBE_CHANNEL = 15
        USER_LIST = 16
        PROXIMITY = 17
        TOPIC = 18
        LISTING_SCOPE = 19
        LANGUAGE = 20
        IP_BLOCK = 21
        CONTENT_LABEL = 22
        CARRIER = 23
        USER_INTEREST = 24
        WEBPAGE = 25
        OPERATING_SYSTEM_VERSION = 26
        APP_PAYMENT_MODEL = 27
        MOBILE_DEVICE = 28
        CUSTOM_AFFINITY = 29
        CUSTOM_INTENT = 30
        LOCATION_GROUP = 31


class CustomInterestErrorEnum(object):
    class CustomInterestError(enum.IntEnum):
        """
        Enum describing possible custom interest errors.

        Attributes:
          UNSPECIFIED (int): Enum unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          NAME_ALREADY_USED (int): Duplicate custom interest name ignoring case.
          CUSTOM_INTEREST_MEMBER_ID_AND_TYPE_PARAMETER_NOT_PRESENT_IN_REMOVE (int): In the remove custom interest member operation, both member ID and pair
          [type, parameter] are not present.
          TYPE_AND_PARAMETER_NOT_FOUND (int): The pair of [type, parameter] does not exist.
          TYPE_AND_PARAMETER_ALREADY_EXISTED (int): The pair of [type, parameter] already exists.
          INVALID_CUSTOM_INTEREST_MEMBER_TYPE (int): Unsupported custom interest member type.
          CANNOT_REMOVE_WHILE_IN_USE (int): Cannot remove a custom interest while it's still being targeted.
          CANNOT_CHANGE_TYPE (int): Cannot mutate custom interest type.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        NAME_ALREADY_USED = 2
        CUSTOM_INTEREST_MEMBER_ID_AND_TYPE_PARAMETER_NOT_PRESENT_IN_REMOVE = 3
        TYPE_AND_PARAMETER_NOT_FOUND = 4
        TYPE_AND_PARAMETER_ALREADY_EXISTED = 5
        INVALID_CUSTOM_INTEREST_MEMBER_TYPE = 6
        CANNOT_REMOVE_WHILE_IN_USE = 7
        CANNOT_CHANGE_TYPE = 8


class CustomInterestMemberTypeEnum(object):
    class CustomInterestMemberType(enum.IntEnum):
        """
        Enum containing possible custom interest member types.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          KEYWORD (int): Custom interest member type KEYWORD.
          URL (int): Custom interest member type URL.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        KEYWORD = 2
        URL = 3


class CustomInterestStatusEnum(object):
    class CustomInterestStatus(enum.IntEnum):
        """
        Enum containing possible custom interest types.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          ENABLED (int): Enabled status - custom interest is enabled and can be targeted to.
          REMOVED (int): Removed status - custom interest is removed and cannot be used for
          targeting.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        ENABLED = 2
        REMOVED = 3


class CustomInterestTypeEnum(object):
    class CustomInterestType(enum.IntEnum):
        """
        Enum containing possible custom interest types.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          CUSTOM_AFFINITY (int): Allows brand advertisers to define custom affinity audience lists.
          CUSTOM_INTENT (int): Allows advertisers to define custom intent audience lists.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        CUSTOM_AFFINITY = 2
        CUSTOM_INTENT = 3


class CustomPlaceholderFieldEnum(object):
    class CustomPlaceholderField(enum.IntEnum):
        """
        Possible values for Custom placeholder fields.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          ID (int): Data Type: STRING. Required. Combination ID and ID2 must be unique per
          offer.
          ID2 (int): Data Type: STRING. Combination ID and ID2 must be unique per offer.
          ITEM_TITLE (int): Data Type: STRING. Required. Main headline with product name to be shown
          in dynamic ad.
          ITEM_SUBTITLE (int): Data Type: STRING. Optional text to be shown in the image ad.
          ITEM_DESCRIPTION (int): Data Type: STRING. Optional description of the product to be shown in the
          ad.
          ITEM_ADDRESS (int): Data Type: STRING. Full address of your offer or service, including
          postal code. This will be used to identify the closest product to the
          user when there are multiple offers in the feed that are relevant to the
          user.
          PRICE (int): Data Type: STRING. Price to be shown in the ad.
          Example: "100.00 USD"
          FORMATTED_PRICE (int): Data Type: STRING. Formatted price to be shown in the ad.
          Example: "Starting at $100.00 USD", "$80 - $100"
          SALE_PRICE (int): Data Type: STRING. Sale price to be shown in the ad.
          Example: "80.00 USD"
          FORMATTED_SALE_PRICE (int): Data Type: STRING. Formatted sale price to be shown in the ad.
          Example: "On sale for $80.00", "$60 - $80"
          IMAGE_URL (int): Data Type: URL. Image to be displayed in the ad. Highly recommended for
          image ads.
          ITEM_CATEGORY (int): Data Type: STRING. Used as a recommendation engine signal to serve items
          in the same category.
          FINAL_URLS (int): Data Type: URL\_LIST. Final URLs for the ad when using Upgraded URLs.
          User will be redirected to these URLs when they click on an ad, or when
          they click on a specific product for ads that have multiple products.
          FINAL_MOBILE_URLS (int): Data Type: URL\_LIST. Final mobile URLs for the ad when using Upgraded
          URLs.
          TRACKING_URL (int): Data Type: URL. Tracking template for the ad when using Upgraded URLs.
          CONTEXTUAL_KEYWORDS (int): Data Type: STRING\_LIST. Keywords used for product retrieval.
          ANDROID_APP_LINK (int): Data Type: STRING. Android app link. Must be formatted as:
          android-app://{package\_id}/{scheme}/{host\_path}. The components are
          defined as follows: package\_id: app ID as specified in Google Play.
          scheme: the scheme to pass to the application. Can be HTTP, or a custom
          scheme. host\_path: identifies the specific content within your
          application.
          SIMILAR_IDS (int): Data Type: STRING\_LIST. List of recommended IDs to show together with
          this item.
          IOS_APP_LINK (int): Data Type: STRING. iOS app link.
          IOS_APP_STORE_ID (int): Data Type: INT64. iOS app store ID.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        ID = 2
        ID2 = 3
        ITEM_TITLE = 4
        ITEM_SUBTITLE = 5
        ITEM_DESCRIPTION = 6
        ITEM_ADDRESS = 7
        PRICE = 8
        FORMATTED_PRICE = 9
        SALE_PRICE = 10
        FORMATTED_SALE_PRICE = 11
        IMAGE_URL = 12
        ITEM_CATEGORY = 13
        FINAL_URLS = 14
        FINAL_MOBILE_URLS = 15
        TRACKING_URL = 16
        CONTEXTUAL_KEYWORDS = 17
        ANDROID_APP_LINK = 18
        SIMILAR_IDS = 19
        IOS_APP_LINK = 20
        IOS_APP_STORE_ID = 21


class CustomerClientLinkErrorEnum(object):
    class CustomerClientLinkError(enum.IntEnum):
        """
        Enum describing possible CustomerClientLink errors.

        Attributes:
          UNSPECIFIED (int): Enum unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          CLIENT_ALREADY_INVITED_BY_THIS_MANAGER (int): Trying to manage a client that already in being managed by customer.
          CLIENT_ALREADY_MANAGED_IN_HIERARCHY (int): Already managed by some other manager in the hierarchy.
          CYCLIC_LINK_NOT_ALLOWED (int): Attempt to create a cycle in the hierarchy.
          CUSTOMER_HAS_TOO_MANY_ACCOUNTS (int): Managed accounts has the maximum number of linked accounts.
          CLIENT_HAS_TOO_MANY_INVITATIONS (int): Invitor has the maximum pending invitations.
          CANNOT_HIDE_OR_UNHIDE_MANAGER_ACCOUNTS (int): Attempt to change hidden status of a link that is not active.
          CUSTOMER_HAS_TOO_MANY_ACCOUNTS_AT_MANAGER (int): Parent manager account has the maximum number of linked accounts.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        CLIENT_ALREADY_INVITED_BY_THIS_MANAGER = 2
        CLIENT_ALREADY_MANAGED_IN_HIERARCHY = 3
        CYCLIC_LINK_NOT_ALLOWED = 4
        CUSTOMER_HAS_TOO_MANY_ACCOUNTS = 5
        CLIENT_HAS_TOO_MANY_INVITATIONS = 6
        CANNOT_HIDE_OR_UNHIDE_MANAGER_ACCOUNTS = 7
        CUSTOMER_HAS_TOO_MANY_ACCOUNTS_AT_MANAGER = 8


class CustomerErrorEnum(object):
    class CustomerError(enum.IntEnum):
        """
        Set of errors that are related to requests dealing with Customer.
        Next id: 26

        Attributes:
          UNSPECIFIED (int): Enum unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          STATUS_CHANGE_DISALLOWED (int): Customer status is not allowed to be changed from DRAFT and CLOSED.
          Currency code and at least one of country code and time zone needs to be
          set when status is changed to ENABLED.
          ACCOUNT_NOT_SET_UP (int): CustomerService cannot get a customer that has not been fully set up.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        STATUS_CHANGE_DISALLOWED = 2
        ACCOUNT_NOT_SET_UP = 3


class CustomerFeedErrorEnum(object):
    class CustomerFeedError(enum.IntEnum):
        """
        Enum describing possible customer feed errors.

        Attributes:
          UNSPECIFIED (int): Enum unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          FEED_ALREADY_EXISTS_FOR_PLACEHOLDER_TYPE (int): An active feed already exists for this customer and place holder type.
          CANNOT_CREATE_FOR_REMOVED_FEED (int): The specified feed is removed.
          CANNOT_CREATE_ALREADY_EXISTING_CUSTOMER_FEED (int): The CustomerFeed already exists. Update should be used to modify the
          existing CustomerFeed.
          CANNOT_MODIFY_REMOVED_CUSTOMER_FEED (int): Cannot update removed customer feed.
          INVALID_PLACEHOLDER_TYPE (int): Invalid placeholder type.
          MISSING_FEEDMAPPING_FOR_PLACEHOLDER_TYPE (int): Feed mapping for this placeholder type does not exist.
          PLACEHOLDER_TYPE_NOT_ALLOWED_ON_CUSTOMER_FEED (int): Placeholder not allowed at the account level.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        FEED_ALREADY_EXISTS_FOR_PLACEHOLDER_TYPE = 2
        CANNOT_CREATE_FOR_REMOVED_FEED = 3
        CANNOT_CREATE_ALREADY_EXISTING_CUSTOMER_FEED = 4
        CANNOT_MODIFY_REMOVED_CUSTOMER_FEED = 5
        INVALID_PLACEHOLDER_TYPE = 6
        MISSING_FEEDMAPPING_FOR_PLACEHOLDER_TYPE = 7
        PLACEHOLDER_TYPE_NOT_ALLOWED_ON_CUSTOMER_FEED = 8


class CustomerManagerLinkErrorEnum(object):
    class CustomerManagerLinkError(enum.IntEnum):
        """
        Enum describing possible CustomerManagerLink errors.

        Attributes:
          UNSPECIFIED (int): Enum unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          NO_PENDING_INVITE (int): No pending invitation.
          SAME_CLIENT_MORE_THAN_ONCE_PER_CALL (int): Attempt to operate on the same client more than once in the same call.
          MANAGER_HAS_MAX_NUMBER_OF_LINKED_ACCOUNTS (int): Manager account has the maximum number of linked accounts.
          CANNOT_UNLINK_ACCOUNT_WITHOUT_ACTIVE_USER (int): If no active user on account it cannot be unlinked from its manager.
          CANNOT_REMOVE_LAST_CLIENT_ACCOUNT_OWNER (int): Account should have at least one active owner on it before being
          unlinked.
          CANNOT_CHANGE_ROLE_BY_NON_ACCOUNT_OWNER (int): Only account owners may change their permission role.
          CANNOT_CHANGE_ROLE_FOR_NON_ACTIVE_LINK_ACCOUNT (int): When a client's link to its manager is not active, the link role cannot
          be changed.
          DUPLICATE_CHILD_FOUND (int): Attempt to link a child to a parent that contains or will contain
          duplicate children.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        NO_PENDING_INVITE = 2
        SAME_CLIENT_MORE_THAN_ONCE_PER_CALL = 3
        MANAGER_HAS_MAX_NUMBER_OF_LINKED_ACCOUNTS = 4
        CANNOT_UNLINK_ACCOUNT_WITHOUT_ACTIVE_USER = 5
        CANNOT_REMOVE_LAST_CLIENT_ACCOUNT_OWNER = 6
        CANNOT_CHANGE_ROLE_BY_NON_ACCOUNT_OWNER = 7
        CANNOT_CHANGE_ROLE_FOR_NON_ACTIVE_LINK_ACCOUNT = 8
        DUPLICATE_CHILD_FOUND = 9


class CustomerMatchUploadKeyTypeEnum(object):
    class CustomerMatchUploadKeyType(enum.IntEnum):
        """
        Enum describing possible customer match upload key types.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          CONTACT_INFO (int): Members are matched from customer info such as email address, phone
          number or physical address.
          CRM_ID (int): Members are matched from a user id generated and assigned by the
          advertiser.
          MOBILE_ADVERTISING_ID (int): Members are matched from mobile advertising ids.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        CONTACT_INFO = 2
        CRM_ID = 3
        MOBILE_ADVERTISING_ID = 4


class CustomerPayPerConversionEligibilityFailureReasonEnum(object):
    class CustomerPayPerConversionEligibilityFailureReason(enum.IntEnum):
        """
        Enum describing possible reasons a customer is not eligible to use
        PaymentMode.CONVERSIONS.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          NOT_ENOUGH_CONVERSIONS (int): Customer does not have enough conversions.
          CONVERSION_LAG_TOO_HIGH (int): Customer's conversion lag is too high.
          HAS_CAMPAIGN_WITH_SHARED_BUDGET (int): Customer uses shared budgets.
          HAS_UPLOAD_CLICKS_CONVERSION (int): Customer has conversions with ConversionActionType.UPLOAD\_CLICKS.
          AVERAGE_DAILY_SPEND_TOO_HIGH (int): Customer's average daily spend is too high.
          ANALYSIS_NOT_COMPLETE (int): Customer's eligibility has not yet been calculated by the Google Ads
          backend. Check back soon.
          OTHER (int): Customer is not eligible due to other reasons.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        NOT_ENOUGH_CONVERSIONS = 2
        CONVERSION_LAG_TOO_HIGH = 3
        HAS_CAMPAIGN_WITH_SHARED_BUDGET = 4
        HAS_UPLOAD_CLICKS_CONVERSION = 5
        AVERAGE_DAILY_SPEND_TOO_HIGH = 6
        ANALYSIS_NOT_COMPLETE = 7
        OTHER = 8


class DataDrivenModelStatusEnum(object):
    class DataDrivenModelStatus(enum.IntEnum):
        """
        Enumerates data driven model statuses.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          AVAILABLE (int): The data driven model is available.
          STALE (int): The data driven model is stale. It hasn't been updated for at least 7
          days. It is still being used, but will become expired if it does not get
          updated for 30 days.
          EXPIRED (int): The data driven model expired. It hasn't been updated for at least 30
          days and cannot be used. Most commonly this is because there hasn't been
          the required number of events in a recent 30-day period.
          NEVER_GENERATED (int): The data driven model has never been generated. Most commonly this is
          because there has never been the required number of events in any 30-day
          period.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        AVAILABLE = 2
        STALE = 3
        EXPIRED = 4
        NEVER_GENERATED = 5


class DatabaseErrorEnum(object):
    class DatabaseError(enum.IntEnum):
        """
        Enum describing possible database errors.

        Attributes:
          UNSPECIFIED (int): Enum unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          CONCURRENT_MODIFICATION (int): Multiple requests were attempting to modify the same resource at once.
          Please retry the request.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        CONCURRENT_MODIFICATION = 2


class DateErrorEnum(object):
    class DateError(enum.IntEnum):
        """
        Enum describing possible date errors.

        Attributes:
          UNSPECIFIED (int): Enum unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          INVALID_FIELD_VALUES_IN_DATE (int): Given field values do not correspond to a valid date.
          INVALID_FIELD_VALUES_IN_DATE_TIME (int): Given field values do not correspond to a valid date time.
          INVALID_STRING_DATE (int): The string date's format should be yyyy-mm-dd.
          INVALID_STRING_DATE_TIME_MICROS (int): The string date time's format should be yyyy-mm-dd hh:mm:ss.ssssss.
          INVALID_STRING_DATE_TIME_SECONDS (int): The string date time's format should be yyyy-mm-dd hh:mm:ss.
          INVALID_STRING_DATE_TIME_SECONDS_WITH_OFFSET (int): The string date time's format should be yyyy-mm-dd hh:mm:ss+|-hh:mm.
          EARLIER_THAN_MINIMUM_DATE (int): Date is before allowed minimum.
          LATER_THAN_MAXIMUM_DATE (int): Date is after allowed maximum.
          DATE_RANGE_MINIMUM_DATE_LATER_THAN_MAXIMUM_DATE (int): Date range bounds are not in order.
          DATE_RANGE_MINIMUM_AND_MAXIMUM_DATES_BOTH_NULL (int): Both dates in range are null.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        INVALID_FIELD_VALUES_IN_DATE = 2
        INVALID_FIELD_VALUES_IN_DATE_TIME = 3
        INVALID_STRING_DATE = 4
        INVALID_STRING_DATE_TIME_MICROS = 6
        INVALID_STRING_DATE_TIME_SECONDS = 11
        INVALID_STRING_DATE_TIME_SECONDS_WITH_OFFSET = 12
        EARLIER_THAN_MINIMUM_DATE = 7
        LATER_THAN_MAXIMUM_DATE = 8
        DATE_RANGE_MINIMUM_DATE_LATER_THAN_MAXIMUM_DATE = 9
        DATE_RANGE_MINIMUM_AND_MAXIMUM_DATES_BOTH_NULL = 10


class DateRangeErrorEnum(object):
    class DateRangeError(enum.IntEnum):
        """
        Enum describing possible date range errors.

        Attributes:
          UNSPECIFIED (int): Enum unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          INVALID_DATE (int): Invalid date.
          START_DATE_AFTER_END_DATE (int): The start date was after the end date.
          CANNOT_SET_DATE_TO_PAST (int): Cannot set date to past time
          AFTER_MAXIMUM_ALLOWABLE_DATE (int): A date was used that is past the system "last" date.
          CANNOT_MODIFY_START_DATE_IF_ALREADY_STARTED (int): Trying to change start date on a resource that has started.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        INVALID_DATE = 2
        START_DATE_AFTER_END_DATE = 3
        CANNOT_SET_DATE_TO_PAST = 4
        AFTER_MAXIMUM_ALLOWABLE_DATE = 5
        CANNOT_MODIFY_START_DATE_IF_ALREADY_STARTED = 6


class DayOfWeekEnum(object):
    class DayOfWeek(enum.IntEnum):
        """
        Enumerates days of the week, e.g., "Monday".

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): The value is unknown in this version.
          MONDAY (int): Monday.
          TUESDAY (int): Tuesday.
          WEDNESDAY (int): Wednesday.
          THURSDAY (int): Thursday.
          FRIDAY (int): Friday.
          SATURDAY (int): Saturday.
          SUNDAY (int): Sunday.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        MONDAY = 2
        TUESDAY = 3
        WEDNESDAY = 4
        THURSDAY = 5
        FRIDAY = 6
        SATURDAY = 7
        SUNDAY = 8


class DeviceEnum(object):
    class Device(enum.IntEnum):
        """
        Enumerates Google Ads devices available for targeting.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): The value is unknown in this version.
          MOBILE (int): Mobile devices with full browsers.
          TABLET (int): Tablets with full browsers.
          DESKTOP (int): Computers.
          CONNECTED_TV (int): Smart TVs and game consoles.
          OTHER (int): Other device types.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        MOBILE = 2
        TABLET = 3
        DESKTOP = 4
        CONNECTED_TV = 6
        OTHER = 5


class DisplayAdFormatSettingEnum(object):
    class DisplayAdFormatSetting(enum.IntEnum):
        """
        Enumerates display ad format settings.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): The value is unknown in this version.
          ALL_FORMATS (int): Text, image and native formats.
          NON_NATIVE (int): Text and image formats.
          NATIVE (int): Native format, i.e. the format rendering is controlled by the publisher
          and not by Google.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        ALL_FORMATS = 2
        NON_NATIVE = 3
        NATIVE = 4


class DisplayUploadProductTypeEnum(object):
    class DisplayUploadProductType(enum.IntEnum):
        """
        Enumerates display upload product types.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): The value is unknown in this version.
          HTML5_UPLOAD_AD (int): HTML5 upload ad. This product type requires the upload\_media\_bundle
          field in DisplayUploadAdInfo to be set.
          DYNAMIC_HTML5_EDUCATION_AD (int): Dynamic HTML5 education ad. This product type requires the
          upload\_media\_bundle field in DisplayUploadAdInfo to be set. Can only
          be used in an education campaign.
          DYNAMIC_HTML5_FLIGHT_AD (int): Dynamic HTML5 flight ad. This product type requires the
          upload\_media\_bundle field in DisplayUploadAdInfo to be set. Can only
          be used in a flight campaign.
          DYNAMIC_HTML5_HOTEL_RENTAL_AD (int): Dynamic HTML5 hotel and rental ad. This product type requires the
          upload\_media\_bundle field in DisplayUploadAdInfo to be set. Can only
          be used in a hotel campaign.
          DYNAMIC_HTML5_JOB_AD (int): Dynamic HTML5 job ad. This product type requires the
          upload\_media\_bundle field in DisplayUploadAdInfo to be set. Can only
          be used in a job campaign.
          DYNAMIC_HTML5_LOCAL_AD (int): Dynamic HTML5 local ad. This product type requires the
          upload\_media\_bundle field in DisplayUploadAdInfo to be set. Can only
          be used in a local campaign.
          DYNAMIC_HTML5_REAL_ESTATE_AD (int): Dynamic HTML5 real estate ad. This product type requires the
          upload\_media\_bundle field in DisplayUploadAdInfo to be set. Can only
          be used in a real estate campaign.
          DYNAMIC_HTML5_CUSTOM_AD (int): Dynamic HTML5 custom ad. This product type requires the
          upload\_media\_bundle field in DisplayUploadAdInfo to be set. Can only
          be used in a custom campaign.
          DYNAMIC_HTML5_TRAVEL_AD (int): Dynamic HTML5 travel ad. This product type requires the
          upload\_media\_bundle field in DisplayUploadAdInfo to be set. Can only
          be used in a travel campaign.
          DYNAMIC_HTML5_HOTEL_AD (int): Dynamic HTML5 hotel ad. This product type requires the
          upload\_media\_bundle field in DisplayUploadAdInfo to be set. Can only
          be used in a hotel campaign.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        HTML5_UPLOAD_AD = 2
        DYNAMIC_HTML5_EDUCATION_AD = 3
        DYNAMIC_HTML5_FLIGHT_AD = 4
        DYNAMIC_HTML5_HOTEL_RENTAL_AD = 5
        DYNAMIC_HTML5_JOB_AD = 6
        DYNAMIC_HTML5_LOCAL_AD = 7
        DYNAMIC_HTML5_REAL_ESTATE_AD = 8
        DYNAMIC_HTML5_CUSTOM_AD = 9
        DYNAMIC_HTML5_TRAVEL_AD = 10
        DYNAMIC_HTML5_HOTEL_AD = 11


class DistinctErrorEnum(object):
    class DistinctError(enum.IntEnum):
        """
        Enum describing possible distinct errors.

        Attributes:
          UNSPECIFIED (int): Enum unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          DUPLICATE_ELEMENT (int): Duplicate element.
          DUPLICATE_TYPE (int): Duplicate type.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        DUPLICATE_ELEMENT = 2
        DUPLICATE_TYPE = 3


class DsaPageFeedCriterionFieldEnum(object):
    class DsaPageFeedCriterionField(enum.IntEnum):
        """
        Possible values for Dynamic Search Ad Page Feed criterion fields.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          PAGE_URL (int): Data Type: URL or URL\_LIST. URL of the web page you want to target.
          LABEL (int): Data Type: STRING\_LIST. The labels that will help you target ads within
          your page feed.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        PAGE_URL = 2
        LABEL = 3


class EducationPlaceholderFieldEnum(object):
    class EducationPlaceholderField(enum.IntEnum):
        """
        Possible values for Education placeholder fields.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          PROGRAM_ID (int): Data Type: STRING. Required. Combination of PROGRAM ID and LOCATION ID
          must be unique per offer.
          LOCATION_ID (int): Data Type: STRING. Combination of PROGRAM ID and LOCATION ID must be
          unique per offer.
          PROGRAM_NAME (int): Data Type: STRING. Required. Main headline with program name to be shown
          in dynamic ad.
          AREA_OF_STUDY (int): Data Type: STRING. Area of study that can be shown in dynamic ad.
          PROGRAM_DESCRIPTION (int): Data Type: STRING. Description of program that can be shown in dynamic
          ad.
          SCHOOL_NAME (int): Data Type: STRING. Name of school that can be shown in dynamic ad.
          ADDRESS (int): Data Type: STRING. Complete school address, including postal code.
          THUMBNAIL_IMAGE_URL (int): Data Type: URL. Image to be displayed in ads.
          ALTERNATIVE_THUMBNAIL_IMAGE_URL (int): Data Type: URL. Alternative hosted file of image to be used in the ad.
          FINAL_URLS (int): Data Type: URL\_LIST. Required. Final URLs to be used in ad when using
          Upgraded URLs; the more specific the better (e.g. the individual URL of
          a specific program and its location).
          FINAL_MOBILE_URLS (int): Data Type: URL\_LIST. Final mobile URLs for the ad when using Upgraded
          URLs.
          TRACKING_URL (int): Data Type: URL. Tracking template for the ad when using Upgraded URLs.
          CONTEXTUAL_KEYWORDS (int): Data Type: STRING\_LIST. Keywords used for product retrieval.
          ANDROID_APP_LINK (int): Data Type: STRING. Android app link. Must be formatted as:
          android-app://{package\_id}/{scheme}/{host\_path}. The components are
          defined as follows: package\_id: app ID as specified in Google Play.
          scheme: the scheme to pass to the application. Can be HTTP, or a custom
          scheme. host\_path: identifies the specific content within your
          application.
          SIMILAR_PROGRAM_IDS (int): Data Type: STRING\_LIST. List of recommended program IDs to show
          together with this item.
          IOS_APP_LINK (int): Data Type: STRING. iOS app link.
          IOS_APP_STORE_ID (int): Data Type: INT64. iOS app store ID.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        PROGRAM_ID = 2
        LOCATION_ID = 3
        PROGRAM_NAME = 4
        AREA_OF_STUDY = 5
        PROGRAM_DESCRIPTION = 6
        SCHOOL_NAME = 7
        ADDRESS = 8
        THUMBNAIL_IMAGE_URL = 9
        ALTERNATIVE_THUMBNAIL_IMAGE_URL = 10
        FINAL_URLS = 11
        FINAL_MOBILE_URLS = 12
        TRACKING_URL = 13
        CONTEXTUAL_KEYWORDS = 14
        ANDROID_APP_LINK = 15
        SIMILAR_PROGRAM_IDS = 16
        IOS_APP_LINK = 17
        IOS_APP_STORE_ID = 18


class EnumErrorEnum(object):
    class EnumError(enum.IntEnum):
        """
        Enum describing possible enum errors.

        Attributes:
          UNSPECIFIED (int): Enum unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          ENUM_VALUE_NOT_PERMITTED (int): The enum value is not permitted.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        ENUM_VALUE_NOT_PERMITTED = 3


class ExtensionFeedItemErrorEnum(object):
    class ExtensionFeedItemError(enum.IntEnum):
        """
        Enum describing possible extension feed item errors.

        Attributes:
          UNSPECIFIED (int): Enum unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          VALUE_OUT_OF_RANGE (int): Value is not within the accepted range.
          URL_LIST_TOO_LONG (int): Url list is too long.
          CANNOT_HAVE_RESTRICTION_ON_EMPTY_GEO_TARGETING (int): Cannot have a geo targeting restriction without having geo targeting.
          CANNOT_SET_WITH_FINAL_URLS (int): Cannot simultaneously set sitelink field with final urls.
          CANNOT_SET_WITHOUT_FINAL_URLS (int): Must set field with final urls.
          INVALID_PHONE_NUMBER (int): Phone number for a call extension is invalid.
          PHONE_NUMBER_NOT_SUPPORTED_FOR_COUNTRY (int): Phone number for a call extension is not supported for the given country
          code.
          CARRIER_SPECIFIC_SHORT_NUMBER_NOT_ALLOWED (int): A carrier specific number in short format is not allowed for call
          extensions.
          PREMIUM_RATE_NUMBER_NOT_ALLOWED (int): Premium rate numbers are not allowed for call extensions.
          DISALLOWED_NUMBER_TYPE (int): Phone number type for a call extension is not allowed.
          For example, personal number is not allowed for a call extension in
          most regions.
          INVALID_DOMESTIC_PHONE_NUMBER_FORMAT (int): Phone number for a call extension does not meet domestic format
          requirements.
          VANITY_PHONE_NUMBER_NOT_ALLOWED (int): Vanity phone numbers (i.e. those including letters) are not allowed for
          call extensions.
          INVALID_CALL_CONVERSION_ACTION (int): Call conversion action provided for a call extension is invalid.
          CUSTOMER_NOT_WHITELISTED_FOR_CALLTRACKING (int): For a call extension, the customer is not whitelisted for call tracking.
          CALLTRACKING_NOT_SUPPORTED_FOR_COUNTRY (int): Call tracking is not supported for the given country for a call
          extension.
          CUSTOMER_CONSENT_FOR_CALL_RECORDING_REQUIRED (int): Customer hasn't consented for call recording, which is required for
          creating/updating call feed items. Please see
          https://support.google.com/google-ads/answer/7412639.
          INVALID_APP_ID (int): App id provided for an app extension is invalid.
          QUOTES_IN_REVIEW_EXTENSION_SNIPPET (int): Quotation marks present in the review text for a review extension.
          HYPHENS_IN_REVIEW_EXTENSION_SNIPPET (int): Hyphen character present in the review text for a review extension.
          REVIEW_EXTENSION_SOURCE_INELIGIBLE (int): A blacklisted review source name or url was provided for a review
          extension.
          SOURCE_NAME_IN_REVIEW_EXTENSION_TEXT (int): Review source name should not be found in the review text.
          INCONSISTENT_CURRENCY_CODES (int): Inconsistent currency codes.
          PRICE_EXTENSION_HAS_DUPLICATED_HEADERS (int): Price extension cannot have duplicated headers.
          PRICE_ITEM_HAS_DUPLICATED_HEADER_AND_DESCRIPTION (int): Price item cannot have duplicated header and description.
          PRICE_EXTENSION_HAS_TOO_FEW_ITEMS (int): Price extension has too few items.
          PRICE_EXTENSION_HAS_TOO_MANY_ITEMS (int): Price extension has too many items.
          UNSUPPORTED_VALUE (int): The input value is not currently supported.
          UNSUPPORTED_VALUE_IN_SELECTED_LANGUAGE (int): The input value is not currently supported in the selected language of an
          extension.
          INVALID_DEVICE_PREFERENCE (int): Unknown or unsupported device preference.
          INVALID_SCHEDULE_END (int): Invalid feed item schedule end time (i.e., endHour = 24 and endMinute !=
          0).
          DATE_TIME_MUST_BE_IN_ACCOUNT_TIME_ZONE (int): Date time zone does not match the account's time zone.
          INVALID_SNIPPETS_HEADER (int): Invalid structured snippet header.
          CANNOT_OPERATE_ON_REMOVED_FEED_ITEM (int): Cannot operate on removed feed item.
          PHONE_NUMBER_NOT_SUPPORTED_WITH_CALLTRACKING_FOR_COUNTRY (int): Phone number not supported when call tracking enabled for country.
          CONFLICTING_CALL_CONVERSION_SETTINGS (int): Cannot set call\_conversion\_action while
          call\_conversion\_tracking\_enabled is set to true.
          EXTENSION_TYPE_MISMATCH (int): The type of the input extension feed item doesn't match the existing
          extension feed item.
          EXTENSION_SUBTYPE_REQUIRED (int): The oneof field extension i.e. subtype of extension feed item is
          required.
          EXTENSION_TYPE_UNSUPPORTED (int): The referenced feed item is not mapped to a supported extension type.
          CANNOT_OPERATE_ON_FEED_WITH_MULTIPLE_MAPPINGS (int): Cannot operate on a Feed with more than one active FeedMapping.
          CANNOT_OPERATE_ON_FEED_WITH_KEY_ATTRIBUTES (int): Cannot operate on a Feed that has key attributes.
          INVALID_PRICE_FORMAT (int): Input price is not in a valid format.
          PROMOTION_INVALID_TIME (int): The promotion time is invalid.
          TOO_MANY_DECIMAL_PLACES_SPECIFIED (int): This field has too many decimal places specified.
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
        CUSTOMER_NOT_WHITELISTED_FOR_CALLTRACKING = 15
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


class ExtensionSettingDeviceEnum(object):
    class ExtensionSettingDevice(enum.IntEnum):
        """
        Possbile device types for an extension setting.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): The value is unknown in this version.
          MOBILE (int): Mobile. The extensions in the extension setting will only serve on
          mobile devices.
          DESKTOP (int): Desktop. The extensions in the extension setting will only serve on
          desktop devices.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        MOBILE = 2
        DESKTOP = 3


class ExtensionSettingErrorEnum(object):
    class ExtensionSettingError(enum.IntEnum):
        """
        Enum describing possible extension setting errors.

        Attributes:
          UNSPECIFIED (int): Enum unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          EXTENSIONS_REQUIRED (int): A platform restriction was provided without input extensions or existing
          extensions.
          FEED_TYPE_EXTENSION_TYPE_MISMATCH (int): The provided feed type does not correspond to the provided extensions.
          INVALID_FEED_TYPE (int): The provided feed type cannot be used.
          INVALID_FEED_TYPE_FOR_CUSTOMER_EXTENSION_SETTING (int): The provided feed type cannot be used at the customer level.
          CANNOT_CHANGE_FEED_ITEM_ON_CREATE (int): Cannot change a feed item field on a CREATE operation.
          CANNOT_UPDATE_NEWLY_CREATED_EXTENSION (int): Cannot update an extension that is not already in this setting.
          NO_EXISTING_AD_GROUP_EXTENSION_SETTING_FOR_TYPE (int): There is no existing AdGroupExtensionSetting for this type.
          NO_EXISTING_CAMPAIGN_EXTENSION_SETTING_FOR_TYPE (int): There is no existing CampaignExtensionSetting for this type.
          NO_EXISTING_CUSTOMER_EXTENSION_SETTING_FOR_TYPE (int): There is no existing CustomerExtensionSetting for this type.
          AD_GROUP_EXTENSION_SETTING_ALREADY_EXISTS (int): The AdGroupExtensionSetting already exists. UPDATE should be used to
          modify the existing AdGroupExtensionSetting.
          CAMPAIGN_EXTENSION_SETTING_ALREADY_EXISTS (int): The CampaignExtensionSetting already exists. UPDATE should be used to
          modify the existing CampaignExtensionSetting.
          CUSTOMER_EXTENSION_SETTING_ALREADY_EXISTS (int): The CustomerExtensionSetting already exists. UPDATE should be used to
          modify the existing CustomerExtensionSetting.
          AD_GROUP_FEED_ALREADY_EXISTS_FOR_PLACEHOLDER_TYPE (int): An active ad group feed already exists for this place holder type.
          CAMPAIGN_FEED_ALREADY_EXISTS_FOR_PLACEHOLDER_TYPE (int): An active campaign feed already exists for this place holder type.
          CUSTOMER_FEED_ALREADY_EXISTS_FOR_PLACEHOLDER_TYPE (int): An active customer feed already exists for this place holder type.
          VALUE_OUT_OF_RANGE (int): Value is not within the accepted range.
          CANNOT_SET_FIELD_WITH_FINAL_URLS (int): Cannot simultaneously set specified field with final urls.
          FINAL_URLS_NOT_SET (int): Must set field with final urls.
          INVALID_PHONE_NUMBER (int): Phone number for a call extension is invalid.
          PHONE_NUMBER_NOT_SUPPORTED_FOR_COUNTRY (int): Phone number for a call extension is not supported for the given country
          code.
          CARRIER_SPECIFIC_SHORT_NUMBER_NOT_ALLOWED (int): A carrier specific number in short format is not allowed for call
          extensions.
          PREMIUM_RATE_NUMBER_NOT_ALLOWED (int): Premium rate numbers are not allowed for call extensions.
          DISALLOWED_NUMBER_TYPE (int): Phone number type for a call extension is not allowed.
          INVALID_DOMESTIC_PHONE_NUMBER_FORMAT (int): Phone number for a call extension does not meet domestic format
          requirements.
          VANITY_PHONE_NUMBER_NOT_ALLOWED (int): Vanity phone numbers (i.e. those including letters) are not allowed for
          call extensions.
          INVALID_COUNTRY_CODE (int): Country code provided for a call extension is invalid.
          INVALID_CALL_CONVERSION_TYPE_ID (int): Call conversion type id provided for a call extension is invalid.
          CUSTOMER_NOT_WHITELISTED_FOR_CALLTRACKING (int): For a call extension, the customer is not whitelisted for call tracking.
          CALLTRACKING_NOT_SUPPORTED_FOR_COUNTRY (int): Call tracking is not supported for the given country for a call
          extension.
          INVALID_APP_ID (int): App id provided for an app extension is invalid.
          QUOTES_IN_REVIEW_EXTENSION_SNIPPET (int): Quotation marks present in the review text for a review extension.
          HYPHENS_IN_REVIEW_EXTENSION_SNIPPET (int): Hyphen character present in the review text for a review extension.
          REVIEW_EXTENSION_SOURCE_NOT_ELIGIBLE (int): A blacklisted review source name or url was provided for a review
          extension.
          SOURCE_NAME_IN_REVIEW_EXTENSION_TEXT (int): Review source name should not be found in the review text.
          MISSING_FIELD (int): Field must be set.
          INCONSISTENT_CURRENCY_CODES (int): Inconsistent currency codes.
          PRICE_EXTENSION_HAS_DUPLICATED_HEADERS (int): Price extension cannot have duplicated headers.
          PRICE_ITEM_HAS_DUPLICATED_HEADER_AND_DESCRIPTION (int): Price item cannot have duplicated header and description.
          PRICE_EXTENSION_HAS_TOO_FEW_ITEMS (int): Price extension has too few items
          PRICE_EXTENSION_HAS_TOO_MANY_ITEMS (int): Price extension has too many items
          UNSUPPORTED_VALUE (int): The input value is not currently supported.
          INVALID_DEVICE_PREFERENCE (int): Unknown or unsupported device preference.
          INVALID_SCHEDULE_END (int): Invalid feed item schedule end time (i.e., endHour = 24 and
          endMinute != 0).
          DATE_TIME_MUST_BE_IN_ACCOUNT_TIME_ZONE (int): Date time zone does not match the account's time zone.
          OVERLAPPING_SCHEDULES_NOT_ALLOWED (int): Overlapping feed item schedule times (e.g., 7-10AM and 8-11AM) are not
          allowed.
          SCHEDULE_END_NOT_AFTER_START (int): Feed item schedule end time must be after start time.
          TOO_MANY_SCHEDULES_PER_DAY (int): There are too many feed item schedules per day.
          DUPLICATE_EXTENSION_FEED_ITEM_EDIT (int): Cannot edit the same extension feed item more than once in the same
          request.
          INVALID_SNIPPETS_HEADER (int): Invalid structured snippet header.
          PHONE_NUMBER_NOT_SUPPORTED_WITH_CALLTRACKING_FOR_COUNTRY (int): Phone number with call tracking enabled is not supported for the
          specified country.
          CAMPAIGN_TARGETING_MISMATCH (int): The targeted adgroup must belong to the targeted campaign.
          CANNOT_OPERATE_ON_REMOVED_FEED (int): The feed used by the ExtensionSetting is removed and cannot be operated
          on. Remove the ExtensionSetting to allow a new one to be created using
          an active feed.
          EXTENSION_TYPE_REQUIRED (int): The ExtensionFeedItem type is required for this operation.
          INCOMPATIBLE_UNDERLYING_MATCHING_FUNCTION (int): The matching function that links the extension feed to the customer,
          campaign, or ad group is not compatible with the ExtensionSetting
          services.
          START_DATE_AFTER_END_DATE (int): Start date must be before end date.
          INVALID_PRICE_FORMAT (int): Input price is not in a valid format.
          PROMOTION_INVALID_TIME (int): The promotion time is invalid.
          PROMOTION_CANNOT_SET_PERCENT_DISCOUNT_AND_MONEY_DISCOUNT (int): Cannot set both percent discount and money discount fields.
          PROMOTION_CANNOT_SET_PROMOTION_CODE_AND_ORDERS_OVER_AMOUNT (int): Cannot set both promotion code and orders over amount fields.
          TOO_MANY_DECIMAL_PLACES_SPECIFIED (int): This field has too many decimal places specified.
          INVALID_LANGUAGE_CODE (int): The language code is not valid.
          UNSUPPORTED_LANGUAGE (int): The language is not supported.
          CUSTOMER_CONSENT_FOR_CALL_RECORDING_REQUIRED (int): Customer hasn't consented for call recording, which is required for
          adding/updating call extensions. Please see
          https://support.google.com/google-ads/answer/7412639.
          EXTENSION_SETTING_UPDATE_IS_A_NOOP (int): The UPDATE operation does not specify any fields other than the resource
          name in the update mask.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        EXTENSIONS_REQUIRED = 2
        FEED_TYPE_EXTENSION_TYPE_MISMATCH = 3
        INVALID_FEED_TYPE = 4
        INVALID_FEED_TYPE_FOR_CUSTOMER_EXTENSION_SETTING = 5
        CANNOT_CHANGE_FEED_ITEM_ON_CREATE = 6
        CANNOT_UPDATE_NEWLY_CREATED_EXTENSION = 7
        NO_EXISTING_AD_GROUP_EXTENSION_SETTING_FOR_TYPE = 8
        NO_EXISTING_CAMPAIGN_EXTENSION_SETTING_FOR_TYPE = 9
        NO_EXISTING_CUSTOMER_EXTENSION_SETTING_FOR_TYPE = 10
        AD_GROUP_EXTENSION_SETTING_ALREADY_EXISTS = 11
        CAMPAIGN_EXTENSION_SETTING_ALREADY_EXISTS = 12
        CUSTOMER_EXTENSION_SETTING_ALREADY_EXISTS = 13
        AD_GROUP_FEED_ALREADY_EXISTS_FOR_PLACEHOLDER_TYPE = 14
        CAMPAIGN_FEED_ALREADY_EXISTS_FOR_PLACEHOLDER_TYPE = 15
        CUSTOMER_FEED_ALREADY_EXISTS_FOR_PLACEHOLDER_TYPE = 16
        VALUE_OUT_OF_RANGE = 17
        CANNOT_SET_FIELD_WITH_FINAL_URLS = 18
        FINAL_URLS_NOT_SET = 19
        INVALID_PHONE_NUMBER = 20
        PHONE_NUMBER_NOT_SUPPORTED_FOR_COUNTRY = 21
        CARRIER_SPECIFIC_SHORT_NUMBER_NOT_ALLOWED = 22
        PREMIUM_RATE_NUMBER_NOT_ALLOWED = 23
        DISALLOWED_NUMBER_TYPE = 24
        INVALID_DOMESTIC_PHONE_NUMBER_FORMAT = 25
        VANITY_PHONE_NUMBER_NOT_ALLOWED = 26
        INVALID_COUNTRY_CODE = 27
        INVALID_CALL_CONVERSION_TYPE_ID = 28
        CUSTOMER_NOT_WHITELISTED_FOR_CALLTRACKING = 29
        CALLTRACKING_NOT_SUPPORTED_FOR_COUNTRY = 30
        INVALID_APP_ID = 31
        QUOTES_IN_REVIEW_EXTENSION_SNIPPET = 32
        HYPHENS_IN_REVIEW_EXTENSION_SNIPPET = 33
        REVIEW_EXTENSION_SOURCE_NOT_ELIGIBLE = 34
        SOURCE_NAME_IN_REVIEW_EXTENSION_TEXT = 35
        MISSING_FIELD = 36
        INCONSISTENT_CURRENCY_CODES = 37
        PRICE_EXTENSION_HAS_DUPLICATED_HEADERS = 38
        PRICE_ITEM_HAS_DUPLICATED_HEADER_AND_DESCRIPTION = 39
        PRICE_EXTENSION_HAS_TOO_FEW_ITEMS = 40
        PRICE_EXTENSION_HAS_TOO_MANY_ITEMS = 41
        UNSUPPORTED_VALUE = 42
        INVALID_DEVICE_PREFERENCE = 43
        INVALID_SCHEDULE_END = 45
        DATE_TIME_MUST_BE_IN_ACCOUNT_TIME_ZONE = 47
        OVERLAPPING_SCHEDULES_NOT_ALLOWED = 48
        SCHEDULE_END_NOT_AFTER_START = 49
        TOO_MANY_SCHEDULES_PER_DAY = 50
        DUPLICATE_EXTENSION_FEED_ITEM_EDIT = 51
        INVALID_SNIPPETS_HEADER = 52
        PHONE_NUMBER_NOT_SUPPORTED_WITH_CALLTRACKING_FOR_COUNTRY = 53
        CAMPAIGN_TARGETING_MISMATCH = 54
        CANNOT_OPERATE_ON_REMOVED_FEED = 55
        EXTENSION_TYPE_REQUIRED = 56
        INCOMPATIBLE_UNDERLYING_MATCHING_FUNCTION = 57
        START_DATE_AFTER_END_DATE = 58
        INVALID_PRICE_FORMAT = 59
        PROMOTION_INVALID_TIME = 60
        PROMOTION_CANNOT_SET_PERCENT_DISCOUNT_AND_MONEY_DISCOUNT = 61
        PROMOTION_CANNOT_SET_PROMOTION_CODE_AND_ORDERS_OVER_AMOUNT = 62
        TOO_MANY_DECIMAL_PLACES_SPECIFIED = 63
        INVALID_LANGUAGE_CODE = 64
        UNSUPPORTED_LANGUAGE = 65
        CUSTOMER_CONSENT_FOR_CALL_RECORDING_REQUIRED = 66
        EXTENSION_SETTING_UPDATE_IS_A_NOOP = 67


class ExtensionTypeEnum(object):
    class ExtensionType(enum.IntEnum):
        """
        Possible data types for an extension in an extension setting.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          NONE (int): None.
          APP (int): App.
          CALL (int): Call.
          CALLOUT (int): Callout.
          MESSAGE (int): Message.
          PRICE (int): Price.
          PROMOTION (int): Promotion.
          REVIEW (int): Review.
          SITELINK (int): Sitelink.
          STRUCTURED_SNIPPET (int): Structured snippet.
          LOCATION (int): Location.
          AFFILIATE_LOCATION (int): Affiliate location.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        NONE = 2
        APP = 3
        CALL = 4
        CALLOUT = 5
        MESSAGE = 6
        PRICE = 7
        PROMOTION = 8
        REVIEW = 9
        SITELINK = 10
        STRUCTURED_SNIPPET = 11
        LOCATION = 12
        AFFILIATE_LOCATION = 13


class ExternalConversionSourceEnum(object):
    class ExternalConversionSource(enum.IntEnum):
        """
        The external conversion source that is associated with a ConversionAction.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Represents value unknown in this version.
          WEBPAGE (int): Conversion that occurs when a user navigates to a particular webpage
          after viewing an ad; Displayed in Google Ads UI as 'Website'.
          ANALYTICS (int): Conversion that comes from linked Google Analytics goal or transaction;
          Displayed in Google Ads UI as 'Analytics'.
          UPLOAD (int): Website conversion that is uploaded through ConversionUploadService;
          Displayed in Google Ads UI as 'Import from clicks'.
          AD_CALL_METRICS (int): Conversion that occurs when a user clicks on a call extension directly on
          an ad; Displayed in Google Ads UI as 'Calls from ads'.
          WEBSITE_CALL_METRICS (int): Conversion that occurs when a user calls a dynamically-generated phone
          number (by installed javascript) from an advertiser's website after
          clicking on an ad; Displayed in Google Ads UI as 'Calls from website'.
          STORE_VISITS (int): Conversion that occurs when a user visits an advertiser's retail store
          after clicking on a Google ad;
          Displayed in Google Ads UI as 'Store visits'.
          ANDROID_IN_APP (int): Conversion that occurs when a user takes an in-app action such as a
          purchase in an Android app;
          Displayed in Google Ads UI as 'Android in-app action'.
          IOS_IN_APP (int): Conversion that occurs when a user takes an in-app action such as a
          purchase in an iOS app;
          Displayed in Google Ads UI as 'iOS in-app action'.
          IOS_FIRST_OPEN (int): Conversion that occurs when a user opens an iOS app for the first time;
          Displayed in Google Ads UI as 'iOS app install (first open)'.
          APP_UNSPECIFIED (int): Legacy app conversions that do not have an AppPlatform provided;
          Displayed in Google Ads UI as 'Mobile app'.
          ANDROID_FIRST_OPEN (int): Conversion that occurs when a user opens an Android app for the first
          time; Displayed in Google Ads UI as 'Android app install (first open)'.
          UPLOAD_CALLS (int): Call conversion that is uploaded through ConversionUploadService;
          Displayed in Google Ads UI as 'Import from calls'.
          FIREBASE (int): Conversion that comes from a linked Firebase event;
          Displayed in Google Ads UI as 'Firebase'.
          CLICK_TO_CALL (int): Conversion that occurs when a user clicks on a mobile phone number;
          Displayed in Google Ads UI as 'Phone number clicks'.
          SALESFORCE (int): Conversion that comes from Salesforce;
          Displayed in Google Ads UI as 'Salesforce.com'.
          STORE_SALES_CRM (int): Conversion that comes from in-store purchases recorded by CRM;
          Displayed in Google Ads UI as 'Store sales (data partner)'.
          STORE_SALES_PAYMENT_NETWORK (int): Conversion that comes from in-store purchases from payment network;
          Displayed in Google Ads UI as 'Store sales (payment network)'.
          GOOGLE_PLAY (int): Codeless Google Play conversion;
          Displayed in Google Ads UI as 'Google Play'.
          THIRD_PARTY_APP_ANALYTICS (int): Conversion that comes from a linked third-party app analytics event;
          Displayed in Google Ads UI as 'Third-party app analytics'.
          GOOGLE_ATTRIBUTION (int): Conversion that is controlled by Google Attribution.
          STORE_SALES_DIRECT (int): Store Sales conversion based on first-party or third-party merchant data
          uploads. Displayed in Google Ads UI as 'Store sales (direct)'.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        WEBPAGE = 2
        ANALYTICS = 3
        UPLOAD = 4
        AD_CALL_METRICS = 5
        WEBSITE_CALL_METRICS = 6
        STORE_VISITS = 7
        ANDROID_IN_APP = 8
        IOS_IN_APP = 9
        IOS_FIRST_OPEN = 10
        APP_UNSPECIFIED = 11
        ANDROID_FIRST_OPEN = 12
        UPLOAD_CALLS = 13
        FIREBASE = 14
        CLICK_TO_CALL = 15
        SALESFORCE = 16
        STORE_SALES_CRM = 17
        STORE_SALES_PAYMENT_NETWORK = 18
        GOOGLE_PLAY = 19
        THIRD_PARTY_APP_ANALYTICS = 20
        GOOGLE_ATTRIBUTION = 21
        STORE_SALES_DIRECT = 22


class FeedAttributeOperation(object):
    class Operator(enum.IntEnum):
        """
        The operator.

        Attributes:
          UNSPECIFIED (int): Unspecified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          ADD (int): Add the attribute to the existing attributes.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        ADD = 2


class FeedAttributeReferenceErrorEnum(object):
    class FeedAttributeReferenceError(enum.IntEnum):
        """
        Enum describing possible feed attribute reference errors.

        Attributes:
          UNSPECIFIED (int): Enum unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          CANNOT_REFERENCE_REMOVED_FEED (int): A feed referenced by ID has been removed.
          INVALID_FEED_NAME (int): There is no enabled feed with the given name.
          INVALID_FEED_ATTRIBUTE_NAME (int): There is no feed attribute in an enabled feed with the given name.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        CANNOT_REFERENCE_REMOVED_FEED = 2
        INVALID_FEED_NAME = 3
        INVALID_FEED_ATTRIBUTE_NAME = 4


class FeedAttributeTypeEnum(object):
    class FeedAttributeType(enum.IntEnum):
        """
        Possible data types for a feed attribute.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          INT64 (int): Int64.
          DOUBLE (int): Double.
          STRING (int): String.
          BOOLEAN (int): Boolean.
          URL (int): Url.
          DATE_TIME (int): Datetime.
          INT64_LIST (int): Int64 list.
          DOUBLE_LIST (int): Double (8 bytes) list.
          STRING_LIST (int): String list.
          BOOLEAN_LIST (int): Boolean list.
          URL_LIST (int): Url list.
          DATE_TIME_LIST (int): Datetime list.
          PRICE (int): Price.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        INT64 = 2
        DOUBLE = 3
        STRING = 4
        BOOLEAN = 5
        URL = 6
        DATE_TIME = 7
        INT64_LIST = 8
        DOUBLE_LIST = 9
        STRING_LIST = 10
        BOOLEAN_LIST = 11
        URL_LIST = 12
        DATE_TIME_LIST = 13
        PRICE = 14


class FeedErrorEnum(object):
    class FeedError(enum.IntEnum):
        """
        Enum describing possible feed errors.

        Attributes:
          UNSPECIFIED (int): Enum unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          ATTRIBUTE_NAMES_NOT_UNIQUE (int): The names of the FeedAttributes must be unique.
          ATTRIBUTES_DO_NOT_MATCH_EXISTING_ATTRIBUTES (int): The attribute list must be an exact copy of the existing list if the
          attribute ID's are present.
          CANNOT_SPECIFY_USER_ORIGIN_FOR_SYSTEM_FEED (int): Cannot specify USER origin for a system generated feed.
          CANNOT_SPECIFY_GOOGLE_ORIGIN_FOR_NON_SYSTEM_FEED (int): Cannot specify GOOGLE origin for a non-system generated feed.
          CANNOT_SPECIFY_FEED_ATTRIBUTES_FOR_SYSTEM_FEED (int): Cannot specify feed attributes for system feed.
          CANNOT_UPDATE_FEED_ATTRIBUTES_WITH_ORIGIN_GOOGLE (int): Cannot update FeedAttributes on feed with origin GOOGLE.
          FEED_REMOVED (int): The given ID refers to a removed Feed. Removed Feeds are immutable.
          INVALID_ORIGIN_VALUE (int): The origin of the feed is not valid for the client.
          FEED_ORIGIN_IS_NOT_USER (int): A user can only create and modify feeds with USER origin.
          INVALID_AUTH_TOKEN_FOR_EMAIL (int): Invalid auth token for the given email.
          INVALID_EMAIL (int): Invalid email specified.
          DUPLICATE_FEED_NAME (int): Feed name matches that of another active Feed.
          INVALID_FEED_NAME (int): Name of feed is not allowed.
          MISSING_OAUTH_INFO (int): Missing OAuthInfo.
          NEW_ATTRIBUTE_CANNOT_BE_PART_OF_UNIQUE_KEY (int): New FeedAttributes must not affect the unique key.
          TOO_MANY_ATTRIBUTES (int): Too many FeedAttributes for a Feed.
          INVALID_BUSINESS_ACCOUNT (int): The business account is not valid.
          BUSINESS_ACCOUNT_CANNOT_ACCESS_LOCATION_ACCOUNT (int): Business account cannot access Google My Business account.
          INVALID_AFFILIATE_CHAIN_ID (int): Invalid chain ID provided for affiliate location feed.
          DUPLICATE_SYSTEM_FEED (int): There is already a feed with the given system feed generation data.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        ATTRIBUTE_NAMES_NOT_UNIQUE = 2
        ATTRIBUTES_DO_NOT_MATCH_EXISTING_ATTRIBUTES = 3
        CANNOT_SPECIFY_USER_ORIGIN_FOR_SYSTEM_FEED = 4
        CANNOT_SPECIFY_GOOGLE_ORIGIN_FOR_NON_SYSTEM_FEED = 5
        CANNOT_SPECIFY_FEED_ATTRIBUTES_FOR_SYSTEM_FEED = 6
        CANNOT_UPDATE_FEED_ATTRIBUTES_WITH_ORIGIN_GOOGLE = 7
        FEED_REMOVED = 8
        INVALID_ORIGIN_VALUE = 9
        FEED_ORIGIN_IS_NOT_USER = 10
        INVALID_AUTH_TOKEN_FOR_EMAIL = 11
        INVALID_EMAIL = 12
        DUPLICATE_FEED_NAME = 13
        INVALID_FEED_NAME = 14
        MISSING_OAUTH_INFO = 15
        NEW_ATTRIBUTE_CANNOT_BE_PART_OF_UNIQUE_KEY = 16
        TOO_MANY_ATTRIBUTES = 17
        INVALID_BUSINESS_ACCOUNT = 18
        BUSINESS_ACCOUNT_CANNOT_ACCESS_LOCATION_ACCOUNT = 19
        INVALID_AFFILIATE_CHAIN_ID = 20
        DUPLICATE_SYSTEM_FEED = 21


class FeedItemErrorEnum(object):
    class FeedItemError(enum.IntEnum):
        """
        Enum describing possible feed item errors.

        Attributes:
          UNSPECIFIED (int): Enum unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          CANNOT_CONVERT_ATTRIBUTE_VALUE_FROM_STRING (int): Cannot convert the feed attribute value from string to its real type.
          CANNOT_OPERATE_ON_REMOVED_FEED_ITEM (int): Cannot operate on removed feed item.
          DATE_TIME_MUST_BE_IN_ACCOUNT_TIME_ZONE (int): Date time zone does not match the account's time zone.
          KEY_ATTRIBUTES_NOT_FOUND (int): Feed item with the key attributes could not be found.
          INVALID_URL (int): Url feed attribute value is not valid.
          MISSING_KEY_ATTRIBUTES (int): Some key attributes are missing.
          KEY_ATTRIBUTES_NOT_UNIQUE (int): Feed item has same key attributes as another feed item.
          CANNOT_MODIFY_KEY_ATTRIBUTE_VALUE (int): Cannot modify key attributes on an existing feed item.
          SIZE_TOO_LARGE_FOR_MULTI_VALUE_ATTRIBUTE (int): The feed attribute value is too large.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        CANNOT_CONVERT_ATTRIBUTE_VALUE_FROM_STRING = 2
        CANNOT_OPERATE_ON_REMOVED_FEED_ITEM = 3
        DATE_TIME_MUST_BE_IN_ACCOUNT_TIME_ZONE = 4
        KEY_ATTRIBUTES_NOT_FOUND = 5
        INVALID_URL = 6
        MISSING_KEY_ATTRIBUTES = 7
        KEY_ATTRIBUTES_NOT_UNIQUE = 8
        CANNOT_MODIFY_KEY_ATTRIBUTE_VALUE = 9
        SIZE_TOO_LARGE_FOR_MULTI_VALUE_ATTRIBUTE = 10


class FeedItemQualityApprovalStatusEnum(object):
    class FeedItemQualityApprovalStatus(enum.IntEnum):
        """
        The possible quality evaluation approval statuses of a feed item.

        Attributes:
          UNSPECIFIED (int): No value has been specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          APPROVED (int): Meets all quality expectations.
          DISAPPROVED (int): Does not meet some quality expectations. The specific reason is found in
          the quality\_disapproval\_reasons field.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        APPROVED = 2
        DISAPPROVED = 3


class FeedItemQualityDisapprovalReasonEnum(object):
    class FeedItemQualityDisapprovalReason(enum.IntEnum):
        """
        The possible quality evaluation disapproval reasons of a feed item.

        Attributes:
          UNSPECIFIED (int): No value has been specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          PRICE_TABLE_REPETITIVE_HEADERS (int): Price contains repetitive headers.
          PRICE_TABLE_REPETITIVE_DESCRIPTION (int): Price contains repetitive description.
          PRICE_TABLE_INCONSISTENT_ROWS (int): Price contains inconsistent items.
          PRICE_DESCRIPTION_HAS_PRICE_QUALIFIERS (int): Price contains qualifiers in description.
          PRICE_UNSUPPORTED_LANGUAGE (int): Price contains an unsupported language.
          PRICE_TABLE_ROW_HEADER_TABLE_TYPE_MISMATCH (int): Price item header is not relevant to the price type.
          PRICE_TABLE_ROW_HEADER_HAS_PROMOTIONAL_TEXT (int): Price item header has promotional text.
          PRICE_TABLE_ROW_DESCRIPTION_NOT_RELEVANT (int): Price item description is not relevant to the item header.
          PRICE_TABLE_ROW_DESCRIPTION_HAS_PROMOTIONAL_TEXT (int): Price item description contains promotional text.
          PRICE_TABLE_ROW_HEADER_DESCRIPTION_REPETITIVE (int): Price item header and description are repetitive.
          PRICE_TABLE_ROW_UNRATEABLE (int): Price item is in a foreign language, nonsense, or can't be rated.
          PRICE_TABLE_ROW_PRICE_INVALID (int): Price item price is invalid or inaccurate.
          PRICE_TABLE_ROW_URL_INVALID (int): Price item URL is invalid or irrelevant.
          PRICE_HEADER_OR_DESCRIPTION_HAS_PRICE (int): Price item header or description has price.
          STRUCTURED_SNIPPETS_HEADER_POLICY_VIOLATED (int): Structured snippet values do not match the header.
          STRUCTURED_SNIPPETS_REPEATED_VALUES (int): Structured snippet values are repeated.
          STRUCTURED_SNIPPETS_EDITORIAL_GUIDELINES (int): Structured snippet values violate editorial guidelines like punctuation.
          STRUCTURED_SNIPPETS_HAS_PROMOTIONAL_TEXT (int): Structured snippet contain promotional text.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        PRICE_TABLE_REPETITIVE_HEADERS = 2
        PRICE_TABLE_REPETITIVE_DESCRIPTION = 3
        PRICE_TABLE_INCONSISTENT_ROWS = 4
        PRICE_DESCRIPTION_HAS_PRICE_QUALIFIERS = 5
        PRICE_UNSUPPORTED_LANGUAGE = 6
        PRICE_TABLE_ROW_HEADER_TABLE_TYPE_MISMATCH = 7
        PRICE_TABLE_ROW_HEADER_HAS_PROMOTIONAL_TEXT = 8
        PRICE_TABLE_ROW_DESCRIPTION_NOT_RELEVANT = 9
        PRICE_TABLE_ROW_DESCRIPTION_HAS_PROMOTIONAL_TEXT = 10
        PRICE_TABLE_ROW_HEADER_DESCRIPTION_REPETITIVE = 11
        PRICE_TABLE_ROW_UNRATEABLE = 12
        PRICE_TABLE_ROW_PRICE_INVALID = 13
        PRICE_TABLE_ROW_URL_INVALID = 14
        PRICE_HEADER_OR_DESCRIPTION_HAS_PRICE = 15
        STRUCTURED_SNIPPETS_HEADER_POLICY_VIOLATED = 16
        STRUCTURED_SNIPPETS_REPEATED_VALUES = 17
        STRUCTURED_SNIPPETS_EDITORIAL_GUIDELINES = 18
        STRUCTURED_SNIPPETS_HAS_PROMOTIONAL_TEXT = 19


class FeedItemStatusEnum(object):
    class FeedItemStatus(enum.IntEnum):
        """
        Possible statuses of a feed item.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          ENABLED (int): Feed item is enabled.
          REMOVED (int): Feed item has been removed.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        ENABLED = 2
        REMOVED = 3


class FeedItemTargetDeviceEnum(object):
    class FeedItemTargetDevice(enum.IntEnum):
        """
        Possible data types for a feed item target device.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          MOBILE (int): Mobile.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        MOBILE = 2


class FeedItemTargetErrorEnum(object):
    class FeedItemTargetError(enum.IntEnum):
        """
        Enum describing possible feed item target errors.

        Attributes:
          UNSPECIFIED (int): Enum unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          MUST_SET_TARGET_ONEOF_ON_CREATE (int): On CREATE, the FeedItemTarget must have a populated field in the oneof
          target.
          FEED_ITEM_TARGET_ALREADY_EXISTS (int): The specified feed item target already exists, so it cannot be added.
          FEED_ITEM_SCHEDULES_CANNOT_OVERLAP (int): The schedules for a given feed item cannot overlap.
          TARGET_LIMIT_EXCEEDED_FOR_GIVEN_TYPE (int): Too many targets of a given type were added for a single feed item.
          TOO_MANY_SCHEDULES_PER_DAY (int): Too many AdSchedules are enabled for the feed item for the given day.
          CANNOT_HAVE_ENABLED_CAMPAIGN_AND_ENABLED_AD_GROUP_TARGETS (int): A feed item may either have an enabled campaign target or an enabled ad
          group target.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        MUST_SET_TARGET_ONEOF_ON_CREATE = 2
        FEED_ITEM_TARGET_ALREADY_EXISTS = 3
        FEED_ITEM_SCHEDULES_CANNOT_OVERLAP = 4
        TARGET_LIMIT_EXCEEDED_FOR_GIVEN_TYPE = 5
        TOO_MANY_SCHEDULES_PER_DAY = 6
        CANNOT_HAVE_ENABLED_CAMPAIGN_AND_ENABLED_AD_GROUP_TARGETS = 7


class FeedItemTargetTypeEnum(object):
    class FeedItemTargetType(enum.IntEnum):
        """
        Possible type of a feed item target.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          CAMPAIGN (int): Feed item targets a campaign.
          AD_GROUP (int): Feed item targets an ad group.
          CRITERION (int): Feed item targets a criterion.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        CAMPAIGN = 2
        AD_GROUP = 3
        CRITERION = 4


class FeedItemValidationErrorEnum(object):
    class FeedItemValidationError(enum.IntEnum):
        """
        The possible validation errors of a feed item.

        Attributes:
          UNSPECIFIED (int): No value has been specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          STRING_TOO_SHORT (int): String is too short.
          STRING_TOO_LONG (int): String is too long.
          VALUE_NOT_SPECIFIED (int): Value is not provided.
          INVALID_DOMESTIC_PHONE_NUMBER_FORMAT (int): Phone number format is invalid for region.
          INVALID_PHONE_NUMBER (int): String does not represent a phone number.
          PHONE_NUMBER_NOT_SUPPORTED_FOR_COUNTRY (int): Phone number format is not compatible with country code.
          PREMIUM_RATE_NUMBER_NOT_ALLOWED (int): Premium rate number is not allowed.
          DISALLOWED_NUMBER_TYPE (int): Phone number type is not allowed.
          VALUE_OUT_OF_RANGE (int): Specified value is outside of the valid range.
          CALLTRACKING_NOT_SUPPORTED_FOR_COUNTRY (int): Call tracking is not supported in the selected country.
          CUSTOMER_NOT_WHITELISTED_FOR_CALLTRACKING (int): Customer is not whitelisted for call tracking.
          INVALID_COUNTRY_CODE (int): Country code is invalid.
          INVALID_APP_ID (int): The specified mobile app id is invalid.
          MISSING_ATTRIBUTES_FOR_FIELDS (int): Some required field attributes are missing.
          INVALID_TYPE_ID (int): Invalid email button type for email extension.
          INVALID_EMAIL_ADDRESS (int): Email address is invalid.
          INVALID_HTTPS_URL (int): The HTTPS URL in email extension is invalid.
          MISSING_DELIVERY_ADDRESS (int): Delivery address is missing from email extension.
          START_DATE_AFTER_END_DATE (int): FeedItem scheduling start date comes after end date.
          MISSING_FEED_ITEM_START_TIME (int): FeedItem scheduling start time is missing.
          MISSING_FEED_ITEM_END_TIME (int): FeedItem scheduling end time is missing.
          MISSING_FEED_ITEM_ID (int): Cannot compute system attributes on a FeedItem that has no FeedItemId.
          VANITY_PHONE_NUMBER_NOT_ALLOWED (int): Call extension vanity phone numbers are not supported.
          INVALID_REVIEW_EXTENSION_SNIPPET (int): Invalid review text.
          INVALID_NUMBER_FORMAT (int): Invalid format for numeric value in ad parameter.
          INVALID_DATE_FORMAT (int): Invalid format for date value in ad parameter.
          INVALID_PRICE_FORMAT (int): Invalid format for price value in ad parameter.
          UNKNOWN_PLACEHOLDER_FIELD (int): Unrecognized type given for value in ad parameter.
          MISSING_ENHANCED_SITELINK_DESCRIPTION_LINE (int): Enhanced sitelinks must have both description lines specified.
          REVIEW_EXTENSION_SOURCE_INELIGIBLE (int): Review source is ineligible.
          HYPHENS_IN_REVIEW_EXTENSION_SNIPPET (int): Review text cannot contain hyphens or dashes.
          DOUBLE_QUOTES_IN_REVIEW_EXTENSION_SNIPPET (int): Review text cannot contain double quote characters.
          QUOTES_IN_REVIEW_EXTENSION_SNIPPET (int): Review text cannot contain quote characters.
          INVALID_FORM_ENCODED_PARAMS (int): Parameters are encoded in the wrong format.
          INVALID_URL_PARAMETER_NAME (int): URL parameter name must contain only letters, numbers, underscores, and
          dashes.
          NO_GEOCODING_RESULT (int): Cannot find address location.
          SOURCE_NAME_IN_REVIEW_EXTENSION_TEXT (int): Review extension text has source name.
          CARRIER_SPECIFIC_SHORT_NUMBER_NOT_ALLOWED (int): Some phone numbers can be shorter than usual. Some of these short numbers
          are carrier-specific, and we disallow those in ad extensions because they
          will not be available to all users.
          INVALID_PLACEHOLDER_FIELD_ID (int): Triggered when a request references a placeholder field id that does not
          exist.
          INVALID_URL_TAG (int): URL contains invalid ValueTrack tags or format.
          LIST_TOO_LONG (int): Provided list exceeds acceptable size.
          INVALID_ATTRIBUTES_COMBINATION (int): Certain combinations of attributes aren't allowed to be specified in the
          same feed item.
          DUPLICATE_VALUES (int): An attribute has the same value repeatedly.
          INVALID_CALL_CONVERSION_ACTION_ID (int): Advertisers can link a conversion action with a phone number to indicate
          that sufficiently long calls forwarded to that phone number should be
          counted as conversions of the specified type.  This is an error message
          indicating that the conversion action specified is invalid (e.g., the
          conversion action does not exist within the appropriate Google Ads
          account, or it is a type of conversion not appropriate to phone call
          conversions).
          CANNOT_SET_WITHOUT_FINAL_URLS (int): Tracking template requires final url to be set.
          APP_ID_DOESNT_EXIST_IN_APP_STORE (int): An app id was provided that doesn't exist in the given app store.
          INVALID_FINAL_URL (int): Invalid U2 final url.
          INVALID_TRACKING_URL (int): Invalid U2 tracking url.
          INVALID_FINAL_URL_FOR_APP_DOWNLOAD_URL (int): Final URL should start from App download URL.
          LIST_TOO_SHORT (int): List provided is too short.
          INVALID_USER_ACTION (int): User Action field has invalid value.
          INVALID_TYPE_NAME (int): Type field has invalid value.
          INVALID_EVENT_CHANGE_STATUS (int): Change status for event is invalid.
          INVALID_SNIPPETS_HEADER (int): The header of a structured snippets extension is not one of the valid
          headers.
          INVALID_ANDROID_APP_LINK (int): Android app link is not formatted correctly
          NUMBER_TYPE_WITH_CALLTRACKING_NOT_SUPPORTED_FOR_COUNTRY (int): Phone number incompatible with call tracking for country.
          RESERVED_KEYWORD_OTHER (int): The input is identical to a reserved keyword
          DUPLICATE_OPTION_LABELS (int): Each option label in the message extension must be unique.
          DUPLICATE_OPTION_PREFILLS (int): Each option prefill in the message extension must be unique.
          UNEQUAL_LIST_LENGTHS (int): In message extensions, the number of optional labels and optional
          prefills must be the same.
          INCONSISTENT_CURRENCY_CODES (int): All currency codes in an ad extension must be the same.
          PRICE_EXTENSION_HAS_DUPLICATED_HEADERS (int): Headers in price extension are not unique.
          ITEM_HAS_DUPLICATED_HEADER_AND_DESCRIPTION (int): Header and description in an item are the same.
          PRICE_EXTENSION_HAS_TOO_FEW_ITEMS (int): Price extension has too few items.
          UNSUPPORTED_VALUE (int): The given value is not supported.
          INVALID_FINAL_MOBILE_URL (int): Invalid final mobile url.
          INVALID_KEYWORDLESS_AD_RULE_LABEL (int): The given string value of Label contains invalid characters
          VALUE_TRACK_PARAMETER_NOT_SUPPORTED (int): The given URL contains value track parameters.
          UNSUPPORTED_VALUE_IN_SELECTED_LANGUAGE (int): The given value is not supported in the selected language of an
          extension.
          INVALID_IOS_APP_LINK (int): The iOS app link is not formatted correctly.
          MISSING_IOS_APP_LINK_OR_IOS_APP_STORE_ID (int): iOS app link or iOS app store id is missing.
          PROMOTION_INVALID_TIME (int): Promotion time is invalid.
          PROMOTION_CANNOT_SET_PERCENT_OFF_AND_MONEY_AMOUNT_OFF (int): Both the percent off and money amount off fields are set.
          PROMOTION_CANNOT_SET_PROMOTION_CODE_AND_ORDERS_OVER_AMOUNT (int): Both the promotion code and orders over amount fields are set.
          TOO_MANY_DECIMAL_PLACES_SPECIFIED (int): Too many decimal places are specified.
          AD_CUSTOMIZERS_NOT_ALLOWED (int): Ad Customizers are present and not allowed.
          INVALID_LANGUAGE_CODE (int): Language code is not valid.
          UNSUPPORTED_LANGUAGE (int): Language is not supported.
          IF_FUNCTION_NOT_ALLOWED (int): IF Function is present and not allowed.
          INVALID_FINAL_URL_SUFFIX (int): Final url suffix is not valid.
          INVALID_TAG_IN_FINAL_URL_SUFFIX (int): Final url suffix contains an invalid tag.
          INVALID_FINAL_URL_SUFFIX_FORMAT (int): Final url suffix is formatted incorrectly.
          CUSTOMER_CONSENT_FOR_CALL_RECORDING_REQUIRED (int): Consent for call recording, which is required for the use of call
          extensions, was not provided by the advertiser. Please see
          https://support.google.com/google-ads/answer/7412639.
          ONLY_ONE_DELIVERY_OPTION_IS_ALLOWED (int): Multiple message delivery options are set.
          NO_DELIVERY_OPTION_IS_SET (int): No message delivery option is set.
          INVALID_CONVERSION_REPORTING_STATE (int): String value of conversion reporting state field is not valid.
          IMAGE_SIZE_WRONG (int): Image size is not right.
          EMAIL_DELIVERY_NOT_AVAILABLE_IN_COUNTRY (int): Email delivery is not supported in the country specified in the country
          code field.
          AUTO_REPLY_NOT_AVAILABLE_IN_COUNTRY (int): Auto reply is not supported in the country specified in the country code
          field.
          INVALID_LATITUDE_VALUE (int): Invalid value specified for latitude.
          INVALID_LONGITUDE_VALUE (int): Invalid value specified for longitude.
          TOO_MANY_LABELS (int): Too many label fields provided.
          INVALID_IMAGE_URL (int): Invalid image url.
          MISSING_LATITUDE_VALUE (int): Latitude value is missing.
          MISSING_LONGITUDE_VALUE (int): Longitude value is missing.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        STRING_TOO_SHORT = 2
        STRING_TOO_LONG = 3
        VALUE_NOT_SPECIFIED = 4
        INVALID_DOMESTIC_PHONE_NUMBER_FORMAT = 5
        INVALID_PHONE_NUMBER = 6
        PHONE_NUMBER_NOT_SUPPORTED_FOR_COUNTRY = 7
        PREMIUM_RATE_NUMBER_NOT_ALLOWED = 8
        DISALLOWED_NUMBER_TYPE = 9
        VALUE_OUT_OF_RANGE = 10
        CALLTRACKING_NOT_SUPPORTED_FOR_COUNTRY = 11
        CUSTOMER_NOT_WHITELISTED_FOR_CALLTRACKING = 12
        INVALID_COUNTRY_CODE = 13
        INVALID_APP_ID = 14
        MISSING_ATTRIBUTES_FOR_FIELDS = 15
        INVALID_TYPE_ID = 16
        INVALID_EMAIL_ADDRESS = 17
        INVALID_HTTPS_URL = 18
        MISSING_DELIVERY_ADDRESS = 19
        START_DATE_AFTER_END_DATE = 20
        MISSING_FEED_ITEM_START_TIME = 21
        MISSING_FEED_ITEM_END_TIME = 22
        MISSING_FEED_ITEM_ID = 23
        VANITY_PHONE_NUMBER_NOT_ALLOWED = 24
        INVALID_REVIEW_EXTENSION_SNIPPET = 25
        INVALID_NUMBER_FORMAT = 26
        INVALID_DATE_FORMAT = 27
        INVALID_PRICE_FORMAT = 28
        UNKNOWN_PLACEHOLDER_FIELD = 29
        MISSING_ENHANCED_SITELINK_DESCRIPTION_LINE = 30
        REVIEW_EXTENSION_SOURCE_INELIGIBLE = 31
        HYPHENS_IN_REVIEW_EXTENSION_SNIPPET = 32
        DOUBLE_QUOTES_IN_REVIEW_EXTENSION_SNIPPET = 33
        QUOTES_IN_REVIEW_EXTENSION_SNIPPET = 34
        INVALID_FORM_ENCODED_PARAMS = 35
        INVALID_URL_PARAMETER_NAME = 36
        NO_GEOCODING_RESULT = 37
        SOURCE_NAME_IN_REVIEW_EXTENSION_TEXT = 38
        CARRIER_SPECIFIC_SHORT_NUMBER_NOT_ALLOWED = 39
        INVALID_PLACEHOLDER_FIELD_ID = 40
        INVALID_URL_TAG = 41
        LIST_TOO_LONG = 42
        INVALID_ATTRIBUTES_COMBINATION = 43
        DUPLICATE_VALUES = 44
        INVALID_CALL_CONVERSION_ACTION_ID = 45
        CANNOT_SET_WITHOUT_FINAL_URLS = 46
        APP_ID_DOESNT_EXIST_IN_APP_STORE = 47
        INVALID_FINAL_URL = 48
        INVALID_TRACKING_URL = 49
        INVALID_FINAL_URL_FOR_APP_DOWNLOAD_URL = 50
        LIST_TOO_SHORT = 51
        INVALID_USER_ACTION = 52
        INVALID_TYPE_NAME = 53
        INVALID_EVENT_CHANGE_STATUS = 54
        INVALID_SNIPPETS_HEADER = 55
        INVALID_ANDROID_APP_LINK = 56
        NUMBER_TYPE_WITH_CALLTRACKING_NOT_SUPPORTED_FOR_COUNTRY = 57
        RESERVED_KEYWORD_OTHER = 58
        DUPLICATE_OPTION_LABELS = 59
        DUPLICATE_OPTION_PREFILLS = 60
        UNEQUAL_LIST_LENGTHS = 61
        INCONSISTENT_CURRENCY_CODES = 62
        PRICE_EXTENSION_HAS_DUPLICATED_HEADERS = 63
        ITEM_HAS_DUPLICATED_HEADER_AND_DESCRIPTION = 64
        PRICE_EXTENSION_HAS_TOO_FEW_ITEMS = 65
        UNSUPPORTED_VALUE = 66
        INVALID_FINAL_MOBILE_URL = 67
        INVALID_KEYWORDLESS_AD_RULE_LABEL = 68
        VALUE_TRACK_PARAMETER_NOT_SUPPORTED = 69
        UNSUPPORTED_VALUE_IN_SELECTED_LANGUAGE = 70
        INVALID_IOS_APP_LINK = 71
        MISSING_IOS_APP_LINK_OR_IOS_APP_STORE_ID = 72
        PROMOTION_INVALID_TIME = 73
        PROMOTION_CANNOT_SET_PERCENT_OFF_AND_MONEY_AMOUNT_OFF = 74
        PROMOTION_CANNOT_SET_PROMOTION_CODE_AND_ORDERS_OVER_AMOUNT = 75
        TOO_MANY_DECIMAL_PLACES_SPECIFIED = 76
        AD_CUSTOMIZERS_NOT_ALLOWED = 77
        INVALID_LANGUAGE_CODE = 78
        UNSUPPORTED_LANGUAGE = 79
        IF_FUNCTION_NOT_ALLOWED = 80
        INVALID_FINAL_URL_SUFFIX = 81
        INVALID_TAG_IN_FINAL_URL_SUFFIX = 82
        INVALID_FINAL_URL_SUFFIX_FORMAT = 83
        CUSTOMER_CONSENT_FOR_CALL_RECORDING_REQUIRED = 84
        ONLY_ONE_DELIVERY_OPTION_IS_ALLOWED = 85
        NO_DELIVERY_OPTION_IS_SET = 86
        INVALID_CONVERSION_REPORTING_STATE = 87
        IMAGE_SIZE_WRONG = 88
        EMAIL_DELIVERY_NOT_AVAILABLE_IN_COUNTRY = 89
        AUTO_REPLY_NOT_AVAILABLE_IN_COUNTRY = 90
        INVALID_LATITUDE_VALUE = 91
        INVALID_LONGITUDE_VALUE = 92
        TOO_MANY_LABELS = 93
        INVALID_IMAGE_URL = 94
        MISSING_LATITUDE_VALUE = 95
        MISSING_LONGITUDE_VALUE = 96


class FeedItemValidationStatusEnum(object):
    class FeedItemValidationStatus(enum.IntEnum):
        """
        The possible validation statuses of a feed item.

        Attributes:
          UNSPECIFIED (int): No value has been specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          PENDING (int): Validation pending.
          INVALID (int): An error was found.
          VALID (int): Feed item is semantically well-formed.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        PENDING = 2
        INVALID = 3
        VALID = 4


class FeedLinkStatusEnum(object):
    class FeedLinkStatus(enum.IntEnum):
        """
        Possible statuses of a feed link.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          ENABLED (int): Feed link is enabled.
          REMOVED (int): Feed link has been removed.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        ENABLED = 2
        REMOVED = 3


class FeedMappingCriterionTypeEnum(object):
    class FeedMappingCriterionType(enum.IntEnum):
        """
        Possible placeholder types for a feed mapping.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          LOCATION_EXTENSION_TARGETING (int): Allows campaign targeting at locations within a location feed.
          DSA_PAGE_FEED (int): Allows url targeting for your dynamic search ads within a page feed.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        LOCATION_EXTENSION_TARGETING = 4
        DSA_PAGE_FEED = 3


class FeedMappingErrorEnum(object):
    class FeedMappingError(enum.IntEnum):
        """
        Enum describing possible feed item errors.

        Attributes:
          UNSPECIFIED (int): Enum unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          INVALID_PLACEHOLDER_FIELD (int): The given placeholder field does not exist.
          INVALID_CRITERION_FIELD (int): The given criterion field does not exist.
          INVALID_PLACEHOLDER_TYPE (int): The given placeholder type does not exist.
          INVALID_CRITERION_TYPE (int): The given criterion type does not exist.
          NO_ATTRIBUTE_FIELD_MAPPINGS (int): A feed mapping must contain at least one attribute field mapping.
          FEED_ATTRIBUTE_TYPE_MISMATCH (int): The type of the feed attribute referenced in the attribute field mapping
          must match the type of the placeholder field.
          CANNOT_OPERATE_ON_MAPPINGS_FOR_SYSTEM_GENERATED_FEED (int): A feed mapping for a system generated feed cannot be operated on.
          MULTIPLE_MAPPINGS_FOR_PLACEHOLDER_TYPE (int): Only one feed mapping for a placeholder type is allowed per feed or
          customer (depending on the placeholder type).
          MULTIPLE_MAPPINGS_FOR_CRITERION_TYPE (int): Only one feed mapping for a criterion type is allowed per customer.
          MULTIPLE_MAPPINGS_FOR_PLACEHOLDER_FIELD (int): Only one feed attribute mapping for a placeholder field is allowed
          (depending on the placeholder type).
          MULTIPLE_MAPPINGS_FOR_CRITERION_FIELD (int): Only one feed attribute mapping for a criterion field is allowed
          (depending on the criterion type).
          UNEXPECTED_ATTRIBUTE_FIELD_MAPPINGS (int): This feed mapping may not contain any explicit attribute field mappings.
          LOCATION_PLACEHOLDER_ONLY_FOR_PLACES_FEEDS (int): Location placeholder feed mappings can only be created for Places feeds.
          CANNOT_MODIFY_MAPPINGS_FOR_TYPED_FEED (int): Mappings for typed feeds cannot be modified.
          INVALID_PLACEHOLDER_TYPE_FOR_NON_SYSTEM_GENERATED_FEED (int): The given placeholder type can only be mapped to system generated feeds.
          INVALID_PLACEHOLDER_TYPE_FOR_SYSTEM_GENERATED_FEED_TYPE (int): The given placeholder type cannot be mapped to a system generated feed
          with the given type.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        INVALID_PLACEHOLDER_FIELD = 2
        INVALID_CRITERION_FIELD = 3
        INVALID_PLACEHOLDER_TYPE = 4
        INVALID_CRITERION_TYPE = 5
        NO_ATTRIBUTE_FIELD_MAPPINGS = 7
        FEED_ATTRIBUTE_TYPE_MISMATCH = 8
        CANNOT_OPERATE_ON_MAPPINGS_FOR_SYSTEM_GENERATED_FEED = 9
        MULTIPLE_MAPPINGS_FOR_PLACEHOLDER_TYPE = 10
        MULTIPLE_MAPPINGS_FOR_CRITERION_TYPE = 11
        MULTIPLE_MAPPINGS_FOR_PLACEHOLDER_FIELD = 12
        MULTIPLE_MAPPINGS_FOR_CRITERION_FIELD = 13
        UNEXPECTED_ATTRIBUTE_FIELD_MAPPINGS = 14
        LOCATION_PLACEHOLDER_ONLY_FOR_PLACES_FEEDS = 15
        CANNOT_MODIFY_MAPPINGS_FOR_TYPED_FEED = 16
        INVALID_PLACEHOLDER_TYPE_FOR_NON_SYSTEM_GENERATED_FEED = 17
        INVALID_PLACEHOLDER_TYPE_FOR_SYSTEM_GENERATED_FEED_TYPE = 18


class FeedMappingStatusEnum(object):
    class FeedMappingStatus(enum.IntEnum):
        """
        Possible statuses of a feed mapping.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          ENABLED (int): Feed mapping is enabled.
          REMOVED (int): Feed mapping has been removed.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        ENABLED = 2
        REMOVED = 3


class FeedOriginEnum(object):
    class FeedOrigin(enum.IntEnum):
        """
        Possible values for a feed origin.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          USER (int): The FeedAttributes for this Feed are managed by the
          user. Users can add FeedAttributes to this Feed.
          GOOGLE (int): The FeedAttributes for an GOOGLE Feed are created by Google. A feed of
          this type is maintained by Google and will have the correct attributes
          for the placeholder type of the feed.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        USER = 2
        GOOGLE = 3


class FeedStatusEnum(object):
    class FeedStatus(enum.IntEnum):
        """
        Possible statuses of a feed.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          ENABLED (int): Feed is enabled.
          REMOVED (int): Feed has been removed.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        ENABLED = 2
        REMOVED = 3


class FieldErrorEnum(object):
    class FieldError(enum.IntEnum):
        """
        Enum describing possible field errors.

        Attributes:
          UNSPECIFIED (int): Enum unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          REQUIRED (int): The required field was not present.
          IMMUTABLE_FIELD (int): The field attempted to be mutated is immutable.
          INVALID_VALUE (int): The field's value is invalid.
          VALUE_MUST_BE_UNSET (int): The field cannot be set.
          REQUIRED_NONEMPTY_LIST (int): The required repeated field was empty.
          FIELD_CANNOT_BE_CLEARED (int): The field cannot be cleared.
          BLACKLISTED_VALUE (int): The field's value is on a blacklist for this field.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        REQUIRED = 2
        IMMUTABLE_FIELD = 3
        INVALID_VALUE = 4
        VALUE_MUST_BE_UNSET = 5
        REQUIRED_NONEMPTY_LIST = 6
        FIELD_CANNOT_BE_CLEARED = 7
        BLACKLISTED_VALUE = 8


class FieldMaskErrorEnum(object):
    class FieldMaskError(enum.IntEnum):
        """
        Enum describing possible field mask errors.

        Attributes:
          UNSPECIFIED (int): Enum unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          FIELD_MASK_MISSING (int): The field mask must be provided for update operations.
          FIELD_MASK_NOT_ALLOWED (int): The field mask must be empty for create and remove operations.
          FIELD_NOT_FOUND (int): The field mask contained an invalid field.
          FIELD_HAS_SUBFIELDS (int): The field mask updated a field with subfields. Fields with subfields may
          be cleared, but not updated. To fix this, the field mask should select
          all the subfields of the invalid field.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        FIELD_MASK_MISSING = 5
        FIELD_MASK_NOT_ALLOWED = 4
        FIELD_NOT_FOUND = 2
        FIELD_HAS_SUBFIELDS = 3


class FlightPlaceholderFieldEnum(object):
    class FlightPlaceholderField(enum.IntEnum):
        """
        Possible values for Flight placeholder fields.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          DESTINATION_ID (int): Data Type: STRING. Required. Destination id. Example: PAR, LON.
          For feed items that only have destination id, destination id must be a
          unique key. For feed items that have both destination id and origin id,
          then the combination must be a unique key.
          ORIGIN_ID (int): Data Type: STRING. Origin id. Example: PAR, LON.
          Optional. Combination of destination id and origin id must be unique per
          offer.
          FLIGHT_DESCRIPTION (int): Data Type: STRING. Required. Main headline with product name to be shown
          in dynamic ad.
          ORIGIN_NAME (int): Data Type: STRING. Shorter names are recommended.
          DESTINATION_NAME (int): Data Type: STRING. Shorter names are recommended.
          FLIGHT_PRICE (int): Data Type: STRING. Price to be shown in the ad.
          Example: "100.00 USD"
          FORMATTED_PRICE (int): Data Type: STRING. Formatted price to be shown in the ad.
          Example: "Starting at $100.00 USD", "$80 - $100"
          FLIGHT_SALE_PRICE (int): Data Type: STRING. Sale price to be shown in the ad.
          Example: "80.00 USD"
          FORMATTED_SALE_PRICE (int): Data Type: STRING. Formatted sale price to be shown in the ad.
          Example: "On sale for $80.00", "$60 - $80"
          IMAGE_URL (int): Data Type: URL. Image to be displayed in the ad.
          FINAL_URLS (int): Data Type: URL\_LIST. Required. Final URLs for the ad when using
          Upgraded URLs. User will be redirected to these URLs when they click on
          an ad, or when they click on a specific flight for ads that show
          multiple flights.
          FINAL_MOBILE_URLS (int): Data Type: URL\_LIST. Final mobile URLs for the ad when using Upgraded
          URLs.
          TRACKING_URL (int): Data Type: URL. Tracking template for the ad when using Upgraded URLs.
          ANDROID_APP_LINK (int): Data Type: STRING. Android app link. Must be formatted as:
          android-app://{package\_id}/{scheme}/{host\_path}. The components are
          defined as follows: package\_id: app ID as specified in Google Play.
          scheme: the scheme to pass to the application. Can be HTTP, or a custom
          scheme. host\_path: identifies the specific content within your
          application.
          SIMILAR_DESTINATION_IDS (int): Data Type: STRING\_LIST. List of recommended destination IDs to show
          together with this item.
          IOS_APP_LINK (int): Data Type: STRING. iOS app link.
          IOS_APP_STORE_ID (int): Data Type: INT64. iOS app store ID.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        DESTINATION_ID = 2
        ORIGIN_ID = 3
        FLIGHT_DESCRIPTION = 4
        ORIGIN_NAME = 5
        DESTINATION_NAME = 6
        FLIGHT_PRICE = 7
        FORMATTED_PRICE = 8
        FLIGHT_SALE_PRICE = 9
        FORMATTED_SALE_PRICE = 10
        IMAGE_URL = 11
        FINAL_URLS = 12
        FINAL_MOBILE_URLS = 13
        TRACKING_URL = 14
        ANDROID_APP_LINK = 15
        SIMILAR_DESTINATION_IDS = 16
        IOS_APP_LINK = 17
        IOS_APP_STORE_ID = 18


class FrequencyCapEventTypeEnum(object):
    class FrequencyCapEventType(enum.IntEnum):
        """
        The type of event that the cap applies to (e.g. impression).

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          IMPRESSION (int): The cap applies on ad impressions.
          VIDEO_VIEW (int): The cap applies on video ad views.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        IMPRESSION = 2
        VIDEO_VIEW = 3


class FrequencyCapLevelEnum(object):
    class FrequencyCapLevel(enum.IntEnum):
        """
        The level on which the cap is to be applied (e.g ad group ad, ad group).
        Cap is applied to all the resources of this level.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          AD_GROUP_AD (int): The cap is applied at the ad group ad level.
          AD_GROUP (int): The cap is applied at the ad group level.
          CAMPAIGN (int): The cap is applied at the campaign level.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        AD_GROUP_AD = 2
        AD_GROUP = 3
        CAMPAIGN = 4


class FrequencyCapTimeUnitEnum(object):
    class FrequencyCapTimeUnit(enum.IntEnum):
        """
        Unit of time the cap is defined at (e.g. day, week).

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          DAY (int): The cap would define limit per one day.
          WEEK (int): The cap would define limit per one week.
          MONTH (int): The cap would define limit per one month.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        DAY = 2
        WEEK = 3
        MONTH = 4


class FunctionErrorEnum(object):
    class FunctionError(enum.IntEnum):
        """
        Enum describing possible function errors.

        Attributes:
          UNSPECIFIED (int): Enum unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          INVALID_FUNCTION_FORMAT (int): The format of the function is not recognized as a supported function
          format.
          DATA_TYPE_MISMATCH (int): Operand data types do not match.
          INVALID_CONJUNCTION_OPERANDS (int): The operands cannot be used together in a conjunction.
          INVALID_NUMBER_OF_OPERANDS (int): Invalid numer of Operands.
          INVALID_OPERAND_TYPE (int): Operand Type not supported.
          INVALID_OPERATOR (int): Operator not supported.
          INVALID_REQUEST_CONTEXT_TYPE (int): Request context type not supported.
          INVALID_FUNCTION_FOR_CALL_PLACEHOLDER (int): The matching function is not allowed for call placeholders
          INVALID_FUNCTION_FOR_PLACEHOLDER (int): The matching function is not allowed for the specified placeholder
          INVALID_OPERAND (int): Invalid operand.
          MISSING_CONSTANT_OPERAND_VALUE (int): Missing value for the constant operand.
          INVALID_CONSTANT_OPERAND_VALUE (int): The value of the constant operand is invalid.
          INVALID_NESTING (int): Invalid function nesting.
          MULTIPLE_FEED_IDS_NOT_SUPPORTED (int): The Feed ID was different from another Feed ID in the same function.
          INVALID_FUNCTION_FOR_FEED_WITH_FIXED_SCHEMA (int): The matching function is invalid for use with a feed with a fixed schema.
          INVALID_ATTRIBUTE_NAME (int): Invalid attribute name.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        INVALID_FUNCTION_FORMAT = 2
        DATA_TYPE_MISMATCH = 3
        INVALID_CONJUNCTION_OPERANDS = 4
        INVALID_NUMBER_OF_OPERANDS = 5
        INVALID_OPERAND_TYPE = 6
        INVALID_OPERATOR = 7
        INVALID_REQUEST_CONTEXT_TYPE = 8
        INVALID_FUNCTION_FOR_CALL_PLACEHOLDER = 9
        INVALID_FUNCTION_FOR_PLACEHOLDER = 10
        INVALID_OPERAND = 11
        MISSING_CONSTANT_OPERAND_VALUE = 12
        INVALID_CONSTANT_OPERAND_VALUE = 13
        INVALID_NESTING = 14
        MULTIPLE_FEED_IDS_NOT_SUPPORTED = 15
        INVALID_FUNCTION_FOR_FEED_WITH_FIXED_SCHEMA = 16
        INVALID_ATTRIBUTE_NAME = 17


class FunctionParsingErrorEnum(object):
    class FunctionParsingError(enum.IntEnum):
        """
        Enum describing possible function parsing errors.

        Attributes:
          UNSPECIFIED (int): Enum unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          NO_MORE_INPUT (int): Unexpected end of function string.
          EXPECTED_CHARACTER (int): Could not find an expected character.
          UNEXPECTED_SEPARATOR (int): Unexpected separator character.
          UNMATCHED_LEFT_BRACKET (int): Unmatched left bracket or parenthesis.
          UNMATCHED_RIGHT_BRACKET (int): Unmatched right bracket or parenthesis.
          TOO_MANY_NESTED_FUNCTIONS (int): Functions are nested too deeply.
          MISSING_RIGHT_HAND_OPERAND (int): Missing right-hand-side operand.
          INVALID_OPERATOR_NAME (int): Invalid operator/function name.
          FEED_ATTRIBUTE_OPERAND_ARGUMENT_NOT_INTEGER (int): Feed attribute operand's argument is not an integer.
          NO_OPERANDS (int): Missing function operands.
          TOO_MANY_OPERANDS (int): Function had too many operands.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        NO_MORE_INPUT = 2
        EXPECTED_CHARACTER = 3
        UNEXPECTED_SEPARATOR = 4
        UNMATCHED_LEFT_BRACKET = 5
        UNMATCHED_RIGHT_BRACKET = 6
        TOO_MANY_NESTED_FUNCTIONS = 7
        MISSING_RIGHT_HAND_OPERAND = 8
        INVALID_OPERATOR_NAME = 9
        FEED_ATTRIBUTE_OPERAND_ARGUMENT_NOT_INTEGER = 10
        NO_OPERANDS = 11
        TOO_MANY_OPERANDS = 12


class GenderTypeEnum(object):
    class GenderType(enum.IntEnum):
        """
        The type of demographic genders (e.g. female).

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          MALE (int): Male.
          FEMALE (int): Female.
          UNDETERMINED (int): Undetermined gender.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        MALE = 10
        FEMALE = 11
        UNDETERMINED = 20


class GeoTargetConstantStatusEnum(object):
    class GeoTargetConstantStatus(enum.IntEnum):
        """
        The possible statuses of a geo target constant.

        Attributes:
          UNSPECIFIED (int): No value has been specified.
          UNKNOWN (int): The received value is not known in this version.

          This is a response-only value.
          ENABLED (int): The geo target constant is valid.
          REMOVAL_PLANNED (int): The geo target constant is obsolete and will be removed.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        ENABLED = 2
        REMOVAL_PLANNED = 3


class GeoTargetConstantSuggestionErrorEnum(object):
    class GeoTargetConstantSuggestionError(enum.IntEnum):
        """
        Enum describing possible geo target constant suggestion errors.

        Attributes:
          UNSPECIFIED (int): Enum unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          LOCATION_NAME_SIZE_LIMIT (int): A location name cannot be greater than 300 characters.
          LOCATION_NAME_LIMIT (int): At most 25 location names can be specified in a SuggestGeoTargetConstants
          method.
          INVALID_COUNTRY_CODE (int): The country code is invalid.
          REQUEST_PARAMETERS_UNSET (int): Geo target constant resource names or location names must be provided in
          the request.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        LOCATION_NAME_SIZE_LIMIT = 2
        LOCATION_NAME_LIMIT = 3
        INVALID_COUNTRY_CODE = 4
        REQUEST_PARAMETERS_UNSET = 5


class GeoTargetingRestrictionEnum(object):
    class GeoTargetingRestriction(enum.IntEnum):
        """
        A restriction used to determine if the request context's
        geo should be matched.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          LOCATION_OF_PRESENCE (int): Indicates that request context should match the physical location of
          the user.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        LOCATION_OF_PRESENCE = 2


class GeoTargetingTypeEnum(object):
    class GeoTargetingType(enum.IntEnum):
        """
        The possible geo targeting types.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): The value is unknown in this version.
          AREA_OF_INTEREST (int): Location the user is interested in while making the query.
          LOCATION_OF_PRESENCE (int): Location of the user issuing the query.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        AREA_OF_INTEREST = 2
        LOCATION_OF_PRESENCE = 3


class GoogleAdsFieldCategoryEnum(object):
    class GoogleAdsFieldCategory(enum.IntEnum):
        """
        The category of the artifact.

        Attributes:
          UNSPECIFIED (int): Unspecified
          UNKNOWN (int): Unknown
          RESOURCE (int): The described artifact is a resource.
          ATTRIBUTE (int): The described artifact is a field and is an attribute of a resource.
          Including a resource attribute field in a query may segment the query if
          the resource to which it is attributed segments the resource found in
          the FROM clause.
          SEGMENT (int): The described artifact is a field and always segments search queries.
          METRIC (int): The described artifact is a field and is a metric. It never segments
          search queries.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        RESOURCE = 2
        ATTRIBUTE = 3
        SEGMENT = 5
        METRIC = 6


class GoogleAdsFieldDataTypeEnum(object):
    class GoogleAdsFieldDataType(enum.IntEnum):
        """
        These are the various types a GoogleAdsService artifact may take on.

        Attributes:
          UNSPECIFIED (int): Unspecified
          UNKNOWN (int): Unknown
          BOOLEAN (int): Maps to google.protobuf.BoolValue

          Applicable operators:  =, !=
          DATE (int): Maps to google.protobuf.StringValue. It can be compared using the set of
          operators specific to dates however.

          Applicable operators:  =, <, >, <=, >=, BETWEEN, DURING, and IN
          DOUBLE (int): Maps to google.protobuf.DoubleValue

          Applicable operators:  =, !=, <, >, IN, NOT IN
          ENUM (int): Maps to an enum. It's specific definition can be found at type\_url.

          Applicable operators: =, !=, IN, NOT IN
          FLOAT (int): Maps to google.protobuf.FloatValue

          Applicable operators:  =, !=, <, >, IN, NOT IN
          INT32 (int): Maps to google.protobuf.Int32Value

          Applicable operators:  =, !=, <, >, <=, >=, BETWEEN, IN, NOT IN
          INT64 (int): Maps to google.protobuf.Int64Value

          Applicable operators:  =, !=, <, >, <=, >=, BETWEEN, IN, NOT IN
          MESSAGE (int): Maps to a protocol buffer message type. The data type's details can be
          found in type\_url.

          No operators work with MESSAGE fields.
          RESOURCE_NAME (int): Maps to google.protobuf.StringValue. Represents the resource name
          (unique id) of a resource or one of its foreign keys.

          No operators work with RESOURCE\_NAME fields.
          STRING (int): Maps to google.protobuf.StringValue.

          Applicable operators:  =, !=, LIKE, NOT LIKE, IN, NOT IN
          UINT64 (int): Maps to google.protobuf.UInt64Value

          Applicable operators:  =, !=, <, >, <=, >=, BETWEEN, IN, NOT IN
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        BOOLEAN = 2
        DATE = 3
        DOUBLE = 4
        ENUM = 5
        FLOAT = 6
        INT32 = 7
        INT64 = 8
        MESSAGE = 9
        RESOURCE_NAME = 10
        STRING = 11
        UINT64 = 12


class HeaderErrorEnum(object):
    class HeaderError(enum.IntEnum):
        """
        Enum describing possible header errors.

        Attributes:
          UNSPECIFIED (int): Enum unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          INVALID_LOGIN_CUSTOMER_ID (int): The login customer id could not be validated.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        INVALID_LOGIN_CUSTOMER_ID = 3


class HotelDateSelectionTypeEnum(object):
    class HotelDateSelectionType(enum.IntEnum):
        """
        Enum describing possible hotel date selection types.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          DEFAULT_SELECTION (int): Dates selected by default.
          USER_SELECTED (int): Dates selected by the user.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        DEFAULT_SELECTION = 50
        USER_SELECTED = 51


class HotelPlaceholderFieldEnum(object):
    class HotelPlaceholderField(enum.IntEnum):
        """
        Possible values for Hotel placeholder fields.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          PROPERTY_ID (int): Data Type: STRING. Required. Unique ID.
          PROPERTY_NAME (int): Data Type: STRING. Required. Main headline with property name to be shown
          in dynamic ad.
          DESTINATION_NAME (int): Data Type: STRING. Name of destination to be shown in dynamic ad.
          DESCRIPTION (int): Data Type: STRING. Description of destination to be shown in dynamic ad.
          ADDRESS (int): Data Type: STRING. Complete property address, including postal code.
          PRICE (int): Data Type: STRING. Price to be shown in the ad.
          Example: "100.00 USD"
          FORMATTED_PRICE (int): Data Type: STRING. Formatted price to be shown in the ad.
          Example: "Starting at $100.00 USD", "$80 - $100"
          SALE_PRICE (int): Data Type: STRING. Sale price to be shown in the ad.
          Example: "80.00 USD"
          FORMATTED_SALE_PRICE (int): Data Type: STRING. Formatted sale price to be shown in the ad.
          Example: "On sale for $80.00", "$60 - $80"
          IMAGE_URL (int): Data Type: URL. Image to be displayed in the ad.
          CATEGORY (int): Data Type: STRING. Category of property used to group like items together
          for recommendation engine.
          STAR_RATING (int): Data Type: INT64. Star rating (1 to 5) used to group like items
          together for recommendation engine.
          CONTEXTUAL_KEYWORDS (int): Data Type: STRING\_LIST. Keywords used for product retrieval.
          FINAL_URLS (int): Data Type: URL\_LIST. Required. Final URLs for the ad when using
          Upgraded URLs. User will be redirected to these URLs when they click on
          an ad, or when they click on a specific flight for ads that show
          multiple flights.
          FINAL_MOBILE_URLS (int): Data Type: URL\_LIST. Final mobile URLs for the ad when using Upgraded
          URLs.
          TRACKING_URL (int): Data Type: URL. Tracking template for the ad when using Upgraded URLs.
          ANDROID_APP_LINK (int): Data Type: STRING. Android app link. Must be formatted as:
          android-app://{package\_id}/{scheme}/{host\_path}. The components are
          defined as follows: package\_id: app ID as specified in Google Play.
          scheme: the scheme to pass to the application. Can be HTTP, or a custom
          scheme. host\_path: identifies the specific content within your
          application.
          SIMILAR_PROPERTY_IDS (int): Data Type: STRING\_LIST. List of recommended property IDs to show
          together with this item.
          IOS_APP_LINK (int): Data Type: STRING. iOS app link.
          IOS_APP_STORE_ID (int): Data Type: INT64. iOS app store ID.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        PROPERTY_ID = 2
        PROPERTY_NAME = 3
        DESTINATION_NAME = 4
        DESCRIPTION = 5
        ADDRESS = 6
        PRICE = 7
        FORMATTED_PRICE = 8
        SALE_PRICE = 9
        FORMATTED_SALE_PRICE = 10
        IMAGE_URL = 11
        CATEGORY = 12
        STAR_RATING = 13
        CONTEXTUAL_KEYWORDS = 14
        FINAL_URLS = 15
        FINAL_MOBILE_URLS = 16
        TRACKING_URL = 17
        ANDROID_APP_LINK = 18
        SIMILAR_PROPERTY_IDS = 19
        IOS_APP_LINK = 20
        IOS_APP_STORE_ID = 21


class HotelRateTypeEnum(object):
    class HotelRateType(enum.IntEnum):
        """
        Enum describing possible hotel rate types.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): The value is unknown in this version.
          UNAVAILABLE (int): Rate type information is unavailable.
          PUBLIC_RATE (int): Rates available to everyone.
          QUALIFIED_RATE (int): A membership program rate is available and satisfies basic requirements
          like having a public rate available. UI treatment will strikethrough the
          public rate and indicate that a discount is available to the user. See
          https://developers.google.com/hotels/hotel-ads/dev-guide/qualified-rates
          for more information.
          PRIVATE_RATE (int): Rates available to users that satisfy some eligibility criteria. e.g.
          all signed-in users, 20% of mobile users, all mobile users in Canada,
          etc.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        UNAVAILABLE = 2
        PUBLIC_RATE = 3
        QUALIFIED_RATE = 4
        PRIVATE_RATE = 5


class IdErrorEnum(object):
    class IdError(enum.IntEnum):
        """
        Enum describing possible id errors.

        Attributes:
          UNSPECIFIED (int): Enum unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          NOT_FOUND (int): Id not found
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        NOT_FOUND = 2


class ImageErrorEnum(object):
    class ImageError(enum.IntEnum):
        """
        Enum describing possible image errors.

        Attributes:
          UNSPECIFIED (int): Enum unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          INVALID_IMAGE (int): The image is not valid.
          STORAGE_ERROR (int): The image could not be stored.
          BAD_REQUEST (int): There was a problem with the request.
          UNEXPECTED_SIZE (int): The image is not of legal dimensions.
          ANIMATED_NOT_ALLOWED (int): Animated image are not permitted.
          ANIMATION_TOO_LONG (int): Animation is too long.
          SERVER_ERROR (int): There was an error on the server.
          CMYK_JPEG_NOT_ALLOWED (int): Image cannot be in CMYK color format.
          FLASH_NOT_ALLOWED (int): Flash images are not permitted.
          FLASH_WITHOUT_CLICKTAG (int): Flash images must support clickTag.
          FLASH_ERROR_AFTER_FIXING_CLICK_TAG (int): A flash error has occurred after fixing the click tag.
          ANIMATED_VISUAL_EFFECT (int): Unacceptable visual effects.
          FLASH_ERROR (int): There was a problem with the flash image.
          LAYOUT_PROBLEM (int): Incorrect image layout.
          PROBLEM_READING_IMAGE_FILE (int): There was a problem reading the image file.
          ERROR_STORING_IMAGE (int): There was an error storing the image.
          ASPECT_RATIO_NOT_ALLOWED (int): The aspect ratio of the image is not allowed.
          FLASH_HAS_NETWORK_OBJECTS (int): Flash cannot have network objects.
          FLASH_HAS_NETWORK_METHODS (int): Flash cannot have network methods.
          FLASH_HAS_URL (int): Flash cannot have a Url.
          FLASH_HAS_MOUSE_TRACKING (int): Flash cannot use mouse tracking.
          FLASH_HAS_RANDOM_NUM (int): Flash cannot have a random number.
          FLASH_SELF_TARGETS (int): Ad click target cannot be '\_self'.
          FLASH_BAD_GETURL_TARGET (int): GetUrl method should only use '\_blank'.
          FLASH_VERSION_NOT_SUPPORTED (int): Flash version is not supported.
          FLASH_WITHOUT_HARD_CODED_CLICK_URL (int): Flash movies need to have hard coded click URL or clickTAG
          INVALID_FLASH_FILE (int): Uploaded flash file is corrupted.
          FAILED_TO_FIX_CLICK_TAG_IN_FLASH (int): Uploaded flash file can be parsed, but the click tag can not be fixed
          properly.
          FLASH_ACCESSES_NETWORK_RESOURCES (int): Flash movie accesses network resources
          FLASH_EXTERNAL_JS_CALL (int): Flash movie attempts to call external javascript code
          FLASH_EXTERNAL_FS_CALL (int): Flash movie attempts to call flash system commands
          FILE_TOO_LARGE (int): Image file is too large.
          IMAGE_DATA_TOO_LARGE (int): Image data is too large.
          IMAGE_PROCESSING_ERROR (int): Error while processing the image.
          IMAGE_TOO_SMALL (int): Image is too small.
          INVALID_INPUT (int): Input was invalid.
          PROBLEM_READING_FILE (int): There was a problem reading the image file.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        INVALID_IMAGE = 2
        STORAGE_ERROR = 3
        BAD_REQUEST = 4
        UNEXPECTED_SIZE = 5
        ANIMATED_NOT_ALLOWED = 6
        ANIMATION_TOO_LONG = 7
        SERVER_ERROR = 8
        CMYK_JPEG_NOT_ALLOWED = 9
        FLASH_NOT_ALLOWED = 10
        FLASH_WITHOUT_CLICKTAG = 11
        FLASH_ERROR_AFTER_FIXING_CLICK_TAG = 12
        ANIMATED_VISUAL_EFFECT = 13
        FLASH_ERROR = 14
        LAYOUT_PROBLEM = 15
        PROBLEM_READING_IMAGE_FILE = 16
        ERROR_STORING_IMAGE = 17
        ASPECT_RATIO_NOT_ALLOWED = 18
        FLASH_HAS_NETWORK_OBJECTS = 19
        FLASH_HAS_NETWORK_METHODS = 20
        FLASH_HAS_URL = 21
        FLASH_HAS_MOUSE_TRACKING = 22
        FLASH_HAS_RANDOM_NUM = 23
        FLASH_SELF_TARGETS = 24
        FLASH_BAD_GETURL_TARGET = 25
        FLASH_VERSION_NOT_SUPPORTED = 26
        FLASH_WITHOUT_HARD_CODED_CLICK_URL = 27
        INVALID_FLASH_FILE = 28
        FAILED_TO_FIX_CLICK_TAG_IN_FLASH = 29
        FLASH_ACCESSES_NETWORK_RESOURCES = 30
        FLASH_EXTERNAL_JS_CALL = 31
        FLASH_EXTERNAL_FS_CALL = 32
        FILE_TOO_LARGE = 33
        IMAGE_DATA_TOO_LARGE = 34
        IMAGE_PROCESSING_ERROR = 35
        IMAGE_TOO_SMALL = 36
        INVALID_INPUT = 37
        PROBLEM_READING_FILE = 38


class IncomeRangeTypeEnum(object):
    class IncomeRangeType(enum.IntEnum):
        """
        The type of demographic income ranges (e.g. between 0% to 50%).

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          INCOME_RANGE_0_50 (int): 0%-50%.
          INCOME_RANGE_50_60 (int): 50% to 60%.
          INCOME_RANGE_60_70 (int): 60% to 70%.
          INCOME_RANGE_70_80 (int): 70% to 80%.
          INCOME_RANGE_80_90 (int): 80% to 90%.
          INCOME_RANGE_90_UP (int): Greater than 90%.
          INCOME_RANGE_UNDETERMINED (int): Undetermined income range.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        INCOME_RANGE_0_50 = 510001
        INCOME_RANGE_50_60 = 510002
        INCOME_RANGE_60_70 = 510003
        INCOME_RANGE_70_80 = 510004
        INCOME_RANGE_80_90 = 510005
        INCOME_RANGE_90_UP = 510006
        INCOME_RANGE_UNDETERMINED = 510000


class InteractionEventTypeEnum(object):
    class InteractionEventType(enum.IntEnum):
        """
        Enum describing possible types of payable and free interactions.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          CLICK (int): Click to site. In most cases, this interaction navigates to an external
          location, usually the advertiser's landing page. This is also the default
          InteractionEventType for click events.
          ENGAGEMENT (int): The user's expressed intent to engage with the ad in-place.
          VIDEO_VIEW (int): User viewed a video ad.
          NONE (int): The default InteractionEventType for ad conversion events.
          This is used when an ad conversion row does NOT indicate
          that the free interactions (i.e., the ad conversions)
          should be 'promoted' and reported as part of the core metrics.
          These are simply other (ad) conversions.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        CLICK = 2
        ENGAGEMENT = 3
        VIDEO_VIEW = 4
        NONE = 5


class InteractionTypeEnum(object):
    class InteractionType(enum.IntEnum):
        """
        Enum describing possible interaction types.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          CALLS (int): Calls.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        CALLS = 8000


class InternalErrorEnum(object):
    class InternalError(enum.IntEnum):
        """
        Enum describing possible internal errors.

        Attributes:
          UNSPECIFIED (int): Enum unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          INTERNAL_ERROR (int): Google Ads API encountered unexpected internal error.
          ERROR_CODE_NOT_PUBLISHED (int): The intended error code doesn't exist in any API version. This will be
          fixed by adding a new error code as soon as possible.
          TRANSIENT_ERROR (int): Google Ads API encountered an unexpected transient error. The user
          should retry their request in these cases.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        INTERNAL_ERROR = 2
        ERROR_CODE_NOT_PUBLISHED = 3
        TRANSIENT_ERROR = 4


class JobPlaceholderFieldEnum(object):
    class JobPlaceholderField(enum.IntEnum):
        """
        Possible values for Job placeholder fields.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          JOB_ID (int): Data Type: STRING. Required. If only JOB\_ID is specified, then it must
          be unique. If both JOB\_ID and LOCATION\_ID are specified, then the pair
          must be unique. ID) pair must be unique.
          LOCATION_ID (int): Data Type: STRING. Combination of JOB\_ID and LOCATION\_ID must be
          unique per offer.
          TITLE (int): Data Type: STRING. Required. Main headline with job title to be shown in
          dynamic ad.
          SUBTITLE (int): Data Type: STRING. Job subtitle to be shown in dynamic ad.
          DESCRIPTION (int): Data Type: STRING. Description of job to be shown in dynamic ad.
          IMAGE_URL (int): Data Type: URL. Image to be displayed in the ad. Highly recommended for
          image ads.
          CATEGORY (int): Data Type: STRING. Category of property used to group like items together
          for recommendation engine.
          CONTEXTUAL_KEYWORDS (int): Data Type: STRING\_LIST. Keywords used for product retrieval.
          ADDRESS (int): Data Type: STRING. Complete property address, including postal code.
          SALARY (int): Data Type: STRING. Salary or salary range of job to be shown in dynamic
          ad.
          FINAL_URLS (int): Data Type: URL\_LIST. Required. Final URLs to be used in ad when using
          Upgraded URLs; the more specific the better (e.g. the individual URL of
          a specific job and its location).
          FINAL_MOBILE_URLS (int): Data Type: URL\_LIST. Final mobile URLs for the ad when using Upgraded
          URLs.
          TRACKING_URL (int): Data Type: URL. Tracking template for the ad when using Upgraded URLs.
          ANDROID_APP_LINK (int): Data Type: STRING. Android app link. Must be formatted as:
          android-app://{package\_id}/{scheme}/{host\_path}. The components are
          defined as follows: package\_id: app ID as specified in Google Play.
          scheme: the scheme to pass to the application. Can be HTTP, or a custom
          scheme. host\_path: identifies the specific content within your
          application.
          SIMILAR_JOB_IDS (int): Data Type: STRING\_LIST. List of recommended job IDs to show together
          with this item.
          IOS_APP_LINK (int): Data Type: STRING. iOS app link.
          IOS_APP_STORE_ID (int): Data Type: INT64. iOS app store ID.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        JOB_ID = 2
        LOCATION_ID = 3
        TITLE = 4
        SUBTITLE = 5
        DESCRIPTION = 6
        IMAGE_URL = 7
        CATEGORY = 8
        CONTEXTUAL_KEYWORDS = 9
        ADDRESS = 10
        SALARY = 11
        FINAL_URLS = 12
        FINAL_MOBILE_URLS = 14
        TRACKING_URL = 15
        ANDROID_APP_LINK = 16
        SIMILAR_JOB_IDS = 17
        IOS_APP_LINK = 18
        IOS_APP_STORE_ID = 19


class KeywordMatchTypeEnum(object):
    class KeywordMatchType(enum.IntEnum):
        """
        Possible Keyword match types.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          EXACT (int): Exact match.
          PHRASE (int): Phrase match.
          BROAD (int): Broad match.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        EXACT = 2
        PHRASE = 3
        BROAD = 4


class KeywordPlanAdGroupErrorEnum(object):
    class KeywordPlanAdGroupError(enum.IntEnum):
        """
        Enum describing possible errors from applying a keyword plan ad group.

        Attributes:
          UNSPECIFIED (int): Enum unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          INVALID_NAME (int): The keyword plan ad group name is missing, empty, longer than allowed
          limit or contains invalid chars.
          DUPLICATE_NAME (int): The keyword plan ad group name is duplicate to an existing keyword plan
          AdGroup name or other keyword plan AdGroup name in the request.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        INVALID_NAME = 2
        DUPLICATE_NAME = 3


class KeywordPlanCampaignErrorEnum(object):
    class KeywordPlanCampaignError(enum.IntEnum):
        """
        Enum describing possible errors from applying a keyword plan campaign.

        Attributes:
          UNSPECIFIED (int): Enum unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          INVALID_NAME (int): A keyword plan campaign name is missing, empty, longer than allowed limit
          or contains invalid chars.
          INVALID_LANGUAGES (int): A keyword plan campaign contains one or more untargetable languages.
          INVALID_GEOS (int): A keyword plan campaign contains one or more invalid geo targets.
          DUPLICATE_NAME (int): The keyword plan campaign name is duplicate to an existing keyword plan
          campaign name or other keyword plan campaign name in the request.
          MAX_GEOS_EXCEEDED (int): The number of geo targets in the keyword plan campaign exceeds limits.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        INVALID_NAME = 2
        INVALID_LANGUAGES = 3
        INVALID_GEOS = 4
        DUPLICATE_NAME = 5
        MAX_GEOS_EXCEEDED = 6


class KeywordPlanCompetitionLevelEnum(object):
    class KeywordPlanCompetitionLevel(enum.IntEnum):
        """
        Competition level of a keyword.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): The value is unknown in this version.
          LOW (int): Low competition.
          MEDIUM (int): Medium competition.
          HIGH (int): High competition.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        LOW = 2
        MEDIUM = 3
        HIGH = 4


class KeywordPlanErrorEnum(object):
    class KeywordPlanError(enum.IntEnum):
        """
        Enum describing possible errors from applying a keyword plan.

        Attributes:
          UNSPECIFIED (int): Enum unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          BID_MULTIPLIER_OUT_OF_RANGE (int): The plan's bid multiplier value is outside the valid range.
          BID_TOO_HIGH (int): The plan's bid value is too high.
          BID_TOO_LOW (int): The plan's bid value is too low.
          BID_TOO_MANY_FRACTIONAL_DIGITS (int): The plan's cpc bid is not a multiple of the minimum billable unit.
          DAILY_BUDGET_TOO_LOW (int): The plan's daily budget value is too low.
          DAILY_BUDGET_TOO_MANY_FRACTIONAL_DIGITS (int): The plan's daily budget is not a multiple of the minimum billable unit.
          INVALID_VALUE (int): The input has an invalid value.
          KEYWORD_PLAN_HAS_NO_KEYWORDS (int): The plan has no keyword.
          KEYWORD_PLAN_NOT_ENABLED (int): The plan is not enabled and API cannot provide mutation, forecast or
          stats.
          KEYWORD_PLAN_NOT_FOUND (int): The requested plan cannot be found for providing forecast or stats.
          MISSING_BID (int): The plan is missing a cpc bid.
          MISSING_FORECAST_PERIOD (int): The plan is missing required forecast\_period field.
          INVALID_FORECAST_DATE_RANGE (int): The plan's forecast\_period has invalid forecast date range.
          INVALID_NAME (int): The plan's name is invalid.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        BID_MULTIPLIER_OUT_OF_RANGE = 2
        BID_TOO_HIGH = 3
        BID_TOO_LOW = 4
        BID_TOO_MANY_FRACTIONAL_DIGITS = 5
        DAILY_BUDGET_TOO_LOW = 6
        DAILY_BUDGET_TOO_MANY_FRACTIONAL_DIGITS = 7
        INVALID_VALUE = 8
        KEYWORD_PLAN_HAS_NO_KEYWORDS = 9
        KEYWORD_PLAN_NOT_ENABLED = 10
        KEYWORD_PLAN_NOT_FOUND = 11
        MISSING_BID = 13
        MISSING_FORECAST_PERIOD = 14
        INVALID_FORECAST_DATE_RANGE = 15
        INVALID_NAME = 16


class KeywordPlanForecastIntervalEnum(object):
    class KeywordPlanForecastInterval(enum.IntEnum):
        """
        Forecast intervals.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): The value is unknown in this version.
          NEXT_WEEK (int): The next week date range for keyword plan. The next week is based
          on the default locale of the user's account and is mostly SUN-SAT or
          MON-SUN.
          This can be different from next-7 days.
          NEXT_MONTH (int): The next month date range for keyword plan.
          NEXT_QUARTER (int): The next quarter date range for keyword plan.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        NEXT_WEEK = 3
        NEXT_MONTH = 4
        NEXT_QUARTER = 5


class KeywordPlanIdeaErrorEnum(object):
    class KeywordPlanIdeaError(enum.IntEnum):
        """
        Enum describing possible errors from KeywordPlanIdeaService.

        Attributes:
          UNSPECIFIED (int): Enum unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          URL_CRAWL_ERROR (int): Error when crawling the input URL.
          INVALID_VALUE (int): The input has an invalid value.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        URL_CRAWL_ERROR = 2
        INVALID_VALUE = 3


class KeywordPlanKeywordErrorEnum(object):
    class KeywordPlanKeywordError(enum.IntEnum):
        """
        Enum describing possible errors from applying a keyword plan keyword.

        Attributes:
          UNSPECIFIED (int): Enum unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          INVALID_KEYWORD_MATCH_TYPE (int): A keyword or negative keyword has invalid match type.
          DUPLICATE_KEYWORD (int): A keyword or negative keyword with same text and match type already
          exists.
          KEYWORD_TEXT_TOO_LONG (int): Keyword or negative keyword text exceeds the allowed limit.
          KEYWORD_HAS_INVALID_CHARS (int): Keyword or negative keyword text has invalid characters or symbols.
          KEYWORD_HAS_TOO_MANY_WORDS (int): Keyword or negative keyword text has too many words.
          INVALID_KEYWORD_TEXT (int): Keyword or negative keyword has invalid text.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        INVALID_KEYWORD_MATCH_TYPE = 2
        DUPLICATE_KEYWORD = 3
        KEYWORD_TEXT_TOO_LONG = 4
        KEYWORD_HAS_INVALID_CHARS = 5
        KEYWORD_HAS_TOO_MANY_WORDS = 6
        INVALID_KEYWORD_TEXT = 7


class KeywordPlanNegativeKeywordErrorEnum(object):
    class KeywordPlanNegativeKeywordError(enum.IntEnum):
        """
        Enum describing possible errors from applying a keyword plan negative
        keyword.

        Attributes:
          UNSPECIFIED (int): Enum unspecified.
          UNKNOWN (int): The received error code is not known in this version.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1


class KeywordPlanNetworkEnum(object):
    class KeywordPlanNetwork(enum.IntEnum):
        """
        Enumerates keyword plan forecastable network types.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): The value is unknown in this version.
          GOOGLE_SEARCH (int): Google Search.
          GOOGLE_SEARCH_AND_PARTNERS (int): Google Search + Search partners.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        GOOGLE_SEARCH = 2
        GOOGLE_SEARCH_AND_PARTNERS = 3


class LabelErrorEnum(object):
    class LabelError(enum.IntEnum):
        """
        Enum describing possible label errors.

        Attributes:
          UNSPECIFIED (int): Enum unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          CANNOT_APPLY_INACTIVE_LABEL (int): An inactive label cannot be applied.
          CANNOT_APPLY_LABEL_TO_DISABLED_AD_GROUP_CRITERION (int): A label cannot be applied to a disabled ad group criterion.
          CANNOT_APPLY_LABEL_TO_NEGATIVE_AD_GROUP_CRITERION (int): A label cannot be applied to a negative ad group criterion.
          EXCEEDED_LABEL_LIMIT_PER_TYPE (int): Cannot apply more than 50 labels per resource.
          INVALID_RESOURCE_FOR_MANAGER_LABEL (int): Labels from a manager account cannot be applied to campaign, ad group,
          ad group ad, or ad group criterion resources.
          DUPLICATE_NAME (int): Label names must be unique.
          INVALID_LABEL_NAME (int): Label names cannot be empty.
          CANNOT_ATTACH_LABEL_TO_DRAFT (int): Labels cannot be applied to a draft.
          CANNOT_ATTACH_NON_MANAGER_LABEL_TO_CUSTOMER (int): Labels not from a manager account cannot be applied to the customer
          resource.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        CANNOT_APPLY_INACTIVE_LABEL = 2
        CANNOT_APPLY_LABEL_TO_DISABLED_AD_GROUP_CRITERION = 3
        CANNOT_APPLY_LABEL_TO_NEGATIVE_AD_GROUP_CRITERION = 4
        EXCEEDED_LABEL_LIMIT_PER_TYPE = 5
        INVALID_RESOURCE_FOR_MANAGER_LABEL = 6
        DUPLICATE_NAME = 7
        INVALID_LABEL_NAME = 8
        CANNOT_ATTACH_LABEL_TO_DRAFT = 9
        CANNOT_ATTACH_NON_MANAGER_LABEL_TO_CUSTOMER = 10


class LabelStatusEnum(object):
    class LabelStatus(enum.IntEnum):
        """
        Possible statuses of a label.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          ENABLED (int): Label is enabled.
          REMOVED (int): Label is removed.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        ENABLED = 2
        REMOVED = 3


class LanguageCodeErrorEnum(object):
    class LanguageCodeError(enum.IntEnum):
        """
        Enum describing language code errors.

        Attributes:
          UNSPECIFIED (int): Enum unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          LANGUAGE_CODE_NOT_FOUND (int): The input language code is not recognized.
          INVALID_LANGUAGE_CODE (int): The language is not allowed to use.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        LANGUAGE_CODE_NOT_FOUND = 2
        INVALID_LANGUAGE_CODE = 3


class LegacyAppInstallAdAppStoreEnum(object):
    class LegacyAppInstallAdAppStore(enum.IntEnum):
        """
        App store type in a legacy app install ad.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          APPLE_APP_STORE (int): Apple iTunes.
          GOOGLE_PLAY (int): Google Play.
          WINDOWS_STORE (int): Windows Store.
          WINDOWS_PHONE_STORE (int): Windows Phone Store.
          CN_APP_STORE (int): The app is hosted in a Chinese app store.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        APPLE_APP_STORE = 2
        GOOGLE_PLAY = 3
        WINDOWS_STORE = 4
        WINDOWS_PHONE_STORE = 5
        CN_APP_STORE = 6


class ListOperationErrorEnum(object):
    class ListOperationError(enum.IntEnum):
        """
        Enum describing possible list operation errors.

        Attributes:
          UNSPECIFIED (int): Enum unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          REQUIRED_FIELD_MISSING (int): Field required in value is missing.
          DUPLICATE_VALUES (int): Duplicate or identical value is sent in multiple list operations.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        REQUIRED_FIELD_MISSING = 7
        DUPLICATE_VALUES = 8


class ListingCustomAttributeIndexEnum(object):
    class ListingCustomAttributeIndex(enum.IntEnum):
        """
        The index of the listing custom attribute.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          INDEX0 (int): First listing custom attribute.
          INDEX1 (int): Second listing custom attribute.
          INDEX2 (int): Third listing custom attribute.
          INDEX3 (int): Fourth listing custom attribute.
          INDEX4 (int): Fifth listing custom attribute.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        INDEX0 = 7
        INDEX1 = 8
        INDEX2 = 9
        INDEX3 = 10
        INDEX4 = 11


class ListingGroupTypeEnum(object):
    class ListingGroupType(enum.IntEnum):
        """
        The type of the listing group.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          SUBDIVISION (int): Subdivision of products along some listing dimension. These nodes
          are not used by serving to target listing entries, but is purely
          to define the structure of the tree.
          UNIT (int): Listing group unit that defines a bid.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        SUBDIVISION = 2
        UNIT = 3


class LocalPlaceholderFieldEnum(object):
    class LocalPlaceholderField(enum.IntEnum):
        """
        Possible values for Local placeholder fields.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          DEAL_ID (int): Data Type: STRING. Required. Unique ID.
          DEAL_NAME (int): Data Type: STRING. Required. Main headline with local deal title to be
          shown in dynamic ad.
          SUBTITLE (int): Data Type: STRING. Local deal subtitle to be shown in dynamic ad.
          DESCRIPTION (int): Data Type: STRING. Description of local deal to be shown in dynamic ad.
          PRICE (int): Data Type: STRING. Price to be shown in the ad. Highly recommended for
          dynamic ads. Example: "100.00 USD"
          FORMATTED_PRICE (int): Data Type: STRING. Formatted price to be shown in the ad.
          Example: "Starting at $100.00 USD", "$80 - $100"
          SALE_PRICE (int): Data Type: STRING. Sale price to be shown in the ad.
          Example: "80.00 USD"
          FORMATTED_SALE_PRICE (int): Data Type: STRING. Formatted sale price to be shown in the ad.
          Example: "On sale for $80.00", "$60 - $80"
          IMAGE_URL (int): Data Type: URL. Image to be displayed in the ad.
          ADDRESS (int): Data Type: STRING. Complete property address, including postal code.
          CATEGORY (int): Data Type: STRING. Category of local deal used to group like items
          together for recommendation engine.
          CONTEXTUAL_KEYWORDS (int): Data Type: STRING\_LIST. Keywords used for product retrieval.
          FINAL_URLS (int): Data Type: URL\_LIST. Required. Final URLs to be used in ad when using
          Upgraded URLs; the more specific the better (e.g. the individual URL of
          a specific local deal and its location).
          FINAL_MOBILE_URLS (int): Data Type: URL\_LIST. Final mobile URLs for the ad when using Upgraded
          URLs.
          TRACKING_URL (int): Data Type: URL. Tracking template for the ad when using Upgraded URLs.
          ANDROID_APP_LINK (int): Data Type: STRING. Android app link. Must be formatted as:
          android-app://{package\_id}/{scheme}/{host\_path}. The components are
          defined as follows: package\_id: app ID as specified in Google Play.
          scheme: the scheme to pass to the application. Can be HTTP, or a custom
          scheme. host\_path: identifies the specific content within your
          application.
          SIMILAR_DEAL_IDS (int): Data Type: STRING\_LIST. List of recommended local deal IDs to show
          together with this item.
          IOS_APP_LINK (int): Data Type: STRING. iOS app link.
          IOS_APP_STORE_ID (int): Data Type: INT64. iOS app store ID.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        DEAL_ID = 2
        DEAL_NAME = 3
        SUBTITLE = 4
        DESCRIPTION = 5
        PRICE = 6
        FORMATTED_PRICE = 7
        SALE_PRICE = 8
        FORMATTED_SALE_PRICE = 9
        IMAGE_URL = 10
        ADDRESS = 11
        CATEGORY = 12
        CONTEXTUAL_KEYWORDS = 13
        FINAL_URLS = 14
        FINAL_MOBILE_URLS = 15
        TRACKING_URL = 16
        ANDROID_APP_LINK = 17
        SIMILAR_DEAL_IDS = 18
        IOS_APP_LINK = 19
        IOS_APP_STORE_ID = 20


class LocationExtensionTargetingCriterionFieldEnum(object):
    class LocationExtensionTargetingCriterionField(enum.IntEnum):
        """
        Possible values for Location Extension Targeting criterion fields.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          ADDRESS_LINE_1 (int): Data Type: STRING. Line 1 of the business address.
          ADDRESS_LINE_2 (int): Data Type: STRING. Line 2 of the business address.
          CITY (int): Data Type: STRING. City of the business address.
          PROVINCE (int): Data Type: STRING. Province of the business address.
          POSTAL_CODE (int): Data Type: STRING. Postal code of the business address.
          COUNTRY_CODE (int): Data Type: STRING. Country code of the business address.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        ADDRESS_LINE_1 = 2
        ADDRESS_LINE_2 = 3
        CITY = 4
        PROVINCE = 5
        POSTAL_CODE = 6
        COUNTRY_CODE = 7


class LocationGroupRadiusUnitsEnum(object):
    class LocationGroupRadiusUnits(enum.IntEnum):
        """
        The unit of radius distance in location group (e.g. MILES)

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          METERS (int): Meters
          MILES (int): Miles
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        METERS = 2
        MILES = 3


class LocationPlaceholderFieldEnum(object):
    class LocationPlaceholderField(enum.IntEnum):
        """
        Possible values for Location placeholder fields.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          BUSINESS_NAME (int): Data Type: STRING. The name of the business.
          ADDRESS_LINE_1 (int): Data Type: STRING. Line 1 of the business address.
          ADDRESS_LINE_2 (int): Data Type: STRING. Line 2 of the business address.
          CITY (int): Data Type: STRING. City of the business address.
          PROVINCE (int): Data Type: STRING. Province of the business address.
          POSTAL_CODE (int): Data Type: STRING. Postal code of the business address.
          COUNTRY_CODE (int): Data Type: STRING. Country code of the business address.
          PHONE_NUMBER (int): Data Type: STRING. Phone number of the business.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        BUSINESS_NAME = 2
        ADDRESS_LINE_1 = 3
        ADDRESS_LINE_2 = 4
        CITY = 5
        PROVINCE = 6
        POSTAL_CODE = 7
        COUNTRY_CODE = 8
        PHONE_NUMBER = 9


class ManagerLinkErrorEnum(object):
    class ManagerLinkError(enum.IntEnum):
        """
        Enum describing possible ManagerLink errors.

        Attributes:
          UNSPECIFIED (int): Enum unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          ACCOUNTS_NOT_COMPATIBLE_FOR_LINKING (int): The manager and client have incompatible account types.
          TOO_MANY_MANAGERS (int): Client is already linked to too many managers.
          TOO_MANY_INVITES (int): Manager has too many pending invitations.
          ALREADY_INVITED_BY_THIS_MANAGER (int): Client is already invited by this manager.
          ALREADY_MANAGED_BY_THIS_MANAGER (int): The client is already managed by this manager.
          ALREADY_MANAGED_IN_HIERARCHY (int): Client is already managed in hierarchy.
          DUPLICATE_CHILD_FOUND (int): Manger and sub-manager to be linked have duplicate client.
          CLIENT_HAS_NO_ADMIN_USER (int): Client has no active user that can access the client account.
          MAX_DEPTH_EXCEEDED (int): Adding this link would exceed the maximum hierarchy depth.
          CYCLE_NOT_ALLOWED (int): Adding this link will create a cycle.
          TOO_MANY_ACCOUNTS (int): Manager account has the maximum number of linked clients.
          TOO_MANY_ACCOUNTS_AT_MANAGER (int): Parent manager account has the maximum number of linked clients.
          NON_OWNER_USER_CANNOT_MODIFY_LINK (int): The account is not authorized owner.
          SUSPENDED_ACCOUNT_CANNOT_ADD_CLIENTS (int): Your manager account is suspended, and you are no longer allowed to link
          to clients.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        ACCOUNTS_NOT_COMPATIBLE_FOR_LINKING = 2
        TOO_MANY_MANAGERS = 3
        TOO_MANY_INVITES = 4
        ALREADY_INVITED_BY_THIS_MANAGER = 5
        ALREADY_MANAGED_BY_THIS_MANAGER = 6
        ALREADY_MANAGED_IN_HIERARCHY = 7
        DUPLICATE_CHILD_FOUND = 8
        CLIENT_HAS_NO_ADMIN_USER = 9
        MAX_DEPTH_EXCEEDED = 10
        CYCLE_NOT_ALLOWED = 11
        TOO_MANY_ACCOUNTS = 12
        TOO_MANY_ACCOUNTS_AT_MANAGER = 13
        NON_OWNER_USER_CANNOT_MODIFY_LINK = 14
        SUSPENDED_ACCOUNT_CANNOT_ADD_CLIENTS = 15


class ManagerLinkStatusEnum(object):
    class ManagerLinkStatus(enum.IntEnum):
        """
        Possible statuses of a link.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          ACTIVE (int): Indicates current in-effect relationship
          INACTIVE (int): Indicates terminated relationship
          PENDING (int): Indicates relationship has been requested by manager, but the client
          hasn't accepted yet.
          REFUSED (int): Relationship was requested by the manager, but the client has refused.
          CANCELED (int): Indicates relationship has been requested by manager, but manager
          canceled it.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        ACTIVE = 2
        INACTIVE = 3
        PENDING = 4
        REFUSED = 5
        CANCELED = 6


class MatchingFunctionContextTypeEnum(object):
    class MatchingFunctionContextType(enum.IntEnum):
        """
        Possible context types for an operand in a matching function.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          FEED_ITEM_ID (int): Feed item id in the request context.
          DEVICE_NAME (int): The device being used (possible values are 'Desktop' or 'Mobile').
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        FEED_ITEM_ID = 2
        DEVICE_NAME = 3


class MatchingFunctionOperatorEnum(object):
    class MatchingFunctionOperator(enum.IntEnum):
        """
        Possible operators in a matching function.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          IN (int): The IN operator.
          IDENTITY (int): The IDENTITY operator.
          EQUALS (int): The EQUALS operator
          AND (int): Operator that takes two or more operands that are of type
          FunctionOperand and checks that all the operands evaluate to true. For
          functions related to ad formats, all the operands must be in
          left\_operands.
          CONTAINS_ANY (int): Operator that returns true if the elements in left\_operands contain any
          of the elements in right\_operands. Otherwise, return false. The
          right\_operands must contain at least 1 and no more than 3
          ConstantOperands.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        IN = 2
        IDENTITY = 3
        EQUALS = 4
        AND = 5
        CONTAINS_ANY = 6


class MediaBundleErrorEnum(object):
    class MediaBundleError(enum.IntEnum):
        """
        Enum describing possible media bundle errors.

        Attributes:
          UNSPECIFIED (int): Enum unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          BAD_REQUEST (int): There was a problem with the request.
          DOUBLECLICK_BUNDLE_NOT_ALLOWED (int): HTML5 ads using DoubleClick Studio created ZIP files are not supported.
          EXTERNAL_URL_NOT_ALLOWED (int): Cannot reference URL external to the media bundle.
          FILE_TOO_LARGE (int): Media bundle file is too large.
          GOOGLE_WEB_DESIGNER_ZIP_FILE_NOT_PUBLISHED (int): ZIP file from Google Web Designer is not published.
          INVALID_INPUT (int): Input was invalid.
          INVALID_MEDIA_BUNDLE (int): There was a problem with the media bundle.
          INVALID_MEDIA_BUNDLE_ENTRY (int): There was a problem with one or more of the media bundle entries.
          INVALID_MIME_TYPE (int): The media bundle contains a file with an unknown mime type
          INVALID_PATH (int): The media bundle contain an invalid asset path.
          INVALID_URL_REFERENCE (int): HTML5 ad is trying to reference an asset not in .ZIP file
          MEDIA_DATA_TOO_LARGE (int): Media data is too large.
          MISSING_PRIMARY_MEDIA_BUNDLE_ENTRY (int): The media bundle contains no primary entry.
          SERVER_ERROR (int): There was an error on the server.
          STORAGE_ERROR (int): The image could not be stored.
          SWIFFY_BUNDLE_NOT_ALLOWED (int): Media bundle created with the Swiffy tool is not allowed.
          TOO_MANY_FILES (int): The media bundle contains too many files.
          UNEXPECTED_SIZE (int): The media bundle is not of legal dimensions.
          UNSUPPORTED_GOOGLE_WEB_DESIGNER_ENVIRONMENT (int): Google Web Designer not created for "Google Ads" environment.
          UNSUPPORTED_HTML5_FEATURE (int): Unsupported HTML5 feature in HTML5 asset.
          URL_IN_MEDIA_BUNDLE_NOT_SSL_COMPLIANT (int): URL in HTML5 entry is not ssl compliant.
          CUSTOM_EXIT_NOT_ALLOWED (int): Custom exits not allowed in HTML5 entry.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        BAD_REQUEST = 3
        DOUBLECLICK_BUNDLE_NOT_ALLOWED = 4
        EXTERNAL_URL_NOT_ALLOWED = 5
        FILE_TOO_LARGE = 6
        GOOGLE_WEB_DESIGNER_ZIP_FILE_NOT_PUBLISHED = 7
        INVALID_INPUT = 8
        INVALID_MEDIA_BUNDLE = 9
        INVALID_MEDIA_BUNDLE_ENTRY = 10
        INVALID_MIME_TYPE = 11
        INVALID_PATH = 12
        INVALID_URL_REFERENCE = 13
        MEDIA_DATA_TOO_LARGE = 14
        MISSING_PRIMARY_MEDIA_BUNDLE_ENTRY = 15
        SERVER_ERROR = 16
        STORAGE_ERROR = 17
        SWIFFY_BUNDLE_NOT_ALLOWED = 18
        TOO_MANY_FILES = 19
        UNEXPECTED_SIZE = 20
        UNSUPPORTED_GOOGLE_WEB_DESIGNER_ENVIRONMENT = 21
        UNSUPPORTED_HTML5_FEATURE = 22
        URL_IN_MEDIA_BUNDLE_NOT_SSL_COMPLIANT = 23
        CUSTOM_EXIT_NOT_ALLOWED = 24


class MediaFileErrorEnum(object):
    class MediaFileError(enum.IntEnum):
        """
        Enum describing possible media file errors.

        Attributes:
          UNSPECIFIED (int): Enum unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          CANNOT_CREATE_STANDARD_ICON (int): Cannot create a standard icon type.
          CANNOT_SELECT_STANDARD_ICON_WITH_OTHER_TYPES (int): May only select Standard Icons alone.
          CANNOT_SPECIFY_MEDIA_FILE_ID_AND_DATA (int): Image contains both a media file ID and data.
          DUPLICATE_MEDIA (int): A media file with given type and reference ID already exists.
          EMPTY_FIELD (int): A required field was not specified or is an empty string.
          RESOURCE_REFERENCED_IN_MULTIPLE_OPS (int): A media file may only be modified once per call.
          FIELD_NOT_SUPPORTED_FOR_MEDIA_SUB_TYPE (int): Field is not supported for the media sub type.
          INVALID_MEDIA_FILE_ID (int): The media file ID is invalid.
          INVALID_MEDIA_SUB_TYPE (int): The media subtype is invalid.
          INVALID_MEDIA_FILE_TYPE (int): The media file type is invalid.
          INVALID_MIME_TYPE (int): The mimetype is invalid.
          INVALID_REFERENCE_ID (int): The media reference ID is invalid.
          INVALID_YOU_TUBE_ID (int): The YouTube video ID is invalid.
          MEDIA_FILE_FAILED_TRANSCODING (int): Media file has failed transcoding
          MEDIA_NOT_TRANSCODED (int): Media file has not been transcoded.
          MEDIA_TYPE_DOES_NOT_MATCH_MEDIA_FILE_TYPE (int): The media type does not match the actual media file's type.
          NO_FIELDS_SPECIFIED (int): None of the fields have been specified.
          NULL_REFERENCE_ID_AND_MEDIA_ID (int): One of reference ID or media file ID must be specified.
          TOO_LONG (int): The string has too many characters.
          UNSUPPORTED_TYPE (int): The specified type is not supported.
          YOU_TUBE_SERVICE_UNAVAILABLE (int): YouTube is unavailable for requesting video data.
          YOU_TUBE_VIDEO_HAS_NON_POSITIVE_DURATION (int): The YouTube video has a non positive duration.
          YOU_TUBE_VIDEO_NOT_FOUND (int): The YouTube video ID is syntactically valid but the video was not found.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        CANNOT_CREATE_STANDARD_ICON = 2
        CANNOT_SELECT_STANDARD_ICON_WITH_OTHER_TYPES = 3
        CANNOT_SPECIFY_MEDIA_FILE_ID_AND_DATA = 4
        DUPLICATE_MEDIA = 5
        EMPTY_FIELD = 6
        RESOURCE_REFERENCED_IN_MULTIPLE_OPS = 7
        FIELD_NOT_SUPPORTED_FOR_MEDIA_SUB_TYPE = 8
        INVALID_MEDIA_FILE_ID = 9
        INVALID_MEDIA_SUB_TYPE = 10
        INVALID_MEDIA_FILE_TYPE = 11
        INVALID_MIME_TYPE = 12
        INVALID_REFERENCE_ID = 13
        INVALID_YOU_TUBE_ID = 14
        MEDIA_FILE_FAILED_TRANSCODING = 15
        MEDIA_NOT_TRANSCODED = 16
        MEDIA_TYPE_DOES_NOT_MATCH_MEDIA_FILE_TYPE = 17
        NO_FIELDS_SPECIFIED = 18
        NULL_REFERENCE_ID_AND_MEDIA_ID = 19
        TOO_LONG = 20
        UNSUPPORTED_TYPE = 21
        YOU_TUBE_SERVICE_UNAVAILABLE = 22
        YOU_TUBE_VIDEO_HAS_NON_POSITIVE_DURATION = 23
        YOU_TUBE_VIDEO_NOT_FOUND = 24


class MediaTypeEnum(object):
    class MediaType(enum.IntEnum):
        """
        The type of media.

        Attributes:
          UNSPECIFIED (int): The media type has not been specified.
          UNKNOWN (int): The received value is not known in this version.

          This is a response-only value.
          IMAGE (int): Static image, used for image ad.
          ICON (int): Small image, used for map ad.
          MEDIA_BUNDLE (int): ZIP file, used in fields of template ads.
          AUDIO (int): Audio file.
          VIDEO (int): Video file.
          DYNAMIC_IMAGE (int): Animated image, such as animated GIF.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        IMAGE = 2
        ICON = 3
        MEDIA_BUNDLE = 4
        AUDIO = 5
        VIDEO = 6
        DYNAMIC_IMAGE = 7


class MediaUploadErrorEnum(object):
    class MediaUploadError(enum.IntEnum):
        """
        Enum describing possible media uploading errors.

        Attributes:
          UNSPECIFIED (int): Enum unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          FILE_TOO_BIG (int): The uploaded file is too big.
          UNPARSEABLE_IMAGE (int): Image data is unparseable.
          ANIMATED_IMAGE_NOT_ALLOWED (int): Animated images are not allowed.
          FORMAT_NOT_ALLOWED (int): The image or media bundle format is not allowed.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        FILE_TOO_BIG = 2
        UNPARSEABLE_IMAGE = 3
        ANIMATED_IMAGE_NOT_ALLOWED = 4
        FORMAT_NOT_ALLOWED = 5


class MerchantCenterLinkStatusEnum(object):
    class MerchantCenterLinkStatus(enum.IntEnum):
        """
        Describes the possible statuses for a link between a Google Ads customer
        and a Google Merchant Center account.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          ENABLED (int): The link is enabled.
          PENDING (int): The link has no effect. It was proposed by the Merchant Center Account
          owner and hasn't been confirmed by the customer.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        ENABLED = 2
        PENDING = 3


class MessagePlaceholderFieldEnum(object):
    class MessagePlaceholderField(enum.IntEnum):
        """
        Possible values for Message placeholder fields.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          BUSINESS_NAME (int): Data Type: STRING. The name of your business.
          COUNTRY_CODE (int): Data Type: STRING. Country code of phone number.
          PHONE_NUMBER (int): Data Type: STRING. A phone number that's capable of sending and receiving
          text messages.
          MESSAGE_EXTENSION_TEXT (int): Data Type: STRING. The text that will go in your click-to-message ad.
          MESSAGE_TEXT (int): Data Type: STRING. The message text automatically shows in people's
          messaging apps when they tap to send you a message.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        BUSINESS_NAME = 2
        COUNTRY_CODE = 3
        PHONE_NUMBER = 4
        MESSAGE_EXTENSION_TEXT = 5
        MESSAGE_TEXT = 6


class MimeTypeEnum(object):
    class MimeType(enum.IntEnum):
        """
        The mime type

        Attributes:
          UNSPECIFIED (int): The mime type has not been specified.
          UNKNOWN (int): The received value is not known in this version.

          This is a response-only value.
          IMAGE_JPEG (int): MIME type of image/jpeg.
          IMAGE_GIF (int): MIME type of image/gif.
          IMAGE_PNG (int): MIME type of image/png.
          FLASH (int): MIME type of application/x-shockwave-flash.
          TEXT_HTML (int): MIME type of text/html.
          PDF (int): MIME type of application/pdf.
          MSWORD (int): MIME type of application/msword.
          MSEXCEL (int): MIME type of application/vnd.ms-excel.
          RTF (int): MIME type of application/rtf.
          AUDIO_WAV (int): MIME type of audio/wav.
          AUDIO_MP3 (int): MIME type of audio/mp3.
          HTML5_AD_ZIP (int): MIME type of application/x-html5-ad-zip.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        IMAGE_JPEG = 2
        IMAGE_GIF = 3
        IMAGE_PNG = 4
        FLASH = 5
        TEXT_HTML = 6
        PDF = 7
        MSWORD = 8
        MSEXCEL = 9
        RTF = 10
        AUDIO_WAV = 11
        AUDIO_MP3 = 12
        HTML5_AD_ZIP = 13


class MinuteOfHourEnum(object):
    class MinuteOfHour(enum.IntEnum):
        """
        Enumerates of quarter-hours. E.g. "FIFTEEN"

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): The value is unknown in this version.
          ZERO (int): Zero minutes past the hour.
          FIFTEEN (int): Fifteen minutes past the hour.
          THIRTY (int): Thirty minutes past the hour.
          FORTY_FIVE (int): Forty-five minutes past the hour.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        ZERO = 2
        FIFTEEN = 3
        THIRTY = 4
        FORTY_FIVE = 5


class MobileDeviceTypeEnum(object):
    class MobileDeviceType(enum.IntEnum):
        """
        The type of mobile device.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          MOBILE (int): Mobile phones.
          TABLET (int): Tablets.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        MOBILE = 2
        TABLET = 3


class MonthOfYearEnum(object):
    class MonthOfYear(enum.IntEnum):
        """
        Enumerates months of the year, e.g., "January".

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): The value is unknown in this version.
          JANUARY (int): January.
          FEBRUARY (int): February.
          MARCH (int): March.
          APRIL (int): April.
          MAY (int): May.
          JUNE (int): June.
          JULY (int): July.
          AUGUST (int): August.
          SEPTEMBER (int): September.
          OCTOBER (int): October.
          NOVEMBER (int): November.
          DECEMBER (int): December.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        JANUARY = 2
        FEBRUARY = 3
        MARCH = 4
        APRIL = 5
        MAY = 6
        JUNE = 7
        JULY = 8
        AUGUST = 9
        SEPTEMBER = 10
        OCTOBER = 11
        NOVEMBER = 12
        DECEMBER = 13


class MultiplierErrorEnum(object):
    class MultiplierError(enum.IntEnum):
        """
        Enum describing possible multiplier errors.

        Attributes:
          UNSPECIFIED (int): Enum unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          MULTIPLIER_TOO_HIGH (int): Multiplier value is too high
          MULTIPLIER_TOO_LOW (int): Multiplier value is too low
          TOO_MANY_FRACTIONAL_DIGITS (int): Too many fractional digits
          MULTIPLIER_NOT_ALLOWED_FOR_BIDDING_STRATEGY (int): A multiplier cannot be set for this bidding strategy
          MULTIPLIER_NOT_ALLOWED_WHEN_BASE_BID_IS_MISSING (int): A multiplier cannot be set when there is no base bid (e.g., content max
          cpc)
          NO_MULTIPLIER_SPECIFIED (int): A bid multiplier must be specified
          MULTIPLIER_CAUSES_BID_TO_EXCEED_DAILY_BUDGET (int): Multiplier causes bid to exceed daily budget
          MULTIPLIER_CAUSES_BID_TO_EXCEED_MONTHLY_BUDGET (int): Multiplier causes bid to exceed monthly budget
          MULTIPLIER_CAUSES_BID_TO_EXCEED_CUSTOM_BUDGET (int): Multiplier causes bid to exceed custom budget
          MULTIPLIER_CAUSES_BID_TO_EXCEED_MAX_ALLOWED_BID (int): Multiplier causes bid to exceed maximum allowed bid
          BID_LESS_THAN_MIN_ALLOWED_BID_WITH_MULTIPLIER (int): Multiplier causes bid to become less than the minimum bid allowed
          MULTIPLIER_AND_BIDDING_STRATEGY_TYPE_MISMATCH (int): Multiplier type (cpc vs. cpm) needs to match campaign's bidding strategy
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        MULTIPLIER_TOO_HIGH = 2
        MULTIPLIER_TOO_LOW = 3
        TOO_MANY_FRACTIONAL_DIGITS = 4
        MULTIPLIER_NOT_ALLOWED_FOR_BIDDING_STRATEGY = 5
        MULTIPLIER_NOT_ALLOWED_WHEN_BASE_BID_IS_MISSING = 6
        NO_MULTIPLIER_SPECIFIED = 7
        MULTIPLIER_CAUSES_BID_TO_EXCEED_DAILY_BUDGET = 8
        MULTIPLIER_CAUSES_BID_TO_EXCEED_MONTHLY_BUDGET = 9
        MULTIPLIER_CAUSES_BID_TO_EXCEED_CUSTOM_BUDGET = 10
        MULTIPLIER_CAUSES_BID_TO_EXCEED_MAX_ALLOWED_BID = 11
        BID_LESS_THAN_MIN_ALLOWED_BID_WITH_MULTIPLIER = 12
        MULTIPLIER_AND_BIDDING_STRATEGY_TYPE_MISMATCH = 13


class MutateErrorEnum(object):
    class MutateError(enum.IntEnum):
        """
        Enum describing possible mutate errors.

        Attributes:
          UNSPECIFIED (int): Enum unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          RESOURCE_NOT_FOUND (int): Requested resource was not found.
          ID_EXISTS_IN_MULTIPLE_MUTATES (int): Cannot mutate the same resource twice in one request.
          INCONSISTENT_FIELD_VALUES (int): The field's contents don't match another field that represents the same
          data.
          MUTATE_NOT_ALLOWED (int): Mutates are not allowed for the requested resource.
          RESOURCE_NOT_IN_GOOGLE_ADS (int): The resource isn't in Google Ads. It belongs to another ads system.
          RESOURCE_ALREADY_EXISTS (int): The resource being created already exists.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        RESOURCE_NOT_FOUND = 3
        ID_EXISTS_IN_MULTIPLE_MUTATES = 7
        INCONSISTENT_FIELD_VALUES = 8
        MUTATE_NOT_ALLOWED = 9
        RESOURCE_NOT_IN_GOOGLE_ADS = 10
        RESOURCE_ALREADY_EXISTS = 11


class MutateJobErrorEnum(object):
    class MutateJobError(enum.IntEnum):
        """
        Enum describing possible request errors.

        Attributes:
          UNSPECIFIED (int): Enum unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          CANNOT_MODIFY_JOB_AFTER_JOB_STARTS_RUNNING (int): The mutate job cannot add more operations or run after it has started
          running.
          EMPTY_OPERATIONS (int): The operations for an AddMutateJobOperations request were empty.
          INVALID_SEQUENCE_TOKEN (int): The sequence token for an AddMutateJobOperations request was invalid.
          RESULTS_NOT_READY (int): Mutate Job Results can only be retrieved once the job is finished.
          INVALID_PAGE_SIZE (int): The page size for ListMutateJobResults was invalid.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        CANNOT_MODIFY_JOB_AFTER_JOB_STARTS_RUNNING = 2
        EMPTY_OPERATIONS = 3
        INVALID_SEQUENCE_TOKEN = 4
        RESULTS_NOT_READY = 5
        INVALID_PAGE_SIZE = 6


class MutateJobStatusEnum(object):
    class MutateJobStatus(enum.IntEnum):
        """
        The mutate job statuses.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          PENDING (int): The job is not currently running.
          RUNNING (int): The job is running.
          DONE (int): The job is done.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        PENDING = 2
        RUNNING = 3
        DONE = 4


class NegativeGeoTargetTypeEnum(object):
    class NegativeGeoTargetType(enum.IntEnum):
        """
        The possible negative geo target types.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): The value is unknown in this version.
          DONT_CARE (int): Specifies that a user is excluded from seeing the ad if they
          are in, or show interest in, advertiser's excluded locations.
          LOCATION_OF_PRESENCE (int): Specifies that a user is excluded from seeing the ad if they
          are in advertiser's excluded locations.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        DONT_CARE = 2
        LOCATION_OF_PRESENCE = 3


class NewResourceCreationErrorEnum(object):
    class NewResourceCreationError(enum.IntEnum):
        """
        Enum describing possible new resource creation errors.

        Attributes:
          UNSPECIFIED (int): Enum unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          CANNOT_SET_ID_FOR_CREATE (int): Do not set the id field while creating new resources.
          DUPLICATE_TEMP_IDS (int): Creating more than one resource with the same temp ID is not allowed.
          TEMP_ID_RESOURCE_HAD_ERRORS (int): Parent resource with specified temp ID failed validation, so no
          validation will be done for this child resource.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        CANNOT_SET_ID_FOR_CREATE = 2
        DUPLICATE_TEMP_IDS = 3
        TEMP_ID_RESOURCE_HAD_ERRORS = 4


class NotEmptyErrorEnum(object):
    class NotEmptyError(enum.IntEnum):
        """
        Enum describing possible not empty errors.

        Attributes:
          UNSPECIFIED (int): Enum unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          EMPTY_LIST (int): Empty list.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        EMPTY_LIST = 2


class NotWhitelistedErrorEnum(object):
    class NotWhitelistedError(enum.IntEnum):
        """
        Enum describing possible not whitelisted errors.

        Attributes:
          UNSPECIFIED (int): Enum unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          CUSTOMER_NOT_WHITELISTED_FOR_THIS_FEATURE (int): Customer is not whitelisted for accessing this feature.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        CUSTOMER_NOT_WHITELISTED_FOR_THIS_FEATURE = 2


class NullErrorEnum(object):
    class NullError(enum.IntEnum):
        """
        Enum describing possible null errors.

        Attributes:
          UNSPECIFIED (int): Enum unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          NULL_CONTENT (int): Specified list/container must not contain any null elements
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        NULL_CONTENT = 2


class OperatingSystemVersionOperatorTypeEnum(object):
    class OperatingSystemVersionOperatorType(enum.IntEnum):
        """
        The type of operating system version.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          EQUALS_TO (int): Equals to the specified version.
          GREATER_THAN_EQUALS_TO (int): Greater than or equals to the specified version.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        EQUALS_TO = 2
        GREATER_THAN_EQUALS_TO = 4


class OperationAccessDeniedErrorEnum(object):
    class OperationAccessDeniedError(enum.IntEnum):
        """
        Enum describing possible operation access denied errors.

        Attributes:
          UNSPECIFIED (int): Enum unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          ACTION_NOT_PERMITTED (int): Unauthorized invocation of a service's method (get, mutate, etc.)
          CREATE_OPERATION_NOT_PERMITTED (int): Unauthorized CREATE operation in invoking a service's mutate method.
          REMOVE_OPERATION_NOT_PERMITTED (int): Unauthorized REMOVE operation in invoking a service's mutate method.
          UPDATE_OPERATION_NOT_PERMITTED (int): Unauthorized UPDATE operation in invoking a service's mutate method.
          MUTATE_ACTION_NOT_PERMITTED_FOR_CLIENT (int): A mutate action is not allowed on this campaign, from this client.
          OPERATION_NOT_PERMITTED_FOR_CAMPAIGN_TYPE (int): This operation is not permitted on this campaign type
          CREATE_AS_REMOVED_NOT_PERMITTED (int): A CREATE operation may not set status to REMOVED.
          OPERATION_NOT_PERMITTED_FOR_REMOVED_RESOURCE (int): This operation is not allowed because the campaign or adgroup is removed.
          OPERATION_NOT_PERMITTED_FOR_AD_GROUP_TYPE (int): This operation is not permitted on this ad group type.
          MUTATE_NOT_PERMITTED_FOR_CUSTOMER (int): The mutate is not allowed for this customer.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        ACTION_NOT_PERMITTED = 2
        CREATE_OPERATION_NOT_PERMITTED = 3
        REMOVE_OPERATION_NOT_PERMITTED = 4
        UPDATE_OPERATION_NOT_PERMITTED = 5
        MUTATE_ACTION_NOT_PERMITTED_FOR_CLIENT = 6
        OPERATION_NOT_PERMITTED_FOR_CAMPAIGN_TYPE = 7
        CREATE_AS_REMOVED_NOT_PERMITTED = 8
        OPERATION_NOT_PERMITTED_FOR_REMOVED_RESOURCE = 9
        OPERATION_NOT_PERMITTED_FOR_AD_GROUP_TYPE = 10
        MUTATE_NOT_PERMITTED_FOR_CUSTOMER = 11


class OperatorErrorEnum(object):
    class OperatorError(enum.IntEnum):
        """
        Enum describing possible operator errors.

        Attributes:
          UNSPECIFIED (int): Enum unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          OPERATOR_NOT_SUPPORTED (int): Operator not supported.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        OPERATOR_NOT_SUPPORTED = 2


class PageOnePromotedStrategyGoalEnum(object):
    class PageOnePromotedStrategyGoal(enum.IntEnum):
        """
        Enum describing possible strategy goals.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          FIRST_PAGE (int): First page on google.com.
          FIRST_PAGE_PROMOTED (int): Top slots of the first page on google.com.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        FIRST_PAGE = 2
        FIRST_PAGE_PROMOTED = 3


class ParentalStatusTypeEnum(object):
    class ParentalStatusType(enum.IntEnum):
        """
        The type of parental statuses (e.g. not a parent).

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          PARENT (int): Parent.
          NOT_A_PARENT (int): Not a parent.
          UNDETERMINED (int): Undetermined parental status.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        PARENT = 300
        NOT_A_PARENT = 301
        UNDETERMINED = 302


class PartialFailureErrorEnum(object):
    class PartialFailureError(enum.IntEnum):
        """
        Enum describing possible partial failure errors.

        Attributes:
          UNSPECIFIED (int): Enum unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          PARTIAL_FAILURE_MODE_REQUIRED (int): The partial failure field was false in the request.
          This method requires this field be set to true.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        PARTIAL_FAILURE_MODE_REQUIRED = 2


class PaymentModeEnum(object):
    class PaymentMode(enum.IntEnum):
        """
        Enum describing possible payment modes.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          CLICKS (int): Pay per click.
          CONVERSION_VALUE (int): Pay per conversion value. This mode is only supported by campaigns with
          AdvertisingChannelType.HOTEL, BiddingStrategyType.COMMISSION, and
          BudgetType.HOTEL\_ADS\_COMMISSION.
          CONVERSIONS (int): Pay per conversion. This mode is only supported by campaigns with
          AdvertisingChannelType.DISPLAY (excluding
          AdvertisingChannelSubType.DISPLAY\_GMAIL),
          BiddingStrategyType.TARGET\_CPA, and BudgetType.FIXED\_CPA. The customer
          must also be eligible for this mode. See
          Customer.eligibility\_failure\_reasons for details.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        CLICKS = 4
        CONVERSION_VALUE = 5
        CONVERSIONS = 6


class PlaceholderTypeEnum(object):
    class PlaceholderType(enum.IntEnum):
        """
        Possible placeholder types for a feed mapping.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          SITELINK (int): Lets you show links in your ad to pages from your website, including the
          main landing page.
          CALL (int): Lets you attach a phone number to an ad, allowing customers to call
          directly from the ad.
          APP (int): Lets you provide users with a link that points to a mobile app in
          addition to a website.
          LOCATION (int): Lets you show locations of businesses from your Google My Business
          account in your ad. This helps people find your locations by showing your
          ads with your address, a map to your location, or the distance to your
          business. This extension type is useful to draw customers to your
          brick-and-mortar location.
          AFFILIATE_LOCATION (int): If you sell your product through retail chains, affiliate location
          extensions let you show nearby stores that carry your products.
          CALLOUT (int): Lets you include additional text with your search ads that provide
          detailed information about your business, including products and services
          you offer. Callouts appear in ads at the top and bottom of Google search
          results.
          STRUCTURED_SNIPPET (int): Lets you add more info to your ad, specific to some predefined categories
          such as types, brands, styles, etc. A minimum of 3 text (SNIPPETS) values
          are required.
          MESSAGE (int): Allows users to see your ad, click an icon, and contact you directly by
          text message. With one tap on your ad, people can contact you to book an
          appointment, get a quote, ask for information, or request a service.
          PRICE (int): Lets you display prices for a list of items along with your ads. A price
          feed is composed of three to eight price table rows.
          PROMOTION (int): Allows you to highlight sales and other promotions that let users see how
          they can save by buying now.
          AD_CUSTOMIZER (int): Lets you dynamically inject custom data into the title and description
          of your ads.
          DYNAMIC_EDUCATION (int): Indicates that this feed is for education dynamic remarketing.
          DYNAMIC_FLIGHT (int): Indicates that this feed is for flight dynamic remarketing.
          DYNAMIC_CUSTOM (int): Indicates that this feed is for a custom dynamic remarketing type. Use
          this only if the other business types don't apply to your products or
          services.
          DYNAMIC_HOTEL (int): Indicates that this feed is for hotels and rentals dynamic remarketing.
          DYNAMIC_REAL_ESTATE (int): Indicates that this feed is for real estate dynamic remarketing.
          DYNAMIC_TRAVEL (int): Indicates that this feed is for travel dynamic remarketing.
          DYNAMIC_LOCAL (int): Indicates that this feed is for local deals dynamic remarketing.
          DYNAMIC_JOB (int): Indicates that this feed is for job dynamic remarketing.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        SITELINK = 2
        CALL = 3
        APP = 4
        LOCATION = 5
        AFFILIATE_LOCATION = 6
        CALLOUT = 7
        STRUCTURED_SNIPPET = 8
        MESSAGE = 9
        PRICE = 10
        PROMOTION = 11
        AD_CUSTOMIZER = 12
        DYNAMIC_EDUCATION = 13
        DYNAMIC_FLIGHT = 14
        DYNAMIC_CUSTOM = 15
        DYNAMIC_HOTEL = 16
        DYNAMIC_REAL_ESTATE = 17
        DYNAMIC_TRAVEL = 18
        DYNAMIC_LOCAL = 19
        DYNAMIC_JOB = 20


class PlacementTypeEnum(object):
    class PlacementType(enum.IntEnum):
        """
        Possible placement types for a feed mapping.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          WEBSITE (int): Websites(e.g. 'www.flowers4sale.com').
          MOBILE_APP_CATEGORY (int): Mobile application categories(e.g. 'Games').
          MOBILE_APPLICATION (int): mobile applications(e.g. 'mobileapp::2-com.whatsthewordanswers').
          YOUTUBE_VIDEO (int): YouTube videos(e.g. 'youtube.com/video/wtLJPvx7-ys').
          YOUTUBE_CHANNEL (int): YouTube channels(e.g. 'youtube.com::L8ZULXASCc1I\_oaOT0NaOQ').
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        WEBSITE = 2
        MOBILE_APP_CATEGORY = 3
        MOBILE_APPLICATION = 4
        YOUTUBE_VIDEO = 5
        YOUTUBE_CHANNEL = 6


class PolicyApprovalStatusEnum(object):
    class PolicyApprovalStatus(enum.IntEnum):
        """
        The possible policy approval statuses. When there are several approval
        statuses available the most severe one will be used. The order of
        severity is DISAPPROVED, AREA\_OF\_INTEREST\_ONLY, APPROVED\_LIMITED and
        APPROVED.

        Attributes:
          UNSPECIFIED (int): No value has been specified.
          UNKNOWN (int): The received value is not known in this version.

          This is a response-only value.
          DISAPPROVED (int): Will not serve.
          APPROVED_LIMITED (int): Serves with restrictions.
          APPROVED (int): Serves without restrictions.
          AREA_OF_INTEREST_ONLY (int): Will not serve in targeted countries, but may serve for users who are
          searching for information about the targeted countries.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        DISAPPROVED = 2
        APPROVED_LIMITED = 3
        APPROVED = 4
        AREA_OF_INTEREST_ONLY = 5


class PolicyFindingErrorEnum(object):
    class PolicyFindingError(enum.IntEnum):
        """
        Enum describing possible policy finding errors.

        Attributes:
          UNSPECIFIED (int): Enum unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          POLICY_FINDING (int): The resource has been disapproved since the policy summary includes
          policy topics of type PROHIBITED.
          POLICY_TOPIC_NOT_FOUND (int): The given policy topic does not exist.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        POLICY_FINDING = 2
        POLICY_TOPIC_NOT_FOUND = 3


class PolicyReviewStatusEnum(object):
    class PolicyReviewStatus(enum.IntEnum):
        """
        The possible policy review statuses.

        Attributes:
          UNSPECIFIED (int): No value has been specified.
          UNKNOWN (int): The received value is not known in this version.

          This is a response-only value.
          REVIEW_IN_PROGRESS (int): Currently under review.
          REVIEWED (int): Primary review complete. Other reviews may be continuing.
          UNDER_APPEAL (int): The resource has been resubmitted for approval or its policy decision has
          been appealed.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        REVIEW_IN_PROGRESS = 2
        REVIEWED = 3
        UNDER_APPEAL = 4


class PolicyTopicEntryTypeEnum(object):
    class PolicyTopicEntryType(enum.IntEnum):
        """
        The possible policy topic entry types.

        Attributes:
          UNSPECIFIED (int): No value has been specified.
          UNKNOWN (int): The received value is not known in this version.

          This is a response-only value.
          PROHIBITED (int): The resource will not be served.
          LIMITED (int): The resource will not be served under some circumstances.
          FULLY_LIMITED (int): The resource cannot serve at all because of the current targeting
          criteria.
          DESCRIPTIVE (int): May be of interest, but does not limit how the resource is served.
          BROADENING (int): Could increase coverage beyond normal.
          AREA_OF_INTEREST_ONLY (int): Constrained for all targeted countries, but may serve in other countries
          through area of interest.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        PROHIBITED = 2
        LIMITED = 4
        FULLY_LIMITED = 8
        DESCRIPTIVE = 5
        BROADENING = 6
        AREA_OF_INTEREST_ONLY = 7


class PolicyTopicEvidenceDestinationMismatchUrlTypeEnum(object):
    class PolicyTopicEvidenceDestinationMismatchUrlType(enum.IntEnum):
        """
        The possible policy topic evidence destination mismatch url types.

        Attributes:
          UNSPECIFIED (int): No value has been specified.
          UNKNOWN (int): The received value is not known in this version.

          This is a response-only value.
          DISPLAY_URL (int): The display url.
          FINAL_URL (int): The final url.
          FINAL_MOBILE_URL (int): The final mobile url.
          TRACKING_URL (int): The tracking url template, with substituted desktop url.
          MOBILE_TRACKING_URL (int): The tracking url template, with substituted mobile url.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        DISPLAY_URL = 2
        FINAL_URL = 3
        FINAL_MOBILE_URL = 4
        TRACKING_URL = 5
        MOBILE_TRACKING_URL = 6


class PolicyTopicEvidenceDestinationNotWorkingDeviceEnum(object):
    class PolicyTopicEvidenceDestinationNotWorkingDevice(enum.IntEnum):
        """
        The possible policy topic evidence destination not working devices.

        Attributes:
          UNSPECIFIED (int): No value has been specified.
          UNKNOWN (int): The received value is not known in this version.

          This is a response-only value.
          DESKTOP (int): Landing page doesn't work on desktop device.
          ANDROID (int): Landing page doesn't work on Android device.
          IOS (int): Landing page doesn't work on iOS device.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        DESKTOP = 2
        ANDROID = 3
        IOS = 4


class PolicyValidationParameterErrorEnum(object):
    class PolicyValidationParameterError(enum.IntEnum):
        """
        Enum describing possible policy validation parameter errors.

        Attributes:
          UNSPECIFIED (int): Enum unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          UNSUPPORTED_AD_TYPE_FOR_IGNORABLE_POLICY_TOPICS (int): Ignorable policy topics are not supported for the ad type.
          UNSUPPORTED_AD_TYPE_FOR_EXEMPT_POLICY_VIOLATION_KEYS (int): Exempt policy violation keys are not supported for the ad type.
          CANNOT_SET_BOTH_IGNORABLE_POLICY_TOPICS_AND_EXEMPT_POLICY_VIOLATION_KEYS (int): Cannot set ignorable policy topics and exempt policy violation keys in
          the same policy violation parameter.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        UNSUPPORTED_AD_TYPE_FOR_IGNORABLE_POLICY_TOPICS = 2
        UNSUPPORTED_AD_TYPE_FOR_EXEMPT_POLICY_VIOLATION_KEYS = 3
        CANNOT_SET_BOTH_IGNORABLE_POLICY_TOPICS_AND_EXEMPT_POLICY_VIOLATION_KEYS = 4


class PolicyViolationErrorEnum(object):
    class PolicyViolationError(enum.IntEnum):
        """
        Enum describing possible policy violation errors.

        Attributes:
          UNSPECIFIED (int): Enum unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          POLICY_ERROR (int): A policy was violated. See PolicyViolationDetails for more detail.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        POLICY_ERROR = 2


class PositiveGeoTargetTypeEnum(object):
    class PositiveGeoTargetType(enum.IntEnum):
        """
        The possible positive geo target types.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): The value is unknown in this version.
          DONT_CARE (int): Specifies that an ad is triggered if the user is in,
          or shows interest in, advertiser's targeted locations.
          AREA_OF_INTEREST (int): Specifies that an ad is triggered if the user
          searches for advertiser's targeted locations.
          LOCATION_OF_PRESENCE (int): Specifies that an ad is triggered if the user is in
          or regularly in advertiser's targeted locations.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        DONT_CARE = 2
        AREA_OF_INTEREST = 3
        LOCATION_OF_PRESENCE = 4


class PreferredContentTypeEnum(object):
    class PreferredContentType(enum.IntEnum):
        """
        Enumerates preferred content criterion type.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): The value is unknown in this version.
          YOUTUBE_TOP_CONTENT (int): Represents top content on YouTube.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        YOUTUBE_TOP_CONTENT = 400


class PriceExtensionPriceQualifierEnum(object):
    class PriceExtensionPriceQualifier(enum.IntEnum):
        """
        Enums of price extension price qualifier.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          FROM (int): 'From' qualifier for the price.
          UP_TO (int): 'Up to' qualifier for the price.
          AVERAGE (int): 'Average' qualifier for the price.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        FROM = 2
        UP_TO = 3
        AVERAGE = 4


class PriceExtensionPriceUnitEnum(object):
    class PriceExtensionPriceUnit(enum.IntEnum):
        """
        Price extension price unit.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          PER_HOUR (int): Per hour.
          PER_DAY (int): Per day.
          PER_WEEK (int): Per week.
          PER_MONTH (int): Per month.
          PER_YEAR (int): Per year.
          PER_NIGHT (int): Per night.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        PER_HOUR = 2
        PER_DAY = 3
        PER_WEEK = 4
        PER_MONTH = 5
        PER_YEAR = 6
        PER_NIGHT = 7


class PriceExtensionTypeEnum(object):
    class PriceExtensionType(enum.IntEnum):
        """
        Price extension type.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          BRANDS (int): The type for showing a list of brands.
          EVENTS (int): The type for showing a list of events.
          LOCATIONS (int): The type for showing locations relevant to your business.
          NEIGHBORHOODS (int): The type for showing sub-regions or districts within a city or region.
          PRODUCT_CATEGORIES (int): The type for showing a collection of product categories.
          PRODUCT_TIERS (int): The type for showing a collection of related product tiers.
          SERVICES (int): The type for showing a collection of services offered by your business.
          SERVICE_CATEGORIES (int): The type for showing a collection of service categories.
          SERVICE_TIERS (int): The type for showing a collection of related service tiers.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        BRANDS = 2
        EVENTS = 3
        LOCATIONS = 4
        NEIGHBORHOODS = 5
        PRODUCT_CATEGORIES = 6
        PRODUCT_TIERS = 7
        SERVICES = 8
        SERVICE_CATEGORIES = 9
        SERVICE_TIERS = 10


class PricePlaceholderFieldEnum(object):
    class PricePlaceholderField(enum.IntEnum):
        """
        Possible values for Price placeholder fields.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          TYPE (int): Data Type: STRING. The type of your price feed. Must match one of the
          predefined price feed type exactly.
          PRICE_QUALIFIER (int): Data Type: STRING. The qualifier of each price. Must match one of the
          predefined price qualifiers exactly.
          TRACKING_TEMPLATE (int): Data Type: URL. Tracking template for the price feed when using Upgraded
          URLs.
          LANGUAGE (int): Data Type: STRING. Language of the price feed. Must match one of the
          available available locale codes exactly.
          FINAL_URL_SUFFIX (int): Data Type: STRING. Final URL suffix for the price feed when using
          parallel tracking.
          ITEM_1_HEADER (int): Data Type: STRING. The header of item 1 of the table.
          ITEM_1_DESCRIPTION (int): Data Type: STRING. The description of item 1 of the table.
          ITEM_1_PRICE (int): Data Type: MONEY. The price (money with currency) of item 1 of the table,
          e.g., 30 USD. The currency must match one of the available currencies.
          ITEM_1_UNIT (int): Data Type: STRING. The price unit of item 1 of the table. Must match one
          of the predefined price units.
          ITEM_1_FINAL_URLS (int): Data Type: URL\_LIST. The final URLs of item 1 of the table when using
          Upgraded URLs.
          ITEM_1_FINAL_MOBILE_URLS (int): Data Type: URL\_LIST. The final mobile URLs of item 1 of the table when
          using Upgraded URLs.
          ITEM_2_HEADER (int): Data Type: STRING. The header of item 2 of the table.
          ITEM_2_DESCRIPTION (int): Data Type: STRING. The description of item 2 of the table.
          ITEM_2_PRICE (int): Data Type: MONEY. The price (money with currency) of item 2 of the table,
          e.g., 30 USD. The currency must match one of the available currencies.
          ITEM_2_UNIT (int): Data Type: STRING. The price unit of item 2 of the table. Must match one
          of the predefined price units.
          ITEM_2_FINAL_URLS (int): Data Type: URL\_LIST. The final URLs of item 2 of the table when using
          Upgraded URLs.
          ITEM_2_FINAL_MOBILE_URLS (int): Data Type: URL\_LIST. The final mobile URLs of item 2 of the table when
          using Upgraded URLs.
          ITEM_3_HEADER (int): Data Type: STRING. The header of item 3 of the table.
          ITEM_3_DESCRIPTION (int): Data Type: STRING. The description of item 3 of the table.
          ITEM_3_PRICE (int): Data Type: MONEY. The price (money with currency) of item 3 of the table,
          e.g., 30 USD. The currency must match one of the available currencies.
          ITEM_3_UNIT (int): Data Type: STRING. The price unit of item 3 of the table. Must match one
          of the predefined price units.
          ITEM_3_FINAL_URLS (int): Data Type: URL\_LIST. The final URLs of item 3 of the table when using
          Upgraded URLs.
          ITEM_3_FINAL_MOBILE_URLS (int): Data Type: URL\_LIST. The final mobile URLs of item 3 of the table when
          using Upgraded URLs.
          ITEM_4_HEADER (int): Data Type: STRING. The header of item 4 of the table.
          ITEM_4_DESCRIPTION (int): Data Type: STRING. The description of item 4 of the table.
          ITEM_4_PRICE (int): Data Type: MONEY. The price (money with currency) of item 4 of the table,
          e.g., 30 USD. The currency must match one of the available currencies.
          ITEM_4_UNIT (int): Data Type: STRING. The price unit of item 4 of the table. Must match one
          of the predefined price units.
          ITEM_4_FINAL_URLS (int): Data Type: URL\_LIST. The final URLs of item 4 of the table when using
          Upgraded URLs.
          ITEM_4_FINAL_MOBILE_URLS (int): Data Type: URL\_LIST. The final mobile URLs of item 4 of the table when
          using Upgraded URLs.
          ITEM_5_HEADER (int): Data Type: STRING. The header of item 5 of the table.
          ITEM_5_DESCRIPTION (int): Data Type: STRING. The description of item 5 of the table.
          ITEM_5_PRICE (int): Data Type: MONEY. The price (money with currency) of item 5 of the table,
          e.g., 30 USD. The currency must match one of the available currencies.
          ITEM_5_UNIT (int): Data Type: STRING. The price unit of item 5 of the table. Must match one
          of the predefined price units.
          ITEM_5_FINAL_URLS (int): Data Type: URL\_LIST. The final URLs of item 5 of the table when using
          Upgraded URLs.
          ITEM_5_FINAL_MOBILE_URLS (int): Data Type: URL\_LIST. The final mobile URLs of item 5 of the table when
          using Upgraded URLs.
          ITEM_6_HEADER (int): Data Type: STRING. The header of item 6 of the table.
          ITEM_6_DESCRIPTION (int): Data Type: STRING. The description of item 6 of the table.
          ITEM_6_PRICE (int): Data Type: MONEY. The price (money with currency) of item 6 of the table,
          e.g., 30 USD. The currency must match one of the available currencies.
          ITEM_6_UNIT (int): Data Type: STRING. The price unit of item 6 of the table. Must match one
          of the predefined price units.
          ITEM_6_FINAL_URLS (int): Data Type: URL\_LIST. The final URLs of item 6 of the table when using
          Upgraded URLs.
          ITEM_6_FINAL_MOBILE_URLS (int): Data Type: URL\_LIST. The final mobile URLs of item 6 of the table when
          using Upgraded URLs.
          ITEM_7_HEADER (int): Data Type: STRING. The header of item 7 of the table.
          ITEM_7_DESCRIPTION (int): Data Type: STRING. The description of item 7 of the table.
          ITEM_7_PRICE (int): Data Type: MONEY. The price (money with currency) of item 7 of the table,
          e.g., 30 USD. The currency must match one of the available currencies.
          ITEM_7_UNIT (int): Data Type: STRING. The price unit of item 7 of the table. Must match one
          of the predefined price units.
          ITEM_7_FINAL_URLS (int): Data Type: URL\_LIST. The final URLs of item 7 of the table when using
          Upgraded URLs.
          ITEM_7_FINAL_MOBILE_URLS (int): Data Type: URL\_LIST. The final mobile URLs of item 7 of the table when
          using Upgraded URLs.
          ITEM_8_HEADER (int): Data Type: STRING. The header of item 8 of the table.
          ITEM_8_DESCRIPTION (int): Data Type: STRING. The description of item 8 of the table.
          ITEM_8_PRICE (int): Data Type: MONEY. The price (money with currency) of item 8 of the table,
          e.g., 30 USD. The currency must match one of the available currencies.
          ITEM_8_UNIT (int): Data Type: STRING. The price unit of item 8 of the table. Must match one
          of the predefined price units.
          ITEM_8_FINAL_URLS (int): Data Type: URL\_LIST. The final URLs of item 8 of the table when using
          Upgraded URLs.
          ITEM_8_FINAL_MOBILE_URLS (int): Data Type: URL\_LIST. The final mobile URLs of item 8 of the table when
          using Upgraded URLs.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        TYPE = 2
        PRICE_QUALIFIER = 3
        TRACKING_TEMPLATE = 4
        LANGUAGE = 5
        FINAL_URL_SUFFIX = 6
        ITEM_1_HEADER = 100
        ITEM_1_DESCRIPTION = 101
        ITEM_1_PRICE = 102
        ITEM_1_UNIT = 103
        ITEM_1_FINAL_URLS = 104
        ITEM_1_FINAL_MOBILE_URLS = 105
        ITEM_2_HEADER = 200
        ITEM_2_DESCRIPTION = 201
        ITEM_2_PRICE = 202
        ITEM_2_UNIT = 203
        ITEM_2_FINAL_URLS = 204
        ITEM_2_FINAL_MOBILE_URLS = 205
        ITEM_3_HEADER = 300
        ITEM_3_DESCRIPTION = 301
        ITEM_3_PRICE = 302
        ITEM_3_UNIT = 303
        ITEM_3_FINAL_URLS = 304
        ITEM_3_FINAL_MOBILE_URLS = 305
        ITEM_4_HEADER = 400
        ITEM_4_DESCRIPTION = 401
        ITEM_4_PRICE = 402
        ITEM_4_UNIT = 403
        ITEM_4_FINAL_URLS = 404
        ITEM_4_FINAL_MOBILE_URLS = 405
        ITEM_5_HEADER = 500
        ITEM_5_DESCRIPTION = 501
        ITEM_5_PRICE = 502
        ITEM_5_UNIT = 503
        ITEM_5_FINAL_URLS = 504
        ITEM_5_FINAL_MOBILE_URLS = 505
        ITEM_6_HEADER = 600
        ITEM_6_DESCRIPTION = 601
        ITEM_6_PRICE = 602
        ITEM_6_UNIT = 603
        ITEM_6_FINAL_URLS = 604
        ITEM_6_FINAL_MOBILE_URLS = 605
        ITEM_7_HEADER = 700
        ITEM_7_DESCRIPTION = 701
        ITEM_7_PRICE = 702
        ITEM_7_UNIT = 703
        ITEM_7_FINAL_URLS = 704
        ITEM_7_FINAL_MOBILE_URLS = 705
        ITEM_8_HEADER = 800
        ITEM_8_DESCRIPTION = 801
        ITEM_8_PRICE = 802
        ITEM_8_UNIT = 803
        ITEM_8_FINAL_URLS = 804
        ITEM_8_FINAL_MOBILE_URLS = 805


class ProductBiddingCategoryLevelEnum(object):
    class ProductBiddingCategoryLevel(enum.IntEnum):
        """
        Enum describing the level of the product bidding category.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          LEVEL1 (int): Level 1.
          LEVEL2 (int): Level 2.
          LEVEL3 (int): Level 3.
          LEVEL4 (int): Level 4.
          LEVEL5 (int): Level 5.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        LEVEL1 = 2
        LEVEL2 = 3
        LEVEL3 = 4
        LEVEL4 = 5
        LEVEL5 = 6


class ProductBiddingCategoryStatusEnum(object):
    class ProductBiddingCategoryStatus(enum.IntEnum):
        """
        Enum describing the status of the product bidding category.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          ACTIVE (int): The category is active and can be used for bidding.
          OBSOLETE (int): The category is obsolete. Used only for reporting purposes.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        ACTIVE = 2
        OBSOLETE = 3


class ProductChannelEnum(object):
    class ProductChannel(enum.IntEnum):
        """
        Enum describing the locality of a product offer.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          ONLINE (int): The item is sold online.
          LOCAL (int): The item is sold in local stores.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        ONLINE = 2
        LOCAL = 3


class ProductChannelExclusivityEnum(object):
    class ProductChannelExclusivity(enum.IntEnum):
        """
        Enum describing the availability of a product offer.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          SINGLE_CHANNEL (int): The item is sold through one channel only, either local stores or online
          as indicated by its ProductChannel.
          MULTI_CHANNEL (int): The item is matched to its online or local stores counterpart, indicating
          it is available for purchase in both ShoppingProductChannels.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        SINGLE_CHANNEL = 2
        MULTI_CHANNEL = 3


class ProductConditionEnum(object):
    class ProductCondition(enum.IntEnum):
        """
        Enum describing the condition of a product offer.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          NEW (int): The product condition is new.
          REFURBISHED (int): The product condition is refurbished.
          USED (int): The product condition is used.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        NEW = 3
        REFURBISHED = 4
        USED = 5


class ProductTypeLevelEnum(object):
    class ProductTypeLevel(enum.IntEnum):
        """
        Enum describing the level of the type of a product offer.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          LEVEL1 (int): Level 1.
          LEVEL2 (int): Level 2.
          LEVEL3 (int): Level 3.
          LEVEL4 (int): Level 4.
          LEVEL5 (int): Level 5.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        LEVEL1 = 7
        LEVEL2 = 8
        LEVEL3 = 9
        LEVEL4 = 10
        LEVEL5 = 11


class PromotionExtensionDiscountModifierEnum(object):
    class PromotionExtensionDiscountModifier(enum.IntEnum):
        """
        A promotion extension discount modifier.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          UP_TO (int): 'Up to'.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        UP_TO = 2


class PromotionExtensionOccasionEnum(object):
    class PromotionExtensionOccasion(enum.IntEnum):
        """
        A promotion extension occasion.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          NEW_YEARS (int): New Year's.
          CHINESE_NEW_YEAR (int): Chinese New Year.
          VALENTINES_DAY (int): Valentine's Day.
          EASTER (int): Easter.
          MOTHERS_DAY (int): Mother's Day.
          FATHERS_DAY (int): Father's Day.
          LABOR_DAY (int): Labor Day.
          BACK_TO_SCHOOL (int): Back To School.
          HALLOWEEN (int): Halloween.
          BLACK_FRIDAY (int): Black Friday.
          CYBER_MONDAY (int): Cyber Monday.
          CHRISTMAS (int): Christmas.
          BOXING_DAY (int): Boxing Day.
          INDEPENDENCE_DAY (int): Independence Day in any country.
          NATIONAL_DAY (int): National Day in any country.
          END_OF_SEASON (int): End of any season.
          WINTER_SALE (int): Winter Sale.
          SUMMER_SALE (int): Summer sale.
          FALL_SALE (int): Fall Sale.
          SPRING_SALE (int): Spring Sale.
          RAMADAN (int): Ramadan.
          EID_AL_FITR (int): Eid al-Fitr.
          EID_AL_ADHA (int): Eid al-Adha.
          SINGLES_DAY (int): Singles Day.
          WOMENS_DAY (int): Women's Day.
          HOLI (int): Holi.
          PARENTS_DAY (int): Parent's Day.
          ST_NICHOLAS_DAY (int): St. Nicholas Day.
          CARNIVAL (int): Carnival.
          EPIPHANY (int): Epiphany, also known as Three Kings' Day.
          ROSH_HASHANAH (int): Rosh Hashanah.
          PASSOVER (int): Passover.
          HANUKKAH (int): Hanukkah.
          DIWALI (int): Diwali.
          NAVRATRI (int): Navratri.
          SONGKRAN (int): Available in Thai: Songkran.
          YEAR_END_GIFT (int): Available in Japanese: Year-end Gift.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        NEW_YEARS = 2
        CHINESE_NEW_YEAR = 3
        VALENTINES_DAY = 4
        EASTER = 5
        MOTHERS_DAY = 6
        FATHERS_DAY = 7
        LABOR_DAY = 8
        BACK_TO_SCHOOL = 9
        HALLOWEEN = 10
        BLACK_FRIDAY = 11
        CYBER_MONDAY = 12
        CHRISTMAS = 13
        BOXING_DAY = 14
        INDEPENDENCE_DAY = 15
        NATIONAL_DAY = 16
        END_OF_SEASON = 17
        WINTER_SALE = 18
        SUMMER_SALE = 19
        FALL_SALE = 20
        SPRING_SALE = 21
        RAMADAN = 22
        EID_AL_FITR = 23
        EID_AL_ADHA = 24
        SINGLES_DAY = 25
        WOMENS_DAY = 26
        HOLI = 27
        PARENTS_DAY = 28
        ST_NICHOLAS_DAY = 29
        CARNIVAL = 30
        EPIPHANY = 31
        ROSH_HASHANAH = 32
        PASSOVER = 33
        HANUKKAH = 34
        DIWALI = 35
        NAVRATRI = 36
        SONGKRAN = 37
        YEAR_END_GIFT = 38


class PromotionPlaceholderFieldEnum(object):
    class PromotionPlaceholderField(enum.IntEnum):
        """
        Possible values for Promotion placeholder fields.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          PROMOTION_TARGET (int): Data Type: STRING. The text that appears on the ad when the extension is
          shown.
          DISCOUNT_MODIFIER (int): Data Type: STRING. Allows you to add "up to" phrase to the promotion,
          in case you have variable promotion rates.
          PERCENT_OFF (int): Data Type: INT64. Takes a value in micros, where 1 million micros
          represents 1%, and is shown as a percentage when rendered.
          MONEY_AMOUNT_OFF (int): Data Type: MONEY. Requires a currency and an amount of money.
          PROMOTION_CODE (int): Data Type: STRING. A string that the user enters to get the discount.
          ORDERS_OVER_AMOUNT (int): Data Type: MONEY. A minimum spend before the user qualifies for the
          promotion.
          PROMOTION_START (int): Data Type: DATE. The start date of the promotion.
          PROMOTION_END (int): Data Type: DATE. The end date of the promotion.
          OCCASION (int): Data Type: STRING. Describes the associated event for the promotion
          using one of the PromotionExtensionOccasion enum values, for example
          NEW\_YEARS.
          FINAL_URLS (int): Data Type: URL\_LIST. Final URLs to be used in the ad when using
          Upgraded URLs.
          FINAL_MOBILE_URLS (int): Data Type: URL\_LIST. Final mobile URLs for the ad when using Upgraded
          URLs.
          TRACKING_URL (int): Data Type: URL. Tracking template for the ad when using Upgraded URLs.
          LANGUAGE (int): Data Type: STRING. A string represented by a language code for the
          promotion.
          FINAL_URL_SUFFIX (int): Data Type: STRING. Final URL suffix for the ad when using parallel
          tracking.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        PROMOTION_TARGET = 2
        DISCOUNT_MODIFIER = 3
        PERCENT_OFF = 4
        MONEY_AMOUNT_OFF = 5
        PROMOTION_CODE = 6
        ORDERS_OVER_AMOUNT = 7
        PROMOTION_START = 8
        PROMOTION_END = 9
        OCCASION = 10
        FINAL_URLS = 11
        FINAL_MOBILE_URLS = 12
        TRACKING_URL = 13
        LANGUAGE = 14
        FINAL_URL_SUFFIX = 15


class ProximityRadiusUnitsEnum(object):
    class ProximityRadiusUnits(enum.IntEnum):
        """
        The unit of radius distance in proximity (e.g. MILES)

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          MILES (int): Miles
          KILOMETERS (int): Kilometers
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        MILES = 2
        KILOMETERS = 3


class QualityScoreBucketEnum(object):
    class QualityScoreBucket(enum.IntEnum):
        """
        Enum listing the possible quality score buckets.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          BELOW_AVERAGE (int): Quality of the creative is below average.
          AVERAGE (int): Quality of the creative is average.
          ABOVE_AVERAGE (int): Quality of the creative is above average.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        BELOW_AVERAGE = 2
        AVERAGE = 3
        ABOVE_AVERAGE = 4


class QueryErrorEnum(object):
    class QueryError(enum.IntEnum):
        """
        Enum describing possible query errors.

        Attributes:
          UNSPECIFIED (int): Name unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          QUERY_ERROR (int): Returned if all other query error reasons are not applicable.
          BAD_ENUM_CONSTANT (int): A condition used in the query references an invalid enum constant.
          BAD_ESCAPE_SEQUENCE (int): Query contains an invalid escape sequence.
          BAD_FIELD_NAME (int): Field name is invalid.
          BAD_LIMIT_VALUE (int): Limit value is invalid (i.e. not a number)
          BAD_NUMBER (int): Encountered number can not be parsed.
          BAD_OPERATOR (int): Invalid operator encountered.
          BAD_PARAMETER_NAME (int): Parameter unknown or not supported.
          BAD_PARAMETER_VALUE (int): Parameter have invalid value.
          BAD_RESOURCE_TYPE_IN_FROM_CLAUSE (int): Invalid resource type was specified in the FROM clause.
          BAD_SYMBOL (int): Non-ASCII symbol encountered outside of strings.
          BAD_VALUE (int): Value is invalid.
          DATE_RANGE_TOO_WIDE (int): Date filters fail to restrict date to a range smaller than 31 days.
          Applicable if the query is segmented by date.
          EXPECTED_AND (int): Expected AND between values with BETWEEN operator.
          EXPECTED_BY (int): Expecting ORDER BY to have BY.
          EXPECTED_DIMENSION_FIELD_IN_SELECT_CLAUSE (int): There was no dimension field selected.
          EXPECTED_FILTERS_ON_DATE_RANGE (int): Missing filters on date related fields.
          EXPECTED_FROM (int): Missing FROM clause.
          EXPECTED_LIST (int): The operator used in the conditions requires the value to be a list.
          EXPECTED_REFERENCED_FIELD_IN_SELECT_CLAUSE (int): Fields used in WHERE or ORDER BY clauses are missing from the SELECT
          clause.
          EXPECTED_SELECT (int): SELECT is missing at the beginning of query.
          EXPECTED_SINGLE_VALUE (int): A list was passed as a value to a condition whose operator expects a
          single value.
          EXPECTED_VALUE_WITH_BETWEEN_OPERATOR (int): Missing one or both values with BETWEEN operator.
          INVALID_DATE_FORMAT (int): Invalid date format. Expected 'YYYY-MM-DD'.
          INVALID_STRING_VALUE (int): Value passed was not a string when it should have been. I.e., it was a
          number or unquoted literal.
          INVALID_VALUE_WITH_BETWEEN_OPERATOR (int): A String value passed to the BETWEEN operator does not parse as a date.
          INVALID_VALUE_WITH_DURING_OPERATOR (int): The value passed to the DURING operator is not a Date range literal
          INVALID_VALUE_WITH_LIKE_OPERATOR (int): A non-string value was passed to the LIKE operator.
          OPERATOR_FIELD_MISMATCH (int): An operator was provided that is inapplicable to the field being
          filtered.
          PROHIBITED_EMPTY_LIST_IN_CONDITION (int): A Condition was found with an empty list.
          PROHIBITED_ENUM_CONSTANT (int): A condition used in the query references an unsupported enum constant.
          PROHIBITED_FIELD_COMBINATION_IN_SELECT_CLAUSE (int): Fields that are not allowed to be selected together were included in
          the SELECT clause.
          PROHIBITED_FIELD_IN_ORDER_BY_CLAUSE (int): A field that is not orderable was included in the ORDER BY clause.
          PROHIBITED_FIELD_IN_SELECT_CLAUSE (int): A field that is not selectable was included in the SELECT clause.
          PROHIBITED_FIELD_IN_WHERE_CLAUSE (int): A field that is not filterable was included in the WHERE clause.
          PROHIBITED_RESOURCE_TYPE_IN_FROM_CLAUSE (int): Resource type specified in the FROM clause is not supported by this
          service.
          PROHIBITED_RESOURCE_TYPE_IN_SELECT_CLAUSE (int): A field that comes from an incompatible resource was included in the
          SELECT clause.
          PROHIBITED_RESOURCE_TYPE_IN_WHERE_CLAUSE (int): A field that comes from an incompatible resource was included in the
          WHERE clause.
          PROHIBITED_METRIC_IN_SELECT_OR_WHERE_CLAUSE (int): A metric incompatible with the main resource or other selected
          segmenting resources was included in the SELECT or WHERE clause.
          PROHIBITED_SEGMENT_IN_SELECT_OR_WHERE_CLAUSE (int): A segment incompatible with the main resource or other selected
          segmenting resources was included in the SELECT or WHERE clause.
          PROHIBITED_SEGMENT_WITH_METRIC_IN_SELECT_OR_WHERE_CLAUSE (int): A segment in the SELECT clause is incompatible with a metric in the
          SELECT or WHERE clause.
          LIMIT_VALUE_TOO_LOW (int): The value passed to the limit clause is too low.
          PROHIBITED_NEWLINE_IN_STRING (int): Query has a string containing a newline character.
          PROHIBITED_VALUE_COMBINATION_IN_LIST (int): List contains values of different types.
          PROHIBITED_VALUE_COMBINATION_WITH_BETWEEN_OPERATOR (int): The values passed to the BETWEEN operator are not of the same type.
          STRING_NOT_TERMINATED (int): Query contains unterminated string.
          TOO_MANY_SEGMENTS (int): Too many segments are specified in SELECT clause.
          UNEXPECTED_END_OF_QUERY (int): Query is incomplete and cannot be parsed.
          UNEXPECTED_FROM_CLAUSE (int): FROM clause cannot be specified in this query.
          UNRECOGNIZED_FIELD (int): Query contains one or more unrecognized fields.
          UNEXPECTED_INPUT (int): Query has an unexpected extra part.
          REQUESTED_METRICS_FOR_MANAGER (int): Metrics cannot be requested for a manager account. To retrieve metrics,
          issue separate requests against each client account under the manager
          account.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        QUERY_ERROR = 50
        BAD_ENUM_CONSTANT = 18
        BAD_ESCAPE_SEQUENCE = 7
        BAD_FIELD_NAME = 12
        BAD_LIMIT_VALUE = 15
        BAD_NUMBER = 5
        BAD_OPERATOR = 3
        BAD_PARAMETER_NAME = 61
        BAD_PARAMETER_VALUE = 62
        BAD_RESOURCE_TYPE_IN_FROM_CLAUSE = 45
        BAD_SYMBOL = 2
        BAD_VALUE = 4
        DATE_RANGE_TOO_WIDE = 36
        EXPECTED_AND = 30
        EXPECTED_BY = 14
        EXPECTED_DIMENSION_FIELD_IN_SELECT_CLAUSE = 37
        EXPECTED_FILTERS_ON_DATE_RANGE = 55
        EXPECTED_FROM = 44
        EXPECTED_LIST = 41
        EXPECTED_REFERENCED_FIELD_IN_SELECT_CLAUSE = 16
        EXPECTED_SELECT = 13
        EXPECTED_SINGLE_VALUE = 42
        EXPECTED_VALUE_WITH_BETWEEN_OPERATOR = 29
        INVALID_DATE_FORMAT = 38
        INVALID_STRING_VALUE = 57
        INVALID_VALUE_WITH_BETWEEN_OPERATOR = 26
        INVALID_VALUE_WITH_DURING_OPERATOR = 22
        INVALID_VALUE_WITH_LIKE_OPERATOR = 56
        OPERATOR_FIELD_MISMATCH = 35
        PROHIBITED_EMPTY_LIST_IN_CONDITION = 28
        PROHIBITED_ENUM_CONSTANT = 54
        PROHIBITED_FIELD_COMBINATION_IN_SELECT_CLAUSE = 31
        PROHIBITED_FIELD_IN_ORDER_BY_CLAUSE = 40
        PROHIBITED_FIELD_IN_SELECT_CLAUSE = 23
        PROHIBITED_FIELD_IN_WHERE_CLAUSE = 24
        PROHIBITED_RESOURCE_TYPE_IN_FROM_CLAUSE = 43
        PROHIBITED_RESOURCE_TYPE_IN_SELECT_CLAUSE = 48
        PROHIBITED_RESOURCE_TYPE_IN_WHERE_CLAUSE = 58
        PROHIBITED_METRIC_IN_SELECT_OR_WHERE_CLAUSE = 49
        PROHIBITED_SEGMENT_IN_SELECT_OR_WHERE_CLAUSE = 51
        PROHIBITED_SEGMENT_WITH_METRIC_IN_SELECT_OR_WHERE_CLAUSE = 53
        LIMIT_VALUE_TOO_LOW = 25
        PROHIBITED_NEWLINE_IN_STRING = 8
        PROHIBITED_VALUE_COMBINATION_IN_LIST = 10
        PROHIBITED_VALUE_COMBINATION_WITH_BETWEEN_OPERATOR = 21
        STRING_NOT_TERMINATED = 6
        TOO_MANY_SEGMENTS = 34
        UNEXPECTED_END_OF_QUERY = 9
        UNEXPECTED_FROM_CLAUSE = 47
        UNRECOGNIZED_FIELD = 32
        UNEXPECTED_INPUT = 11
        REQUESTED_METRICS_FOR_MANAGER = 59


class QuotaErrorEnum(object):
    class QuotaError(enum.IntEnum):
        """
        Enum describing possible quota errors.

        Attributes:
          UNSPECIFIED (int): Enum unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          RESOURCE_EXHAUSTED (int): Too many requests.
          ACCESS_PROHIBITED (int): Access is prohibited.
          RESOURCE_TEMPORARILY_EXHAUSTED (int): Too many requests in a short amount of time.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        RESOURCE_EXHAUSTED = 2
        ACCESS_PROHIBITED = 3
        RESOURCE_TEMPORARILY_EXHAUSTED = 4


class RangeErrorEnum(object):
    class RangeError(enum.IntEnum):
        """
        Enum describing possible range errors.

        Attributes:
          UNSPECIFIED (int): Enum unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          TOO_LOW (int): Too low.
          TOO_HIGH (int): Too high.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        TOO_LOW = 2
        TOO_HIGH = 3


class RealEstatePlaceholderFieldEnum(object):
    class RealEstatePlaceholderField(enum.IntEnum):
        """
        Possible values for Real Estate placeholder fields.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          LISTING_ID (int): Data Type: STRING. Unique ID.
          LISTING_NAME (int): Data Type: STRING. Main headline with listing name to be shown in dynamic
          ad.
          CITY_NAME (int): Data Type: STRING. City name to be shown in dynamic ad.
          DESCRIPTION (int): Data Type: STRING. Description of listing to be shown in dynamic ad.
          ADDRESS (int): Data Type: STRING. Complete listing address, including postal code.
          PRICE (int): Data Type: STRING. Price to be shown in the ad.
          Example: "100.00 USD"
          FORMATTED_PRICE (int): Data Type: STRING. Formatted price to be shown in the ad.
          Example: "Starting at $100.00 USD", "$80 - $100"
          IMAGE_URL (int): Data Type: URL. Image to be displayed in the ad.
          PROPERTY_TYPE (int): Data Type: STRING. Type of property (house, condo, apartment, etc.) used
          to group like items together for recommendation engine.
          LISTING_TYPE (int): Data Type: STRING. Type of listing (resale, rental, foreclosure, etc.)
          used to group like items together for recommendation engine.
          CONTEXTUAL_KEYWORDS (int): Data Type: STRING\_LIST. Keywords used for product retrieval.
          FINAL_URLS (int): Data Type: URL\_LIST. Final URLs to be used in ad when using Upgraded
          URLs; the more specific the better (e.g. the individual URL of a
          specific listing and its location).
          FINAL_MOBILE_URLS (int): Data Type: URL\_LIST. Final mobile URLs for the ad when using Upgraded
          URLs.
          TRACKING_URL (int): Data Type: URL. Tracking template for the ad when using Upgraded URLs.
          ANDROID_APP_LINK (int): Data Type: STRING. Android app link. Must be formatted as:
          android-app://{package\_id}/{scheme}/{host\_path}. The components are
          defined as follows: package\_id: app ID as specified in Google Play.
          scheme: the scheme to pass to the application. Can be HTTP, or a custom
          scheme. host\_path: identifies the specific content within your
          application.
          SIMILAR_LISTING_IDS (int): Data Type: STRING\_LIST. List of recommended listing IDs to show
          together with this item.
          IOS_APP_LINK (int): Data Type: STRING. iOS app link.
          IOS_APP_STORE_ID (int): Data Type: INT64. iOS app store ID.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        LISTING_ID = 2
        LISTING_NAME = 3
        CITY_NAME = 4
        DESCRIPTION = 5
        ADDRESS = 6
        PRICE = 7
        FORMATTED_PRICE = 8
        IMAGE_URL = 9
        PROPERTY_TYPE = 10
        LISTING_TYPE = 11
        CONTEXTUAL_KEYWORDS = 12
        FINAL_URLS = 13
        FINAL_MOBILE_URLS = 14
        TRACKING_URL = 15
        ANDROID_APP_LINK = 16
        SIMILAR_LISTING_IDS = 17
        IOS_APP_LINK = 18
        IOS_APP_STORE_ID = 19


class RecommendationErrorEnum(object):
    class RecommendationError(enum.IntEnum):
        """
        Enum describing possible errors from applying a recommendation.

        Attributes:
          UNSPECIFIED (int): Enum unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          BUDGET_AMOUNT_TOO_SMALL (int): The specified budget amount is too low e.g. lower than minimum currency
          unit or lower than ad group minimum cost-per-click.
          BUDGET_AMOUNT_TOO_LARGE (int): The specified budget amount is too large.
          INVALID_BUDGET_AMOUNT (int): The specified budget amount is not a valid amount. e.g. not a multiple
          of minimum currency unit.
          POLICY_ERROR (int): The specified keyword or ad violates ad policy.
          INVALID_BID_AMOUNT (int): The specified bid amount is not valid. e.g. too many fractional digits,
          or negative amount.
          ADGROUP_KEYWORD_LIMIT (int): The number of keywords in ad group have reached the maximum allowed.
          RECOMMENDATION_ALREADY_APPLIED (int): The recommendation requested to apply has already been applied.
          RECOMMENDATION_INVALIDATED (int): The recommendation requested to apply has been invalidated.
          TOO_MANY_OPERATIONS (int): The number of operations in a single request exceeds the maximum allowed.
          NO_OPERATIONS (int): There are no operations in the request.
          DIFFERENT_TYPES_NOT_SUPPORTED (int): Operations with multiple recommendation types are not supported when
          partial failure mode is not enabled.
          DUPLICATE_RESOURCE_NAME (int): Request contains multiple operations with the same resource\_name.
          RECOMMENDATION_ALREADY_DISMISSED (int): The recommendation requested to dismiss has already been dismissed.
          INVALID_APPLY_REQUEST (int): The recommendation apply request was malformed and invalid.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        BUDGET_AMOUNT_TOO_SMALL = 2
        BUDGET_AMOUNT_TOO_LARGE = 3
        INVALID_BUDGET_AMOUNT = 4
        POLICY_ERROR = 5
        INVALID_BID_AMOUNT = 6
        ADGROUP_KEYWORD_LIMIT = 7
        RECOMMENDATION_ALREADY_APPLIED = 8
        RECOMMENDATION_INVALIDATED = 9
        TOO_MANY_OPERATIONS = 10
        NO_OPERATIONS = 11
        DIFFERENT_TYPES_NOT_SUPPORTED = 12
        DUPLICATE_RESOURCE_NAME = 13
        RECOMMENDATION_ALREADY_DISMISSED = 14
        INVALID_APPLY_REQUEST = 15


class RecommendationTypeEnum(object):
    class RecommendationType(enum.IntEnum):
        """
        Types of recommendations.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          CAMPAIGN_BUDGET (int): Budget recommendation for budget constrained campaigns.
          KEYWORD (int): Keyword recommendation.
          TEXT_AD (int): Recommendation to add a new text ad.
          TARGET_CPA_OPT_IN (int): Recommendation to update a campaign to use a Target CPA bidding strategy.
          MAXIMIZE_CONVERSIONS_OPT_IN (int): Recommendation to update a campaign to use the Maximize Conversions
          bidding strategy.
          ENHANCED_CPC_OPT_IN (int): Recommendation to enable Enhanced Cost Per Click for a campaign.
          SEARCH_PARTNERS_OPT_IN (int): Recommendation to start showing your campaign's ads on Google Search
          Partners Websites.
          MAXIMIZE_CLICKS_OPT_IN (int): Recommendation to update a campaign to use a Maximize Clicks bidding
          strategy.
          OPTIMIZE_AD_ROTATION (int): Recommendation to start using the "Optimize" ad rotation setting for the
          given ad group.
          CALLOUT_EXTENSION (int): Recommendation to add callout extensions to a campaign.
          SITELINK_EXTENSION (int): Recommendation to add sitelink extensions to a campaign.
          CALL_EXTENSION (int): Recommendation to add call extensions to a campaign.
          KEYWORD_MATCH_TYPE (int): Recommendation to change an existing keyword from one match type to a
          broader match type.
          MOVE_UNUSED_BUDGET (int): Recommendation to move unused budget from one budget to a constrained
          budget.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        CAMPAIGN_BUDGET = 2
        KEYWORD = 3
        TEXT_AD = 4
        TARGET_CPA_OPT_IN = 5
        MAXIMIZE_CONVERSIONS_OPT_IN = 6
        ENHANCED_CPC_OPT_IN = 7
        SEARCH_PARTNERS_OPT_IN = 8
        MAXIMIZE_CLICKS_OPT_IN = 9
        OPTIMIZE_AD_ROTATION = 10
        CALLOUT_EXTENSION = 11
        SITELINK_EXTENSION = 12
        CALL_EXTENSION = 13
        KEYWORD_MATCH_TYPE = 14
        MOVE_UNUSED_BUDGET = 15


class RegionCodeErrorEnum(object):
    class RegionCodeError(enum.IntEnum):
        """
        Enum describing possible region code errors.

        Attributes:
          UNSPECIFIED (int): Enum unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          INVALID_REGION_CODE (int): Invalid region code.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        INVALID_REGION_CODE = 2


class RequestErrorEnum(object):
    class RequestError(enum.IntEnum):
        """
        Enum describing possible request errors.

        Attributes:
          UNSPECIFIED (int): Enum unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          RESOURCE_NAME_MISSING (int): Resource name is required for this request.
          RESOURCE_NAME_MALFORMED (int): Resource name provided is malformed.
          BAD_RESOURCE_ID (int): Resource name provided is malformed.
          INVALID_CUSTOMER_ID (int): Customer ID is invalid.
          OPERATION_REQUIRED (int): Mutate operation should have either create, update, or remove specified.
          RESOURCE_NOT_FOUND (int): Requested resource not found.
          INVALID_PAGE_TOKEN (int): Next page token specified in user request is invalid.
          EXPIRED_PAGE_TOKEN (int): Next page token specified in user request has expired.
          INVALID_PAGE_SIZE (int): Page size specified in user request is invalid.
          REQUIRED_FIELD_MISSING (int): Required field is missing.
          IMMUTABLE_FIELD (int): The field cannot be modified because it's immutable. It's also possible
          that the field can be modified using 'create' operation but not 'update'.
          TOO_MANY_MUTATE_OPERATIONS (int): Received too many entries in request.
          CANNOT_BE_EXECUTED_BY_MANAGER_ACCOUNT (int): Request cannot be executed by a manager account.
          CANNOT_MODIFY_FOREIGN_FIELD (int): Mutate request was attempting to modify a readonly field.
          For instance, Budget fields can be requested for Ad Group,
          but are read-only for adGroups:mutate.
          INVALID_ENUM_VALUE (int): Enum value is not permitted.
          DEVELOPER_TOKEN_PARAMETER_MISSING (int): The developer-token parameter is required for all requests.
          LOGIN_CUSTOMER_ID_PARAMETER_MISSING (int): The login-customer-id parameter is required for this request.
          VALIDATE_ONLY_REQUEST_HAS_PAGE_TOKEN (int): page\_token is set in the validate only request
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        RESOURCE_NAME_MISSING = 3
        RESOURCE_NAME_MALFORMED = 4
        BAD_RESOURCE_ID = 17
        INVALID_CUSTOMER_ID = 16
        OPERATION_REQUIRED = 5
        RESOURCE_NOT_FOUND = 6
        INVALID_PAGE_TOKEN = 7
        EXPIRED_PAGE_TOKEN = 8
        INVALID_PAGE_SIZE = 22
        REQUIRED_FIELD_MISSING = 9
        IMMUTABLE_FIELD = 11
        TOO_MANY_MUTATE_OPERATIONS = 13
        CANNOT_BE_EXECUTED_BY_MANAGER_ACCOUNT = 14
        CANNOT_MODIFY_FOREIGN_FIELD = 15
        INVALID_ENUM_VALUE = 18
        DEVELOPER_TOKEN_PARAMETER_MISSING = 19
        LOGIN_CUSTOMER_ID_PARAMETER_MISSING = 20
        VALIDATE_ONLY_REQUEST_HAS_PAGE_TOKEN = 21


class ResourceAccessDeniedErrorEnum(object):
    class ResourceAccessDeniedError(enum.IntEnum):
        """
        Enum describing possible resource access denied errors.

        Attributes:
          UNSPECIFIED (int): Enum unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          WRITE_ACCESS_DENIED (int): User did not have write access.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        WRITE_ACCESS_DENIED = 3


class ResourceCountLimitExceededErrorEnum(object):
    class ResourceCountLimitExceededError(enum.IntEnum):
        """
        Enum describing possible resource count limit exceeded errors.

        Attributes:
          UNSPECIFIED (int): Enum unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          ACCOUNT_LIMIT (int): Indicates that this request would exceed the number of allowed resources
          for the Google Ads account. The exact resource type and limit being
          checked can be inferred from accountLimitType.
          CAMPAIGN_LIMIT (int): Indicates that this request would exceed the number of allowed resources
          in a Campaign. The exact resource type and limit being checked can be
          inferred from accountLimitType, and the numeric id of the
          Campaign involved is given by enclosingId.
          ADGROUP_LIMIT (int): Indicates that this request would exceed the number of allowed resources
          in an ad group. The exact resource type and limit being checked can be
          inferred from accountLimitType, and the numeric id of the
          ad group involved is given by enclosingId.
          AD_GROUP_AD_LIMIT (int): Indicates that this request would exceed the number of allowed resources
          in an ad group ad. The exact resource type and limit being checked can
          be inferred from accountLimitType, and the enclosingId
          contains the ad group id followed by the ad id, separated by a single
          comma (,).
          AD_GROUP_CRITERION_LIMIT (int): Indicates that this request would exceed the number of allowed resources
          in an ad group criterion. The exact resource type and limit being checked
          can be inferred from accountLimitType, and the
          enclosingId contains the ad group id followed by the
          criterion id, separated by a single comma (,).
          SHARED_SET_LIMIT (int): Indicates that this request would exceed the number of allowed resources
          in this shared set. The exact resource type and limit being checked can
          be inferred from accountLimitType, and the numeric id of the
          shared set involved is given by enclosingId.
          MATCHING_FUNCTION_LIMIT (int): Exceeds a limit related to a matching function.
          RESPONSE_ROW_LIMIT_EXCEEDED (int): The response for this request would exceed the maximum number of rows
          that can be returned.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        ACCOUNT_LIMIT = 2
        CAMPAIGN_LIMIT = 3
        ADGROUP_LIMIT = 4
        AD_GROUP_AD_LIMIT = 5
        AD_GROUP_CRITERION_LIMIT = 6
        SHARED_SET_LIMIT = 7
        MATCHING_FUNCTION_LIMIT = 8
        RESPONSE_ROW_LIMIT_EXCEEDED = 9


class SearchEngineResultsPageTypeEnum(object):
    class SearchEngineResultsPageType(enum.IntEnum):
        """
        The type of the search engine results page.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          ADS_ONLY (int): Only ads were contained in the search engine results page.
          ORGANIC_ONLY (int): Only organic results were contained in the search engine results page.
          ADS_AND_ORGANIC (int): Both ads and organic results were contained in the search engine results
          page.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        ADS_ONLY = 2
        ORGANIC_ONLY = 3
        ADS_AND_ORGANIC = 4


class SearchTermMatchTypeEnum(object):
    class SearchTermMatchType(enum.IntEnum):
        """
        Possible match types for a keyword triggering an ad, including variants.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          BROAD (int): Broad match.
          EXACT (int): Exact match.
          PHRASE (int): Phrase match.
          NEAR_EXACT (int): Exact match (close variant).
          NEAR_PHRASE (int): Phrase match (close variant).
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        BROAD = 2
        EXACT = 3
        PHRASE = 4
        NEAR_EXACT = 5
        NEAR_PHRASE = 6


class SearchTermTargetingStatusEnum(object):
    class SearchTermTargetingStatus(enum.IntEnum):
        """
        Indicates whether the search term is one of your targeted or excluded
        keywords.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          ADDED (int): Search term is added to targeted keywords.
          EXCLUDED (int): Search term matches a negative keyword.
          ADDED_EXCLUDED (int): Search term has been both added and excluded.
          NONE (int): Search term is neither targeted nor excluded.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        ADDED = 2
        EXCLUDED = 3
        ADDED_EXCLUDED = 4
        NONE = 5


class ServedAssetFieldTypeEnum(object):
    class ServedAssetFieldType(enum.IntEnum):
        """
        The possible asset field types.

        Attributes:
          UNSPECIFIED (int): No value has been specified.
          UNKNOWN (int): The received value is not known in this version.

          This is a response-only value.
          HEADLINE_1 (int): The asset is used in headline 1.
          HEADLINE_2 (int): The asset is used in headline 2.
          HEADLINE_3 (int): The asset is used in headline 3.
          DESCRIPTION_1 (int): The asset is used in description 1.
          DESCRIPTION_2 (int): The asset is used in description 2.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        HEADLINE_1 = 2
        HEADLINE_2 = 3
        HEADLINE_3 = 4
        DESCRIPTION_1 = 5
        DESCRIPTION_2 = 6


class SettingErrorEnum(object):
    class SettingError(enum.IntEnum):
        """
        Enum describing possible setting errors.

        Attributes:
          UNSPECIFIED (int): Enum unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          SETTING_TYPE_IS_NOT_AVAILABLE (int): The campaign setting is not available for this Google Ads account.
          SETTING_TYPE_IS_NOT_COMPATIBLE_WITH_CAMPAIGN (int): The setting is not compatible with the campaign.
          TARGETING_SETTING_CONTAINS_INVALID_CRITERION_TYPE_GROUP (int): The supplied TargetingSetting contains an invalid CriterionTypeGroup. See
          CriterionTypeGroup documentation for CriterionTypeGroups allowed
          in Campaign or AdGroup TargetingSettings.
          TARGETING_SETTING_DEMOGRAPHIC_CRITERION_TYPE_GROUPS_MUST_BE_SET_TO_TARGET_ALL (int): TargetingSetting must not explicitly set any of the Demographic
          CriterionTypeGroups (AGE\_RANGE, GENDER, PARENT, INCOME\_RANGE) to false
          (it's okay to not set them at all, in which case the system will set
          them to true automatically).
          TARGETING_SETTING_CANNOT_CHANGE_TARGET_ALL_TO_FALSE_FOR_DEMOGRAPHIC_CRITERION_TYPE_GROUP (int): TargetingSetting cannot change any of the Demographic
          CriterionTypeGroups (AGE\_RANGE, GENDER, PARENT, INCOME\_RANGE) from
          true to false.
          DYNAMIC_SEARCH_ADS_SETTING_AT_LEAST_ONE_FEED_ID_MUST_BE_PRESENT (int): At least one feed id should be present.
          DYNAMIC_SEARCH_ADS_SETTING_CONTAINS_INVALID_DOMAIN_NAME (int): The supplied DynamicSearchAdsSetting contains an invalid domain name.
          DYNAMIC_SEARCH_ADS_SETTING_CONTAINS_SUBDOMAIN_NAME (int): The supplied DynamicSearchAdsSetting contains a subdomain name.
          DYNAMIC_SEARCH_ADS_SETTING_CONTAINS_INVALID_LANGUAGE_CODE (int): The supplied DynamicSearchAdsSetting contains an invalid language code.
          TARGET_ALL_IS_NOT_ALLOWED_FOR_PLACEMENT_IN_SEARCH_CAMPAIGN (int): TargetingSettings in search campaigns should not have
          CriterionTypeGroup.PLACEMENT set to targetAll.
          UNIVERSAL_APP_CAMPAIGN_SETTING_DUPLICATE_DESCRIPTION (int): Duplicate description in universal app setting description field.
          UNIVERSAL_APP_CAMPAIGN_SETTING_DESCRIPTION_LINE_WIDTH_TOO_LONG (int): Description line width is too long in universal app setting description
          field.
          UNIVERSAL_APP_CAMPAIGN_SETTING_APP_ID_CANNOT_BE_MODIFIED (int): Universal app setting appId field cannot be modified for COMPLETE
          campaigns.
          TOO_MANY_YOUTUBE_MEDIA_IDS_IN_UNIVERSAL_APP_CAMPAIGN (int): YoutubeVideoMediaIds in universal app setting cannot exceed size limit.
          TOO_MANY_IMAGE_MEDIA_IDS_IN_UNIVERSAL_APP_CAMPAIGN (int): ImageMediaIds in universal app setting cannot exceed size limit.
          MEDIA_INCOMPATIBLE_FOR_UNIVERSAL_APP_CAMPAIGN (int): Media is incompatible for universal app campaign.
          TOO_MANY_EXCLAMATION_MARKS (int): Too many exclamation marks in universal app campaign ad text ideas.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        SETTING_TYPE_IS_NOT_AVAILABLE = 3
        SETTING_TYPE_IS_NOT_COMPATIBLE_WITH_CAMPAIGN = 4
        TARGETING_SETTING_CONTAINS_INVALID_CRITERION_TYPE_GROUP = 5
        TARGETING_SETTING_DEMOGRAPHIC_CRITERION_TYPE_GROUPS_MUST_BE_SET_TO_TARGET_ALL = 6
        TARGETING_SETTING_CANNOT_CHANGE_TARGET_ALL_TO_FALSE_FOR_DEMOGRAPHIC_CRITERION_TYPE_GROUP = 7
        DYNAMIC_SEARCH_ADS_SETTING_AT_LEAST_ONE_FEED_ID_MUST_BE_PRESENT = 8
        DYNAMIC_SEARCH_ADS_SETTING_CONTAINS_INVALID_DOMAIN_NAME = 9
        DYNAMIC_SEARCH_ADS_SETTING_CONTAINS_SUBDOMAIN_NAME = 10
        DYNAMIC_SEARCH_ADS_SETTING_CONTAINS_INVALID_LANGUAGE_CODE = 11
        TARGET_ALL_IS_NOT_ALLOWED_FOR_PLACEMENT_IN_SEARCH_CAMPAIGN = 12
        UNIVERSAL_APP_CAMPAIGN_SETTING_DUPLICATE_DESCRIPTION = 13
        UNIVERSAL_APP_CAMPAIGN_SETTING_DESCRIPTION_LINE_WIDTH_TOO_LONG = 14
        UNIVERSAL_APP_CAMPAIGN_SETTING_APP_ID_CANNOT_BE_MODIFIED = 15
        TOO_MANY_YOUTUBE_MEDIA_IDS_IN_UNIVERSAL_APP_CAMPAIGN = 16
        TOO_MANY_IMAGE_MEDIA_IDS_IN_UNIVERSAL_APP_CAMPAIGN = 17
        MEDIA_INCOMPATIBLE_FOR_UNIVERSAL_APP_CAMPAIGN = 18
        TOO_MANY_EXCLAMATION_MARKS = 19


class SharedCriterionErrorEnum(object):
    class SharedCriterionError(enum.IntEnum):
        """
        Enum describing possible shared criterion errors.

        Attributes:
          UNSPECIFIED (int): Enum unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          CRITERION_TYPE_NOT_ALLOWED_FOR_SHARED_SET_TYPE (int): The criterion is not appropriate for the shared set type.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        CRITERION_TYPE_NOT_ALLOWED_FOR_SHARED_SET_TYPE = 2


class SharedSetErrorEnum(object):
    class SharedSetError(enum.IntEnum):
        """
        Enum describing possible shared set errors.

        Attributes:
          UNSPECIFIED (int): Enum unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          CUSTOMER_CANNOT_CREATE_SHARED_SET_OF_THIS_TYPE (int): The customer cannot create this type of shared set.
          DUPLICATE_NAME (int): A shared set with this name already exists.
          SHARED_SET_REMOVED (int): Removed shared sets cannot be mutated.
          SHARED_SET_IN_USE (int): The shared set cannot be removed because it is in use.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        CUSTOMER_CANNOT_CREATE_SHARED_SET_OF_THIS_TYPE = 2
        DUPLICATE_NAME = 3
        SHARED_SET_REMOVED = 4
        SHARED_SET_IN_USE = 5


class SharedSetStatusEnum(object):
    class SharedSetStatus(enum.IntEnum):
        """
        Enum listing the possible shared set statuses.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          ENABLED (int): The shared set is enabled.
          REMOVED (int): The shared set is removed and can no longer be used.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        ENABLED = 2
        REMOVED = 3


class SharedSetTypeEnum(object):
    class SharedSetType(enum.IntEnum):
        """
        Enum listing the possible shared set types.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          NEGATIVE_KEYWORDS (int): A set of keywords that can be excluded from targeting.
          NEGATIVE_PLACEMENTS (int): A set of placements that can be excluded from targeting.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        NEGATIVE_KEYWORDS = 2
        NEGATIVE_PLACEMENTS = 3


class SimulationModificationMethodEnum(object):
    class SimulationModificationMethod(enum.IntEnum):
        """
        Enum describing the method by which a simulation modifies a field.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          UNIFORM (int): The values in a simulation were applied to all children of a given
          resource uniformly. Overrides on child resources were not respected.
          DEFAULT (int): The values in a simulation were applied to the given resource.
          Overrides on child resources were respected, and traffic estimates
          do not include these resources.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        UNIFORM = 2
        DEFAULT = 3


class SimulationTypeEnum(object):
    class SimulationType(enum.IntEnum):
        """
        Enum describing the field a simulation modifies.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          CPC_BID (int): The simulation is for a cpc bid.
          CPV_BID (int): The simulation is for a cpv bid.
          TARGET_CPA (int): The simulation is for a cpa target.
          BID_MODIFIER (int): The simulation is for a bid modifier.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        CPC_BID = 2
        CPV_BID = 3
        TARGET_CPA = 4
        BID_MODIFIER = 5


class SitelinkPlaceholderFieldEnum(object):
    class SitelinkPlaceholderField(enum.IntEnum):
        """
        Possible values for Sitelink placeholder fields.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          TEXT (int): Data Type: STRING. The link text for your sitelink.
          LINE_1 (int): Data Type: STRING. First line of the sitelink description.
          LINE_2 (int): Data Type: STRING. Second line of the sitelink description.
          FINAL_URLS (int): Data Type: URL\_LIST. Final URLs for the sitelink when using Upgraded
          URLs.
          FINAL_MOBILE_URLS (int): Data Type: URL\_LIST. Final Mobile URLs for the sitelink when using
          Upgraded URLs.
          TRACKING_URL (int): Data Type: URL. Tracking template for the sitelink when using Upgraded
          URLs.
          FINAL_URL_SUFFIX (int): Data Type: STRING. Final URL suffix for sitelink when using parallel
          tracking.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        TEXT = 2
        LINE_1 = 3
        LINE_2 = 4
        FINAL_URLS = 5
        FINAL_MOBILE_URLS = 6
        TRACKING_URL = 7
        FINAL_URL_SUFFIX = 8


class SizeLimitErrorEnum(object):
    class SizeLimitError(enum.IntEnum):
        """
        Enum describing possible size limit errors.

        Attributes:
          UNSPECIFIED (int): Enum unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          REQUEST_SIZE_LIMIT_EXCEEDED (int): The number of entries in the request exceeds the system limit.
          RESPONSE_SIZE_LIMIT_EXCEEDED (int): The number of entries in the response exceeds the system limit.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        REQUEST_SIZE_LIMIT_EXCEEDED = 2
        RESPONSE_SIZE_LIMIT_EXCEEDED = 3


class SlotEnum(object):
    class Slot(enum.IntEnum):
        """
        Enumerates possible positions of the Ad.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): The value is unknown in this version.
          SEARCH_SIDE (int): Google search: Side.
          SEARCH_TOP (int): Google search: Top.
          SEARCH_OTHER (int): Google search: Other.
          CONTENT (int): Google Display Network.
          SEARCH_PARTNER_TOP (int): Search partners: Top.
          SEARCH_PARTNER_OTHER (int): Search partners: Other.
          MIXED (int): Cross-network.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        SEARCH_SIDE = 2
        SEARCH_TOP = 3
        SEARCH_OTHER = 4
        CONTENT = 5
        SEARCH_PARTNER_TOP = 6
        SEARCH_PARTNER_OTHER = 7
        MIXED = 8


class SpendingLimitTypeEnum(object):
    class SpendingLimitType(enum.IntEnum):
        """
        The possible spending limit types used by certain resources as an
        alternative to absolute money values in micros.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          INFINITE (int): Infinite, indicates unlimited spending power.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        INFINITE = 2


class StringFormatErrorEnum(object):
    class StringFormatError(enum.IntEnum):
        """
        Enum describing possible string format errors.

        Attributes:
          UNSPECIFIED (int): Enum unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          ILLEGAL_CHARS (int): The input string value contains disallowed characters.
          INVALID_FORMAT (int): The input string value is invalid for the associated field.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        ILLEGAL_CHARS = 2
        INVALID_FORMAT = 3


class StringLengthErrorEnum(object):
    class StringLengthError(enum.IntEnum):
        """
        Enum describing possible string length errors.

        Attributes:
          UNSPECIFIED (int): Enum unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          TOO_SHORT (int): Too short.
          TOO_LONG (int): Too long.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        TOO_SHORT = 2
        TOO_LONG = 3


class StructuredSnippetPlaceholderFieldEnum(object):
    class StructuredSnippetPlaceholderField(enum.IntEnum):
        """
        Possible values for Structured Snippet placeholder fields.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          HEADER (int): Data Type: STRING. The category of snippet of your products/services.
          Must match one of the predefined structured snippets headers exactly.
          See
          https://developers.google.com/adwords/api
          /docs/appendix/structured-snippet-headers
          SNIPPETS (int): Data Type: STRING\_LIST. Text values that describe your
          products/services. All text must be family safe. Special or non-ASCII
          characters are not permitted. A snippet can be at most 25 characters.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        HEADER = 2
        SNIPPETS = 3


class SystemManagedResourceSourceEnum(object):
    class SystemManagedResourceSource(enum.IntEnum):
        """
        Enum listing the possible system managed entity sources.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          AD_VARIATIONS (int): Generated ad variations experiment ad.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        AD_VARIATIONS = 2


class TargetCpaOptInRecommendationGoalEnum(object):
    class TargetCpaOptInRecommendationGoal(enum.IntEnum):
        """
        Goal of TargetCpaOptIn recommendation.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          SAME_COST (int): Recommendation to set Target CPA to maintain the same cost.
          SAME_CONVERSIONS (int): Recommendation to set Target CPA to maintain the same conversions.
          SAME_CPA (int): Recommendation to set Target CPA to maintain the same CPA.
          CLOSEST_CPA (int): Recommendation to set Target CPA to a value that is as close as possible
          to, yet lower than, the actual CPA (computed for past 28 days).
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        SAME_COST = 2
        SAME_CONVERSIONS = 3
        SAME_CPA = 4
        CLOSEST_CPA = 5


class TargetImpressionShareLocationEnum(object):
    class TargetImpressionShareLocation(enum.IntEnum):
        """
        Enum describing possible goals.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          ANYWHERE_ON_PAGE (int): Any location on the web page.
          TOP_OF_PAGE (int): Top box of ads.
          ABSOLUTE_TOP_OF_PAGE (int): Top slot in the top box of ads.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        ANYWHERE_ON_PAGE = 2
        TOP_OF_PAGE = 3
        ABSOLUTE_TOP_OF_PAGE = 4


class TargetingDimensionEnum(object):
    class TargetingDimension(enum.IntEnum):
        """
        Enum describing possible targeting dimensions.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          KEYWORD (int): Keyword criteria, e.g. 'mars cruise'. KEYWORD may be used as a custom bid
          dimension. Keywords are always a targeting dimension, so may not be set
          as a target "ALL" dimension with TargetRestriction.
          AUDIENCE (int): Audience criteria, which include user list, user interest, custom
          affinity,  and custom in market.
          TOPIC (int): Topic criteria for targeting categories of content, e.g.
          'category::Animals>Pets' Used for Display and Video targeting.
          GENDER (int): Criteria for targeting gender.
          AGE_RANGE (int): Criteria for targeting age ranges.
          PLACEMENT (int): Placement criteria, which include websites like 'www.flowers4sale.com',
          as well as mobile applications, mobile app categories, YouTube videos,
          and YouTube channels.
          PARENTAL_STATUS (int): Criteria for parental status targeting.
          INCOME_RANGE (int): Criteria for income range targeting.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        KEYWORD = 2
        AUDIENCE = 3
        TOPIC = 4
        GENDER = 5
        AGE_RANGE = 6
        PLACEMENT = 7
        PARENTAL_STATUS = 8
        INCOME_RANGE = 9


class TimeTypeEnum(object):
    class TimeType(enum.IntEnum):
        """
        The possible time types used by certain resources as an alternative to
        absolute timestamps.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          NOW (int): As soon as possible.
          FOREVER (int): An infinite point in the future.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        NOW = 2
        FOREVER = 3


class TrackingCodePageFormatEnum(object):
    class TrackingCodePageFormat(enum.IntEnum):
        """
        The format of the web page where the tracking tag and snippet will be
        installed.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          HTML (int): Standard HTML page format.
          AMP (int): Google AMP page format.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        HTML = 2
        AMP = 3


class TrackingCodeTypeEnum(object):
    class TrackingCodeType(enum.IntEnum):
        """
        The type of the generated tag snippets for tracking conversions.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          WEBPAGE (int): The snippet that is fired as a result of a website page loading.
          WEBPAGE_ONCLICK (int): The snippet contains a JavaScript function which fires the tag. This
          function is typically called from an onClick handler added to a link or
          button element on the page.
          CLICK_TO_CALL (int): For embedding on a mobile webpage. The snippet contains a JavaScript
          function which fires the tag.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        WEBPAGE = 2
        WEBPAGE_ONCLICK = 3
        CLICK_TO_CALL = 4


class TravelPlaceholderFieldEnum(object):
    class TravelPlaceholderField(enum.IntEnum):
        """
        Possible values for Travel placeholder fields.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          DESTINATION_ID (int): Data Type: STRING. Required. Destination id. Example: PAR, LON.
          For feed items that only have destination id, destination id must be a
          unique key. For feed items that have both destination id and origin id,
          then the combination must be a unique key.
          ORIGIN_ID (int): Data Type: STRING. Origin id. Example: PAR, LON. Combination of
          DESTINATION\_ID and ORIGIN\_ID must be unique per offer.
          TITLE (int): Data Type: STRING. Required. Main headline with name to be shown in
          dynamic ad.
          DESTINATION_NAME (int): Data Type: STRING. The destination name. Shorter names are recommended.
          ORIGIN_NAME (int): Data Type: STRING. Origin name. Shorter names are recommended.
          PRICE (int): Data Type: STRING. Price to be shown in the ad. Highly recommended for
          dynamic ads.
          Example: "100.00 USD"
          FORMATTED_PRICE (int): Data Type: STRING. Formatted price to be shown in the ad.
          Example: "Starting at $100.00 USD", "$80 - $100"
          SALE_PRICE (int): Data Type: STRING. Sale price to be shown in the ad.
          Example: "80.00 USD"
          FORMATTED_SALE_PRICE (int): Data Type: STRING. Formatted sale price to be shown in the ad.
          Example: "On sale for $80.00", "$60 - $80"
          IMAGE_URL (int): Data Type: URL. Image to be displayed in the ad.
          CATEGORY (int): Data Type: STRING. Category of travel offer used to group like items
          together for recommendation engine.
          CONTEXTUAL_KEYWORDS (int): Data Type: STRING\_LIST. Keywords used for product retrieval.
          DESTINATION_ADDRESS (int): Data Type: STRING. Address of travel offer, including postal code.
          FINAL_URL (int): Data Type: URL\_LIST. Required. Final URLs to be used in ad, when using
          Upgraded URLs; the more specific the better (e.g. the individual URL of
          a specific travel offer and its location).
          FINAL_MOBILE_URLS (int): Data Type: URL\_LIST. Final mobile URLs for the ad when using Upgraded
          URLs.
          TRACKING_URL (int): Data Type: URL. Tracking template for the ad when using Upgraded URLs.
          ANDROID_APP_LINK (int): Data Type: STRING. Android app link. Must be formatted as:
          android-app://{package\_id}/{scheme}/{host\_path}. The components are
          defined as follows: package\_id: app ID as specified in Google Play.
          scheme: the scheme to pass to the application. Can be HTTP, or a custom
          scheme. host\_path: identifies the specific content within your
          application.
          SIMILAR_DESTINATION_IDS (int): Data Type: STRING\_LIST. List of recommended destination IDs to show
          together with this item.
          IOS_APP_LINK (int): Data Type: STRING. iOS app link.
          IOS_APP_STORE_ID (int): Data Type: INT64. iOS app store ID.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        DESTINATION_ID = 2
        ORIGIN_ID = 3
        TITLE = 4
        DESTINATION_NAME = 5
        ORIGIN_NAME = 6
        PRICE = 7
        FORMATTED_PRICE = 8
        SALE_PRICE = 9
        FORMATTED_SALE_PRICE = 10
        IMAGE_URL = 11
        CATEGORY = 12
        CONTEXTUAL_KEYWORDS = 13
        DESTINATION_ADDRESS = 14
        FINAL_URL = 15
        FINAL_MOBILE_URLS = 16
        TRACKING_URL = 17
        ANDROID_APP_LINK = 18
        SIMILAR_DESTINATION_IDS = 19
        IOS_APP_LINK = 20
        IOS_APP_STORE_ID = 21


class UrlFieldErrorEnum(object):
    class UrlFieldError(enum.IntEnum):
        """
        Enum describing possible url field errors.

        Attributes:
          UNSPECIFIED (int): Enum unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          INVALID_TRACKING_URL_TEMPLATE (int): The tracking url template is invalid.
          INVALID_TAG_IN_TRACKING_URL_TEMPLATE (int): The tracking url template contains invalid tag.
          MISSING_TRACKING_URL_TEMPLATE_TAG (int): The tracking url template must contain at least one tag (e.g. {lpurl}),
          This applies only to tracking url template associated with website ads or
          product ads.
          MISSING_PROTOCOL_IN_TRACKING_URL_TEMPLATE (int): The tracking url template must start with a valid protocol (or lpurl
          tag).
          INVALID_PROTOCOL_IN_TRACKING_URL_TEMPLATE (int): The tracking url template starts with an invalid protocol.
          MALFORMED_TRACKING_URL_TEMPLATE (int): The tracking url template contains illegal characters.
          MISSING_HOST_IN_TRACKING_URL_TEMPLATE (int): The tracking url template must contain a host name (or lpurl tag).
          INVALID_TLD_IN_TRACKING_URL_TEMPLATE (int): The tracking url template has an invalid or missing top level domain
          extension.
          REDUNDANT_NESTED_TRACKING_URL_TEMPLATE_TAG (int): The tracking url template contains nested occurrences of the same
          conditional tag (i.e. {ifmobile:{ifmobile:x}}).
          INVALID_FINAL_URL (int): The final url is invalid.
          INVALID_TAG_IN_FINAL_URL (int): The final url contains invalid tag.
          REDUNDANT_NESTED_FINAL_URL_TAG (int): The final url contains nested occurrences of the same conditional tag
          (i.e. {ifmobile:{ifmobile:x}}).
          MISSING_PROTOCOL_IN_FINAL_URL (int): The final url must start with a valid protocol.
          INVALID_PROTOCOL_IN_FINAL_URL (int): The final url starts with an invalid protocol.
          MALFORMED_FINAL_URL (int): The final url contains illegal characters.
          MISSING_HOST_IN_FINAL_URL (int): The final url must contain a host name.
          INVALID_TLD_IN_FINAL_URL (int): The tracking url template has an invalid or missing top level domain
          extension.
          INVALID_FINAL_MOBILE_URL (int): The final mobile url is invalid.
          INVALID_TAG_IN_FINAL_MOBILE_URL (int): The final mobile url contains invalid tag.
          REDUNDANT_NESTED_FINAL_MOBILE_URL_TAG (int): The final mobile url contains nested occurrences of the same conditional
          tag (i.e. {ifmobile:{ifmobile:x}}).
          MISSING_PROTOCOL_IN_FINAL_MOBILE_URL (int): The final mobile url must start with a valid protocol.
          INVALID_PROTOCOL_IN_FINAL_MOBILE_URL (int): The final mobile url starts with an invalid protocol.
          MALFORMED_FINAL_MOBILE_URL (int): The final mobile url contains illegal characters.
          MISSING_HOST_IN_FINAL_MOBILE_URL (int): The final mobile url must contain a host name.
          INVALID_TLD_IN_FINAL_MOBILE_URL (int): The tracking url template has an invalid or missing top level domain
          extension.
          INVALID_FINAL_APP_URL (int): The final app url is invalid.
          INVALID_TAG_IN_FINAL_APP_URL (int): The final app url contains invalid tag.
          REDUNDANT_NESTED_FINAL_APP_URL_TAG (int): The final app url contains nested occurrences of the same conditional tag
          (i.e. {ifmobile:{ifmobile:x}}).
          MULTIPLE_APP_URLS_FOR_OSTYPE (int): More than one app url found for the same OS type.
          INVALID_OSTYPE (int): The OS type given for an app url is not valid.
          INVALID_PROTOCOL_FOR_APP_URL (int): The protocol given for an app url is not valid. (E.g. "android-app://")
          INVALID_PACKAGE_ID_FOR_APP_URL (int): The package id (app id) given for an app url is not valid.
          URL_CUSTOM_PARAMETERS_COUNT_EXCEEDS_LIMIT (int): The number of url custom parameters for an resource exceeds the maximum
          limit allowed.
          INVALID_CHARACTERS_IN_URL_CUSTOM_PARAMETER_KEY (int): An invalid character appears in the parameter key.
          INVALID_CHARACTERS_IN_URL_CUSTOM_PARAMETER_VALUE (int): An invalid character appears in the parameter value.
          INVALID_TAG_IN_URL_CUSTOM_PARAMETER_VALUE (int): The url custom parameter value fails url tag validation.
          REDUNDANT_NESTED_URL_CUSTOM_PARAMETER_TAG (int): The custom parameter contains nested occurrences of the same conditional
          tag (i.e. {ifmobile:{ifmobile:x}}).
          MISSING_PROTOCOL (int): The protocol (http:// or https://) is missing.
          INVALID_PROTOCOL (int): Unsupported protocol in URL. Only http and https are supported.
          INVALID_URL (int): The url is invalid.
          DESTINATION_URL_DEPRECATED (int): Destination Url is deprecated.
          INVALID_TAG_IN_URL (int): The url contains invalid tag.
          MISSING_URL_TAG (int): The url must contain at least one tag (e.g. {lpurl}), This applies only
          to urls associated with website ads or product ads.
          DUPLICATE_URL_ID (int): Duplicate url id.
          INVALID_URL_ID (int): Invalid url id.
          FINAL_URL_SUFFIX_MALFORMED (int): The final url suffix cannot begin with '?' or '&' characters and must be
          a valid query string.
          INVALID_TAG_IN_FINAL_URL_SUFFIX (int): The final url suffix cannot contain {lpurl} related or {ignore} tags.
          INVALID_TOP_LEVEL_DOMAIN (int): The top level domain is invalid, e.g, not a public top level domain
          listed in publicsuffix.org.
          MALFORMED_TOP_LEVEL_DOMAIN (int): Malformed top level domain in URL.
          MALFORMED_URL (int): Malformed URL.
          MISSING_HOST (int): No host found in URL.
          NULL_CUSTOM_PARAMETER_VALUE (int): Custom parameter value cannot be null.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        INVALID_TRACKING_URL_TEMPLATE = 2
        INVALID_TAG_IN_TRACKING_URL_TEMPLATE = 3
        MISSING_TRACKING_URL_TEMPLATE_TAG = 4
        MISSING_PROTOCOL_IN_TRACKING_URL_TEMPLATE = 5
        INVALID_PROTOCOL_IN_TRACKING_URL_TEMPLATE = 6
        MALFORMED_TRACKING_URL_TEMPLATE = 7
        MISSING_HOST_IN_TRACKING_URL_TEMPLATE = 8
        INVALID_TLD_IN_TRACKING_URL_TEMPLATE = 9
        REDUNDANT_NESTED_TRACKING_URL_TEMPLATE_TAG = 10
        INVALID_FINAL_URL = 11
        INVALID_TAG_IN_FINAL_URL = 12
        REDUNDANT_NESTED_FINAL_URL_TAG = 13
        MISSING_PROTOCOL_IN_FINAL_URL = 14
        INVALID_PROTOCOL_IN_FINAL_URL = 15
        MALFORMED_FINAL_URL = 16
        MISSING_HOST_IN_FINAL_URL = 17
        INVALID_TLD_IN_FINAL_URL = 18
        INVALID_FINAL_MOBILE_URL = 19
        INVALID_TAG_IN_FINAL_MOBILE_URL = 20
        REDUNDANT_NESTED_FINAL_MOBILE_URL_TAG = 21
        MISSING_PROTOCOL_IN_FINAL_MOBILE_URL = 22
        INVALID_PROTOCOL_IN_FINAL_MOBILE_URL = 23
        MALFORMED_FINAL_MOBILE_URL = 24
        MISSING_HOST_IN_FINAL_MOBILE_URL = 25
        INVALID_TLD_IN_FINAL_MOBILE_URL = 26
        INVALID_FINAL_APP_URL = 27
        INVALID_TAG_IN_FINAL_APP_URL = 28
        REDUNDANT_NESTED_FINAL_APP_URL_TAG = 29
        MULTIPLE_APP_URLS_FOR_OSTYPE = 30
        INVALID_OSTYPE = 31
        INVALID_PROTOCOL_FOR_APP_URL = 32
        INVALID_PACKAGE_ID_FOR_APP_URL = 33
        URL_CUSTOM_PARAMETERS_COUNT_EXCEEDS_LIMIT = 34
        INVALID_CHARACTERS_IN_URL_CUSTOM_PARAMETER_KEY = 39
        INVALID_CHARACTERS_IN_URL_CUSTOM_PARAMETER_VALUE = 40
        INVALID_TAG_IN_URL_CUSTOM_PARAMETER_VALUE = 41
        REDUNDANT_NESTED_URL_CUSTOM_PARAMETER_TAG = 42
        MISSING_PROTOCOL = 43
        INVALID_PROTOCOL = 52
        INVALID_URL = 44
        DESTINATION_URL_DEPRECATED = 45
        INVALID_TAG_IN_URL = 46
        MISSING_URL_TAG = 47
        DUPLICATE_URL_ID = 48
        INVALID_URL_ID = 49
        FINAL_URL_SUFFIX_MALFORMED = 50
        INVALID_TAG_IN_FINAL_URL_SUFFIX = 51
        INVALID_TOP_LEVEL_DOMAIN = 53
        MALFORMED_TOP_LEVEL_DOMAIN = 54
        MALFORMED_URL = 55
        MISSING_HOST = 56
        NULL_CUSTOM_PARAMETER_VALUE = 57


class UserInterestTaxonomyTypeEnum(object):
    class UserInterestTaxonomyType(enum.IntEnum):
        """
        Enum containing the possible UserInterestTaxonomyTypes.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          AFFINITY (int): The affinity for this user interest.
          IN_MARKET (int): The market for this user interest.
          MOBILE_APP_INSTALL_USER (int): Users known to have installed applications in the specified categories.
          VERTICAL_GEO (int): The geographical location of the interest-based vertical.
          NEW_SMART_PHONE_USER (int): User interest criteria for new smart phone users.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        AFFINITY = 2
        IN_MARKET = 3
        MOBILE_APP_INSTALL_USER = 4
        VERTICAL_GEO = 5
        NEW_SMART_PHONE_USER = 6


class UserListAccessStatusEnum(object):
    class UserListAccessStatus(enum.IntEnum):
        """
        Enum containing possible user list access statuses.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          ENABLED (int): The access is enabled.
          DISABLED (int): The access is disabled.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        ENABLED = 2
        DISABLED = 3


class UserListClosingReasonEnum(object):
    class UserListClosingReason(enum.IntEnum):
        """
        Enum describing possible user list closing reasons.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          UNUSED (int): The userlist was closed because of not being used for over one year.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        UNUSED = 2


class UserListCombinedRuleOperatorEnum(object):
    class UserListCombinedRuleOperator(enum.IntEnum):
        """
        Enum describing possible user list combined rule operators.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          AND (int): A AND B.
          AND_NOT (int): A AND NOT B.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        AND = 2
        AND_NOT = 3


class UserListCrmDataSourceTypeEnum(object):
    class UserListCrmDataSourceType(enum.IntEnum):
        """
        Enum describing possible user list crm data source type.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          FIRST_PARTY (int): The uploaded data is first-party data.
          THIRD_PARTY_CREDIT_BUREAU (int): The uploaded data is from a third-party credit bureau.
          THIRD_PARTY_VOTER_FILE (int): The uploaded data is from a third-party voter file.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        FIRST_PARTY = 2
        THIRD_PARTY_CREDIT_BUREAU = 3
        THIRD_PARTY_VOTER_FILE = 4


class UserListDateRuleItemOperatorEnum(object):
    class UserListDateRuleItemOperator(enum.IntEnum):
        """
        Enum describing possible user list date rule item operators.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          EQUALS (int): Equals.
          NOT_EQUALS (int): Not Equals.
          BEFORE (int): Before.
          AFTER (int): After.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        EQUALS = 2
        NOT_EQUALS = 3
        BEFORE = 4
        AFTER = 5


class UserListErrorEnum(object):
    class UserListError(enum.IntEnum):
        """
        Enum describing possible user list errors.

        Attributes:
          UNSPECIFIED (int): Enum unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          EXTERNAL_REMARKETING_USER_LIST_MUTATE_NOT_SUPPORTED (int): Creating and updating external remarketing user lists is not supported.
          CONCRETE_TYPE_REQUIRED (int): Concrete type of user list is required.
          CONVERSION_TYPE_ID_REQUIRED (int): Creating/updating user list conversion types requires specifying the
          conversion type Id.
          DUPLICATE_CONVERSION_TYPES (int): Remarketing user list cannot have duplicate conversion types.
          INVALID_CONVERSION_TYPE (int): Conversion type is invalid/unknown.
          INVALID_DESCRIPTION (int): User list description is empty or invalid.
          INVALID_NAME (int): User list name is empty or invalid.
          INVALID_TYPE (int): Type of the UserList does not match.
          CAN_NOT_ADD_LOGICAL_LIST_AS_LOGICAL_LIST_OPERAND (int): Embedded logical user lists are not allowed.
          INVALID_USER_LIST_LOGICAL_RULE_OPERAND (int): User list rule operand is invalid.
          NAME_ALREADY_USED (int): Name is already being used for another user list for the account.
          NEW_CONVERSION_TYPE_NAME_REQUIRED (int): Name is required when creating a new conversion type.
          CONVERSION_TYPE_NAME_ALREADY_USED (int): The given conversion type name has been used.
          OWNERSHIP_REQUIRED_FOR_SET (int): Only an owner account may edit a user list.
          USER_LIST_MUTATE_NOT_SUPPORTED (int): Creating user list without setting type in oneof user\_list field, or
          creating/updating read-only user list types is not allowed.
          INVALID_RULE (int): Rule is invalid.
          INVALID_DATE_RANGE (int): The specified date range is empty.
          CAN_NOT_MUTATE_SENSITIVE_USERLIST (int): A UserList which is privacy sensitive or legal rejected cannot be mutated
          by external users.
          MAX_NUM_RULEBASED_USERLISTS (int): Maximum number of rulebased user lists a customer can have.
          CANNOT_MODIFY_BILLABLE_RECORD_COUNT (int): BasicUserList's billable record field cannot be modified once it is set.
          APP_ID_NOT_SET (int): crm\_based\_user\_list.app\_id field must be set when upload\_key\_type
          is MOBILE\_ADVERTISING\_ID.
          USERLIST_NAME_IS_RESERVED_FOR_SYSTEM_LIST (int): Name of the user list is reserved for system generated lists and cannot
          be used.
          ADVERTISER_NOT_WHITELISTED_FOR_USING_UPLOADED_DATA (int): Advertiser needs to be whitelisted to use remarketing lists created from
          advertiser uploaded data (e.g., Customer Match lists).
          RULE_TYPE_IS_NOT_SUPPORTED (int): The provided rule\_type is not supported for the user list.
          CAN_NOT_ADD_A_SIMILAR_USERLIST_AS_LOGICAL_LIST_OPERAND (int): Similar user list cannot be used as a logical user list operand.
          CAN_NOT_MIX_CRM_BASED_IN_LOGICAL_LIST_WITH_OTHER_LISTS (int): Logical user list should not have a mix of CRM based user list and other
          types of lists in its rules.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        EXTERNAL_REMARKETING_USER_LIST_MUTATE_NOT_SUPPORTED = 2
        CONCRETE_TYPE_REQUIRED = 3
        CONVERSION_TYPE_ID_REQUIRED = 4
        DUPLICATE_CONVERSION_TYPES = 5
        INVALID_CONVERSION_TYPE = 6
        INVALID_DESCRIPTION = 7
        INVALID_NAME = 8
        INVALID_TYPE = 9
        CAN_NOT_ADD_LOGICAL_LIST_AS_LOGICAL_LIST_OPERAND = 10
        INVALID_USER_LIST_LOGICAL_RULE_OPERAND = 11
        NAME_ALREADY_USED = 12
        NEW_CONVERSION_TYPE_NAME_REQUIRED = 13
        CONVERSION_TYPE_NAME_ALREADY_USED = 14
        OWNERSHIP_REQUIRED_FOR_SET = 15
        USER_LIST_MUTATE_NOT_SUPPORTED = 16
        INVALID_RULE = 17
        INVALID_DATE_RANGE = 27
        CAN_NOT_MUTATE_SENSITIVE_USERLIST = 28
        MAX_NUM_RULEBASED_USERLISTS = 29
        CANNOT_MODIFY_BILLABLE_RECORD_COUNT = 30
        APP_ID_NOT_SET = 31
        USERLIST_NAME_IS_RESERVED_FOR_SYSTEM_LIST = 32
        ADVERTISER_NOT_WHITELISTED_FOR_USING_UPLOADED_DATA = 33
        RULE_TYPE_IS_NOT_SUPPORTED = 34
        CAN_NOT_ADD_A_SIMILAR_USERLIST_AS_LOGICAL_LIST_OPERAND = 35
        CAN_NOT_MIX_CRM_BASED_IN_LOGICAL_LIST_WITH_OTHER_LISTS = 36


class UserListLogicalRuleOperatorEnum(object):
    class UserListLogicalRuleOperator(enum.IntEnum):
        """
        Enum describing possible user list logical rule operators.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          ALL (int): And - all of the operands.
          ANY (int): Or - at least one of the operands.
          NONE (int): Not - none of the operands.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        ALL = 2
        ANY = 3
        NONE = 4


class UserListMembershipStatusEnum(object):
    class UserListMembershipStatus(enum.IntEnum):
        """
        Enum containing possible user list membership statuses.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          OPEN (int): Open status - List is accruing members and can be targeted to.
          CLOSED (int): Closed status - No new members being added. Cannot be used for targeting.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        OPEN = 2
        CLOSED = 3


class UserListNumberRuleItemOperatorEnum(object):
    class UserListNumberRuleItemOperator(enum.IntEnum):
        """
        Enum describing possible user list number rule item operators.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          GREATER_THAN (int): Greater than.
          GREATER_THAN_OR_EQUAL (int): Greater than or equal.
          EQUALS (int): Equals.
          NOT_EQUALS (int): Not equals.
          LESS_THAN (int): Less than.
          LESS_THAN_OR_EQUAL (int): Less than or equal.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        GREATER_THAN = 2
        GREATER_THAN_OR_EQUAL = 3
        EQUALS = 4
        NOT_EQUALS = 5
        LESS_THAN = 6
        LESS_THAN_OR_EQUAL = 7


class UserListPrepopulationStatusEnum(object):
    class UserListPrepopulationStatus(enum.IntEnum):
        """
        Enum describing possible user list prepopulation status.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          REQUESTED (int): Prepopoulation is being requested.
          FINISHED (int): Prepopulation is finished.
          FAILED (int): Prepopulation failed.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        REQUESTED = 2
        FINISHED = 3
        FAILED = 4


class UserListRuleTypeEnum(object):
    class UserListRuleType(enum.IntEnum):
        """
        Enum describing possible user list rule types.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          AND_OF_ORS (int): Conjunctive normal form.
          OR_OF_ANDS (int): Disjunctive normal form.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        AND_OF_ORS = 2
        OR_OF_ANDS = 3


class UserListSizeRangeEnum(object):
    class UserListSizeRange(enum.IntEnum):
        """
        Enum containing possible user list size ranges.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          LESS_THAN_FIVE_HUNDRED (int): User list has less than 500 users.
          LESS_THAN_ONE_THOUSAND (int): User list has number of users in range of 500 to 1000.
          ONE_THOUSAND_TO_TEN_THOUSAND (int): User list has number of users in range of 1000 to 10000.
          TEN_THOUSAND_TO_FIFTY_THOUSAND (int): User list has number of users in range of 10000 to 50000.
          FIFTY_THOUSAND_TO_ONE_HUNDRED_THOUSAND (int): User list has number of users in range of 50000 to 100000.
          ONE_HUNDRED_THOUSAND_TO_THREE_HUNDRED_THOUSAND (int): User list has number of users in range of 100000 to 300000.
          THREE_HUNDRED_THOUSAND_TO_FIVE_HUNDRED_THOUSAND (int): User list has number of users in range of 300000 to 500000.
          FIVE_HUNDRED_THOUSAND_TO_ONE_MILLION (int): User list has number of users in range of 500000 to 1 million.
          ONE_MILLION_TO_TWO_MILLION (int): User list has number of users in range of 1 to 2 millions.
          TWO_MILLION_TO_THREE_MILLION (int): User list has number of users in range of 2 to 3 millions.
          THREE_MILLION_TO_FIVE_MILLION (int): User list has number of users in range of 3 to 5 millions.
          FIVE_MILLION_TO_TEN_MILLION (int): User list has number of users in range of 5 to 10 millions.
          TEN_MILLION_TO_TWENTY_MILLION (int): User list has number of users in range of 10 to 20 millions.
          TWENTY_MILLION_TO_THIRTY_MILLION (int): User list has number of users in range of 20 to 30 millions.
          THIRTY_MILLION_TO_FIFTY_MILLION (int): User list has number of users in range of 30 to 50 millions.
          OVER_FIFTY_MILLION (int): User list has over 50 million users.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        LESS_THAN_FIVE_HUNDRED = 2
        LESS_THAN_ONE_THOUSAND = 3
        ONE_THOUSAND_TO_TEN_THOUSAND = 4
        TEN_THOUSAND_TO_FIFTY_THOUSAND = 5
        FIFTY_THOUSAND_TO_ONE_HUNDRED_THOUSAND = 6
        ONE_HUNDRED_THOUSAND_TO_THREE_HUNDRED_THOUSAND = 7
        THREE_HUNDRED_THOUSAND_TO_FIVE_HUNDRED_THOUSAND = 8
        FIVE_HUNDRED_THOUSAND_TO_ONE_MILLION = 9
        ONE_MILLION_TO_TWO_MILLION = 10
        TWO_MILLION_TO_THREE_MILLION = 11
        THREE_MILLION_TO_FIVE_MILLION = 12
        FIVE_MILLION_TO_TEN_MILLION = 13
        TEN_MILLION_TO_TWENTY_MILLION = 14
        TWENTY_MILLION_TO_THIRTY_MILLION = 15
        THIRTY_MILLION_TO_FIFTY_MILLION = 16
        OVER_FIFTY_MILLION = 17


class UserListStringRuleItemOperatorEnum(object):
    class UserListStringRuleItemOperator(enum.IntEnum):
        """
        Enum describing possible user list string rule item operators.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          CONTAINS (int): Contains.
          EQUALS (int): Equals.
          STARTS_WITH (int): Starts with.
          ENDS_WITH (int): Ends with.
          NOT_EQUALS (int): Not equals.
          NOT_CONTAINS (int): Not contains.
          NOT_STARTS_WITH (int): Not starts with.
          NOT_ENDS_WITH (int): Not ends with.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        CONTAINS = 2
        EQUALS = 3
        STARTS_WITH = 4
        ENDS_WITH = 5
        NOT_EQUALS = 6
        NOT_CONTAINS = 7
        NOT_STARTS_WITH = 8
        NOT_ENDS_WITH = 9


class UserListTypeEnum(object):
    class UserListType(enum.IntEnum):
        """
        Enum containing possible user list types.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          REMARKETING (int): UserList represented as a collection of conversion types.
          LOGICAL (int): UserList represented as a combination of other user lists/interests.
          EXTERNAL_REMARKETING (int): UserList created in the Google Ad Manager platform.
          RULE_BASED (int): UserList associated with a rule.
          SIMILAR (int): UserList with users similar to users of another UserList.
          CRM_BASED (int): UserList of first-party CRM data provided by advertiser in the form of
          emails or other formats.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        REMARKETING = 2
        LOGICAL = 3
        EXTERNAL_REMARKETING = 4
        RULE_BASED = 5
        SIMILAR = 6
        CRM_BASED = 7


class VanityPharmaDisplayUrlModeEnum(object):
    class VanityPharmaDisplayUrlMode(enum.IntEnum):
        """
        Enum describing possible display modes for vanity pharma URLs.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          MANUFACTURER_WEBSITE_URL (int): Replace vanity pharma URL with manufacturer website url.
          WEBSITE_DESCRIPTION (int): Replace vanity pharma URL with description of the website.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        MANUFACTURER_WEBSITE_URL = 2
        WEBSITE_DESCRIPTION = 3


class VanityPharmaTextEnum(object):
    class VanityPharmaText(enum.IntEnum):
        """
        Enum describing possible text.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          PRESCRIPTION_TREATMENT_WEBSITE_EN (int): Prescription treatment website with website content in English.
          PRESCRIPTION_TREATMENT_WEBSITE_ES (int): Prescription treatment website with website content in Spanish
          (Sitio de tratamientos con receta).
          PRESCRIPTION_DEVICE_WEBSITE_EN (int): Prescription device website with website content in English.
          PRESCRIPTION_DEVICE_WEBSITE_ES (int): Prescription device website with website content in Spanish (Sitio de
          dispositivos con receta).
          MEDICAL_DEVICE_WEBSITE_EN (int): Medical device website with website content in English.
          MEDICAL_DEVICE_WEBSITE_ES (int): Medical device website with website content in Spanish (Sitio de
          dispositivos médicos).
          PREVENTATIVE_TREATMENT_WEBSITE_EN (int): Preventative treatment website with website content in English.
          PREVENTATIVE_TREATMENT_WEBSITE_ES (int): Preventative treatment website with website content in Spanish (Sitio de
          tratamientos preventivos).
          PRESCRIPTION_CONTRACEPTION_WEBSITE_EN (int): Prescription contraception website with website content in English.
          PRESCRIPTION_CONTRACEPTION_WEBSITE_ES (int): Prescription contraception website with website content in Spanish (Sitio
          de anticonceptivos con receta).
          PRESCRIPTION_VACCINE_WEBSITE_EN (int): Prescription vaccine website with website content in English.
          PRESCRIPTION_VACCINE_WEBSITE_ES (int): Prescription vaccine website with website content in Spanish (Sitio de
          vacunas con receta).
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        PRESCRIPTION_TREATMENT_WEBSITE_EN = 2
        PRESCRIPTION_TREATMENT_WEBSITE_ES = 3
        PRESCRIPTION_DEVICE_WEBSITE_EN = 4
        PRESCRIPTION_DEVICE_WEBSITE_ES = 5
        MEDICAL_DEVICE_WEBSITE_EN = 6
        MEDICAL_DEVICE_WEBSITE_ES = 7
        PREVENTATIVE_TREATMENT_WEBSITE_EN = 8
        PREVENTATIVE_TREATMENT_WEBSITE_ES = 9
        PRESCRIPTION_CONTRACEPTION_WEBSITE_EN = 10
        PRESCRIPTION_CONTRACEPTION_WEBSITE_ES = 11
        PRESCRIPTION_VACCINE_WEBSITE_EN = 12
        PRESCRIPTION_VACCINE_WEBSITE_ES = 13


class WebpageConditionOperandEnum(object):
    class WebpageConditionOperand(enum.IntEnum):
        """
        The webpage condition operand in webpage criterion.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          URL (int): Operand denoting a webpage URL targeting condition.
          CATEGORY (int): Operand denoting a webpage category targeting condition.
          PAGE_TITLE (int): Operand denoting a webpage title targeting condition.
          PAGE_CONTENT (int): Operand denoting a webpage content targeting condition.
          CUSTOM_LABEL (int): Operand denoting a webpage custom label targeting condition.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        URL = 2
        CATEGORY = 3
        PAGE_TITLE = 4
        PAGE_CONTENT = 5
        CUSTOM_LABEL = 6


class WebpageConditionOperatorEnum(object):
    class WebpageConditionOperator(enum.IntEnum):
        """
        The webpage condition operator in webpage criterion.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          EQUALS (int): The argument web condition is equal to the compared web condition.
          CONTAINS (int): The argument web condition is part of the compared web condition.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        EQUALS = 2
        CONTAINS = 3


class YoutubeVideoRegistrationErrorEnum(object):
    class YoutubeVideoRegistrationError(enum.IntEnum):
        """
        Enum describing YouTube video registration errors.

        Attributes:
          UNSPECIFIED (int): Enum unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          VIDEO_NOT_FOUND (int): Video to be registered wasn't found.
          VIDEO_NOT_ACCESSIBLE (int): Video to be registered is not accessible (e.g. private).
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        VIDEO_NOT_FOUND = 2
        VIDEO_NOT_ACCESSIBLE = 3
