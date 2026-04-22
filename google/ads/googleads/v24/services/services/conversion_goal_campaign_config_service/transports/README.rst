
transport inheritance structure
_______________________________

`ConversionGoalCampaignConfigServiceTransport` is the ABC for all transports.
- public child `ConversionGoalCampaignConfigServiceGrpcTransport` for sync gRPC transport (defined in `grpc.py`).
- public child `ConversionGoalCampaignConfigServiceGrpcAsyncIOTransport` for async gRPC transport (defined in `grpc_asyncio.py`).
- private child `_BaseConversionGoalCampaignConfigServiceRestTransport` for base REST transport with inner classes `_BaseMETHOD` (defined in `rest_base.py`).
- public child `ConversionGoalCampaignConfigServiceRestTransport` for sync REST transport with inner classes `METHOD` derived from the parent's corresponding `_BaseMETHOD` classes (defined in `rest.py`).
