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
    package="google.ads.googleads.v14.resources",
    marshal="google.ads.googleads.v14",
    manifest={
        "CampaignSearchTermInsight",
    },
)


class CampaignSearchTermInsight(proto.Message):
    r"""A Campaign search term view.
    Historical data is available starting March 2023.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        resource_name (str):
            Output only. The resource name of the campaign level search
            term insight. Campaign level search term insight resource
            names have the form:

            ``customers/{customer_id}/campaignSearchTermInsights/{campaign_id}~{category_id}``
        category_label (str):
            Output only. The label for the search
            category. An empty string denotes the catch-all
            category for search terms that didn't fit into
            another category.

            This field is a member of `oneof`_ ``_category_label``.
        id (int):
            Output only. The ID of the insight.

            This field is a member of `oneof`_ ``_id``.
        campaign_id (int):
            Output only. The ID of the campaign.

            This field is a member of `oneof`_ ``_campaign_id``.
    """

    resource_name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    category_label: str = proto.Field(
        proto.STRING,
        number=2,
        optional=True,
    )
    id: int = proto.Field(
        proto.INT64,
        number=3,
        optional=True,
    )
    campaign_id: int = proto.Field(
        proto.INT64,
        number=4,
        optional=True,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
