# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: google/ads/googleads_v5/proto/errors/access_invitation_error.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='google/ads/googleads_v5/proto/errors/access_invitation_error.proto',
  package='google.ads.googleads.v5.errors',
  syntax='proto3',
  serialized_options=b'\n\"com.google.ads.googleads.v5.errorsB\032AccessInvitationErrorProtoP\001ZDgoogle.golang.org/genproto/googleapis/ads/googleads/v5/errors;errors\242\002\003GAA\252\002\036Google.Ads.GoogleAds.V5.Errors\312\002\036Google\\Ads\\GoogleAds\\V5\\Errors\352\002\"Google::Ads::GoogleAds::V5::Errors',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\nBgoogle/ads/googleads_v5/proto/errors/access_invitation_error.proto\x12\x1egoogle.ads.googleads.v5.errors\x1a\x1cgoogle/api/annotations.proto\"\x93\x01\n\x19\x41\x63\x63\x65ssInvitationErrorEnum\"v\n\x15\x41\x63\x63\x65ssInvitationError\x12\x0f\n\x0bUNSPECIFIED\x10\x00\x12\x0b\n\x07UNKNOWN\x10\x01\x12\x19\n\x15INVALID_EMAIL_ADDRESS\x10\x02\x12$\n EMAIL_ADDRESS_ALREADY_HAS_ACCESS\x10\x03\x42\xf5\x01\n\"com.google.ads.googleads.v5.errorsB\x1a\x41\x63\x63\x65ssInvitationErrorProtoP\x01ZDgoogle.golang.org/genproto/googleapis/ads/googleads/v5/errors;errors\xa2\x02\x03GAA\xaa\x02\x1eGoogle.Ads.GoogleAds.V5.Errors\xca\x02\x1eGoogle\\Ads\\GoogleAds\\V5\\Errors\xea\x02\"Google::Ads::GoogleAds::V5::Errorsb\x06proto3'
  ,
  dependencies=[google_dot_api_dot_annotations__pb2.DESCRIPTOR,])



_ACCESSINVITATIONERRORENUM_ACCESSINVITATIONERROR = _descriptor.EnumDescriptor(
  name='AccessInvitationError',
  full_name='google.ads.googleads.v5.errors.AccessInvitationErrorEnum.AccessInvitationError',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='UNSPECIFIED', index=0, number=0,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='UNKNOWN', index=1, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='INVALID_EMAIL_ADDRESS', index=2, number=2,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='EMAIL_ADDRESS_ALREADY_HAS_ACCESS', index=3, number=3,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=162,
  serialized_end=280,
)
_sym_db.RegisterEnumDescriptor(_ACCESSINVITATIONERRORENUM_ACCESSINVITATIONERROR)


_ACCESSINVITATIONERRORENUM = _descriptor.Descriptor(
  name='AccessInvitationErrorEnum',
  full_name='google.ads.googleads.v5.errors.AccessInvitationErrorEnum',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _ACCESSINVITATIONERRORENUM_ACCESSINVITATIONERROR,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=133,
  serialized_end=280,
)

_ACCESSINVITATIONERRORENUM_ACCESSINVITATIONERROR.containing_type = _ACCESSINVITATIONERRORENUM
DESCRIPTOR.message_types_by_name['AccessInvitationErrorEnum'] = _ACCESSINVITATIONERRORENUM
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

AccessInvitationErrorEnum = _reflection.GeneratedProtocolMessageType('AccessInvitationErrorEnum', (_message.Message,), {
  'DESCRIPTOR' : _ACCESSINVITATIONERRORENUM,
  '__module__' : 'google.ads.googleads_v5.proto.errors.access_invitation_error_pb2'
  ,
  '__doc__': """Container for enum describing possible AccessInvitation errors.""",
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v5.errors.AccessInvitationErrorEnum)
  })
_sym_db.RegisterMessage(AccessInvitationErrorEnum)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
