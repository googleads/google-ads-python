
transport inheritance structure
_______________________________

`AudienceInsightsServiceTransport` is the ABC for all transports.
- public child `AudienceInsightsServiceGrpcTransport` for sync gRPC transport (defined in `grpc.py`).
- public child `AudienceInsightsServiceGrpcAsyncIOTransport` for async gRPC transport (defined in `grpc_asyncio.py`).
- private child `_BaseAudienceInsightsServiceRestTransport` for base REST transport with inner classes `_BaseMETHOD` (defined in `rest_base.py`).
- public child `AudienceInsightsServiceRestTransport` for sync REST transport with inner classes `METHOD` derived from the parent's corresponding `_BaseMETHOD` classes (defined in `rest.py`).
