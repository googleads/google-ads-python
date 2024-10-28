
transport inheritance structure
_______________________________

`AdGroupFeedServiceTransport` is the ABC for all transports.
- public child `AdGroupFeedServiceGrpcTransport` for sync gRPC transport (defined in `grpc.py`).
- public child `AdGroupFeedServiceGrpcAsyncIOTransport` for async gRPC transport (defined in `grpc_asyncio.py`).
- private child `_BaseAdGroupFeedServiceRestTransport` for base REST transport with inner classes `_BaseMETHOD` (defined in `rest_base.py`).
- public child `AdGroupFeedServiceRestTransport` for sync REST transport with inner classes `METHOD` derived from the parent's corresponding `_BaseMETHOD` classes (defined in `rest.py`).
