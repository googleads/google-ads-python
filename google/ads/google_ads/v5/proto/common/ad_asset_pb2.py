# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: google/ads/googleads_v5/proto/common/ad_asset.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.ads.google_ads.v5.proto.enums import served_asset_field_type_pb2 as google_dot_ads_dot_googleads__v5_dot_proto_dot_enums_dot_served__asset__field__type__pb2
from google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='google/ads/googleads_v5/proto/common/ad_asset.proto',
  package='google.ads.googleads.v5.common',
  syntax='proto3',
  serialized_options=b'\n\"com.google.ads.googleads.v5.commonB\014AdAssetProtoP\001ZDgoogle.golang.org/genproto/googleapis/ads/googleads/v5/common;common\242\002\003GAA\252\002\036Google.Ads.GoogleAds.V5.Common\312\002\036Google\\Ads\\GoogleAds\\V5\\Common\352\002\"Google::Ads::GoogleAds::V5::Common',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n3google/ads/googleads_v5/proto/common/ad_asset.proto\x12\x1egoogle.ads.googleads.v5.common\x1a\x41google/ads/googleads_v5/proto/enums/served_asset_field_type.proto\x1a\x1cgoogle/api/annotations.proto\"\x8d\x01\n\x0b\x41\x64TextAsset\x12\x11\n\x04text\x18\x04 \x01(\tH\x00\x88\x01\x01\x12\x62\n\x0cpinned_field\x18\x02 \x01(\x0e\x32L.google.ads.googleads.v5.enums.ServedAssetFieldTypeEnum.ServedAssetFieldTypeB\x07\n\x05_text\",\n\x0c\x41\x64ImageAsset\x12\x12\n\x05\x61sset\x18\x02 \x01(\tH\x00\x88\x01\x01\x42\x08\n\x06_asset\",\n\x0c\x41\x64VideoAsset\x12\x12\n\x05\x61sset\x18\x02 \x01(\tH\x00\x88\x01\x01\x42\x08\n\x06_asset\"2\n\x12\x41\x64MediaBundleAsset\x12\x12\n\x05\x61sset\x18\x02 \x01(\tH\x00\x88\x01\x01\x42\x08\n\x06_assetB\xe7\x01\n\"com.google.ads.googleads.v5.commonB\x0c\x41\x64\x41ssetProtoP\x01ZDgoogle.golang.org/genproto/googleapis/ads/googleads/v5/common;common\xa2\x02\x03GAA\xaa\x02\x1eGoogle.Ads.GoogleAds.V5.Common\xca\x02\x1eGoogle\\Ads\\GoogleAds\\V5\\Common\xea\x02\"Google::Ads::GoogleAds::V5::Commonb\x06proto3'
  ,
  dependencies=[google_dot_ads_dot_googleads__v5_dot_proto_dot_enums_dot_served__asset__field__type__pb2.DESCRIPTOR,google_dot_api_dot_annotations__pb2.DESCRIPTOR,])




_ADTEXTASSET = _descriptor.Descriptor(
  name='AdTextAsset',
  full_name='google.ads.googleads.v5.common.AdTextAsset',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='text', full_name='google.ads.googleads.v5.common.AdTextAsset.text', index=0,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='pinned_field', full_name='google.ads.googleads.v5.common.AdTextAsset.pinned_field', index=1,
      number=2, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
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
      name='_text', full_name='google.ads.googleads.v5.common.AdTextAsset._text',
      index=0, containing_type=None,
      create_key=_descriptor._internal_create_key,
    fields=[]),
  ],
  serialized_start=185,
  serialized_end=326,
)


_ADIMAGEASSET = _descriptor.Descriptor(
  name='AdImageAsset',
  full_name='google.ads.googleads.v5.common.AdImageAsset',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='asset', full_name='google.ads.googleads.v5.common.AdImageAsset.asset', index=0,
      number=2, type=9, cpp_type=9, label=1,
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
      name='_asset', full_name='google.ads.googleads.v5.common.AdImageAsset._asset',
      index=0, containing_type=None,
      create_key=_descriptor._internal_create_key,
    fields=[]),
  ],
  serialized_start=328,
  serialized_end=372,
)


_ADVIDEOASSET = _descriptor.Descriptor(
  name='AdVideoAsset',
  full_name='google.ads.googleads.v5.common.AdVideoAsset',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='asset', full_name='google.ads.googleads.v5.common.AdVideoAsset.asset', index=0,
      number=2, type=9, cpp_type=9, label=1,
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
      name='_asset', full_name='google.ads.googleads.v5.common.AdVideoAsset._asset',
      index=0, containing_type=None,
      create_key=_descriptor._internal_create_key,
    fields=[]),
  ],
  serialized_start=374,
  serialized_end=418,
)


