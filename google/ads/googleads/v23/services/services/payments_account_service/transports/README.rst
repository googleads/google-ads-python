
transport inheritance structure
_______________________________

`PaymentsAccountServiceTransport` is the ABC for all transports.
- public child `PaymentsAccountServiceGrpcTransport` for sync gRPC transport (defined in `grpc.py`).
- public child `PaymentsAccountServiceGrpcAsyncIOTransport` for async gRPC transport (defined in `grpc_asyncio.py`).
- private child `_BasePaymentsAccountServiceRestTransport` for base REST transport with inner classes `_BaseMETHOD` (defined in `rest_base.py`).
- public child `PaymentsAccountServiceRestTransport` for sync REST transport with inner classes `METHOD` derived from the parent's corresponding `_BaseMETHOD` classes (defined in `rest.py`).
