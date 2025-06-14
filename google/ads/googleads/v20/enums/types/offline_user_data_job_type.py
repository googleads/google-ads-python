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
    package="google.ads.googleads.v20.enums",
    marshal="google.ads.googleads.v20",
    manifest={
        "OfflineUserDataJobTypeEnum",
    },
)


class OfflineUserDataJobTypeEnum(proto.Message):
    r"""Container for enum describing types of an offline user data
    job.

    """

    class OfflineUserDataJobType(proto.Enum):
        r"""The type of an offline user data job.

        Values:
            UNSPECIFIED (0):
                Not specified.
            UNKNOWN (1):
                Used for return value only. Represents value
                unknown in this version.
            STORE_SALES_UPLOAD_FIRST_PARTY (2):
                Store Sales Direct data for self service.
            STORE_SALES_UPLOAD_THIRD_PARTY (3):
                Store Sales Direct data for third party.
            CUSTOMER_MATCH_USER_LIST (4):
                Customer Match user list data.
            CUSTOMER_MATCH_WITH_ATTRIBUTES (5):
                Customer Match with attribute data.
        """

        UNSPECIFIED = 0
        UNKNOWN = 1
        STORE_SALES_UPLOAD_FIRST_PARTY = 2
        STORE_SALES_UPLOAD_THIRD_PARTY = 3
        CUSTOMER_MATCH_USER_LIST = 4
        CUSTOMER_MATCH_WITH_ATTRIBUTES = 5


__all__ = tuple(sorted(__protobuf__.manifest))
