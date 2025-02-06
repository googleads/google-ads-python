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

from typing import MutableSequence

import proto  # type: ignore

from google.rpc import status_pb2  # type: ignore


__protobuf__ = proto.module(
    package="google.ads.googleads.v17.services",
    marshal="google.ads.googleads.v17",
    manifest={
        "AppendLeadConversationRequest",
        "AppendLeadConversationResponse",
        "Conversation",
        "ConversationOrError",
    },
)


class AppendLeadConversationRequest(proto.Message):
    r"""Request message for
    [LocalServicesLeadService.AppendLeadConversation][google.ads.googleads.v17.services.LocalServicesLeadService.AppendLeadConversation].

    Attributes:
        customer_id (str):
            Required. The Id of the customer which owns
            the leads onto which the conversations will be
            appended.
        conversations (MutableSequence[google.ads.googleads.v17.services.types.Conversation]):
            Required. Conversations that are being
            appended.
    """

    customer_id: str = proto.Field(
        proto.STRING,
        number=1,
    )
    conversations: MutableSequence["Conversation"] = proto.RepeatedField(
        proto.MESSAGE,
        number=2,
        message="Conversation",
    )


class AppendLeadConversationResponse(proto.Message):
    r"""Response message for
    [LocalServicesLeadService.AppendLeadConversation][google.ads.googleads.v17.services.LocalServicesLeadService.AppendLeadConversation].

    Attributes:
        responses (MutableSequence[google.ads.googleads.v17.services.types.ConversationOrError]):
            Required. List of append conversation
            operation results.
    """

    responses: MutableSequence["ConversationOrError"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="ConversationOrError",
    )


class Conversation(proto.Message):
    r"""Details of the conversation that needs to be appended.
    Attributes:
        local_services_lead (str):
            Required. The resource name of the local
            services lead that the conversation should be
            applied to.
        text (str):
            Required. Text message that user wanted to
            append to lead.
    """

    local_services_lead: str = proto.Field(
        proto.STRING,
        number=1,
    )
    text: str = proto.Field(
        proto.STRING,
        number=2,
    )


class ConversationOrError(proto.Message):
    r"""Result of the append conversation operation.
    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        local_services_lead_conversation (str):
            The resource name of the appended local
            services lead conversation.

            This field is a member of `oneof`_ ``append_lead_conversation_response``.
        partial_failure_error (google.rpc.status_pb2.Status):
            Failure status when the request could not be
            processed.

            This field is a member of `oneof`_ ``append_lead_conversation_response``.
    """

    local_services_lead_conversation: str = proto.Field(
        proto.STRING,
        number=1,
        oneof="append_lead_conversation_response",
    )
    partial_failure_error: status_pb2.Status = proto.Field(
        proto.MESSAGE,
        number=2,
        oneof="append_lead_conversation_response",
        message=status_pb2.Status,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
