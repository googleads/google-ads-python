# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: google/ads/googleads_v3/proto/enums/search_term_targeting_status.proto

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
  name='google/ads/googleads_v3/proto/enums/search_term_targeting_status.proto',
  package='google.ads.googleads.v3.enums',
  syntax='proto3',
  serialized_options=_b('\n!com.google.ads.googleads.v3.enumsB\036SearchTermTargetingStatusProtoP\001ZBgoogle.golang.org/genproto/googleapis/ads/googleads/v3/enums;enums\242\002\003GAA\252\002\035Google.Ads.GoogleAds.V3.Enums\312\002\035Google\\Ads\\GoogleAds\\V3\\Enums\352\002!Google::Ads::GoogleAds::V3::Enums'),
  serialized_pb=_b('\nFgoogle/ads/googleads_v3/proto/enums/search_term_targeting_status.proto\x12\x1dgoogle.ads.googleads.v3.enums\x1a\x1cgoogle/api/annotations.proto\"\x91\x01\n\x1dSearchTermTargetingStatusEnum\"p\n\x19SearchTermTargetingStatus\x12\x0f\n\x0bUNSPECIFIED\x10\x00\x12\x0b\n\x07UNKNOWN\x10\x01\x12\t\n\x05\x41\x44\x44\x45\x44\x10\x02\x12\x0c\n\x08\x45XCLUDED\x10\x03\x12\x12\n\x0e\x41\x44\x44\x45\x44_EXCLUDED\x10\x04\x12\x08\n\x04NONE\x10\x05\x42\xf3\x01\n!com.google.ads.googleads.v3.enumsB\x1eSearchTermTargetingStatusProtoP\x01ZBgoogle.golang.org/genproto/googleapis/ads/googleads/v3/enums;enums\xa2\x02\x03GAA\xaa\x02\x1dGoogle.Ads.GoogleAds.V3.Enums\xca\x02\x1dGoogle\\Ads\\GoogleAds\\V3\\Enums\xea\x02!Google::Ads::GoogleAds::V3::Enumsb\x06proto3')
  ,
  dependencies=[google_dot_api_dot_annotations__pb2.DESCRIPTOR,])



_SEARCHTERMTARGETINGSTATUSENUM_SEARCHTERMTARGETINGSTATUS = _descriptor.EnumDescriptor(
  name='SearchTermTargetingStatus',
  full_name='google.ads.googleads.v3.enums.SearchTermTargetingStatusEnum.SearchTermTargetingStatus',
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
      name='ADDED', index=2, number=2,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='EXCLUDED', index=3, number=3,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ADDED_EXCLUDED', index=4, number=4,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='NONE', index=5, number=5,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=169,
  serialized_end=281,
)
_sym_db.RegisterEnumDescriptor(_SEARCHTERMTARGETINGSTATUSENUM_SEARCHTERMTARGETINGSTATUS)


_SEARCHTERMTARGETINGSTATUSENUM = _descriptor.Descriptor(
  name='SearchTermTargetingStatusEnum',
  full_name='google.ads.googleads.v3.enums.SearchTermTargetingStatusEnum',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _SEARCHTERMTARGETINGSTATUSENUM_SEARCHTERMTARGETINGSTATUS,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=136,
  serialized_end=281,
)

_SEARCHTERMTARGETINGSTATUSENUM_SEARCHTERMTARGETINGSTATUS.containing_type = _SEARCHTERMTARGETINGSTATUSENUM
DESCRIPTOR.message_types_by_name['SearchTermTargetingStatusEnum'] = _SEARCHTERMTARGETINGSTATUSENUM
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

SearchTermTargetingStatusEnum = _reflection.GeneratedProtocolMessageType('SearchTermTargetingStatusEnum', (_message.Message,), dict(
  DESCRIPTOR = _SEARCHTERMTARGETINGSTATUSENUM,
  __module__ = 'google.ads.googleads_v3.proto.enums.search_term_targeting_status_pb2'
  ,
  __doc__ = """Container for enum indicating whether a search term is one of your
  targeted or excluded keywords.
  """,
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v3.enums.SearchTermTargetingStatusEnum)
  ))
_sym_db.RegisterMessage(SearchTermTargetingStatusEnum)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
