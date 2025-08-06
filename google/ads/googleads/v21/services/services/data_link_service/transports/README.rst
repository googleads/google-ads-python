
transport inheritance structure
_______________________________

`DataLinkServiceTransport` is the ABC for all transports.
- public child `DataLinkServiceGrpcTransport` for sync gRPC transport (defined in `grpc.py`).
- public child `DataLinkServiceGrpcAsyncIOTransport` for async gRPC transport (defined in `grpc_asyncio.py`).
- private child `_BaseDataLinkServiceRestTransport` for base REST transport with inner classes `_BaseMETHOD` (defined in `rest_base.py`).
- public child `DataLinkServiceRestTransport` for sync REST transport with inner classes `METHOD` derived from the parent's corresponding `_BaseMETHOD` classes (defined in `rest.py`).
