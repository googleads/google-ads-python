# -*- coding: utf-8 -*-
# Copyright 2023 Google LLC
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
    package="google.ads.googleads.v15.common",
    marshal="google.ads.googleads.v15",
    manifest={
        "CustomParameter",
    },
)


class CustomParameter(proto.Message):
    r"""A mapping that can be used by custom parameter tags in a
    ``tracking_url_template``, ``final_urls``, or ``mobile_final_urls``.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        key (str):
            The key matching the parameter tag name.

            This field is a member of `oneof`_ ``_key``.
        value (str):
            The value to be substituted.

            This field is a member of `oneof`_ ``_value``.
    """

    key: str = proto.Field(
        proto.STRING,
        number=3,
        optional=True,
    )
    value: str = proto.Field(
        proto.STRING,
        number=4,
        optional=True,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
