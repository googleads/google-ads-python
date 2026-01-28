
transport inheritance structure
_______________________________

`CampaignCriterionServiceTransport` is the ABC for all transports.
- public child `CampaignCriterionServiceGrpcTransport` for sync gRPC transport (defined in `grpc.py`).
- public child `CampaignCriterionServiceGrpcAsyncIOTransport` for async gRPC transport (defined in `grpc_asyncio.py`).
- private child `_BaseCampaignCriterionServiceRestTransport` for base REST transport with inner classes `_BaseMETHOD` (defined in `rest_base.py`).
- public child `CampaignCriterionServiceRestTransport` for sync REST transport with inner classes `METHOD` derived from the parent's corresponding `_BaseMETHOD` classes (defined in `rest.py`).
