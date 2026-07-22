# -*- coding: utf-8 -*-
# Copyright 2026 Google LLC
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

from google.ads.googleads.v25.enums.types import gls_phone_number_type


__protobuf__ = proto.module(
    package="google.ads.googleads.v25.common",
    marshal="google.ads.googleads.v25",
    manifest={
        "LocalServicesDocumentReadOnly",
        "LocalServicesPhoneNumber",
    },
)


class LocalServicesDocumentReadOnly(proto.Message):
    r"""A Local Services Document with read only accessible data.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        document_url (str):
            URL to access an already uploaded Local
            Services document.

            This field is a member of `oneof`_ ``_document_url``.
    """

    document_url: str = proto.Field(
        proto.STRING,
        number=1,
        optional=True,
    )


class LocalServicesPhoneNumber(proto.Message):
    r"""Phone number associated with the provider.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        phone_number (str):
            The phone number.

            This field is a member of `oneof`_ ``_phone_number``.
        country_code (str):
            Upper-case, two-letter codes as defined by
            ISO-3166.

            This field is a member of `oneof`_ ``_country_code``.
        phone_number_type (google.ads.googleads.v25.enums.types.GlsPhoneNumberTypeEnum.GlsPhoneNumberType):
            The type of the phone number.

            This field is a member of `oneof`_ ``_phone_number_type``.
    """

    phone_number: str = proto.Field(
        proto.STRING,
        number=1,
        optional=True,
    )
    country_code: str = proto.Field(
        proto.STRING,
        number=2,
        optional=True,
    )
    phone_number_type: (
        gls_phone_number_type.GlsPhoneNumberTypeEnum.GlsPhoneNumberType
    ) = proto.Field(
        proto.ENUM,
        number=3,
        optional=True,
        enum=gls_phone_number_type.GlsPhoneNumberTypeEnum.GlsPhoneNumberType,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
