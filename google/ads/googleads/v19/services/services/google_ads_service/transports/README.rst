
transport inheritance structure
_______________________________

`GoogleAdsServiceTransport` is the ABC for all transports.
- public child `GoogleAdsServiceGrpcTransport` for sync gRPC transport (defined in `grpc.py`).
- public child `GoogleAdsServiceGrpcAsyncIOTransport` for async gRPC transport (defined in `grpc_asyncio.py`).
- private child `_BaseGoogleAdsServiceRestTransport` for base REST transport with inner classes `_BaseMETHOD` (defined in `rest_base.py`).
- public child `GoogleAdsServiceRestTransport` for sync REST transport with inner classes `METHOD` derived from the parent's corresponding `_BaseMETHOD` classes (defined in `rest.py`).
