
transport inheritance structure
_______________________________

`CustomerLifecycleGoalServiceTransport` is the ABC for all transports.
- public child `CustomerLifecycleGoalServiceGrpcTransport` for sync gRPC transport (defined in `grpc.py`).
- public child `CustomerLifecycleGoalServiceGrpcAsyncIOTransport` for async gRPC transport (defined in `grpc_asyncio.py`).
- private child `_BaseCustomerLifecycleGoalServiceRestTransport` for base REST transport with inner classes `_BaseMETHOD` (defined in `rest_base.py`).
- public child `CustomerLifecycleGoalServiceRestTransport` for sync REST transport with inner classes `METHOD` derived from the parent's corresponding `_BaseMETHOD` classes (defined in `rest.py`).
