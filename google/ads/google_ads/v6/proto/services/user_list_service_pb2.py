# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: google/ads/googleads_v6/proto/services/user_list_service.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.ads.google_ads.v6.proto.resources import user_list_pb2 as google_dot_ads_dot_googleads__v6_dot_proto_dot_resources_dot_user__list__pb2
from google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2
from google.api import client_pb2 as google_dot_api_dot_client__pb2
from google.api import field_behavior_pb2 as google_dot_api_dot_field__behavior__pb2
from google.api import resource_pb2 as google_dot_api_dot_resource__pb2
from google.protobuf import field_mask_pb2 as google_dot_protobuf_dot_field__mask__pb2
from google.rpc import status_pb2 as google_dot_rpc_dot_status__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='google/ads/googleads_v6/proto/services/user_list_service.proto',
  package='google.ads.googleads.v6.services',
  syntax='proto3',
  serialized_options=b'\n$com.google.ads.googleads.v6.servicesB\024UserListServiceProtoP\001ZHgoogle.golang.org/genproto/googleapis/ads/googleads/v6/services;services\242\002\003GAA\252\002 Google.Ads.GoogleAds.V6.Services\312\002 Google\\Ads\\GoogleAds\\V6\\Services\352\002$Google::Ads::GoogleAds::V6::Services',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n>google/ads/googleads_v6/proto/services/user_list_service.proto\x12 google.ads.googleads.v6.services\x1a\x37google/ads/googleads_v6/proto/resources/user_list.proto\x1a\x1cgoogle/api/annotations.proto\x1a\x17google/api/client.proto\x1a\x1fgoogle/api/field_behavior.proto\x1a\x19google/api/resource.proto\x1a google/protobuf/field_mask.proto\x1a\x17google/rpc/status.proto\"V\n\x12GetUserListRequest\x12@\n\rresource_name\x18\x01 \x01(\tB)\xe0\x41\x02\xfa\x41#\n!googleads.googleapis.com/UserList\"\xb0\x01\n\x16MutateUserListsRequest\x12\x18\n\x0b\x63ustomer_id\x18\x01 \x01(\tB\x03\xe0\x41\x02\x12L\n\noperations\x18\x02 \x03(\x0b\x32\x33.google.ads.googleads.v6.services.UserListOperationB\x03\xe0\x41\x02\x12\x17\n\x0fpartial_failure\x18\x03 \x01(\x08\x12\x15\n\rvalidate_only\x18\x04 \x01(\x08\"\xe1\x01\n\x11UserListOperation\x12/\n\x0bupdate_mask\x18\x04 \x01(\x0b\x32\x1a.google.protobuf.FieldMask\x12=\n\x06\x63reate\x18\x01 \x01(\x0b\x32+.google.ads.googleads.v6.resources.UserListH\x00\x12=\n\x06update\x18\x02 \x01(\x0b\x32+.google.ads.googleads.v6.resources.UserListH\x00\x12\x10\n\x06remove\x18\x03 \x01(\tH\x00\x42\x0b\n\toperation\"\x95\x01\n\x17MutateUserListsResponse\x12\x31\n\x15partial_failure_error\x18\x03 \x01(\x0b\x32\x12.google.rpc.Status\x12G\n\x07results\x18\x02 \x03(\x0b\x32\x36.google.ads.googleads.v6.services.MutateUserListResult\"-\n\x14MutateUserListResult\x12\x15\n\rresource_name\x18\x01 \x01(\t2\xc3\x03\n\x0fUserListService\x12\xb5\x01\n\x0bGetUserList\x12\x34.google.ads.googleads.v6.services.GetUserListRequest\x1a+.google.ads.googleads.v6.resources.UserList\"C\x82\xd3\xe4\x93\x02-\x12+/v6/{resource_name=customers/*/userLists/*}\xda\x41\rresource_name\x12\xda\x01\n\x0fMutateUserLists\x12\x38.google.ads.googleads.v6.services.MutateUserListsRequest\x1a\x39.google.ads.googleads.v6.services.MutateUserListsResponse\"R\x82\xd3\xe4\x93\x02\x33\"./v6/customers/{customer_id=*}/userLists:mutate:\x01*\xda\x41\x16\x63ustomer_id,operations\x1a\x1b\xca\x41\x18googleads.googleapis.comB\xfb\x01\n$com.google.ads.googleads.v6.servicesB\x14UserListServiceProtoP\x01ZHgoogle.golang.org/genproto/googleapis/ads/googleads/v6/services;services\xa2\x02\x03GAA\xaa\x02 Google.Ads.GoogleAds.V6.Services\xca\x02 Google\\Ads\\GoogleAds\\V6\\Services\xea\x02$Google::Ads::GoogleAds::V6::Servicesb\x06proto3'
  ,
  dependencies=[google_dot_ads_dot_googleads__v6_dot_proto_dot_resources_dot_user__list__pb2.DESCRIPTOR,google_dot_api_dot_annotations__pb2.DESCRIPTOR,google_dot_api_dot_client__pb2.DESCRIPTOR,google_dot_api_dot_field__behavior__pb2.DESCRIPTOR,google_dot_api_dot_resource__pb2.DESCRIPTOR,google_dot_protobuf_dot_field__mask__pb2.DESCRIPTOR,google_dot_rpc_dot_status__pb2.DESCRIPTOR,])




