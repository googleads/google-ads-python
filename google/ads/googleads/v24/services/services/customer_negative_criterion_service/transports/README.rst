
transport inheritance structure
_______________________________

`CustomerNegativeCriterionServiceTransport` is the ABC for all transports.
- public child `CustomerNegativeCriterionServiceGrpcTransport` for sync gRPC transport (defined in `grpc.py`).
- public child `CustomerNegativeCriterionServiceGrpcAsyncIOTransport` for async gRPC transport (defined in `grpc_asyncio.py`).
- private child `_BaseCustomerNegativeCriterionServiceRestTransport` for base REST transport with inner classes `_BaseMETHOD` (defined in `rest_base.py`).
- public child `CustomerNegativeCriterionServiceRestTransport` for sync REST transport with inner classes `METHOD` derived from the parent's corresponding `_BaseMETHOD` classes (defined in `rest.py`).
