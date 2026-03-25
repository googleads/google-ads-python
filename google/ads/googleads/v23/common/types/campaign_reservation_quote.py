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
    package="google.ads.googleads.v23.common",
    marshal="google.ads.googleads.v23",
    manifest={
        "CampaignReservationQuote",
    },
)


class CampaignReservationQuote(proto.Message):
    r"""The campaign reservation quote.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        campaign (str):
            The campaign resource name, as it was specified in the
            request. It could contain a temp ID. Format:
            customers/{customer_id}/campaigns/{campaign_id}
        max_budget_micros (int):
            Maximum budget to get all available
            impressions at the current CPM. Capped at 10M
            USD. Specified in micros of the advertiser
            currency.
        possible_hold_duration_seconds (int):
            The possible duration of the hold, in
            seconds.
        suggested_cpm_micros (int):
            The CPM that would be accepted for the
            campaign calculated at the proposed budget.
            Specified in micros of the advertiser currency.

            This field is a member of `oneof`_ ``suggested_quote``.
    """

    campaign: str = proto.Field(
        proto.STRING,
        number=1,
    )
    max_budget_micros: int = proto.Field(
        proto.INT64,
        number=3,
    )
    possible_hold_duration_seconds: int = proto.Field(
        proto.INT64,
        number=4,
    )
    suggested_cpm_micros: int = proto.Field(
        proto.INT64,
        number=2,
        oneof="suggested_quote",
    )


__all__ = tuple(sorted(__protobuf__.manifest))
