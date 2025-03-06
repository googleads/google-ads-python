
transport inheritance structure
_______________________________

`FeedItemTargetServiceTransport` is the ABC for all transports.
- public child `FeedItemTargetServiceGrpcTransport` for sync gRPC transport (defined in `grpc.py`).
- public child `FeedItemTargetServiceGrpcAsyncIOTransport` for async gRPC transport (defined in `grpc_asyncio.py`).
- private child `_BaseFeedItemTargetServiceRestTransport` for base REST transport with inner classes `_BaseMETHOD` (defined in `rest_base.py`).
- public child `FeedItemTargetServiceRestTransport` for sync REST transport with inner classes `METHOD` derived from the parent's corresponding `_BaseMETHOD` classes (defined in `rest.py`).
