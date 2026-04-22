
transport inheritance structure
_______________________________

`CustomerServiceTransport` is the ABC for all transports.
- public child `CustomerServiceGrpcTransport` for sync gRPC transport (defined in `grpc.py`).
- public child `CustomerServiceGrpcAsyncIOTransport` for async gRPC transport (defined in `grpc_asyncio.py`).
- private child `_BaseCustomerServiceRestTransport` for base REST transport with inner classes `_BaseMETHOD` (defined in `rest_base.py`).
- public child `CustomerServiceRestTransport` for sync REST transport with inner classes `METHOD` derived from the parent's corresponding `_BaseMETHOD` classes (defined in `rest.py`).
