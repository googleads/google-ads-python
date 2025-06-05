
transport inheritance structure
_______________________________

`ContentCreatorInsightsServiceTransport` is the ABC for all transports.
- public child `ContentCreatorInsightsServiceGrpcTransport` for sync gRPC transport (defined in `grpc.py`).
- public child `ContentCreatorInsightsServiceGrpcAsyncIOTransport` for async gRPC transport (defined in `grpc_asyncio.py`).
- private child `_BaseContentCreatorInsightsServiceRestTransport` for base REST transport with inner classes `_BaseMETHOD` (defined in `rest_base.py`).
- public child `ContentCreatorInsightsServiceRestTransport` for sync REST transport with inner classes `METHOD` derived from the parent's corresponding `_BaseMETHOD` classes (defined in `rest.py`).
