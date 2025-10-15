
transport inheritance structure
_______________________________

`SharedCriterionServiceTransport` is the ABC for all transports.
- public child `SharedCriterionServiceGrpcTransport` for sync gRPC transport (defined in `grpc.py`).
- public child `SharedCriterionServiceGrpcAsyncIOTransport` for async gRPC transport (defined in `grpc_asyncio.py`).
- private child `_BaseSharedCriterionServiceRestTransport` for base REST transport with inner classes `_BaseMETHOD` (defined in `rest_base.py`).
- public child `SharedCriterionServiceRestTransport` for sync REST transport with inner classes `METHOD` derived from the parent's corresponding `_BaseMETHOD` classes (defined in `rest.py`).
