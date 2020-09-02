# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from google.ads.google_ads.v5.proto.resources import product_bidding_category_constant_pb2 as google_dot_ads_dot_googleads__v5_dot_proto_dot_resources_dot_product__bidding__category__constant__pb2
from google.ads.google_ads.v5.proto.services import product_bidding_category_constant_service_pb2 as google_dot_ads_dot_googleads__v5_dot_proto_dot_services_dot_product__bidding__category__constant__service__pb2


class ProductBiddingCategoryConstantServiceStub(object):
    """Proto file describing the Product Bidding Category constant service

    Service to fetch Product Bidding Categories.
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetProductBiddingCategoryConstant = channel.unary_unary(
                '/google.ads.googleads.v5.services.ProductBiddingCategoryConstantService/GetProductBiddingCategoryConstant',
                request_serializer=google_dot_ads_dot_googleads__v5_dot_proto_dot_services_dot_product__bidding__category__constant__service__pb2.GetProductBiddingCategoryConstantRequest.SerializeToString,
                response_deserializer=google_dot_ads_dot_googleads__v5_dot_proto_dot_resources_dot_product__bidding__category__constant__pb2.ProductBiddingCategoryConstant.FromString,
                )


class ProductBiddingCategoryConstantServiceServicer(object):
    """Proto file describing the Product Bidding Category constant service

    Service to fetch Product Bidding Categories.
    """

    def GetProductBiddingCategoryConstant(self, request, context):
        """Returns the requested Product Bidding Category in full detail.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ProductBiddingCategoryConstantServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'GetProductBiddingCategoryConstant': grpc.unary_unary_rpc_method_handler(
                    servicer.GetProductBiddingCategoryConstant,
                    request_deserializer=google_dot_ads_dot_googleads__v5_dot_proto_dot_services_dot_product__bidding__category__constant__service__pb2.GetProductBiddingCategoryConstantRequest.FromString,
                    response_serializer=google_dot_ads_dot_googleads__v5_dot_proto_dot_resources_dot_product__bidding__category__constant__pb2.ProductBiddingCategoryConstant.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'google.ads.googleads.v5.services.ProductBiddingCategoryConstantService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class ProductBiddingCategoryConstantService(object):
    """Proto file describing the Product Bidding Category constant service

    Service to fetch Product Bidding Categories.
    """

    @staticmethod
    def GetProductBiddingCategoryConstant(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/google.ads.googleads.v5.services.ProductBiddingCategoryConstantService/GetProductBiddingCategoryConstant',
            google_dot_ads_dot_googleads__v5_dot_proto_dot_services_dot_product__bidding__category__constant__service__pb2.GetProductBiddingCategoryConstantRequest.SerializeToString,
            google_dot_ads_dot_googleads__v5_dot_proto_dot_resources_dot_product__bidding__category__constant__pb2.ProductBiddingCategoryConstant.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)
