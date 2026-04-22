
transport inheritance structure
_______________________________

`UserListCustomerTypeServiceTransport` is the ABC for all transports.
- public child `UserListCustomerTypeServiceGrpcTransport` for sync gRPC transport (defined in `grpc.py`).
- public child `UserListCustomerTypeServiceGrpcAsyncIOTransport` for async gRPC transport (defined in `grpc_asyncio.py`).
- private child `_BaseUserListCustomerTypeServiceRestTransport` for base REST transport with inner classes `_BaseMETHOD` (defined in `rest_base.py`).
- public child `UserListCustomerTypeServiceRestTransport` for sync REST transport with inner classes `METHOD` derived from the parent's corresponding `_BaseMETHOD` classes (defined in `rest.py`).
