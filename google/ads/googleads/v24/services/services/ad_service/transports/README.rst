
transport inheritance structure
_______________________________

`AdServiceTransport` is the ABC for all transports.
- public child `AdServiceGrpcTransport` for sync gRPC transport (defined in `grpc.py`).
- public child `AdServiceGrpcAsyncIOTransport` for async gRPC transport (defined in `grpc_asyncio.py`).
- private child `_BaseAdServiceRestTransport` for base REST transport with inner classes `_BaseMETHOD` (defined in `rest_base.py`).
- public child `AdServiceRestTransport` for sync REST transport with inner classes `METHOD` derived from the parent's corresponding `_BaseMETHOD` classes (defined in `rest.py`).
