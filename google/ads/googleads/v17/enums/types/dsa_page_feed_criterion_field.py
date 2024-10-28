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
        "DsaPageFeedCriterionFieldEnum",
    },
)


class DsaPageFeedCriterionFieldEnum(proto.Message):
    r"""Values for Dynamic Search Ad Page Feed criterion fields."""

    class DsaPageFeedCriterionField(proto.Enum):
        r"""Possible values for Dynamic Search Ad Page Feed criterion
        fields.

        Values:
            UNSPECIFIED (0):
                Not specified.
            UNKNOWN (1):
                Used for return value only. Represents value
                unknown in this version.
            PAGE_URL (2):
                Data Type: URL or URL_LIST. URL of the web page you want to
                target.
            LABEL (3):
                Data Type: STRING_LIST. The labels that will help you target
                ads within your page feed.
        """

        UNSPECIFIED = 0
        UNKNOWN = 1
        PAGE_URL = 2
        LABEL = 3


__all__ = tuple(sorted(__protobuf__.manifest))
