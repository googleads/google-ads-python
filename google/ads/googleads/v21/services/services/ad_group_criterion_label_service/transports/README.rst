
transport inheritance structure
_______________________________

`AdGroupCriterionLabelServiceTransport` is the ABC for all transports.
- public child `AdGroupCriterionLabelServiceGrpcTransport` for sync gRPC transport (defined in `grpc.py`).
- public child `AdGroupCriterionLabelServiceGrpcAsyncIOTransport` for async gRPC transport (defined in `grpc_asyncio.py`).
- private child `_BaseAdGroupCriterionLabelServiceRestTransport` for base REST transport with inner classes `_BaseMETHOD` (defined in `rest_base.py`).
- public child `AdGroupCriterionLabelServiceRestTransport` for sync REST transport with inner classes `METHOD` derived from the parent's corresponding `_BaseMETHOD` classes (defined in `rest.py`).
