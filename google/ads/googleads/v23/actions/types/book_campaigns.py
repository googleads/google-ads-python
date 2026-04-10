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

from typing import MutableSequence

import proto  # type: ignore

from google.ads.googleads.v23.enums.types import reservation_request_type


__protobuf__ = proto.module(
    package="google.ads.googleads.v23.actions",
    marshal="google.ads.googleads.v23",
    manifest={
        "BookCampaignsOperation",
        "BookCampaignsResult",
    },
)


class BookCampaignsOperation(proto.Message):
    r"""Request message for the BookCampaigns action.
    Request including this operation can have a latency of up to 30
    seconds. This feature is not publicly available.

    Attributes:
        campaigns (MutableSequence[google.ads.googleads.v23.actions.types.BookCampaignsOperation.Campaign]):
            Campaigns to book. Maximum 2 campaigns per
            request.
        quote_signature (str):
            If provided, the signature of the previous
            quote. Clients should always provide the quote
            signature from previous quotes if they haven't
            changed the campaigns to prevent price
            fluctuations within a user session.
    """

    class Campaign(proto.Message):
        r"""A single campaign to book.

        Attributes:
            campaign (str):
                Campaign resource to book. Format:
                customers/{customer_id}/campaigns/{campaign_id}
            request_type (google.ads.googleads.v23.enums.types.ReservationRequestTypeEnum.ReservationRequestType):
                Determines if the current request should book
                the inventory or hold it.
        """

        campaign: str = proto.Field(
            proto.STRING,
            number=1,
        )
        request_type: (
            reservation_request_type.ReservationRequestTypeEnum.ReservationRequestType
        ) = proto.Field(
            proto.ENUM,
            number=2,
            enum=reservation_request_type.ReservationRequestTypeEnum.ReservationRequestType,
        )

    campaigns: MutableSequence[Campaign] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message=Campaign,
    )
    quote_signature: str = proto.Field(
        proto.STRING,
        number=2,
    )


class BookCampaignsResult(proto.Message):
    r"""Response message for the BookCampaigns action. Note that if the
    response contains errors, the action response will not be returned,
    but a quote may still be returned in the
    ErrorDetails.reservation_error_details field.

    """


__all__ = tuple(sorted(__protobuf__.manifest))
