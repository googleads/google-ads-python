# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from google.ads.google_ads.v5.proto.resources import ad_parameter_pb2 as google_dot_ads_dot_googleads__v5_dot_proto_dot_resources_dot_ad__parameter__pb2
from google.ads.google_ads.v5.proto.services import ad_parameter_service_pb2 as google_dot_ads_dot_googleads__v5_dot_proto_dot_services_dot_ad__parameter__service__pb2


class AdParameterServiceStub(object):
    """Proto file describing the Ad Parameter service.

    Service to manage ad parameters.
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetAdParameter = channel.unary_unary(
                '/google.ads.googleads.v5.services.AdParameterService/GetAdParameter',
                request_serializer=google_dot_ads_dot_googleads__v5_dot_proto_dot_services_dot_ad__parameter__service__pb2.GetAdParameterRequest.SerializeToString,
                response_deserializer=google_dot_ads_dot_googleads__v5_dot_proto_dot_resources_dot_ad__parameter__pb2.AdParameter.FromString,
                )
        self.MutateAdParameters = channel.unary_unary(
                '/google.ads.googleads.v5.services.AdParameterService/MutateAdParameters',
                request_serializer=google_dot_ads_dot_googleads__v5_dot_proto_dot_services_dot_ad__parameter__service__pb2.MutateAdParametersRequest.SerializeToString,
                response_deserializer=google_dot_ads_dot_googleads__v5_dot_proto_dot_services_dot_ad__parameter__service__pb2.MutateAdParametersResponse.FromString,
                )


class AdParameterServiceServicer(object):
    """Proto file describing the Ad Parameter service.

    Service to manage ad parameters.
    """

    def GetAdParameter(self, request, context):
        """Returns the requested ad parameter in full detail.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def MutateAdParameters(self, request, context):
        """Creates, updates, or removes ad parameters. Operation statuses are
        returned.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_AdParameterServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'GetAdParameter': grpc.unary_unary_rpc_method_handler(
                    servicer.GetAdParameter,
                    request_deserializer=google_dot_ads_dot_googleads__v5_dot_proto_dot_services_dot_ad__parameter__service__pb2.GetAdParameterRequest.FromString,
                    response_serializer=google_dot_ads_dot_googleads__v5_dot_proto_dot_resources_dot_ad__parameter__pb2.AdParameter.SerializeToString,
            ),
            'MutateAdParameters': grpc.unary_unary_rpc_method_handler(
                    servicer.MutateAdParameters,
                    request_deserializer=google_dot_ads_dot_googleads__v5_dot_proto_dot_services_dot_ad__parameter__service__pb2.MutateAdParametersRequest.FromString,
                    response_serializer=google_dot_ads_dot_googleads__v5_dot_proto_dot_services_dot_ad__parameter__service__pb2.MutateAdParametersResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'google.ads.googleads.v5.services.AdParameterService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class AdParameterService(object):
    """Proto file describing the Ad Parameter service.

    Service to manage ad parameters.
    """

    @staticmethod
    def GetAdParameter(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/google.ads.googleads.v5.services.AdParameterService/GetAdParameter',
            google_dot_ads_dot_googleads__v5_dot_proto_dot_services_dot_ad__parameter__service__pb2.GetAdParameterRequest.SerializeToString,
            google_dot_ads_dot_googleads__v5_dot_proto_dot_resources_dot_ad__parameter__pb2.AdParameter.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def MutateAdParameters(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/google.ads.googleads.v5.services.AdParameterService/MutateAdParameters',
            google_dot_ads_dot_googleads__v5_dot_proto_dot_services_dot_ad__parameter__service__pb2.MutateAdParametersRequest.SerializeToString,
            google_dot_ads_dot_googleads__v5_dot_proto_dot_services_dot_ad__parameter__service__pb2.MutateAdParametersResponse.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)
