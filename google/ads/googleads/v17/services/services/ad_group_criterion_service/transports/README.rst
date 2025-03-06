
transport inheritance structure
_______________________________

`AdGroupCriterionServiceTransport` is the ABC for all transports.
- public child `AdGroupCriterionServiceGrpcTransport` for sync gRPC transport (defined in `grpc.py`).
- public child `AdGroupCriterionServiceGrpcAsyncIOTransport` for async gRPC transport (defined in `grpc_asyncio.py`).
- private child `_BaseAdGroupCriterionServiceRestTransport` for base REST transport with inner classes `_BaseMETHOD` (defined in `rest_base.py`).
- public child `AdGroupCriterionServiceRestTransport` for sync REST transport with inner classes `METHOD` derived from the parent's corresponding `_BaseMETHOD` classes (defined in `rest.py`).
