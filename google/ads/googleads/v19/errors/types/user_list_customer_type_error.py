# -*- coding: utf-8 -*-
# Copyright 2024 Google LLC
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
    package="google.ads.googleads.v19.errors",
    marshal="google.ads.googleads.v19",
    manifest={
        "UserListCustomerTypeErrorEnum",
    },
)


class UserListCustomerTypeErrorEnum(proto.Message):
    r"""Container for enum describing possible user list customer
    type errors.

    """

    class UserListCustomerTypeError(proto.Enum):
        r"""Enum describing possible user list customer type errors.

        Values:
            UNSPECIFIED (0):
                Enum unspecified.
            UNKNOWN (1):
                The received error code is not known in this
                version.
            CONFLICTING_CUSTOMER_TYPES (2):
                Cannot add the conflicting customer types to
                the same user list. Conflicting labels:

                1. Purchasers - Converted Leads
                2. Purchasers - Qualified Leads
                3. Purchasers - Cart Abandoners
                4. Qualified Leads - Converted Leads
                5. Disengaged customers - Converted Leads
                6. Disengaged customers - Qualified Leads
                7. Disengaged customers- Cart Abandoners
            NO_ACCESS_TO_USER_LIST (3):
                The account does not have access to the user
                list.
            USERLIST_NOT_ELIGIBLE (4):
                The given user list is not eligible for applying customer
                types. The user list must belong to one of the following
                types: CRM_BASED, RULE_BASED, ADVERTISER_DATA_MODEL_BASED,
                GCN.
            CONVERSION_TRACKING_NOT_ENABLED_OR_NOT_MCC_MANAGER_ACCOUNT (5):
                To edit the user list customer type,
                conversion tracking must be enabled in your
                account. If cross-tracking is enabled, your
                account must be a MCC manager account to modify
                user list customer types. More info at
                https://support.google.com/google-ads/answer/3030657
            TOO_MANY_USER_LISTS_FOR_THE_CUSTOMER_TYPE (6):
                Too many user lists for the customer type.
        """

        UNSPECIFIED = 0
        UNKNOWN = 1
        CONFLICTING_CUSTOMER_TYPES = 2
        NO_ACCESS_TO_USER_LIST = 3
        USERLIST_NOT_ELIGIBLE = 4
        CONVERSION_TRACKING_NOT_ENABLED_OR_NOT_MCC_MANAGER_ACCOUNT = 5
        TOO_MANY_USER_LISTS_FOR_THE_CUSTOMER_TYPE = 6


__all__ = tuple(sorted(__protobuf__.manifest))
