
transport inheritance structure
_______________________________

`KeywordPlanAdGroupServiceTransport` is the ABC for all transports.
- public child `KeywordPlanAdGroupServiceGrpcTransport` for sync gRPC transport (defined in `grpc.py`).
- public child `KeywordPlanAdGroupServiceGrpcAsyncIOTransport` for async gRPC transport (defined in `grpc_asyncio.py`).
- private child `_BaseKeywordPlanAdGroupServiceRestTransport` for base REST transport with inner classes `_BaseMETHOD` (defined in `rest_base.py`).
- public child `KeywordPlanAdGroupServiceRestTransport` for sync REST transport with inner classes `METHOD` derived from the parent's corresponding `_BaseMETHOD` classes (defined in `rest.py`).
