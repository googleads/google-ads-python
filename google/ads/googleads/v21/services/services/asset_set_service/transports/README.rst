
transport inheritance structure
_______________________________

`AssetSetServiceTransport` is the ABC for all transports.
- public child `AssetSetServiceGrpcTransport` for sync gRPC transport (defined in `grpc.py`).
- public child `AssetSetServiceGrpcAsyncIOTransport` for async gRPC transport (defined in `grpc_asyncio.py`).
- private child `_BaseAssetSetServiceRestTransport` for base REST transport with inner classes `_BaseMETHOD` (defined in `rest_base.py`).
- public child `AssetSetServiceRestTransport` for sync REST transport with inner classes `METHOD` derived from the parent's corresponding `_BaseMETHOD` classes (defined in `rest.py`).
