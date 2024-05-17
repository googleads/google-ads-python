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
    package="google.ads.googleads.v16.enums",
    marshal="google.ads.googleads.v16",
    manifest={
        "LocalServicesBusinessRegistrationCheckRejectionReasonEnum",
    },
)


class LocalServicesBusinessRegistrationCheckRejectionReasonEnum(proto.Message):
    r"""Container for enum describing the rejection reason of a local
    services business registration check verification artifact.

    """

    class LocalServicesBusinessRegistrationCheckRejectionReason(proto.Enum):
        r"""Enums describing possible rejection reasons of a local
        services business registration check verification artifact.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        BUSINESS_NAME_MISMATCH = 2
        BUSINESS_DETAILS_MISMATCH = 3
        ID_NOT_FOUND = 4
        POOR_DOCUMENT_IMAGE_QUALITY = 5
        DOCUMENT_EXPIRED = 6
        DOCUMENT_INVALID = 7
        DOCUMENT_TYPE_MISMATCH = 8
        DOCUMENT_UNVERIFIABLE = 9
        OTHER = 10


__all__ = tuple(sorted(__protobuf__.manifest))
