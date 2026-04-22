
transport inheritance structure
_______________________________

`CampaignConversionGoalServiceTransport` is the ABC for all transports.
- public child `CampaignConversionGoalServiceGrpcTransport` for sync gRPC transport (defined in `grpc.py`).
- public child `CampaignConversionGoalServiceGrpcAsyncIOTransport` for async gRPC transport (defined in `grpc_asyncio.py`).
- private child `_BaseCampaignConversionGoalServiceRestTransport` for base REST transport with inner classes `_BaseMETHOD` (defined in `rest_base.py`).
- public child `CampaignConversionGoalServiceRestTransport` for sync REST transport with inner classes `METHOD` derived from the parent's corresponding `_BaseMETHOD` classes (defined in `rest.py`).
