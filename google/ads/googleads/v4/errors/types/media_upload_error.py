# -*- coding: utf-8 -*-

# Copyright 2020 Google LLC
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

import proto  # type: ignore


__protobuf__ = proto.module(
    package="google.ads.googleads.v4.errors",
    marshal="google.ads.googleads.v4",
    manifest={"MediaUploadErrorEnum",},
)


class MediaUploadErrorEnum(proto.Message):
    r"""Container for enum describing possible media uploading
    errors.
    """

    class MediaUploadError(proto.Enum):
        r"""Enum describing possible media uploading errors."""
        UNSPECIFIED = 0
        UNKNOWN = 1
        FILE_TOO_BIG = 2
        UNPARSEABLE_IMAGE = 3
        ANIMATED_IMAGE_NOT_ALLOWED = 4
        FORMAT_NOT_ALLOWED = 5
        EXTERNAL_URL_NOT_ALLOWED = 6
        INVALID_URL_REFERENCE = 7
        MISSING_PRIMARY_MEDIA_BUNDLE_ENTRY = 8


__all__ = tuple(sorted(__protobuf__.manifest))
