# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: google/ads/googleads_v1/proto/services/conversion_upload_service.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2
from google.protobuf import wrappers_pb2 as google_dot_protobuf_dot_wrappers__pb2
from google.rpc import status_pb2 as google_dot_rpc_dot_status__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='google/ads/googleads_v1/proto/services/conversion_upload_service.proto',
  package='google.ads.googleads.v1.services',
  syntax='proto3',
  serialized_options=_b('\n$com.google.ads.googleads.v1.servicesB\034ConversionUploadServiceProtoP\001ZHgoogle.golang.org/genproto/googleapis/ads/googleads/v1/services;services\242\002\003GAA\252\002 Google.Ads.GoogleAds.V1.Services\312\002 Google\\Ads\\GoogleAds\\V1\\Services\352\002$Google::Ads::GoogleAds::V1::Services'),
  serialized_pb=_b('\nFgoogle/ads/googleads_v1/proto/services/conversion_upload_service.proto\x12 google.ads.googleads.v1.services\x1a\x1cgoogle/api/annotations.proto\x1a\x1egoogle/protobuf/wrappers.proto\x1a\x17google/rpc/status.proto\"\x95\x01\n\x1dUploadClickConversionsRequest\x12\x13\n\x0b\x63ustomer_id\x18\x01 \x01(\t\x12\x46\n\x0b\x63onversions\x18\x02 \x03(\x0b\x32\x31.google.ads.googleads.v1.services.ClickConversion\x12\x17\n\x0fpartial_failure\x18\x03 \x01(\x08\"\x9d\x01\n\x1eUploadClickConversionsResponse\x12\x31\n\x15partial_failure_error\x18\x01 \x01(\x0b\x32\x12.google.rpc.Status\x12H\n\x07results\x18\x02 \x03(\x0b\x32\x37.google.ads.googleads.v1.services.ClickConversionResult\"\xae\x03\n\x0f\x43lickConversion\x12+\n\x05gclid\x18\x01 \x01(\x0b\x32\x1c.google.protobuf.StringValue\x12\x37\n\x11\x63onversion_action\x18\x02 \x01(\x0b\x32\x1c.google.protobuf.StringValue\x12:\n\x14\x63onversion_date_time\x18\x03 \x01(\x0b\x32\x1c.google.protobuf.StringValue\x12\x36\n\x10\x63onversion_value\x18\x04 \x01(\x0b\x32\x1c.google.protobuf.DoubleValue\x12\x33\n\rcurrency_code\x18\x05 \x01(\x0b\x32\x1c.google.protobuf.StringValue\x12.\n\x08order_id\x18\x06 \x01(\x0b\x32\x1c.google.protobuf.StringValue\x12\\\n\x19\x65xternal_attribution_data\x18\x07 \x01(\x0b\x32\x39.google.ads.googleads.v1.services.ExternalAttributionData\"\x9e\x01\n\x17\x45xternalAttributionData\x12\x41\n\x1b\x65xternal_attribution_credit\x18\x01 \x01(\x0b\x32\x1c.google.protobuf.DoubleValue\x12@\n\x1a\x65xternal_attribution_model\x18\x02 \x01(\x0b\x32\x1c.google.protobuf.StringValue\"\xb9\x01\n\x15\x43lickConversionResult\x12+\n\x05gclid\x18\x01 \x01(\x0b\x32\x1c.google.protobuf.StringValue\x12\x37\n\x11\x63onversion_action\x18\x02 \x01(\x0b\x32\x1c.google.protobuf.StringValue\x12:\n\x14\x63onversion_date_time\x18\x03 \x01(\x0b\x32\x1c.google.protobuf.StringValue2\xf8\x01\n\x17\x43onversionUploadService\x12\xdc\x01\n\x16UploadClickConversions\x12?.google.ads.googleads.v1.services.UploadClickConversionsRequest\x1a@.google.ads.googleads.v1.services.UploadClickConversionsResponse\"?\x82\xd3\xe4\x93\x02\x39\"4/v1/customers/{customer_id=*}:uploadClickConversions:\x01*B\x83\x02\n$com.google.ads.googleads.v1.servicesB\x1c\x43onversionUploadServiceProtoP\x01ZHgoogle.golang.org/genproto/googleapis/ads/googleads/v1/services;services\xa2\x02\x03GAA\xaa\x02 Google.Ads.GoogleAds.V1.Services\xca\x02 Google\\Ads\\GoogleAds\\V1\\Services\xea\x02$Google::Ads::GoogleAds::V1::Servicesb\x06proto3')
  ,
  dependencies=[google_dot_api_dot_annotations__pb2.DESCRIPTOR,google_dot_protobuf_dot_wrappers__pb2.DESCRIPTOR,google_dot_rpc_dot_status__pb2.DESCRIPTOR,])




