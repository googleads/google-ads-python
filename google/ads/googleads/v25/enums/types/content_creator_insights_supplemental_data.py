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


import proto  # type: ignore


__protobuf__ = proto.module(
    package="google.ads.googleads.v25.enums",
    marshal="google.ads.googleads.v25",
    manifest={
        "ContentCreatorInsightsSupplementalDataEnum",
    },
)


class ContentCreatorInsightsSupplementalDataEnum(proto.Message):
    r"""Container for enum describing supplemental data for the
    Content Creator Insights Service.

    """

    class ContentCreatorInsightsSupplementalData(proto.Enum):
        r"""Supplemental data for the Content Creator Insights Service.

        Values:
            UNSPECIFIED (0):
                Not specified.
            UNKNOWN (1):
                The value is unknown in this version.
            BRAND_SENTIMENT_DATA (2):
                Populate brand sentiment data in
                [ContentCreatorInsightsService.GenerateTrendingInsights][google.ads.googleads.v25.services.ContentCreatorInsightsService.GenerateTrendingInsights].
                This is only available when requesting trending insights for
                a brand topic. A brand topic is a Knowledge Graph entity
                that is tagged with
                [BRAND][google.ads.googleads.v25.enums.InsightsKnowledgeGraphEntityCapabilitiesEnum.InsightsKnowledgeGraphEntityCapabilities.BRAND].
                Use
                [AudienceInsightsService.ListAudienceInsightsAttributes][]
                to get the list of supported Knowledge Graph entities.
            LOCAL_CREATOR_DATA (3):
                Populate local creator data in
                [ContentCreatorInsightsService.GenerateTrendingInsights][google.ads.googleads.v25.services.ContentCreatorInsightsService.GenerateTrendingInsights]
                and
                [ContentCreatorInsightsService.GenerateCreatorInsights][google.ads.googleads.v25.services.ContentCreatorInsightsService.GenerateCreatorInsights].
                This is only available when requesting trending or creator
                insights for a content or creator topic. These topics are
                Knowledge Graph entities tagged with
                [CONTENT_TRENDING_INSIGHTS][google.ads.googleads.v25.enums.InsightsKnowledgeGraphEntityCapabilitiesEnum.InsightsKnowledgeGraphEntityCapabilities.CONTENT_TRENDING_INSIGHTS]
                or
                [CREATOR_TOPIC_INSIGHTS][google.ads.googleads.v25.enums.InsightsKnowledgeGraphEntityCapabilitiesEnum.InsightsKnowledgeGraphEntityCapabilities.CREATOR_TOPIC_INSIGHTS].
                Local creator discovery is not supported when
                [GenerateCreatorInsightsRequest.sub_country_locations][google.ads.googleads.v25.services.GenerateCreatorInsightsRequest.sub_country_locations]
                or
                [GenerateTrendingInsightsRequest.sub_country_locations][google.ads.googleads.v25.services.GenerateTrendingInsightsRequest.sub_country_locations]
                is set. Use
                [AudienceInsightsService.ListAudienceInsightsAttributes][]
                to get the list of supported Knowledge Graph entities.
        """

        UNSPECIFIED = 0
        UNKNOWN = 1
        BRAND_SENTIMENT_DATA = 2
        LOCAL_CREATOR_DATA = 3


__all__ = tuple(sorted(__protobuf__.manifest))
