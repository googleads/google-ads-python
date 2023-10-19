# -*- coding: utf-8 -*-
# Copyright 2023 Google LLC
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
    package="google.ads.googleads.v15.enums",
    marshal="google.ads.googleads.v15",
    manifest={
        "LocalServicesInsuranceRejectionReasonEnum",
    },
)


class LocalServicesInsuranceRejectionReasonEnum(proto.Message):
    r"""Container for enum describing the rejection reason of a local
    services insurance verification artifact.

    """

    class LocalServicesInsuranceRejectionReason(proto.Enum):
        r"""Enums describing possible rejection reasons of a local
        services insurance verification artifact.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        BUSINESS_NAME_MISMATCH = 2
        INSURANCE_AMOUNT_INSUFFICIENT = 3
        EXPIRED = 4
        NO_SIGNATURE = 5
        NO_POLICY_NUMBER = 6
        NO_COMMERCIAL_GENERAL_LIABILITY = 7
        EDITABLE_FORMAT = 8
        CATEGORY_MISMATCH = 9
        MISSING_EXPIRATION_DATE = 10
        POOR_QUALITY = 11
        POTENTIALLY_EDITED = 12
        WRONG_DOCUMENT_TYPE = 13
        NON_FINAL = 14
        OTHER = 15


__all__ = tuple(sorted(__protobuf__.manifest))