_UPLOADCLICKCONVERSIONSREQUEST = _descriptor.Descriptor(
  name='UploadClickConversionsRequest',
  full_name='google.ads.googleads.v1.services.UploadClickConversionsRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='customer_id', full_name='google.ads.googleads.v1.services.UploadClickConversionsRequest.customer_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='conversions', full_name='google.ads.googleads.v1.services.UploadClickConversionsRequest.conversions', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='partial_failure', full_name='google.ads.googleads.v1.services.UploadClickConversionsRequest.partial_failure', index=2,
      number=3, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
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
  ],
  serialized_start=196,
  serialized_end=345,
)


_UPLOADCLICKCONVERSIONSRESPONSE = _descriptor.Descriptor(
  name='UploadClickConversionsResponse',
  full_name='google.ads.googleads.v1.services.UploadClickConversionsResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='partial_failure_error', full_name='google.ads.googleads.v1.services.UploadClickConversionsResponse.partial_failure_error', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='results', full_name='google.ads.googleads.v1.services.UploadClickConversionsResponse.results', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
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
  ],
  serialized_start=348,
  serialized_end=505,
)


_CLICKCONVERSION = _descriptor.Descriptor(
  name='ClickConversion',
  full_name='google.ads.googleads.v1.services.ClickConversion',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='gclid', full_name='google.ads.googleads.v1.services.ClickConversion.gclid', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='conversion_action', full_name='google.ads.googleads.v1.services.ClickConversion.conversion_action', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='conversion_date_time', full_name='google.ads.googleads.v1.services.ClickConversion.conversion_date_time', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='conversion_value', full_name='google.ads.googleads.v1.services.ClickConversion.conversion_value', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='currency_code', full_name='google.ads.googleads.v1.services.ClickConversion.currency_code', index=4,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='order_id', full_name='google.ads.googleads.v1.services.ClickConversion.order_id', index=5,
      number=6, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='external_attribution_data', full_name='google.ads.googleads.v1.services.ClickConversion.external_attribution_data', index=6,
      number=7, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
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
  ],
  serialized_start=508,
  serialized_end=938,
)


_EXTERNALATTRIBUTIONDATA = _descriptor.Descriptor(
  name='ExternalAttributionData',
  full_name='google.ads.googleads.v1.services.ExternalAttributionData',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='external_attribution_credit', full_name='google.ads.googleads.v1.services.ExternalAttributionData.external_attribution_credit', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='external_attribution_model', full_name='google.ads.googleads.v1.services.ExternalAttributionData.external_attribution_model', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
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
  ],
  serialized_start=941,
  serialized_end=1099,
)


_CLICKCONVERSIONRESULT = _descriptor.Descriptor(
  name='ClickConversionResult',
  full_name='google.ads.googleads.v1.services.ClickConversionResult',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='gclid', full_name='google.ads.googleads.v1.services.ClickConversionResult.gclid', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='conversion_action', full_name='google.ads.googleads.v1.services.ClickConversionResult.conversion_action', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='conversion_date_time', full_name='google.ads.googleads.v1.services.ClickConversionResult.conversion_date_time', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
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
  ],
  serialized_start=1102,
  serialized_end=1287,
)

