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
    package="google.ads.googleads.v20.resources",
    marshal="google.ads.googleads.v20",
    manifest={
        "MobileAppCategoryConstant",
    },
)


class MobileAppCategoryConstant(proto.Message):
    r"""A mobile application category constant.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        resource_name (str):
            Output only. The resource name of the mobile app category
            constant. Mobile app category constant resource names have
            the form:

            ``mobileAppCategoryConstants/{mobile_app_category_id}``
        id (int):
            Output only. The ID of the mobile app
            category constant.

            This field is a member of `oneof`_ ``_id``.
        name (str):
            Output only. Mobile app category name.

            This field is a member of `oneof`_ ``_name``.
    """

    resource_name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    id: int = proto.Field(
        proto.INT32,
        number=4,
        optional=True,
    )
    name: str = proto.Field(
        proto.STRING,
        number=5,
        optional=True,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
