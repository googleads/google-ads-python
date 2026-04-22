
transport inheritance structure
_______________________________

`ProductLinkServiceTransport` is the ABC for all transports.
- public child `ProductLinkServiceGrpcTransport` for sync gRPC transport (defined in `grpc.py`).
- public child `ProductLinkServiceGrpcAsyncIOTransport` for async gRPC transport (defined in `grpc_asyncio.py`).
- private child `_BaseProductLinkServiceRestTransport` for base REST transport with inner classes `_BaseMETHOD` (defined in `rest_base.py`).
- public child `ProductLinkServiceRestTransport` for sync REST transport with inner classes `METHOD` derived from the parent's corresponding `_BaseMETHOD` classes (defined in `rest.py`).