_UPLOADCLICKCONVERSIONSREQUEST.fields_by_name['conversions'].message_type = _CLICKCONVERSION
_UPLOADCLICKCONVERSIONSRESPONSE.fields_by_name['partial_failure_error'].message_type = google_dot_rpc_dot_status__pb2._STATUS
_UPLOADCLICKCONVERSIONSRESPONSE.fields_by_name['results'].message_type = _CLICKCONVERSIONRESULT
_CLICKCONVERSION.fields_by_name['gclid'].message_type = google_dot_protobuf_dot_wrappers__pb2._STRINGVALUE
_CLICKCONVERSION.fields_by_name['conversion_action'].message_type = google_dot_protobuf_dot_wrappers__pb2._STRINGVALUE
_CLICKCONVERSION.fields_by_name['conversion_date_time'].message_type = google_dot_protobuf_dot_wrappers__pb2._STRINGVALUE
_CLICKCONVERSION.fields_by_name['conversion_value'].message_type = google_dot_protobuf_dot_wrappers__pb2._DOUBLEVALUE
_CLICKCONVERSION.fields_by_name['currency_code'].message_type = google_dot_protobuf_dot_wrappers__pb2._STRINGVALUE
_CLICKCONVERSION.fields_by_name['order_id'].message_type = google_dot_protobuf_dot_wrappers__pb2._STRINGVALUE
_CLICKCONVERSION.fields_by_name['external_attribution_data'].message_type = _EXTERNALATTRIBUTIONDATA
_EXTERNALATTRIBUTIONDATA.fields_by_name['external_attribution_credit'].message_type = google_dot_protobuf_dot_wrappers__pb2._DOUBLEVALUE
_EXTERNALATTRIBUTIONDATA.fields_by_name['external_attribution_model'].message_type = google_dot_protobuf_dot_wrappers__pb2._STRINGVALUE
_CLICKCONVERSIONRESULT.fields_by_name['gclid'].message_type = google_dot_protobuf_dot_wrappers__pb2._STRINGVALUE
_CLICKCONVERSIONRESULT.fields_by_name['conversion_action'].message_type = google_dot_protobuf_dot_wrappers__pb2._STRINGVALUE
_CLICKCONVERSIONRESULT.fields_by_name['conversion_date_time'].message_type = google_dot_protobuf_dot_wrappers__pb2._STRINGVALUE
DESCRIPTOR.message_types_by_name['UploadClickConversionsRequest'] = _UPLOADCLICKCONVERSIONSREQUEST
DESCRIPTOR.message_types_by_name['UploadClickConversionsResponse'] = _UPLOADCLICKCONVERSIONSRESPONSE
DESCRIPTOR.message_types_by_name['ClickConversion'] = _CLICKCONVERSION
DESCRIPTOR.message_types_by_name['ExternalAttributionData'] = _EXTERNALATTRIBUTIONDATA
DESCRIPTOR.message_types_by_name['ClickConversionResult'] = _CLICKCONVERSIONRESULT
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

UploadClickConversionsRequest = _reflection.GeneratedProtocolMessageType('UploadClickConversionsRequest', (_message.Message,), dict(
  DESCRIPTOR = _UPLOADCLICKCONVERSIONSREQUEST,
  __module__ = 'google.ads.googleads_v1.proto.services.conversion_upload_service_pb2'
  ,
  __doc__ = """Request message for
  [ConversionUploadService.UploadClickConversions][google.ads.googleads.v1.services.ConversionUploadService.UploadClickConversions].
  
  
  Attributes:
      customer_id:
          The ID of the customer performing the upload.
      conversions:
          The conversions that are being uploaded.
      partial_failure:
          If true, successful operations will be carried out and invalid
          operations will return errors. If false, all operations will
          be carried out in one transaction if and only if they are all
          valid. This should always be set to true.
  """,
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v1.services.UploadClickConversionsRequest)
  ))
_sym_db.RegisterMessage(UploadClickConversionsRequest)

UploadClickConversionsResponse = _reflection.GeneratedProtocolMessageType('UploadClickConversionsResponse', (_message.Message,), dict(
  DESCRIPTOR = _UPLOADCLICKCONVERSIONSRESPONSE,
  __module__ = 'google.ads.googleads_v1.proto.services.conversion_upload_service_pb2'
  ,
  __doc__ = """Response message for
  [ConversionUploadService.UploadClickConversions][google.ads.googleads.v1.services.ConversionUploadService.UploadClickConversions].
  
  
  Attributes:
      partial_failure_error:
          Errors that pertain to conversion failures in the partial
          failure mode. Returned when all errors occur inside the
          conversions. If any errors occur outside the conversions (e.g.
          auth errors), we return an RPC level error.
      results:
          Returned for successfully processed conversions. Proto will be
          empty for rows that received an error.
  """,
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v1.services.UploadClickConversionsResponse)
  ))
