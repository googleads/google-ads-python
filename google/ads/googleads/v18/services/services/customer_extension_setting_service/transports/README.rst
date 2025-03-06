
transport inheritance structure
_______________________________

`CustomerExtensionSettingServiceTransport` is the ABC for all transports.
- public child `CustomerExtensionSettingServiceGrpcTransport` for sync gRPC transport (defined in `grpc.py`).
- public child `CustomerExtensionSettingServiceGrpcAsyncIOTransport` for async gRPC transport (defined in `grpc_asyncio.py`).
- private child `_BaseCustomerExtensionSettingServiceRestTransport` for base REST transport with inner classes `_BaseMETHOD` (defined in `rest_base.py`).
- public child `CustomerExtensionSettingServiceRestTransport` for sync REST transport with inner classes `METHOD` derived from the parent's corresponding `_BaseMETHOD` classes (defined in `rest.py`).
