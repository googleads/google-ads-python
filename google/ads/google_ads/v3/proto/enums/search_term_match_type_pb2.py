# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: google/ads/googleads_v3/proto/enums/search_term_match_type.proto

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
  name='google/ads/googleads_v3/proto/enums/search_term_match_type.proto',
  package='google.ads.googleads.v3.enums',
  syntax='proto3',
  serialized_options=_b('\n!com.google.ads.googleads.v3.enumsB\030SearchTermMatchTypeProtoP\001ZBgoogle.golang.org/genproto/googleapis/ads/googleads/v3/enums;enums\242\002\003GAA\252\002\035Google.Ads.GoogleAds.V3.Enums\312\002\035Google\\Ads\\GoogleAds\\V3\\Enums\352\002!Google::Ads::GoogleAds::V3::Enums'),
  serialized_pb=_b('\n@google/ads/googleads_v3/proto/enums/search_term_match_type.proto\x12\x1dgoogle.ads.googleads.v3.enums\x1a\x1cgoogle/api/annotations.proto\"\x91\x01\n\x17SearchTermMatchTypeEnum\"v\n\x13SearchTermMatchType\x12\x0f\n\x0bUNSPECIFIED\x10\x00\x12\x0b\n\x07UNKNOWN\x10\x01\x12\t\n\x05\x42ROAD\x10\x02\x12\t\n\x05\x45XACT\x10\x03\x12\n\n\x06PHRASE\x10\x04\x12\x0e\n\nNEAR_EXACT\x10\x05\x12\x0f\n\x0bNEAR_PHRASE\x10\x06\x42\xed\x01\n!com.google.ads.googleads.v3.enumsB\x18SearchTermMatchTypeProtoP\x01ZBgoogle.golang.org/genproto/googleapis/ads/googleads/v3/enums;enums\xa2\x02\x03GAA\xaa\x02\x1dGoogle.Ads.GoogleAds.V3.Enums\xca\x02\x1dGoogle\\Ads\\GoogleAds\\V3\\Enums\xea\x02!Google::Ads::GoogleAds::V3::Enumsb\x06proto3')
  ,
  dependencies=[google_dot_api_dot_annotations__pb2.DESCRIPTOR,])



_SEARCHTERMMATCHTYPEENUM_SEARCHTERMMATCHTYPE = _descriptor.EnumDescriptor(
  name='SearchTermMatchType',
  full_name='google.ads.googleads.v3.enums.SearchTermMatchTypeEnum.SearchTermMatchType',
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
      name='BROAD', index=2, number=2,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='EXACT', index=3, number=3,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='PHRASE', index=4, number=4,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='NEAR_EXACT', index=5, number=5,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='NEAR_PHRASE', index=6, number=6,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=157,
  serialized_end=275,
)
_sym_db.RegisterEnumDescriptor(_SEARCHTERMMATCHTYPEENUM_SEARCHTERMMATCHTYPE)


_SEARCHTERMMATCHTYPEENUM = _descriptor.Descriptor(
  name='SearchTermMatchTypeEnum',
  full_name='google.ads.googleads.v3.enums.SearchTermMatchTypeEnum',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _SEARCHTERMMATCHTYPEENUM_SEARCHTERMMATCHTYPE,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=130,
  serialized_end=275,
)

_SEARCHTERMMATCHTYPEENUM_SEARCHTERMMATCHTYPE.containing_type = _SEARCHTERMMATCHTYPEENUM
DESCRIPTOR.message_types_by_name['SearchTermMatchTypeEnum'] = _SEARCHTERMMATCHTYPEENUM
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

SearchTermMatchTypeEnum = _reflection.GeneratedProtocolMessageType('SearchTermMatchTypeEnum', (_message.Message,), dict(
  DESCRIPTOR = _SEARCHTERMMATCHTYPEENUM,
  __module__ = 'google.ads.googleads_v3.proto.enums.search_term_match_type_pb2'
  ,
  __doc__ = """Container for enum describing match types for a keyword triggering an
  ad.
  """,
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v3.enums.SearchTermMatchTypeEnum)
  ))
_sym_db.RegisterMessage(SearchTermMatchTypeEnum)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
