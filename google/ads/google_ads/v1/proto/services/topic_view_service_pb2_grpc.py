# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

from google.ads.google_ads.v1.proto.resources import topic_view_pb2 as google_dot_ads_dot_googleads__v1_dot_proto_dot_resources_dot_topic__view__pb2
from google.ads.google_ads.v1.proto.services import topic_view_service_pb2 as google_dot_ads_dot_googleads__v1_dot_proto_dot_services_dot_topic__view__service__pb2


class TopicViewServiceStub(object):
  """Proto file describing the Topic View service.

  Service to manage topic views.
  """

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.GetTopicView = channel.unary_unary(
        '/google.ads.googleads.v1.services.TopicViewService/GetTopicView',
        request_serializer=google_dot_ads_dot_googleads__v1_dot_proto_dot_services_dot_topic__view__service__pb2.GetTopicViewRequest.SerializeToString,
        response_deserializer=google_dot_ads_dot_googleads__v1_dot_proto_dot_resources_dot_topic__view__pb2.TopicView.FromString,
        )


class TopicViewServiceServicer(object):
  """Proto file describing the Topic View service.

  Service to manage topic views.
  """

  def GetTopicView(self, request, context):
    """Returns the requested topic view in full detail.
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_TopicViewServiceServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'GetTopicView': grpc.unary_unary_rpc_method_handler(
          servicer.GetTopicView,
          request_deserializer=google_dot_ads_dot_googleads__v1_dot_proto_dot_services_dot_topic__view__service__pb2.GetTopicViewRequest.FromString,
          response_serializer=google_dot_ads_dot_googleads__v1_dot_proto_dot_resources_dot_topic__view__pb2.TopicView.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'google.ads.googleads.v1.services.TopicViewService', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
