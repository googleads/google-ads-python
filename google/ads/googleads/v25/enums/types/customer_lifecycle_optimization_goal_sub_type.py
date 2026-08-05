# -*- coding: utf-8 -*-
# Copyright 2026 Google LLC
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
    package="google.ads.googleads.v25.enums",
    marshal="google.ads.googleads.v25",
    manifest={
        "CustomerLifecycleOptimizationGoalSubTypeEnum",
    },
)


class CustomerLifecycleOptimizationGoalSubTypeEnum(proto.Message):
    r"""Container for enum describing customer lifecycle optimization
    goal sub types.

    """

    class CustomerLifecycleOptimizationGoalSubType(proto.Enum):
        r"""The possible sub types of customer lifecycle optimization
        goal.

        Values:
            UNSPECIFIED (0):
                Not specified.
            UNKNOWN (1):
                Used for return value only. Represents value
                unknown in this version.
            NEW_CUSTOMER_ACQUISITION_VALUE (2):
                New customer acquisition value.
            NEW_CUSTOMER_ACQUISITION_ONLY (3):
                New customer acquisition only.
            CUSTOMER_RETENTION_VALUE (4):
                Customer retention value.
            CUSTOMER_RETENTION_ONLY (5):
                Customer retention only.
            LOYALTY_RETENTION_VALUE (7):
                Loyalty retention value.
            LOYALTY_RETENTION_BENEFITS (8):
                Loyalty retention benefits.
        """

        UNSPECIFIED = 0
        UNKNOWN = 1
        NEW_CUSTOMER_ACQUISITION_VALUE = 2
        NEW_CUSTOMER_ACQUISITION_ONLY = 3
        CUSTOMER_RETENTION_VALUE = 4
        CUSTOMER_RETENTION_ONLY = 5
        LOYALTY_RETENTION_VALUE = 7
        LOYALTY_RETENTION_BENEFITS = 8


__all__ = tuple(sorted(__protobuf__.manifest))
