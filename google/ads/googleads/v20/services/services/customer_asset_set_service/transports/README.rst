
transport inheritance structure
_______________________________

`CustomerAssetSetServiceTransport` is the ABC for all transports.
- public child `CustomerAssetSetServiceGrpcTransport` for sync gRPC transport (defined in `grpc.py`).
- public child `CustomerAssetSetServiceGrpcAsyncIOTransport` for async gRPC transport (defined in `grpc_asyncio.py`).
- private child `_BaseCustomerAssetSetServiceRestTransport` for base REST transport with inner classes `_BaseMETHOD` (defined in `rest_base.py`).
- public child `CustomerAssetSetServiceRestTransport` for sync REST transport with inner classes `METHOD` derived from the parent's corresponding `_BaseMETHOD` classes (defined in `rest.py`).
