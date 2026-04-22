
transport inheritance structure
_______________________________

`IncentiveServiceTransport` is the ABC for all transports.
- public child `IncentiveServiceGrpcTransport` for sync gRPC transport (defined in `grpc.py`).
- public child `IncentiveServiceGrpcAsyncIOTransport` for async gRPC transport (defined in `grpc_asyncio.py`).
- private child `_BaseIncentiveServiceRestTransport` for base REST transport with inner classes `_BaseMETHOD` (defined in `rest_base.py`).
- public child `IncentiveServiceRestTransport` for sync REST transport with inner classes `METHOD` derived from the parent's corresponding `_BaseMETHOD` classes (defined in `rest.py`).
