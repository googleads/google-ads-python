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

from google.ads.googleads.v26.enums.types import (
    search_lift_keyword_bundle_status,
)
from google.ads.googleads.v26.enums.types import (
    search_lift_matching_info_source,
)


__protobuf__ = proto.module(
    package="google.ads.googleads.v26.resources",
    marshal="google.ads.googleads.v26",
    manifest={
        "SearchLiftKeywordBundle",
    },
)


class SearchLiftKeywordBundle(proto.Message):
    r"""A search lift keyword bundle.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        resource_name (str):
            Immutable. The resource name of the search lift keyword
            bundle. Search lift keyword bundle resource names have the
            form:

            ``customers/{customer_id}/searchLiftKeywordBundles/{SearchLiftKeywordBundle.search_lift_keyword_bundle_id}``
        search_lift_keyword_bundle_id (int):
            Output only. The unique identifier for the
            keyword bundle.

            This field is a member of `oneof`_ ``_search_lift_keyword_bundle_id``.
        keywords (MutableSequence[google.ads.googleads.v26.resources.types.SearchLiftKeywordBundle.SearchLiftKeyword]):
            Output only. The keywords in this bundle.
        source (google.ads.googleads.v26.enums.types.SearchLiftMatchingInfoSourceEnum.SearchLiftMatchingInfoSource):
            Output only. The source of the keywords.
        status (google.ads.googleads.v26.enums.types.SearchLiftKeywordBundleStatusEnum.SearchLiftKeywordBundleStatus):
            Output only. The status of the keyword
            bundle.
    """

    class SearchLiftKeyword(proto.Message):
        r"""A keyword in a search lift keyword bundle.

        .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

        Attributes:
            text (str):
                Output only. The keyword text.

                This field is a member of `oneof`_ ``_text``.
        """

        text: str = proto.Field(
            proto.STRING,
            number=1,
            optional=True,
        )

    resource_name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    search_lift_keyword_bundle_id: int = proto.Field(
        proto.INT64,
        number=2,
        optional=True,
    )
    keywords: MutableSequence[SearchLiftKeyword] = proto.RepeatedField(
        proto.MESSAGE,
        number=3,
        message=SearchLiftKeyword,
    )
    source: (
        search_lift_matching_info_source.SearchLiftMatchingInfoSourceEnum.SearchLiftMatchingInfoSource
    ) = proto.Field(
        proto.ENUM,
        number=4,
        enum=search_lift_matching_info_source.SearchLiftMatchingInfoSourceEnum.SearchLiftMatchingInfoSource,
    )
    status: (
        search_lift_keyword_bundle_status.SearchLiftKeywordBundleStatusEnum.SearchLiftKeywordBundleStatus
    ) = proto.Field(
        proto.ENUM,
        number=5,
        enum=search_lift_keyword_bundle_status.SearchLiftKeywordBundleStatusEnum.SearchLiftKeywordBundleStatus,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
