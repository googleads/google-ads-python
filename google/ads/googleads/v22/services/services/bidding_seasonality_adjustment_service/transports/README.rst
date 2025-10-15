
transport inheritance structure
_______________________________

`BiddingSeasonalityAdjustmentServiceTransport` is the ABC for all transports.
- public child `BiddingSeasonalityAdjustmentServiceGrpcTransport` for sync gRPC transport (defined in `grpc.py`).
- public child `BiddingSeasonalityAdjustmentServiceGrpcAsyncIOTransport` for async gRPC transport (defined in `grpc_asyncio.py`).
- private child `_BaseBiddingSeasonalityAdjustmentServiceRestTransport` for base REST transport with inner classes `_BaseMETHOD` (defined in `rest_base.py`).
- public child `BiddingSeasonalityAdjustmentServiceRestTransport` for sync REST transport with inner classes `METHOD` derived from the parent's corresponding `_BaseMETHOD` classes (defined in `rest.py`).