_sym_db.RegisterMessage(UploadClickConversionsResponse)

ClickConversion = _reflection.GeneratedProtocolMessageType('ClickConversion', (_message.Message,), dict(
  DESCRIPTOR = _CLICKCONVERSION,
  __module__ = 'google.ads.googleads_v1.proto.services.conversion_upload_service_pb2'
  ,
  __doc__ = """A click conversion.
  
  
  Attributes:
      gclid:
          The Google click ID (gclid) associated with this conversion.
      conversion_action:
          Resource name of the conversion action associated with this
          conversion. Note: Although this resource name consists of a
          customer id and a conversion action id, validation will ignore
          the customer id and use the conversion action id as the sole
          identifier of the conversion action.
      conversion_date_time:
          The date time at which the conversion occurred. Must be after
          the click time. The timezone must be specified. The format is
          "yyyy-mm-dd hh:mm:ss+\|-hh:mm", e.g. “2019-01-01
          12:32:45-08:00”.
      conversion_value:
          The value of the conversion for the advertiser.
      currency_code:
          Currency associated with the conversion value. This is the ISO
          4217 3-character currency code. For example: USD, EUR.
      order_id:
          The order ID associated with the conversion. An order id can
          only be used for one conversion per conversion action.
      external_attribution_data:
          Additional data about externally attributed conversions. This
          field is required for conversions with an externally
          attributed conversion action, but should not be set otherwise.
  """,
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v1.services.ClickConversion)
  ))
_sym_db.RegisterMessage(ClickConversion)

ExternalAttributionData = _reflection.GeneratedProtocolMessageType('ExternalAttributionData', (_message.Message,), dict(
  DESCRIPTOR = _EXTERNALATTRIBUTIONDATA,
  __module__ = 'google.ads.googleads_v1.proto.services.conversion_upload_service_pb2'
  ,
  __doc__ = """Contains additional information about externally attributed conversions.
  
  
  Attributes:
      external_attribution_credit:
          Represents the fraction of the conversion that is attributed
          to the Google Ads click.
      external_attribution_model:
          Specifies the attribution model name.
  """,
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v1.services.ExternalAttributionData)
  ))
_sym_db.RegisterMessage(ExternalAttributionData)

ClickConversionResult = _reflection.GeneratedProtocolMessageType('ClickConversionResult', (_message.Message,), dict(
  DESCRIPTOR = _CLICKCONVERSIONRESULT,
  __module__ = 'google.ads.googleads_v1.proto.services.conversion_upload_service_pb2'
  ,
  __doc__ = """Identifying information for a successfully processed ClickConversion.
  
  
  Attributes:
      gclid:
          The Google Click ID (gclid) associated with this conversion.
      conversion_action:
          Resource name of the conversion action associated with this
          conversion.
      conversion_date_time:
          The date time at which the conversion occurred. The format is
          "yyyy-mm-dd hh:mm:ss+\|-hh:mm", e.g. “2019-01-01
          12:32:45-08:00”.
  """,
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v1.services.ClickConversionResult)
  ))
_sym_db.RegisterMessage(ClickConversionResult)


DESCRIPTOR._options = None

_CONVERSIONUPLOADSERVICE = _descriptor.ServiceDescriptor(
  name='ConversionUploadService',
  full_name='google.ads.googleads.v1.services.ConversionUploadService',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  serialized_start=1290,
  serialized_end=1538,
  methods=[
  _descriptor.MethodDescriptor(
    name='UploadClickConversions',
    full_name='google.ads.googleads.v1.services.ConversionUploadService.UploadClickConversions',
    index=0,
    containing_service=None,
    input_type=_UPLOADCLICKCONVERSIONSREQUEST,
    output_type=_UPLOADCLICKCONVERSIONSRESPONSE,
    serialized_options=_b('\202\323\344\223\0029\"4/v1/customers/{customer_id=*}:uploadClickConversions:\001*'),
  ),
])
_sym_db.RegisterServiceDescriptor(_CONVERSIONUPLOADSERVICE)

DESCRIPTOR.services_by_name['ConversionUploadService'] = _CONVERSIONUPLOADSERVICE

# @@protoc_insertion_point(module_scope)