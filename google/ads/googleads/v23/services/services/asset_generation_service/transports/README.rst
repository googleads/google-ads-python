
transport inheritance structure
_______________________________

`AssetGenerationServiceTransport` is the ABC for all transports.
- public child `AssetGenerationServiceGrpcTransport` for sync gRPC transport (defined in `grpc.py`).
- public child `AssetGenerationServiceGrpcAsyncIOTransport` for async gRPC transport (defined in `grpc_asyncio.py`).
- private child `_BaseAssetGenerationServiceRestTransport` for base REST transport with inner classes `_BaseMETHOD` (defined in `rest_base.py`).
- public child `AssetGenerationServiceRestTransport` for sync REST transport with inner classes `METHOD` derived from the parent's corresponding `_BaseMETHOD` classes (defined in `rest.py`).
