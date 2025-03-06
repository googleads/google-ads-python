
transport inheritance structure
_______________________________

`AdParameterServiceTransport` is the ABC for all transports.
- public child `AdParameterServiceGrpcTransport` for sync gRPC transport (defined in `grpc.py`).
- public child `AdParameterServiceGrpcAsyncIOTransport` for async gRPC transport (defined in `grpc_asyncio.py`).
- private child `_BaseAdParameterServiceRestTransport` for base REST transport with inner classes `_BaseMETHOD` (defined in `rest_base.py`).
- public child `AdParameterServiceRestTransport` for sync REST transport with inner classes `METHOD` derived from the parent's corresponding `_BaseMETHOD` classes (defined in `rest.py`).
