
transport inheritance structure
_______________________________

`CustomerCustomizerServiceTransport` is the ABC for all transports.
- public child `CustomerCustomizerServiceGrpcTransport` for sync gRPC transport (defined in `grpc.py`).
- public child `CustomerCustomizerServiceGrpcAsyncIOTransport` for async gRPC transport (defined in `grpc_asyncio.py`).
- private child `_BaseCustomerCustomizerServiceRestTransport` for base REST transport with inner classes `_BaseMETHOD` (defined in `rest_base.py`).
- public child `CustomerCustomizerServiceRestTransport` for sync REST transport with inner classes `METHOD` derived from the parent's corresponding `_BaseMETHOD` classes (defined in `rest.py`).
