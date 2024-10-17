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

from google.ads.googleads.v18.resources.types import data_link as gagr_data_link


__protobuf__ = proto.module(
    package="google.ads.googleads.v18.services",
    marshal="google.ads.googleads.v18",
    manifest={"CreateDataLinkRequest", "CreateDataLinkResponse",},
)


class CreateDataLinkRequest(proto.Message):
    r"""Request message for
    [DataLinkService.CreateDataLink][google.ads.googleads.v18.services.DataLinkService.CreateDataLink].

    Attributes:
        customer_id (str):
            Required. The ID of the customer for which
            the data link is created.
        data_link (google.ads.googleads.v18.resources.types.DataLink):
            Required. The data link to be created.
    """

    customer_id: str = proto.Field(
        proto.STRING, number=1,
    )
    data_link: gagr_data_link.DataLink = proto.Field(
        proto.MESSAGE, number=2, message=gagr_data_link.DataLink,
    )


class CreateDataLinkResponse(proto.Message):
    r"""Response message for
    [DataLinkService.CreateDataLink][google.ads.googleads.v18.services.DataLinkService.CreateDataLink].

    Attributes:
        resource_name (str):
            Returned for successful operations. Resource
            name of the data link.
    """

    resource_name: str = proto.Field(
        proto.STRING, number=1,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
