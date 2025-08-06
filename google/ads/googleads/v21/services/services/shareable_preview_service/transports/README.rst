
transport inheritance structure
_______________________________

`ShareablePreviewServiceTransport` is the ABC for all transports.
- public child `ShareablePreviewServiceGrpcTransport` for sync gRPC transport (defined in `grpc.py`).
- public child `ShareablePreviewServiceGrpcAsyncIOTransport` for async gRPC transport (defined in `grpc_asyncio.py`).
- private child `_BaseShareablePreviewServiceRestTransport` for base REST transport with inner classes `_BaseMETHOD` (defined in `rest_base.py`).
- public child `ShareablePreviewServiceRestTransport` for sync REST transport with inner classes `METHOD` derived from the parent's corresponding `_BaseMETHOD` classes (defined in `rest.py`).
