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

from google.ads.googleads.v20.enums.types import manager_link_status


__protobuf__ = proto.module(
    package="google.ads.googleads.v20.resources",
    marshal="google.ads.googleads.v20",
    manifest={
        "CustomerManagerLink",
    },
)


class CustomerManagerLink(proto.Message):
    r"""Represents customer-manager link relationship.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        resource_name (str):
            Immutable. Name of the resource. CustomerManagerLink
            resource names have the form:
            ``customers/{customer_id}/customerManagerLinks/{manager_customer_id}~{manager_link_id}``
        manager_customer (str):
            Output only. The manager customer linked to
            the customer.

            This field is a member of `oneof`_ ``_manager_customer``.
        manager_link_id (int):
            Output only. ID of the customer-manager link.
            This field is read only.

            This field is a member of `oneof`_ ``_manager_link_id``.
        status (google.ads.googleads.v20.enums.types.ManagerLinkStatusEnum.ManagerLinkStatus):
            Status of the link between the customer and
            the manager.
    """

    resource_name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    manager_customer: str = proto.Field(
        proto.STRING,
        number=6,
        optional=True,
    )
    manager_link_id: int = proto.Field(
        proto.INT64,
        number=7,
        optional=True,
    )
    status: manager_link_status.ManagerLinkStatusEnum.ManagerLinkStatus = (
        proto.Field(
            proto.ENUM,
            number=5,
            enum=manager_link_status.ManagerLinkStatusEnum.ManagerLinkStatus,
        )
    )


__all__ = tuple(sorted(__protobuf__.manifest))