_GETUSERLISTREQUEST = _descriptor.Descriptor(
  name='GetUserListRequest',
  full_name='google.ads.googleads.v6.services.GetUserListRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='resource_name', full_name='google.ads.googleads.v6.services.GetUserListRequest.resource_name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\340A\002\372A#\n!googleads.googleapis.com/UserList', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=331,
  serialized_end=417,
)


_MUTATEUSERLISTSREQUEST = _descriptor.Descriptor(
  name='MutateUserListsRequest',
  full_name='google.ads.googleads.v6.services.MutateUserListsRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='customer_id', full_name='google.ads.googleads.v6.services.MutateUserListsRequest.customer_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\340A\002', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='operations', full_name='google.ads.googleads.v6.services.MutateUserListsRequest.operations', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\340A\002', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='partial_failure', full_name='google.ads.googleads.v6.services.MutateUserListsRequest.partial_failure', index=2,
      number=3, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='validate_only', full_name='google.ads.googleads.v6.services.MutateUserListsRequest.validate_only', index=3,
      number=4, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=420,
  serialized_end=596,
)


_USERLISTOPERATION = _descriptor.Descriptor(
  name='UserListOperation',
  full_name='google.ads.googleads.v6.services.UserListOperation',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='update_mask', full_name='google.ads.googleads.v6.services.UserListOperation.update_mask', index=0,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='create', full_name='google.ads.googleads.v6.services.UserListOperation.create', index=1,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='update', full_name='google.ads.googleads.v6.services.UserListOperation.update', index=2,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='remove', full_name='google.ads.googleads.v6.services.UserListOperation.remove', index=3,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
    _descriptor.OneofDescriptor(
      name='operation', full_name='google.ads.googleads.v6.services.UserListOperation.operation',
      index=0, containing_type=None,
      create_key=_descriptor._internal_create_key,
    fields=[]),
  ],
  serialized_start=599,
  serialized_end=824,
)


_MUTATEUSERLISTSRESPONSE = _descriptor.Descriptor(
  name='MutateUserListsResponse',
  full_name='google.ads.googleads.v6.services.MutateUserListsResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='partial_failure_error', full_name='google.ads.googleads.v6.services.MutateUserListsResponse.partial_failure_error', index=0,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='results', full_name='google.ads.googleads.v6.services.MutateUserListsResponse.results', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=827,
  serialized_end=976,
)


_MUTATEUSERLISTRESULT = _descriptor.Descriptor(
  name='MutateUserListResult',
  full_name='google.ads.googleads.v6.services.MutateUserListResult',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='resource_name', full_name='google.ads.googleads.v6.services.MutateUserListResult.resource_name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=978,
  serialized_end=1023,
)

