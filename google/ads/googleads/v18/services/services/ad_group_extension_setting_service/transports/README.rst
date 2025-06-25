
transport inheritance structure
_______________________________

`AdGroupExtensionSettingServiceTransport` is the ABC for all transports.
- public child `AdGroupExtensionSettingServiceGrpcTransport` for sync gRPC transport (defined in `grpc.py`).
- public child `AdGroupExtensionSettingServiceGrpcAsyncIOTransport` for async gRPC transport (defined in `grpc_asyncio.py`).
- private child `_BaseAdGroupExtensionSettingServiceRestTransport` for base REST transport with inner classes `_BaseMETHOD` (defined in `rest_base.py`).
- public child `AdGroupExtensionSettingServiceRestTransport` for sync REST transport with inner classes `METHOD` derived from the parent's corresponding `_BaseMETHOD` classes (defined in `rest.py`).
