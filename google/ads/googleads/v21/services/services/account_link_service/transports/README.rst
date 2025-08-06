
transport inheritance structure
_______________________________

`AccountLinkServiceTransport` is the ABC for all transports.
- public child `AccountLinkServiceGrpcTransport` for sync gRPC transport (defined in `grpc.py`).
- public child `AccountLinkServiceGrpcAsyncIOTransport` for async gRPC transport (defined in `grpc_asyncio.py`).
- private child `_BaseAccountLinkServiceRestTransport` for base REST transport with inner classes `_BaseMETHOD` (defined in `rest_base.py`).
- public child `AccountLinkServiceRestTransport` for sync REST transport with inner classes `METHOD` derived from the parent's corresponding `_BaseMETHOD` classes (defined in `rest.py`).
