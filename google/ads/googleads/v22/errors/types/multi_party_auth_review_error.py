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
    package="google.ads.googleads.v22.errors",
    marshal="google.ads.googleads.v22",
    manifest={
        "MultiPartyAuthReviewErrorEnum",
    },
)


class MultiPartyAuthReviewErrorEnum(proto.Message):
    r"""Container for enum describing possible MultiPartyAuthReview
    errors.

    """

    class MultiPartyAuthReviewError(proto.Enum):
        r"""Enum describing possible MultiPartyAuthReview errors.

        Values:
            UNSPECIFIED (0):
                Enum unspecified.
            UNKNOWN (1):
                The error code is not in this version.
            ACCESS_INVITATION_NOT_FOUND (2):
                The Multi-Party Authorization review
                requested was not found.
            ACCESS_INVITATION_INVALID_STATUS (3):
                The Multi-Party Authorization review is not
                PENDING.
            INVALID_STATUS_TRANSITION (4):
                The status transition is not allowed.
            PERMISSION_DENIED (5):
                The user does not have permission to perform
                this action.
        """

        UNSPECIFIED = 0
        UNKNOWN = 1
        ACCESS_INVITATION_NOT_FOUND = 2
        ACCESS_INVITATION_INVALID_STATUS = 3
        INVALID_STATUS_TRANSITION = 4
        PERMISSION_DENIED = 5


__all__ = tuple(sorted(__protobuf__.manifest))
