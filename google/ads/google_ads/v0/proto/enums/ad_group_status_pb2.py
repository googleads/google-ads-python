# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: google/ads/googleads_v0/proto/enums/ad_group_status.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='google/ads/googleads_v0/proto/enums/ad_group_status.proto',
  package='google.ads.googleads.v0.enums',
  syntax='proto3',
  serialized_options=_b('\n!com.google.ads.googleads.v0.enumsB\022AdGroupStatusProtoP\001ZBgoogle.golang.org/genproto/googleapis/ads/googleads/v0/enums;enums\242\002\003GAA\252\002\035Google.Ads.GoogleAds.V0.Enums\312\002\035Google\\Ads\\GoogleAds\\V0\\Enums\352\002!Google::Ads::GoogleAds::V0::Enums'),
  serialized_pb=_b('\n9google/ads/googleads_v0/proto/enums/ad_group_status.proto\x12\x1dgoogle.ads.googleads.v0.enums\"h\n\x11\x41\x64GroupStatusEnum\"S\n\rAdGroupStatus\x12\x0f\n\x0bUNSPECIFIED\x10\x00\x12\x0b\n\x07UNKNOWN\x10\x01\x12\x0b\n\x07\x45NABLED\x10\x02\x12\n\n\x06PAUSED\x10\x03\x12\x0b\n\x07REMOVED\x10\x04\x42\xe7\x01\n!com.google.ads.googleads.v0.enumsB\x12\x41\x64GroupStatusProtoP\x01ZBgoogle.golang.org/genproto/googleapis/ads/googleads/v0/enums;enums\xa2\x02\x03GAA\xaa\x02\x1dGoogle.Ads.GoogleAds.V0.Enums\xca\x02\x1dGoogle\\Ads\\GoogleAds\\V0\\Enums\xea\x02!Google::Ads::GoogleAds::V0::Enumsb\x06proto3')
)



_ADGROUPSTATUSENUM_ADGROUPSTATUS = _descriptor.EnumDescriptor(
  name='AdGroupStatus',
  full_name='google.ads.googleads.v0.enums.AdGroupStatusEnum.AdGroupStatus',
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
      name='ENABLED', index=2, number=2,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='PAUSED', index=3, number=3,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='REMOVED', index=4, number=4,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=113,
  serialized_end=196,
)
_sym_db.RegisterEnumDescriptor(_ADGROUPSTATUSENUM_ADGROUPSTATUS)


_ADGROUPSTATUSENUM = _descriptor.Descriptor(
  name='AdGroupStatusEnum',
  full_name='google.ads.googleads.v0.enums.AdGroupStatusEnum',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _ADGROUPSTATUSENUM_ADGROUPSTATUS,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=92,
  serialized_end=196,
)

_ADGROUPSTATUSENUM_ADGROUPSTATUS.containing_type = _ADGROUPSTATUSENUM
DESCRIPTOR.message_types_by_name['AdGroupStatusEnum'] = _ADGROUPSTATUSENUM
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

AdGroupStatusEnum = _reflection.GeneratedProtocolMessageType('AdGroupStatusEnum', (_message.Message,), dict(
  DESCRIPTOR = _ADGROUPSTATUSENUM,
  __module__ = 'google.ads.googleads_v0.proto.enums.ad_group_status_pb2'
  ,
  __doc__ = """Container for enum describing possible statuses of an ad group.
  """,
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v0.enums.AdGroupStatusEnum)
  ))
_sym_db.RegisterMessage(AdGroupStatusEnum)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
