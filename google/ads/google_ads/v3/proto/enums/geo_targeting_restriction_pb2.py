# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: google/ads/googleads_v3/proto/enums/geo_targeting_restriction.proto

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
  name='google/ads/googleads_v3/proto/enums/geo_targeting_restriction.proto',
  package='google.ads.googleads.v3.enums',
  syntax='proto3',
  serialized_options=_b('\n!com.google.ads.googleads.v3.enumsB\034GeoTargetingRestrictionProtoP\001ZBgoogle.golang.org/genproto/googleapis/ads/googleads/v3/enums;enums\242\002\003GAA\252\002\035Google.Ads.GoogleAds.V3.Enums\312\002\035Google\\Ads\\GoogleAds\\V3\\Enums\352\002!Google::Ads::GoogleAds::V3::Enums'),
  serialized_pb=_b('\nCgoogle/ads/googleads_v3/proto/enums/geo_targeting_restriction.proto\x12\x1dgoogle.ads.googleads.v3.enums\x1a\x1cgoogle/api/annotations.proto\"p\n\x1bGeoTargetingRestrictionEnum\"Q\n\x17GeoTargetingRestriction\x12\x0f\n\x0bUNSPECIFIED\x10\x00\x12\x0b\n\x07UNKNOWN\x10\x01\x12\x18\n\x14LOCATION_OF_PRESENCE\x10\x02\x42\xf1\x01\n!com.google.ads.googleads.v3.enumsB\x1cGeoTargetingRestrictionProtoP\x01ZBgoogle.golang.org/genproto/googleapis/ads/googleads/v3/enums;enums\xa2\x02\x03GAA\xaa\x02\x1dGoogle.Ads.GoogleAds.V3.Enums\xca\x02\x1dGoogle\\Ads\\GoogleAds\\V3\\Enums\xea\x02!Google::Ads::GoogleAds::V3::Enumsb\x06proto3')
  ,
  dependencies=[google_dot_api_dot_annotations__pb2.DESCRIPTOR,])



_GEOTARGETINGRESTRICTIONENUM_GEOTARGETINGRESTRICTION = _descriptor.EnumDescriptor(
  name='GeoTargetingRestriction',
  full_name='google.ads.googleads.v3.enums.GeoTargetingRestrictionEnum.GeoTargetingRestriction',
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
      name='LOCATION_OF_PRESENCE', index=2, number=2,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=163,
  serialized_end=244,
)
_sym_db.RegisterEnumDescriptor(_GEOTARGETINGRESTRICTIONENUM_GEOTARGETINGRESTRICTION)


_GEOTARGETINGRESTRICTIONENUM = _descriptor.Descriptor(
  name='GeoTargetingRestrictionEnum',
  full_name='google.ads.googleads.v3.enums.GeoTargetingRestrictionEnum',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _GEOTARGETINGRESTRICTIONENUM_GEOTARGETINGRESTRICTION,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=132,
  serialized_end=244,
)

_GEOTARGETINGRESTRICTIONENUM_GEOTARGETINGRESTRICTION.containing_type = _GEOTARGETINGRESTRICTIONENUM
DESCRIPTOR.message_types_by_name['GeoTargetingRestrictionEnum'] = _GEOTARGETINGRESTRICTIONENUM
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

GeoTargetingRestrictionEnum = _reflection.GeneratedProtocolMessageType('GeoTargetingRestrictionEnum', (_message.Message,), dict(
  DESCRIPTOR = _GEOTARGETINGRESTRICTIONENUM,
  __module__ = 'google.ads.googleads_v3.proto.enums.geo_targeting_restriction_pb2'
  ,
  __doc__ = """Message describing feed item geo targeting restriction.
  """,
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v3.enums.GeoTargetingRestrictionEnum)
  ))
_sym_db.RegisterMessage(GeoTargetingRestrictionEnum)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
