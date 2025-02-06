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
    package="google.ads.googleads.v17.enums",
    marshal="google.ads.googleads.v17",
    manifest={
        "LocalServicesLicenseRejectionReasonEnum",
    },
)


class LocalServicesLicenseRejectionReasonEnum(proto.Message):
    r"""Container for enum describing the rejection reason of a local
    services license verification artifact.

    """

    class LocalServicesLicenseRejectionReason(proto.Enum):
        r"""Enums describing possible rejection reasons of a local
        services license verification artifact.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        BUSINESS_NAME_MISMATCH = 2
        UNAUTHORIZED = 3
        EXPIRED = 4
        POOR_QUALITY = 5
        UNVERIFIABLE = 6
        WRONG_DOCUMENT_OR_ID = 7
        OTHER = 8


__all__ = tuple(sorted(__protobuf__.manifest))
