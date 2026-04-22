
transport inheritance structure
_______________________________

`CustomerLabelServiceTransport` is the ABC for all transports.
- public child `CustomerLabelServiceGrpcTransport` for sync gRPC transport (defined in `grpc.py`).
- public child `CustomerLabelServiceGrpcAsyncIOTransport` for async gRPC transport (defined in `grpc_asyncio.py`).
- private child `_BaseCustomerLabelServiceRestTransport` for base REST transport with inner classes `_BaseMETHOD` (defined in `rest_base.py`).
- public child `CustomerLabelServiceRestTransport` for sync REST transport with inner classes `METHOD` derived from the parent's corresponding `_BaseMETHOD` classes (defined in `rest.py`).
