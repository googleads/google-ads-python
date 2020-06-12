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


from google.protobuf import wrappers_pb2 as wrappers  # type: ignore


__protobuf__ = proto.module(
    package="google.ads.googleads.v4.common",
    marshal="google.ads.googleads.v4",
    manifest={"TextLabel",},
)


class TextLabel(proto.Message):
    r"""A type of label displaying text on a colored background.

    Attributes:
        background_color (google.protobuf.wrappers_pb2.StringValue):
            Background color of the label in RGB format. This string
            must match the regular expression
            '^#([a-fA-F0-9]{6}|[a-fA-F0-9]{3})$'. Note: The background
            color may not be visible for manager accounts.
        description (google.protobuf.wrappers_pb2.StringValue):
            A short description of the label. The length
            must be no more than 200 characters.
    """

    background_color = proto.Field(
        proto.MESSAGE, number=1, message=wrappers.StringValue,
    )
    description = proto.Field(
        proto.MESSAGE, number=2, message=wrappers.StringValue,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
