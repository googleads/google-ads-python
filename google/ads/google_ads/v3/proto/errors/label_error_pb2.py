# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: google/ads/googleads_v3/proto/errors/label_error.proto

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
  name='google/ads/googleads_v3/proto/errors/label_error.proto',
  package='google.ads.googleads.v3.errors',
  syntax='proto3',
  serialized_options=_b('\n\"com.google.ads.googleads.v3.errorsB\017LabelErrorProtoP\001ZDgoogle.golang.org/genproto/googleapis/ads/googleads/v3/errors;errors\242\002\003GAA\252\002\036Google.Ads.GoogleAds.V3.Errors\312\002\036Google\\Ads\\GoogleAds\\V3\\Errors\352\002\"Google::Ads::GoogleAds::V3::Errors'),
  serialized_pb=_b('\n6google/ads/googleads_v3/proto/errors/label_error.proto\x12\x1egoogle.ads.googleads.v3.errors\x1a\x1cgoogle/api/annotations.proto\"\x96\x03\n\x0eLabelErrorEnum\"\x83\x03\n\nLabelError\x12\x0f\n\x0bUNSPECIFIED\x10\x00\x12\x0b\n\x07UNKNOWN\x10\x01\x12\x1f\n\x1b\x43\x41NNOT_APPLY_INACTIVE_LABEL\x10\x02\x12\x35\n1CANNOT_APPLY_LABEL_TO_DISABLED_AD_GROUP_CRITERION\x10\x03\x12\x35\n1CANNOT_APPLY_LABEL_TO_NEGATIVE_AD_GROUP_CRITERION\x10\x04\x12!\n\x1d\x45XCEEDED_LABEL_LIMIT_PER_TYPE\x10\x05\x12&\n\"INVALID_RESOURCE_FOR_MANAGER_LABEL\x10\x06\x12\x12\n\x0e\x44UPLICATE_NAME\x10\x07\x12\x16\n\x12INVALID_LABEL_NAME\x10\x08\x12 \n\x1c\x43\x41NNOT_ATTACH_LABEL_TO_DRAFT\x10\t\x12/\n+CANNOT_ATTACH_NON_MANAGER_LABEL_TO_CUSTOMER\x10\nB\xea\x01\n\"com.google.ads.googleads.v3.errorsB\x0fLabelErrorProtoP\x01ZDgoogle.golang.org/genproto/googleapis/ads/googleads/v3/errors;errors\xa2\x02\x03GAA\xaa\x02\x1eGoogle.Ads.GoogleAds.V3.Errors\xca\x02\x1eGoogle\\Ads\\GoogleAds\\V3\\Errors\xea\x02\"Google::Ads::GoogleAds::V3::Errorsb\x06proto3')
  ,
  dependencies=[google_dot_api_dot_annotations__pb2.DESCRIPTOR,])



_LABELERRORENUM_LABELERROR = _descriptor.EnumDescriptor(
  name='LabelError',
  full_name='google.ads.googleads.v3.errors.LabelErrorEnum.LabelError',
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
      name='CANNOT_APPLY_INACTIVE_LABEL', index=2, number=2,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CANNOT_APPLY_LABEL_TO_DISABLED_AD_GROUP_CRITERION', index=3, number=3,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CANNOT_APPLY_LABEL_TO_NEGATIVE_AD_GROUP_CRITERION', index=4, number=4,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='EXCEEDED_LABEL_LIMIT_PER_TYPE', index=5, number=5,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='INVALID_RESOURCE_FOR_MANAGER_LABEL', index=6, number=6,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='DUPLICATE_NAME', index=7, number=7,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='INVALID_LABEL_NAME', index=8, number=8,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CANNOT_ATTACH_LABEL_TO_DRAFT', index=9, number=9,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CANNOT_ATTACH_NON_MANAGER_LABEL_TO_CUSTOMER', index=10, number=10,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=140,
  serialized_end=527,
)
_sym_db.RegisterEnumDescriptor(_LABELERRORENUM_LABELERROR)


_LABELERRORENUM = _descriptor.Descriptor(
  name='LabelErrorEnum',
  full_name='google.ads.googleads.v3.errors.LabelErrorEnum',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _LABELERRORENUM_LABELERROR,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=121,
  serialized_end=527,
)

_LABELERRORENUM_LABELERROR.containing_type = _LABELERRORENUM
DESCRIPTOR.message_types_by_name['LabelErrorEnum'] = _LABELERRORENUM
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

LabelErrorEnum = _reflection.GeneratedProtocolMessageType('LabelErrorEnum', (_message.Message,), dict(
  DESCRIPTOR = _LABELERRORENUM,
  __module__ = 'google.ads.googleads_v3.proto.errors.label_error_pb2'
  ,
  __doc__ = """Container for enum describing possible label errors.
  """,
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v3.errors.LabelErrorEnum)
  ))
_sym_db.RegisterMessage(LabelErrorEnum)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
