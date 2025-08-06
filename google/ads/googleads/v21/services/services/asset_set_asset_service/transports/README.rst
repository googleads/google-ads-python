
transport inheritance structure
_______________________________

`AssetSetAssetServiceTransport` is the ABC for all transports.
- public child `AssetSetAssetServiceGrpcTransport` for sync gRPC transport (defined in `grpc.py`).
- public child `AssetSetAssetServiceGrpcAsyncIOTransport` for async gRPC transport (defined in `grpc_asyncio.py`).
- private child `_BaseAssetSetAssetServiceRestTransport` for base REST transport with inner classes `_BaseMETHOD` (defined in `rest_base.py`).
- public child `AssetSetAssetServiceRestTransport` for sync REST transport with inner classes `METHOD` derived from the parent's corresponding `_BaseMETHOD` classes (defined in `rest.py`).
