# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: google/ads/googleads_v0/proto/enums/webpage_condition_operand.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='google/ads/googleads_v0/proto/enums/webpage_condition_operand.proto',
  package='google.ads.googleads.v0.enums',
  syntax='proto3',
  serialized_options=_b('\n!com.google.ads.googleads.v0.enumsB\034WebpageConditionOperandProtoP\001ZBgoogle.golang.org/genproto/googleapis/ads/googleads/v0/enums;enums\242\002\003GAA\252\002\035Google.Ads.GoogleAds.V0.Enums\312\002\035Google\\Ads\\GoogleAds\\V0\\Enums\352\002!Google::Ads::GoogleAds::V0::Enums'),
  serialized_pb=_b('\nCgoogle/ads/googleads_v0/proto/enums/webpage_condition_operand.proto\x12\x1dgoogle.ads.googleads.v0.enums\"\xa2\x01\n\x1bWebpageConditionOperandEnum\"\x82\x01\n\x17WebpageConditionOperand\x12\x0f\n\x0bUNSPECIFIED\x10\x00\x12\x0b\n\x07UNKNOWN\x10\x01\x12\x07\n\x03URL\x10\x02\x12\x0c\n\x08\x43\x41TEGORY\x10\x03\x12\x0e\n\nPAGE_TITLE\x10\x04\x12\x10\n\x0cPAGE_CONTENT\x10\x05\x12\x10\n\x0c\x43USTOM_LABEL\x10\x06\x42\xf1\x01\n!com.google.ads.googleads.v0.enumsB\x1cWebpageConditionOperandProtoP\x01ZBgoogle.golang.org/genproto/googleapis/ads/googleads/v0/enums;enums\xa2\x02\x03GAA\xaa\x02\x1dGoogle.Ads.GoogleAds.V0.Enums\xca\x02\x1dGoogle\\Ads\\GoogleAds\\V0\\Enums\xea\x02!Google::Ads::GoogleAds::V0::Enumsb\x06proto3')
)



_WEBPAGECONDITIONOPERANDENUM_WEBPAGECONDITIONOPERAND = _descriptor.EnumDescriptor(
  name='WebpageConditionOperand',
  full_name='google.ads.googleads.v0.enums.WebpageConditionOperandEnum.WebpageConditionOperand',
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
      name='URL', index=2, number=2,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CATEGORY', index=3, number=3,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='PAGE_TITLE', index=4, number=4,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='PAGE_CONTENT', index=5, number=5,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CUSTOM_LABEL', index=6, number=6,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=135,
  serialized_end=265,
)
_sym_db.RegisterEnumDescriptor(_WEBPAGECONDITIONOPERANDENUM_WEBPAGECONDITIONOPERAND)


_WEBPAGECONDITIONOPERANDENUM = _descriptor.Descriptor(
  name='WebpageConditionOperandEnum',
  full_name='google.ads.googleads.v0.enums.WebpageConditionOperandEnum',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _WEBPAGECONDITIONOPERANDENUM_WEBPAGECONDITIONOPERAND,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=103,
  serialized_end=265,
)

_WEBPAGECONDITIONOPERANDENUM_WEBPAGECONDITIONOPERAND.containing_type = _WEBPAGECONDITIONOPERANDENUM
DESCRIPTOR.message_types_by_name['WebpageConditionOperandEnum'] = _WEBPAGECONDITIONOPERANDENUM
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

WebpageConditionOperandEnum = _reflection.GeneratedProtocolMessageType('WebpageConditionOperandEnum', (_message.Message,), dict(
  DESCRIPTOR = _WEBPAGECONDITIONOPERANDENUM,
  __module__ = 'google.ads.googleads_v0.proto.enums.webpage_condition_operand_pb2'
  ,
  __doc__ = """Container for enum describing webpage condition operand in webpage
  criterion.
  """,
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v0.enums.WebpageConditionOperandEnum)
  ))
_sym_db.RegisterMessage(WebpageConditionOperandEnum)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
