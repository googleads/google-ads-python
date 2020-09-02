# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: google/ads/googleads_v5/proto/enums/slot.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='google/ads/googleads_v5/proto/enums/slot.proto',
  package='google.ads.googleads.v5.enums',
  syntax='proto3',
  serialized_options=b'\n!com.google.ads.googleads.v5.enumsB\tSlotProtoP\001ZBgoogle.golang.org/genproto/googleapis/ads/googleads/v5/enums;enums\242\002\003GAA\252\002\035Google.Ads.GoogleAds.V5.Enums\312\002\035Google\\Ads\\GoogleAds\\V5\\Enums\352\002!Google::Ads::GoogleAds::V5::Enums',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n.google/ads/googleads_v5/proto/enums/slot.proto\x12\x1dgoogle.ads.googleads.v5.enums\x1a\x1cgoogle/api/annotations.proto\"\xae\x01\n\x08SlotEnum\"\xa1\x01\n\x04Slot\x12\x0f\n\x0bUNSPECIFIED\x10\x00\x12\x0b\n\x07UNKNOWN\x10\x01\x12\x0f\n\x0bSEARCH_SIDE\x10\x02\x12\x0e\n\nSEARCH_TOP\x10\x03\x12\x10\n\x0cSEARCH_OTHER\x10\x04\x12\x0b\n\x07\x43ONTENT\x10\x05\x12\x16\n\x12SEARCH_PARTNER_TOP\x10\x06\x12\x18\n\x14SEARCH_PARTNER_OTHER\x10\x07\x12\t\n\x05MIXED\x10\x08\x42\xde\x01\n!com.google.ads.googleads.v5.enumsB\tSlotProtoP\x01ZBgoogle.golang.org/genproto/googleapis/ads/googleads/v5/enums;enums\xa2\x02\x03GAA\xaa\x02\x1dGoogle.Ads.GoogleAds.V5.Enums\xca\x02\x1dGoogle\\Ads\\GoogleAds\\V5\\Enums\xea\x02!Google::Ads::GoogleAds::V5::Enumsb\x06proto3'
  ,
  dependencies=[google_dot_api_dot_annotations__pb2.DESCRIPTOR,])



_SLOTENUM_SLOT = _descriptor.EnumDescriptor(
  name='Slot',
  full_name='google.ads.googleads.v5.enums.SlotEnum.Slot',
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
      name='SEARCH_SIDE', index=2, number=2,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='SEARCH_TOP', index=3, number=3,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='SEARCH_OTHER', index=4, number=4,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='CONTENT', index=5, number=5,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='SEARCH_PARTNER_TOP', index=6, number=6,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='SEARCH_PARTNER_OTHER', index=7, number=7,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='MIXED', index=8, number=8,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=125,
  serialized_end=286,
)
_sym_db.RegisterEnumDescriptor(_SLOTENUM_SLOT)


_SLOTENUM = _descriptor.Descriptor(
  name='SlotEnum',
  full_name='google.ads.googleads.v5.enums.SlotEnum',
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
    _SLOTENUM_SLOT,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=112,
  serialized_end=286,
)

_SLOTENUM_SLOT.containing_type = _SLOTENUM
DESCRIPTOR.message_types_by_name['SlotEnum'] = _SLOTENUM
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

SlotEnum = _reflection.GeneratedProtocolMessageType('SlotEnum', (_message.Message,), {
  'DESCRIPTOR' : _SLOTENUM,
  '__module__' : 'google.ads.googleads_v5.proto.enums.slot_pb2'
  ,
  '__doc__': """Container for enumeration of possible positions of the Ad.""",
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v5.enums.SlotEnum)
  })
_sym_db.RegisterMessage(SlotEnum)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
