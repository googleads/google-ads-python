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


from google.ads.googleads.v4.resources.types import media_file
from google.rpc import status_pb2 as status  # type: ignore


__protobuf__ = proto.module(
    package="google.ads.googleads.v4.services",
    marshal="google.ads.googleads.v4",
    manifest={
        "GetMediaFileRequest",
        "MutateMediaFilesRequest",
        "MediaFileOperation",
        "MutateMediaFilesResponse",
        "MutateMediaFileResult",
    },
)


class GetMediaFileRequest(proto.Message):
    r"""Request message for
    [MediaFileService.GetMediaFile][google.ads.googleads.v4.services.MediaFileService.GetMediaFile]

    Attributes:
        resource_name (str):
            Required. The resource name of the media file
            to fetch.
    """

    resource_name = proto.Field(proto.STRING, number=1)


class MutateMediaFilesRequest(proto.Message):
    r"""Request message for
    [MediaFileService.MutateMediaFiles][google.ads.googleads.v4.services.MediaFileService.MutateMediaFiles]

    Attributes:
        customer_id (str):
            Required. The ID of the customer whose media
            files are being modified.
        operations (Sequence[google.ads.googleads.v4.services.types.MediaFileOperation]):
            Required. The list of operations to perform
            on individual media file.
        partial_failure (bool):
            If true, successful operations will be
            carried out and invalid operations will return
            errors. If false, all operations will be carried
            out in one transaction if and only if they are
            all valid. Default is false.
        validate_only (bool):
            If true, the request is validated but not
            executed. Only errors are returned, not results.
    """

    customer_id = proto.Field(proto.STRING, number=1)
    operations = proto.RepeatedField(
        proto.MESSAGE, number=2, message="MediaFileOperation",
    )
    partial_failure = proto.Field(proto.BOOL, number=3)
    validate_only = proto.Field(proto.BOOL, number=4)


class MediaFileOperation(proto.Message):
    r"""A single operation to create media file.

    Attributes:
        create (google.ads.googleads.v4.resources.types.MediaFile):
            Create operation: No resource name is
            expected for the new media file.
    """

    create = proto.Field(
        proto.MESSAGE,
        number=1,
        oneof="operation",
        message=media_file.MediaFile,
    )


class MutateMediaFilesResponse(proto.Message):
    r"""Response message for a media file mutate.

    Attributes:
        partial_failure_error (google.rpc.status_pb2.Status):
            Errors that pertain to operation failures in the partial
            failure mode. Returned only when partial_failure = true and
            all errors occur inside the operations. If any errors occur
            outside the operations (e.g. auth errors), we return an RPC
            level error.
        results (Sequence[google.ads.googleads.v4.services.types.MutateMediaFileResult]):
            All results for the mutate.
    """

    partial_failure_error = proto.Field(
        proto.MESSAGE, number=3, message=status.Status,
    )
    results = proto.RepeatedField(
        proto.MESSAGE, number=2, message="MutateMediaFileResult",
    )


class MutateMediaFileResult(proto.Message):
    r"""The result for the media file mutate.

    Attributes:
        resource_name (str):
            The resource name returned for successful
            operations.
    """

    resource_name = proto.Field(proto.STRING, number=1)


__all__ = tuple(sorted(__protobuf__.manifest))
