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
    package="google.ads.googleads.v20.errors",
    marshal="google.ads.googleads.v20",
    manifest={
        "YoutubeVideoRegistrationErrorEnum",
    },
)


class YoutubeVideoRegistrationErrorEnum(proto.Message):
    r"""Container for enum describing YouTube video registration
    errors.

    """

    class YoutubeVideoRegistrationError(proto.Enum):
        r"""Enum describing YouTube video registration errors.

        Values:
            UNSPECIFIED (0):
                Enum unspecified.
            UNKNOWN (1):
                The received error code is not known in this
                version.
            VIDEO_NOT_FOUND (2):
                Video to be registered wasn't found.
            VIDEO_NOT_ACCESSIBLE (3):
                Video to be registered is not accessible (for
                example, private).
            VIDEO_NOT_ELIGIBLE (4):
                Video to be registered is not eligible (for
                example, mature content).
        """

        UNSPECIFIED = 0
        UNKNOWN = 1
        VIDEO_NOT_FOUND = 2
        VIDEO_NOT_ACCESSIBLE = 3
        VIDEO_NOT_ELIGIBLE = 4


__all__ = tuple(sorted(__protobuf__.manifest))
