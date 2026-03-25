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

from google.ads.googleads.v23.actions.types import book_campaigns
from google.ads.googleads.v23.actions.types import quote_campaigns


__protobuf__ = proto.module(
    package="google.ads.googleads.v23.services",
    marshal="google.ads.googleads.v23",
    manifest={
        "QuoteCampaignsRequest",
        "QuoteCampaignsResponse",
        "BookCampaignsRequest",
        "BookCampaignsResponse",
    },
)


class QuoteCampaignsRequest(proto.Message):
    r"""Request message for
    [ReservationService.QuoteCampaigns][google.ads.googleads.v23.services.ReservationService.QuoteCampaigns].

    Attributes:
        customer_id (str):
            Required. The ID of the customer making the
            request.
        operation (google.ads.googleads.v23.actions.types.QuoteCampaignsOperation):
            The operation to quote the campaigns.
    """

    customer_id: str = proto.Field(
        proto.STRING,
        number=1,
    )
    operation: quote_campaigns.QuoteCampaignsOperation = proto.Field(
        proto.MESSAGE,
        number=2,
        message=quote_campaigns.QuoteCampaignsOperation,
    )


class QuoteCampaignsResponse(proto.Message):
    r"""Response message for
    [ReservationService.QuoteCampaigns][google.ads.googleads.v23.services.ReservationService.QuoteCampaigns].

    Attributes:
        result (google.ads.googleads.v23.actions.types.QuoteCampaignsResult):
            The result of the quote campaigns operation.
    """

    result: quote_campaigns.QuoteCampaignsResult = proto.Field(
        proto.MESSAGE,
        number=1,
        message=quote_campaigns.QuoteCampaignsResult,
    )


class BookCampaignsRequest(proto.Message):
    r"""Request message for
    [ReservationService.BookCampaigns][google.ads.googleads.v23.services.ReservationService.BookCampaigns].

    Attributes:
        customer_id (str):
            Required. The ID of the customer making the
            request.
        operation (google.ads.googleads.v23.actions.types.BookCampaignsOperation):
            The operation to book the campaigns.
    """

    customer_id: str = proto.Field(
        proto.STRING,
        number=1,
    )
    operation: book_campaigns.BookCampaignsOperation = proto.Field(
        proto.MESSAGE,
        number=2,
        message=book_campaigns.BookCampaignsOperation,
    )


class BookCampaignsResponse(proto.Message):
    r"""Response message for
    [ReservationService.BookCampaigns][google.ads.googleads.v23.services.ReservationService.BookCampaigns].

    Attributes:
        result (google.ads.googleads.v23.actions.types.BookCampaignsResult):
            The result of the book campaigns operation.
    """

    result: book_campaigns.BookCampaignsResult = proto.Field(
        proto.MESSAGE,
        number=1,
        message=book_campaigns.BookCampaignsResult,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
