
transport inheritance structure
_______________________________

`AdGroupAssetServiceTransport` is the ABC for all transports.
- public child `AdGroupAssetServiceGrpcTransport` for sync gRPC transport (defined in `grpc.py`).
- public child `AdGroupAssetServiceGrpcAsyncIOTransport` for async gRPC transport (defined in `grpc_asyncio.py`).
- private child `_BaseAdGroupAssetServiceRestTransport` for base REST transport with inner classes `_BaseMETHOD` (defined in `rest_base.py`).
- public child `AdGroupAssetServiceRestTransport` for sync REST transport with inner classes `METHOD` derived from the parent's corresponding `_BaseMETHOD` classes (defined in `rest.py`).
