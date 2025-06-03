
transport inheritance structure
_______________________________

`ThirdPartyAppAnalyticsLinkServiceTransport` is the ABC for all transports.
- public child `ThirdPartyAppAnalyticsLinkServiceGrpcTransport` for sync gRPC transport (defined in `grpc.py`).
- public child `ThirdPartyAppAnalyticsLinkServiceGrpcAsyncIOTransport` for async gRPC transport (defined in `grpc_asyncio.py`).
- private child `_BaseThirdPartyAppAnalyticsLinkServiceRestTransport` for base REST transport with inner classes `_BaseMETHOD` (defined in `rest_base.py`).
- public child `ThirdPartyAppAnalyticsLinkServiceRestTransport` for sync REST transport with inner classes `METHOD` derived from the parent's corresponding `_BaseMETHOD` classes (defined in `rest.py`).
