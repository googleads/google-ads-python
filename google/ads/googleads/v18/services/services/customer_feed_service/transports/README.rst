
transport inheritance structure
_______________________________

`CustomerFeedServiceTransport` is the ABC for all transports.
- public child `CustomerFeedServiceGrpcTransport` for sync gRPC transport (defined in `grpc.py`).
- public child `CustomerFeedServiceGrpcAsyncIOTransport` for async gRPC transport (defined in `grpc_asyncio.py`).
- private child `_BaseCustomerFeedServiceRestTransport` for base REST transport with inner classes `_BaseMETHOD` (defined in `rest_base.py`).
- public child `CustomerFeedServiceRestTransport` for sync REST transport with inner classes `METHOD` derived from the parent's corresponding `_BaseMETHOD` classes (defined in `rest.py`).
