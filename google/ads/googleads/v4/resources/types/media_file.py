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


from google.ads.googleads.v4.enums.types import media_type
from google.ads.googleads.v4.enums.types import mime_type as gage_mime_type
from google.protobuf import wrappers_pb2 as wrappers  # type: ignore


__protobuf__ = proto.module(
    package="google.ads.googleads.v4.resources",
    marshal="google.ads.googleads.v4",
    manifest={
        "MediaFile",
        "MediaImage",
        "MediaBundle",
        "MediaAudio",
        "MediaVideo",
    },
)


class MediaFile(proto.Message):
    r"""A media file.

    Attributes:
        resource_name (str):
            Immutable. The resource name of the media file. Media file
            resource names have the form:

            ``customers/{customer_id}/mediaFiles/{media_file_id}``
        id (google.protobuf.wrappers_pb2.Int64Value):
            Output only. The ID of the media file.
        type_ (google.ads.googleads.v4.enums.types.MediaTypeEnum.MediaType):
            Immutable. Type of the media file.
        mime_type (google.ads.googleads.v4.enums.types.MimeTypeEnum.MimeType):
            Output only. The mime type of the media file.
        source_url (google.protobuf.wrappers_pb2.StringValue):
            Immutable. The URL of where the original
            media file was downloaded from (or a file name).
            Only used for media of type AUDIO and IMAGE.
        name (google.protobuf.wrappers_pb2.StringValue):
            Immutable. The name of the media file. The
            name can be used by clients to help identify
            previously uploaded media.
        file_size (google.protobuf.wrappers_pb2.Int64Value):
            Output only. The size of the media file in
            bytes.
        image (google.ads.googleads.v4.resources.types.MediaImage):
            Immutable. Encapsulates an Image.
        media_bundle (google.ads.googleads.v4.resources.types.MediaBundle):
            Immutable. A ZIP archive media the content of
            which contains HTML5 assets.
        audio (google.ads.googleads.v4.resources.types.MediaAudio):
            Output only. Encapsulates an Audio.
        video (google.ads.googleads.v4.resources.types.MediaVideo):
            Immutable. Encapsulates a Video.
    """

    resource_name = proto.Field(proto.STRING, number=1)
    id = proto.Field(proto.MESSAGE, number=2, message=wrappers.Int64Value,)
    type_ = proto.Field(
        proto.ENUM, number=5, enum=media_type.MediaTypeEnum.MediaType,
    )
    mime_type = proto.Field(
        proto.ENUM, number=6, enum=gage_mime_type.MimeTypeEnum.MimeType,
    )
    source_url = proto.Field(
        proto.MESSAGE, number=7, message=wrappers.StringValue,
    )
    name = proto.Field(proto.MESSAGE, number=8, message=wrappers.StringValue,)
    file_size = proto.Field(
        proto.MESSAGE, number=9, message=wrappers.Int64Value,
    )
    image = proto.Field(
        proto.MESSAGE, number=3, oneof="mediatype", message="MediaImage",
    )
    media_bundle = proto.Field(
        proto.MESSAGE, number=4, oneof="mediatype", message="MediaBundle",
    )
    audio = proto.Field(
        proto.MESSAGE, number=10, oneof="mediatype", message="MediaAudio",
    )
    video = proto.Field(
        proto.MESSAGE, number=11, oneof="mediatype", message="MediaVideo",
    )


class MediaImage(proto.Message):
    r"""Encapsulates an Image.

    Attributes:
        data (google.protobuf.wrappers_pb2.BytesValue):
            Immutable. Raw image data.
    """

    data = proto.Field(proto.MESSAGE, number=1, message=wrappers.BytesValue,)


class MediaBundle(proto.Message):
    r"""Represents a ZIP archive media the content of which contains
    HTML5 assets.

    Attributes:
        data (google.protobuf.wrappers_pb2.BytesValue):
            Immutable. Raw zipped data.
    """

    data = proto.Field(proto.MESSAGE, number=1, message=wrappers.BytesValue,)


class MediaAudio(proto.Message):
    r"""Encapsulates an Audio.

    Attributes:
        ad_duration_millis (google.protobuf.wrappers_pb2.Int64Value):
            Output only. The duration of the Audio in
            milliseconds.
    """

    ad_duration_millis = proto.Field(
        proto.MESSAGE, number=1, message=wrappers.Int64Value,
    )


class MediaVideo(proto.Message):
    r"""Encapsulates a Video.

    Attributes:
        ad_duration_millis (google.protobuf.wrappers_pb2.Int64Value):
            Output only. The duration of the Video in
            milliseconds.
        youtube_video_id (google.protobuf.wrappers_pb2.StringValue):
            Immutable. The YouTube video ID (as seen in
            YouTube URLs). Adding prefix
            "https://www.youtube.com/watch?v=" to this ID
            will get the YouTube streaming URL for this
            video.
        advertising_id_code (google.protobuf.wrappers_pb2.StringValue):
            Output only. The Advertising Digital
            Identification code for this video, as defined
            by the American Association of Advertising
            Agencies, used mainly for television
            commercials.
        isci_code (google.protobuf.wrappers_pb2.StringValue):
            Output only. The Industry Standard Commercial
            Identifier code for this video, used mainly for
            television commercials.
    """

    ad_duration_millis = proto.Field(
        proto.MESSAGE, number=1, message=wrappers.Int64Value,
    )
    youtube_video_id = proto.Field(
        proto.MESSAGE, number=2, message=wrappers.StringValue,
    )
    advertising_id_code = proto.Field(
        proto.MESSAGE, number=3, message=wrappers.StringValue,
    )
    isci_code = proto.Field(
        proto.MESSAGE, number=4, message=wrappers.StringValue,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
