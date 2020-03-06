# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

from google.ads.google_ads.v3.proto.resources import user_list_pb2 as google_dot_ads_dot_googleads__v3_dot_proto_dot_resources_dot_user__list__pb2
from google.ads.google_ads.v3.proto.services import user_list_service_pb2 as google_dot_ads_dot_googleads__v3_dot_proto_dot_services_dot_user__list__service__pb2


class UserListServiceStub(object):
  """Proto file describing the User List service.

  Service to manage user lists.
  """

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.GetUserList = channel.unary_unary(
        '/google.ads.googleads.v3.services.UserListService/GetUserList',
        request_serializer=google_dot_ads_dot_googleads__v3_dot_proto_dot_services_dot_user__list__service__pb2.GetUserListRequest.SerializeToString,
        response_deserializer=google_dot_ads_dot_googleads__v3_dot_proto_dot_resources_dot_user__list__pb2.UserList.FromString,
        )
    self.MutateUserLists = channel.unary_unary(
        '/google.ads.googleads.v3.services.UserListService/MutateUserLists',
        request_serializer=google_dot_ads_dot_googleads__v3_dot_proto_dot_services_dot_user__list__service__pb2.MutateUserListsRequest.SerializeToString,
        response_deserializer=google_dot_ads_dot_googleads__v3_dot_proto_dot_services_dot_user__list__service__pb2.MutateUserListsResponse.FromString,
        )


class UserListServiceServicer(object):
  """Proto file describing the User List service.

  Service to manage user lists.
  """

  def GetUserList(self, request, context):
    """Returns the requested user list.
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def MutateUserLists(self, request, context):
    """Creates or updates user lists. Operation statuses are returned.
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_UserListServiceServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'GetUserList': grpc.unary_unary_rpc_method_handler(
          servicer.GetUserList,
          request_deserializer=google_dot_ads_dot_googleads__v3_dot_proto_dot_services_dot_user__list__service__pb2.GetUserListRequest.FromString,
          response_serializer=google_dot_ads_dot_googleads__v3_dot_proto_dot_resources_dot_user__list__pb2.UserList.SerializeToString,
      ),
      'MutateUserLists': grpc.unary_unary_rpc_method_handler(
          servicer.MutateUserLists,
          request_deserializer=google_dot_ads_dot_googleads__v3_dot_proto_dot_services_dot_user__list__service__pb2.MutateUserListsRequest.FromString,
          response_serializer=google_dot_ads_dot_googleads__v3_dot_proto_dot_services_dot_user__list__service__pb2.MutateUserListsResponse.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'google.ads.googleads.v3.services.UserListService', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
