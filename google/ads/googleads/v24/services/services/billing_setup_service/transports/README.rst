
transport inheritance structure
_______________________________

`BillingSetupServiceTransport` is the ABC for all transports.
- public child `BillingSetupServiceGrpcTransport` for sync gRPC transport (defined in `grpc.py`).
- public child `BillingSetupServiceGrpcAsyncIOTransport` for async gRPC transport (defined in `grpc_asyncio.py`).
- private child `_BaseBillingSetupServiceRestTransport` for base REST transport with inner classes `_BaseMETHOD` (defined in `rest_base.py`).
- public child `BillingSetupServiceRestTransport` for sync REST transport with inner classes `METHOD` derived from the parent's corresponding `_BaseMETHOD` classes (defined in `rest.py`).
