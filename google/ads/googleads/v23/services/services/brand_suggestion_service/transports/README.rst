
transport inheritance structure
_______________________________

`BrandSuggestionServiceTransport` is the ABC for all transports.
- public child `BrandSuggestionServiceGrpcTransport` for sync gRPC transport (defined in `grpc.py`).
- public child `BrandSuggestionServiceGrpcAsyncIOTransport` for async gRPC transport (defined in `grpc_asyncio.py`).
- private child `_BaseBrandSuggestionServiceRestTransport` for base REST transport with inner classes `_BaseMETHOD` (defined in `rest_base.py`).
- public child `BrandSuggestionServiceRestTransport` for sync REST transport with inner classes `METHOD` derived from the parent's corresponding `_BaseMETHOD` classes (defined in `rest.py`).
