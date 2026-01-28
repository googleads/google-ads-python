
transport inheritance structure
_______________________________

`UserDataServiceTransport` is the ABC for all transports.
- public child `UserDataServiceGrpcTransport` for sync gRPC transport (defined in `grpc.py`).
- public child `UserDataServiceGrpcAsyncIOTransport` for async gRPC transport (defined in `grpc_asyncio.py`).
- private child `_BaseUserDataServiceRestTransport` for base REST transport with inner classes `_BaseMETHOD` (defined in `rest_base.py`).
- public child `UserDataServiceRestTransport` for sync REST transport with inner classes `METHOD` derived from the parent's corresponding `_BaseMETHOD` classes (defined in `rest.py`).
