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
    package="google.ads.googleads.v24.enums",
    marshal="google.ads.googleads.v24",
    manifest={
        "MultiPartyAuthReviewStatusEnum",
    },
)


class MultiPartyAuthReviewStatusEnum(proto.Message):
    r"""The status of a Multi-Party Authorization review."""

    class MultiPartyAuthReviewStatus(proto.Enum):
        r"""The possible statuses of a Multi-Party Authorization review.

        Values:
            UNSPECIFIED (0):
                Not specified.
            UNKNOWN (1):
                Value unknown in this version.
            APPROVED (2):
                The Multi-Party Authorization request has
                been approved by another admin.
            PENDING (3):
                The Multi-Party Authorization request has
                been sent but not yet approved by another admin.
            REVOKED (4):
                The Multi-Party Authorization request has
                been revoked by the requester.
            REJECTED (5):
                The Multi-Party Authorization request has
                been rejected by another admin.
            EXPIRED (6):
                The Multi-Party Authorization request has
                expired.
        """

        UNSPECIFIED = 0
        UNKNOWN = 1
        APPROVED = 2
        PENDING = 3
        REVOKED = 4
        REJECTED = 5
        EXPIRED = 6


__all__ = tuple(sorted(__protobuf__.manifest))
