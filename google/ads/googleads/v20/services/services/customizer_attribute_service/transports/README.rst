
transport inheritance structure
_______________________________

`CustomizerAttributeServiceTransport` is the ABC for all transports.
- public child `CustomizerAttributeServiceGrpcTransport` for sync gRPC transport (defined in `grpc.py`).
- public child `CustomizerAttributeServiceGrpcAsyncIOTransport` for async gRPC transport (defined in `grpc_asyncio.py`).
- private child `_BaseCustomizerAttributeServiceRestTransport` for base REST transport with inner classes `_BaseMETHOD` (defined in `rest_base.py`).
- public child `CustomizerAttributeServiceRestTransport` for sync REST transport with inner classes `METHOD` derived from the parent's corresponding `_BaseMETHOD` classes (defined in `rest.py`).
