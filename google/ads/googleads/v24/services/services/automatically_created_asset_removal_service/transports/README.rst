
transport inheritance structure
_______________________________

`AutomaticallyCreatedAssetRemovalServiceTransport` is the ABC for all transports.
- public child `AutomaticallyCreatedAssetRemovalServiceGrpcTransport` for sync gRPC transport (defined in `grpc.py`).
- public child `AutomaticallyCreatedAssetRemovalServiceGrpcAsyncIOTransport` for async gRPC transport (defined in `grpc_asyncio.py`).
- private child `_BaseAutomaticallyCreatedAssetRemovalServiceRestTransport` for base REST transport with inner classes `_BaseMETHOD` (defined in `rest_base.py`).
- public child `AutomaticallyCreatedAssetRemovalServiceRestTransport` for sync REST transport with inner classes `METHOD` derived from the parent's corresponding `_BaseMETHOD` classes (defined in `rest.py`).
