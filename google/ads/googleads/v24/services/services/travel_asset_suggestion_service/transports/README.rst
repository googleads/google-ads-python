
transport inheritance structure
_______________________________

`TravelAssetSuggestionServiceTransport` is the ABC for all transports.
- public child `TravelAssetSuggestionServiceGrpcTransport` for sync gRPC transport (defined in `grpc.py`).
- public child `TravelAssetSuggestionServiceGrpcAsyncIOTransport` for async gRPC transport (defined in `grpc_asyncio.py`).
- private child `_BaseTravelAssetSuggestionServiceRestTransport` for base REST transport with inner classes `_BaseMETHOD` (defined in `rest_base.py`).
- public child `TravelAssetSuggestionServiceRestTransport` for sync REST transport with inner classes `METHOD` derived from the parent's corresponding `_BaseMETHOD` classes (defined in `rest.py`).
