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
    manifest={"CustomerManagerLink",},
)


class CustomerManagerLink(proto.Message):
    r"""Represents customer-manager link relationship.

    Attributes:
        resource_name (str):
            Immutable. Name of the resource. CustomerManagerLink
            resource names have the form:
            ``customers/{customer_id}/customerManagerLinks/{manager_customer_id}~{manager_link_id}``
        manager_customer (google.protobuf.wrappers_pb2.StringValue):
            Output only. The manager customer linked to
            the customer.
        manager_link_id (google.protobuf.wrappers_pb2.Int64Value):
            Output only. ID of the customer-manager link.
            This field is read only.
        status (google.ads.googleads.v4.enums.types.ManagerLinkStatusEnum.ManagerLinkStatus):
            Status of the link between the customer and
            the manager.
    """

    resource_name = proto.Field(proto.STRING, number=1)
    manager_customer = proto.Field(
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


__all__ = tuple(sorted(__protobuf__.manifest))