_MUTATEUSERLISTSREQUEST.fields_by_name['operations'].message_type = _USERLISTOPERATION
_USERLISTOPERATION.fields_by_name['update_mask'].message_type = google_dot_protobuf_dot_field__mask__pb2._FIELDMASK
_USERLISTOPERATION.fields_by_name['create'].message_type = google_dot_ads_dot_googleads__v6_dot_proto_dot_resources_dot_user__list__pb2._USERLIST
_USERLISTOPERATION.fields_by_name['update'].message_type = google_dot_ads_dot_googleads__v6_dot_proto_dot_resources_dot_user__list__pb2._USERLIST
_USERLISTOPERATION.oneofs_by_name['operation'].fields.append(
  _USERLISTOPERATION.fields_by_name['create'])
_USERLISTOPERATION.fields_by_name['create'].containing_oneof = _USERLISTOPERATION.oneofs_by_name['operation']
_USERLISTOPERATION.oneofs_by_name['operation'].fields.append(
  _USERLISTOPERATION.fields_by_name['update'])
_USERLISTOPERATION.fields_by_name['update'].containing_oneof = _USERLISTOPERATION.oneofs_by_name['operation']
_USERLISTOPERATION.oneofs_by_name['operation'].fields.append(
  _USERLISTOPERATION.fields_by_name['remove'])
_USERLISTOPERATION.fields_by_name['remove'].containing_oneof = _USERLISTOPERATION.oneofs_by_name['operation']
_MUTATEUSERLISTSRESPONSE.fields_by_name['partial_failure_error'].message_type = google_dot_rpc_dot_status__pb2._STATUS
_MUTATEUSERLISTSRESPONSE.fields_by_name['results'].message_type = _MUTATEUSERLISTRESULT
DESCRIPTOR.message_types_by_name['GetUserListRequest'] = _GETUSERLISTREQUEST
DESCRIPTOR.message_types_by_name['MutateUserListsRequest'] = _MUTATEUSERLISTSREQUEST
DESCRIPTOR.message_types_by_name['UserListOperation'] = _USERLISTOPERATION
DESCRIPTOR.message_types_by_name['MutateUserListsResponse'] = _MUTATEUSERLISTSRESPONSE
DESCRIPTOR.message_types_by_name['MutateUserListResult'] = _MUTATEUSERLISTRESULT
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

GetUserListRequest = _reflection.GeneratedProtocolMessageType('GetUserListRequest', (_message.Message,), {
  'DESCRIPTOR' : _GETUSERLISTREQUEST,
  '__module__' : 'google.ads.googleads_v6.proto.services.user_list_service_pb2'
  ,
  '__doc__': """Request message for [UserListService.GetUserList][google.ads.googleads
  .v6.services.UserListService.GetUserList].
  
  Attributes:
      resource_name:
          Required. The resource name of the user list to fetch.
  """,
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v6.services.GetUserListRequest)
  })
_sym_db.RegisterMessage(GetUserListRequest)

MutateUserListsRequest = _reflection.GeneratedProtocolMessageType('MutateUserListsRequest', (_message.Message,), {
  'DESCRIPTOR' : _MUTATEUSERLISTSREQUEST,
  '__module__' : 'google.ads.googleads_v6.proto.services.user_list_service_pb2'
  ,
  '__doc__': """Request message for [UserListService.MutateUserLists][google.ads.googl
  eads.v6.services.UserListService.MutateUserLists].
  
  Attributes:
      customer_id:
          Required. The ID of the customer whose user lists are being
          modified.
      operations:
          Required. The list of operations to perform on individual user
          lists.
      partial_failure:
          If true, successful operations will be carried out and invalid
          operations will return errors. If false, all operations will
          be carried out in one transaction if and only if they are all
          valid. Default is false.
      validate_only:
          If true, the request is validated but not executed. Only
          errors are returned, not results.
  """,
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v6.services.MutateUserListsRequest)
  })
_sym_db.RegisterMessage(MutateUserListsRequest)

