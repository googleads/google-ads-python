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

from google.ads.googleads.v23.common.types import campaign_reservation_quote


__protobuf__ = proto.module(
    package="google.ads.googleads.v23.actions",
    marshal="google.ads.googleads.v23",
    manifest={
        "QuoteCampaignsOperation",
        "QuoteCampaignsResult",
    },
)


class QuoteCampaignsOperation(proto.Message):
    r"""Request message for the QuoteCampaigns action.
    Request including this operation can have a latency of up to 30
    seconds. This feature is not publicly available.

    Attributes:
        campaigns (MutableSequence[google.ads.googleads.v23.actions.types.QuoteCampaignsOperation.Campaign]):
            Campaigns for which the quotes are requested.
            Maximum 2 campaigns per request.
        quote_signature (str):
            If provided, the signature of the previous
            quote. Clients should always provide the quote
            signature from previous quotes if they haven't
            changed the campaigns to prevent price
            fluctuations within a user session.
    """

    class Campaign(proto.Message):
        r"""A campaign for which the quote is requested.

        Attributes:
            campaign (str):
                Campaign for which the quote is requested. Format:
                customers/{customer_id}/campaigns/{campaign_id}
        """

        campaign: str = proto.Field(
            proto.STRING,
            number=1,
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


class QuoteCampaignsResult(proto.Message):
    r"""The response of the QuoteCampaigns action, when the action is
    successful. Note that if the response contains errors, the action
    response will not be returned, but a quote may still be returned in
    the ErrorDetails.reservation_error_details field.

    Attributes:
        quotes (MutableSequence[google.ads.googleads.v23.common.types.CampaignReservationQuote]):
            The quotes for the requested campaigns.
        quote_signature (str):
            The signature of the quote. This signature
            should be used when booking the quote.
    """

    quotes: MutableSequence[
        campaign_reservation_quote.CampaignReservationQuote
    ] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message=campaign_reservation_quote.CampaignReservationQuote,
    )
    quote_signature: str = proto.Field(
        proto.STRING,
        number=2,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
