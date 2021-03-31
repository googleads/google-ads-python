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


from google.ads.googleads.v5.enums.types import mime_type as gage_mime_type


__protobuf__ = proto.module(
    package="google.ads.googleads.v5.common",
    marshal="google.ads.googleads.v5",
    manifest={
        "YoutubeVideoAsset",
        "MediaBundleAsset",
        "ImageAsset",
        "ImageDimension",
        "TextAsset",
        "BookOnGoogleAsset",
    },
)


class YoutubeVideoAsset(proto.Message):
    r"""A YouTube asset.

    Attributes:
        youtube_video_id (str):
            YouTube video id. This is the 11 character
            string value used in the YouTube video URL.
    """

    youtube_video_id = proto.Field(proto.STRING, number=2, optional=True)


class MediaBundleAsset(proto.Message):
    r"""A MediaBundle asset.

    Attributes:
        data (bytes):
            Media bundle (ZIP file) asset data. The
            format of the uploaded ZIP file depends on the
            ad field where it will be used. For more
            information on the format, see the documentation
            of the ad field where you plan on using the
            MediaBundleAsset. This field is mutate only.
    """

    data = proto.Field(proto.BYTES, number=2, optional=True)


class ImageAsset(proto.Message):
    r"""An Image asset.

    Attributes:
        data (bytes):
            The raw bytes data of an image. This field is
            mutate only.
        file_size (int):
            File size of the image asset in bytes.
        mime_type (google.ads.googleads.v5.enums.types.MimeTypeEnum.MimeType):
            MIME type of the image asset.
        full_size (google.ads.googleads.v5.common.types.ImageDimension):
            Metadata for this image at its original size.
    """

    data = proto.Field(proto.BYTES, number=5, optional=True)
    file_size = proto.Field(proto.INT64, number=6, optional=True)
    mime_type = proto.Field(
        proto.ENUM, number=3, enum=gage_mime_type.MimeTypeEnum.MimeType,
    )
    full_size = proto.Field(proto.MESSAGE, number=4, message="ImageDimension",)


class ImageDimension(proto.Message):
    r"""Metadata for an image at a certain size, either original or
    resized.

    Attributes:
        height_pixels (int):
            Height of the image.
        width_pixels (int):
            Width of the image.
        url (str):
            A URL that returns the image with this height
            and width.
    """

    height_pixels = proto.Field(proto.INT64, number=4, optional=True)
    width_pixels = proto.Field(proto.INT64, number=5, optional=True)
    url = proto.Field(proto.STRING, number=6, optional=True)


class TextAsset(proto.Message):
    r"""A Text asset.

    Attributes:
        text (str):
            Text content of the text asset.
    """

    text = proto.Field(proto.STRING, number=2, optional=True)


class BookOnGoogleAsset(proto.Message):
    r"""A Book on Google asset. Used to redirect user to book through
    Google. Book on Google will change the redirect url to book
    directly through Google.
    """


__all__ = tuple(sorted(__protobuf__.manifest))