UserListOperation = _reflection.GeneratedProtocolMessageType('UserListOperation', (_message.Message,), {
  'DESCRIPTOR' : _USERLISTOPERATION,
  '__module__' : 'google.ads.googleads_v6.proto.services.user_list_service_pb2'
  ,
  '__doc__': """A single operation (create, update) on a user list.
  
  Attributes:
      update_mask:
          FieldMask that determines which resource fields are modified
          in an update.
      operation:
          The mutate operation.
      create:
          Create operation: No resource name is expected for the new
          user list.
      update:
          Update operation: The user list is expected to have a valid
          resource name.
      remove:
          Remove operation: A resource name for the removed user list is
          expected, in this format:
          ``customers/{customer_id}/userLists/{user_list_id}``
  """,
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v6.services.UserListOperation)
  })
_sym_db.RegisterMessage(UserListOperation)

MutateUserListsResponse = _reflection.GeneratedProtocolMessageType('MutateUserListsResponse', (_message.Message,), {
  'DESCRIPTOR' : _MUTATEUSERLISTSRESPONSE,
  '__module__' : 'google.ads.googleads_v6.proto.services.user_list_service_pb2'
  ,
  '__doc__': """Response message for user list mutate.
  
  Attributes:
      partial_failure_error:
          Errors that pertain to operation failures in the partial
          failure mode. Returned only when partial\_failure = true and
          all errors occur inside the operations. If any errors occur
          outside the operations (e.g. auth errors), we return an RPC
          level error.
      results:
          All results for the mutate.
  """,
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v6.services.MutateUserListsResponse)
  })
_sym_db.RegisterMessage(MutateUserListsResponse)

MutateUserListResult = _reflection.GeneratedProtocolMessageType('MutateUserListResult', (_message.Message,), {
  'DESCRIPTOR' : _MUTATEUSERLISTRESULT,
  '__module__' : 'google.ads.googleads_v6.proto.services.user_list_service_pb2'
  ,
  '__doc__': """The result for the user list mutate.
  
  Attributes:
      resource_name:
          Returned for successful operations.
  """,
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v6.services.MutateUserListResult)
  })
_sym_db.RegisterMessage(MutateUserListResult)


DESCRIPTOR._options = None
_GETUSERLISTREQUEST.fields_by_name['resource_name']._options = None
_MUTATEUSERLISTSREQUEST.fields_by_name['customer_id']._options = None
_MUTATEUSERLISTSREQUEST.fields_by_name['operations']._options = None

_USERLISTSERVICE = _descriptor.ServiceDescriptor(
  name='UserListService',
  full_name='google.ads.googleads.v6.services.UserListService',
  file=DESCRIPTOR,
  index=0,
  serialized_options=b'\312A\030googleads.googleapis.com',
  create_key=_descriptor._internal_create_key,
  serialized_start=1026,
  serialized_end=1477,
  methods=[
  _descriptor.MethodDescriptor(
    name='GetUserList',
    full_name='google.ads.googleads.v6.services.UserListService.GetUserList',
    index=0,
    containing_service=None,
    input_type=_GETUSERLISTREQUEST,
    output_type=google_dot_ads_dot_googleads__v6_dot_proto_dot_resources_dot_user__list__pb2._USERLIST,
    serialized_options=b'\202\323\344\223\002-\022+/v6/{resource_name=customers/*/userLists/*}\332A\rresource_name',
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='MutateUserLists',
    full_name='google.ads.googleads.v6.services.UserListService.MutateUserLists',
    index=1,
    containing_service=None,
    input_type=_MUTATEUSERLISTSREQUEST,
    output_type=_MUTATEUSERLISTSRESPONSE,
    serialized_options=b'\202\323\344\223\0023\"./v6/customers/{customer_id=*}/userLists:mutate:\001*\332A\026customer_id,operations',
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_USERLISTSERVICE)

DESCRIPTOR.services_by_name['UserListService'] = _USERLISTSERVICE

# @@protoc_insertion_point(module_scope)
