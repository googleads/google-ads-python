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


from google.ads.googleads.v4.enums.types import manager_link_status
from google.protobuf import wrappers_pb2 as wrappers  # type: ignore


__protobuf__ = proto.module(
    package="google.ads.googleads.v4.resources",
    marshal="google.ads.googleads.v4",
    manifest={"CustomerClientLink",},
)


class CustomerClientLink(proto.Message):
    r"""Represents customer client link relationship.

    Attributes:
        resource_name (str):
            Immutable. Name of the resource. CustomerClientLink resource
            names have the form:
            ``customers/{customer_id}/customerClientLinks/{client_customer_id}~{manager_link_id}``
        client_customer (google.protobuf.wrappers_pb2.StringValue):
            Immutable. The client customer linked to this
            customer.
        manager_link_id (google.protobuf.wrappers_pb2.Int64Value):
            Output only. This is uniquely identifies a
            customer client link. Read only.
        status (google.ads.googleads.v4.enums.types.ManagerLinkStatusEnum.ManagerLinkStatus):
            This is the status of the link between client
            and manager.
        hidden (google.protobuf.wrappers_pb2.BoolValue):
            The visibility of the link. Users can choose
            whether or not to see hidden links in the Google
            Ads UI. Default value is false
    """

    resource_name = proto.Field(proto.STRING, number=1)
    client_customer = proto.Field(
        proto.MESSAGE, number=3, message=wrappers.StringValue,
    )
    manager_link_id = proto.Field(
        proto.MESSAGE, number=4, message=wrappers.Int64Value,
    )
    status = proto.Field(
        proto.ENUM,
        number=5,
        enum=manager_link_status.ManagerLinkStatusEnum.ManagerLinkStatus,
    )
    hidden = proto.Field(proto.MESSAGE, number=6, message=wrappers.BoolValue,)


__all__ = tuple(sorted(__protobuf__.manifest))
