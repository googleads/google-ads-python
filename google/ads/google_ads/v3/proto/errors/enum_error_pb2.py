# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: google/ads/googleads_v3/proto/errors/enum_error.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='google/ads/googleads_v3/proto/errors/enum_error.proto',
  package='google.ads.googleads.v3.errors',
  syntax='proto3',
  serialized_options=_b('\n\"com.google.ads.googleads.v3.errorsB\016EnumErrorProtoP\001ZDgoogle.golang.org/genproto/googleapis/ads/googleads/v3/errors;errors\242\002\003GAA\252\002\036Google.Ads.GoogleAds.V3.Errors\312\002\036Google\\Ads\\GoogleAds\\V3\\Errors\352\002\"Google::Ads::GoogleAds::V3::Errors'),
  serialized_pb=_b('\n5google/ads/googleads_v3/proto/errors/enum_error.proto\x12\x1egoogle.ads.googleads.v3.errors\x1a\x1cgoogle/api/annotations.proto\"X\n\rEnumErrorEnum\"G\n\tEnumError\x12\x0f\n\x0bUNSPECIFIED\x10\x00\x12\x0b\n\x07UNKNOWN\x10\x01\x12\x1c\n\x18\x45NUM_VALUE_NOT_PERMITTED\x10\x03\x42\xe9\x01\n\"com.google.ads.googleads.v3.errorsB\x0e\x45numErrorProtoP\x01ZDgoogle.golang.org/genproto/googleapis/ads/googleads/v3/errors;errors\xa2\x02\x03GAA\xaa\x02\x1eGoogle.Ads.GoogleAds.V3.Errors\xca\x02\x1eGoogle\\Ads\\GoogleAds\\V3\\Errors\xea\x02\"Google::Ads::GoogleAds::V3::Errorsb\x06proto3')
  ,
  dependencies=[google_dot_api_dot_annotations__pb2.DESCRIPTOR,])



_ENUMERRORENUM_ENUMERROR = _descriptor.EnumDescriptor(
  name='EnumError',
  full_name='google.ads.googleads.v3.errors.EnumErrorEnum.EnumError',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='UNSPECIFIED', index=0, number=0,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='UNKNOWN', index=1, number=1,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ENUM_VALUE_NOT_PERMITTED', index=2, number=3,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=136,
  serialized_end=207,
)
_sym_db.RegisterEnumDescriptor(_ENUMERRORENUM_ENUMERROR)


_ENUMERRORENUM = _descriptor.Descriptor(
  name='EnumErrorEnum',
  full_name='google.ads.googleads.v3.errors.EnumErrorEnum',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _ENUMERRORENUM_ENUMERROR,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=119,
  serialized_end=207,
)

_ENUMERRORENUM_ENUMERROR.containing_type = _ENUMERRORENUM
DESCRIPTOR.message_types_by_name['EnumErrorEnum'] = _ENUMERRORENUM
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

EnumErrorEnum = _reflection.GeneratedProtocolMessageType('EnumErrorEnum', (_message.Message,), dict(
  DESCRIPTOR = _ENUMERRORENUM,
  __module__ = 'google.ads.googleads_v3.proto.errors.enum_error_pb2'
  ,
  __doc__ = """Container for enum describing possible enum errors.
  """,
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v3.errors.EnumErrorEnum)
  ))
_sym_db.RegisterMessage(EnumErrorEnum)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
