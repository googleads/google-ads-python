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

from typing import MutableSequence

import proto  # type: ignore

from google.ads.googleads.v26.enums.types import local_services_lead_type


__protobuf__ = proto.module(
    package="google.ads.googleads.v26.services",
    marshal="google.ads.googleads.v26",
    manifest={
        "CheckLocalServicesEligibilityRequest",
        "CheckLocalServicesEligibilityResponse",
        "SuggestionReason",
        "EligibleGoal",
        "EligibleCategory",
    },
)


class CheckLocalServicesEligibilityRequest(proto.Message):
    r"""Request message for
    [LocalServicesEligibilityService.CheckLocalServicesEligibility][google.ads.googleads.v26.services.LocalServicesEligibilityService.CheckLocalServicesEligibility].

    Attributes:
        customer_id (str):
            Required. The ID of the customer whose
            eligibility is being checked.
        listing_id (str):
            Required. The Google Business Profile listing
            ID to check eligibility for.
    """

    customer_id: str = proto.Field(
        proto.STRING,
        number=1,
    )
    listing_id: str = proto.Field(
        proto.STRING,
        number=2,
    )


class CheckLocalServicesEligibilityResponse(proto.Message):
    r"""Response message for
    [LocalServicesEligibilityService.CheckLocalServicesEligibility][google.ads.googleads.v26.services.LocalServicesEligibilityService.CheckLocalServicesEligibility].


    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        eligible (bool):
            Overall eligibility status of the customer.

            This field is a member of `oneof`_ ``_eligible``.
        suggestion_reasons (MutableSequence[google.ads.googleads.v26.services.types.SuggestionReason]):
            Detailed suggestion reasons for checking
            eligibility (e.g. licensing issues).
        eligible_goals (MutableSequence[google.ads.googleads.v26.services.types.EligibleGoal]):
            List of eligible goals mapped to their
            categories.
    """

    eligible: bool = proto.Field(
        proto.BOOL,
        number=1,
        optional=True,
    )
    suggestion_reasons: MutableSequence["SuggestionReason"] = (
        proto.RepeatedField(
            proto.MESSAGE,
            number=2,
            message="SuggestionReason",
        )
    )
    eligible_goals: MutableSequence["EligibleGoal"] = proto.RepeatedField(
        proto.MESSAGE,
        number=3,
        message="EligibleGoal",
    )


class SuggestionReason(proto.Message):
    r"""Suggestion reason details.

    Attributes:
        short_text (str):
            Short summary text explaining the reason.
        long_text (str):
            Detailed long text description.
    """

    short_text: str = proto.Field(
        proto.STRING,
        number=1,
    )
    long_text: str = proto.Field(
        proto.STRING,
        number=2,
    )


class EligibleGoal(proto.Message):
    r"""Eligible goal mapping details.

    Attributes:
        lead_type (google.ads.googleads.v26.enums.types.LocalServicesLeadTypeEnum.LeadType):
            Eligible lead type.
        categories (MutableSequence[google.ads.googleads.v26.services.types.EligibleCategory]):
            Eligible categories for this lead type.
    """

    lead_type: local_services_lead_type.LocalServicesLeadTypeEnum.LeadType = (
        proto.Field(
            proto.ENUM,
            number=1,
            enum=local_services_lead_type.LocalServicesLeadTypeEnum.LeadType,
        )
    )
    categories: MutableSequence["EligibleCategory"] = proto.RepeatedField(
        proto.MESSAGE,
        number=2,
        message="EligibleCategory",
    )


class EligibleCategory(proto.Message):
    r"""Eligible category information.

    Attributes:
        category_id (str):
            The unique identifier for the service category. For example,
            'xcat:service_area_business_plumber'.
        display_name (str):
            The localized display name of the category.
            For example, 'Plumber'.
        job_types (MutableSequence[str]):
            The list of available job type IDs for this category. For
            example, 'install_faucet', 'drain_cleaning'.
        callouts (MutableSequence[str]):
            The list of available business callout IDs for this
            category. For example, 'family_owned', '24_7_service'.
    """

    category_id: str = proto.Field(
        proto.STRING,
        number=1,
    )
    display_name: str = proto.Field(
        proto.STRING,
        number=2,
    )
    job_types: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=3,
    )
    callouts: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=4,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
