
transport inheritance structure
_______________________________

`BiddingStrategyServiceTransport` is the ABC for all transports.
- public child `BiddingStrategyServiceGrpcTransport` for sync gRPC transport (defined in `grpc.py`).
- public child `BiddingStrategyServiceGrpcAsyncIOTransport` for async gRPC transport (defined in `grpc_asyncio.py`).
- private child `_BaseBiddingStrategyServiceRestTransport` for base REST transport with inner classes `_BaseMETHOD` (defined in `rest_base.py`).
- public child `BiddingStrategyServiceRestTransport` for sync REST transport with inner classes `METHOD` derived from the parent's corresponding `_BaseMETHOD` classes (defined in `rest.py`).
