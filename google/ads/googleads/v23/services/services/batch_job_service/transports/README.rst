
transport inheritance structure
_______________________________

`BatchJobServiceTransport` is the ABC for all transports.
- public child `BatchJobServiceGrpcTransport` for sync gRPC transport (defined in `grpc.py`).
- public child `BatchJobServiceGrpcAsyncIOTransport` for async gRPC transport (defined in `grpc_asyncio.py`).
- private child `_BaseBatchJobServiceRestTransport` for base REST transport with inner classes `_BaseMETHOD` (defined in `rest_base.py`).
- public child `BatchJobServiceRestTransport` for sync REST transport with inner classes `METHOD` derived from the parent's corresponding `_BaseMETHOD` classes (defined in `rest.py`).
