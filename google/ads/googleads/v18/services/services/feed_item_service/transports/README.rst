
transport inheritance structure
_______________________________

`FeedItemServiceTransport` is the ABC for all transports.
- public child `FeedItemServiceGrpcTransport` for sync gRPC transport (defined in `grpc.py`).
- public child `FeedItemServiceGrpcAsyncIOTransport` for async gRPC transport (defined in `grpc_asyncio.py`).
- private child `_BaseFeedItemServiceRestTransport` for base REST transport with inner classes `_BaseMETHOD` (defined in `rest_base.py`).
- public child `FeedItemServiceRestTransport` for sync REST transport with inner classes `METHOD` derived from the parent's corresponding `_BaseMETHOD` classes (defined in `rest.py`).
