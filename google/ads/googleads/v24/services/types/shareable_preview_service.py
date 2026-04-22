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

from google.ads.googleads.v24.actions.types import generate_shareable_previews


__protobuf__ = proto.module(
    package="google.ads.googleads.v24.services",
    marshal="google.ads.googleads.v24",
    manifest={
        "GenerateShareablePreviewsRequest",
        "GenerateShareablePreviewsResponse",
    },
)


class GenerateShareablePreviewsRequest(proto.Message):
    r"""Request message for
    [ShareablePreviewService.GenerateShareablePreviews][google.ads.googleads.v24.services.ShareablePreviewService.GenerateShareablePreviews].

    Attributes:
        customer_id (str):
            Required. The customer creating the shareable
            previews request.
        operation (google.ads.googleads.v24.actions.types.GenerateShareablePreviewsOperation):
            The operation to generate shareable previews.
    """

    customer_id: str = proto.Field(
        proto.STRING,
        number=1,
    )
    operation: (
        generate_shareable_previews.GenerateShareablePreviewsOperation
    ) = proto.Field(
        proto.MESSAGE,
        number=3,
        message=generate_shareable_previews.GenerateShareablePreviewsOperation,
    )


class GenerateShareablePreviewsResponse(proto.Message):
    r"""Response message for
    [ShareablePreviewService.GenerateShareablePreviews][google.ads.googleads.v24.services.ShareablePreviewService.GenerateShareablePreviews].

    Attributes:
        result (google.ads.googleads.v24.actions.types.GenerateShareablePreviewsResult):
            The result of the generate shareable previews
            action.
    """

    result: generate_shareable_previews.GenerateShareablePreviewsResult = (
        proto.Field(
            proto.MESSAGE,
            number=3,
            message=generate_shareable_previews.GenerateShareablePreviewsResult,
        )
    )


__all__ = tuple(sorted(__protobuf__.manifest))
