
transport inheritance structure
_______________________________

`OfflineUserDataJobServiceTransport` is the ABC for all transports.
- public child `OfflineUserDataJobServiceGrpcTransport` for sync gRPC transport (defined in `grpc.py`).
- public child `OfflineUserDataJobServiceGrpcAsyncIOTransport` for async gRPC transport (defined in `grpc_asyncio.py`).
- private child `_BaseOfflineUserDataJobServiceRestTransport` for base REST transport with inner classes `_BaseMETHOD` (defined in `rest_base.py`).
- public child `OfflineUserDataJobServiceRestTransport` for sync REST transport with inner classes `METHOD` derived from the parent's corresponding `_BaseMETHOD` classes (defined in `rest.py`).