_ADMEDIABUNDLEASSET = _descriptor.Descriptor(
  name='AdMediaBundleAsset',
  full_name='google.ads.googleads.v5.common.AdMediaBundleAsset',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='asset', full_name='google.ads.googleads.v5.common.AdMediaBundleAsset.asset', index=0,
      number=2, type=9, cpp_type=9, label=1,
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
      name='_asset', full_name='google.ads.googleads.v5.common.AdMediaBundleAsset._asset',
      index=0, containing_type=None,
      create_key=_descriptor._internal_create_key,
    fields=[]),
  ],
  serialized_start=420,
  serialized_end=470,
)

_ADTEXTASSET.fields_by_name['pinned_field'].enum_type = google_dot_ads_dot_googleads__v5_dot_proto_dot_enums_dot_served__asset__field__type__pb2._SERVEDASSETFIELDTYPEENUM_SERVEDASSETFIELDTYPE
_ADTEXTASSET.oneofs_by_name['_text'].fields.append(
  _ADTEXTASSET.fields_by_name['text'])
_ADTEXTASSET.fields_by_name['text'].containing_oneof = _ADTEXTASSET.oneofs_by_name['_text']
_ADIMAGEASSET.oneofs_by_name['_asset'].fields.append(
  _ADIMAGEASSET.fields_by_name['asset'])
_ADIMAGEASSET.fields_by_name['asset'].containing_oneof = _ADIMAGEASSET.oneofs_by_name['_asset']
_ADVIDEOASSET.oneofs_by_name['_asset'].fields.append(
  _ADVIDEOASSET.fields_by_name['asset'])
_ADVIDEOASSET.fields_by_name['asset'].containing_oneof = _ADVIDEOASSET.oneofs_by_name['_asset']
_ADMEDIABUNDLEASSET.oneofs_by_name['_asset'].fields.append(
  _ADMEDIABUNDLEASSET.fields_by_name['asset'])
_ADMEDIABUNDLEASSET.fields_by_name['asset'].containing_oneof = _ADMEDIABUNDLEASSET.oneofs_by_name['_asset']
DESCRIPTOR.message_types_by_name['AdTextAsset'] = _ADTEXTASSET
DESCRIPTOR.message_types_by_name['AdImageAsset'] = _ADIMAGEASSET
DESCRIPTOR.message_types_by_name['AdVideoAsset'] = _ADVIDEOASSET
DESCRIPTOR.message_types_by_name['AdMediaBundleAsset'] = _ADMEDIABUNDLEASSET
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

AdTextAsset = _reflection.GeneratedProtocolMessageType('AdTextAsset', (_message.Message,), {
  'DESCRIPTOR' : _ADTEXTASSET,
  '__module__' : 'google.ads.googleads_v5.proto.common.ad_asset_pb2'
  ,
  '__doc__': """A text asset used inside an ad.
  
  Attributes:
      text:
          Asset text.
      pinned_field:
          The pinned field of the asset. This restricts the asset to
          only serve within this field. Multiple assets can be pinned to
          the same field. An asset that is unpinned or pinned to a
          different field will not serve in a field where some other
          asset has been pinned.
  """,
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v5.common.AdTextAsset)
  })
_sym_db.RegisterMessage(AdTextAsset)

AdImageAsset = _reflection.GeneratedProtocolMessageType('AdImageAsset', (_message.Message,), {
  'DESCRIPTOR' : _ADIMAGEASSET,
  '__module__' : 'google.ads.googleads_v5.proto.common.ad_asset_pb2'
  ,
  '__doc__': """An image asset used inside an ad.
  
  Attributes:
      asset:
          The Asset resource name of this image.
  """,
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v5.common.AdImageAsset)
  })
_sym_db.RegisterMessage(AdImageAsset)

AdVideoAsset = _reflection.GeneratedProtocolMessageType('AdVideoAsset', (_message.Message,), {
  'DESCRIPTOR' : _ADVIDEOASSET,
  '__module__' : 'google.ads.googleads_v5.proto.common.ad_asset_pb2'
  ,
  '__doc__': """A video asset used inside an ad.
  
  Attributes:
      asset:
          The Asset resource name of this video.
  """,
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v5.common.AdVideoAsset)
  })
_sym_db.RegisterMessage(AdVideoAsset)

AdMediaBundleAsset = _reflection.GeneratedProtocolMessageType('AdMediaBundleAsset', (_message.Message,), {
  'DESCRIPTOR' : _ADMEDIABUNDLEASSET,
  '__module__' : 'google.ads.googleads_v5.proto.common.ad_asset_pb2'
  ,
  '__doc__': """A media bundle asset used inside an ad.
  
  Attributes:
      asset:
          The Asset resource name of this media bundle.
  """,
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v5.common.AdMediaBundleAsset)
  })
_sym_db.RegisterMessage(AdMediaBundleAsset)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
