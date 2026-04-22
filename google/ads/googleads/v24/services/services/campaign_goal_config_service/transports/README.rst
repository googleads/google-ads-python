
transport inheritance structure
_______________________________

`CampaignGoalConfigServiceTransport` is the ABC for all transports.
- public child `CampaignGoalConfigServiceGrpcTransport` for sync gRPC transport (defined in `grpc.py`).
- public child `CampaignGoalConfigServiceGrpcAsyncIOTransport` for async gRPC transport (defined in `grpc_asyncio.py`).
- private child `_BaseCampaignGoalConfigServiceRestTransport` for base REST transport with inner classes `_BaseMETHOD` (defined in `rest_base.py`).
- public child `CampaignGoalConfigServiceRestTransport` for sync REST transport with inner classes `METHOD` derived from the parent's corresponding `_BaseMETHOD` classes (defined in `rest.py`).
