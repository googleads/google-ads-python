
transport inheritance structure
_______________________________

`CampaignBudgetServiceTransport` is the ABC for all transports.
- public child `CampaignBudgetServiceGrpcTransport` for sync gRPC transport (defined in `grpc.py`).
- public child `CampaignBudgetServiceGrpcAsyncIOTransport` for async gRPC transport (defined in `grpc_asyncio.py`).
- private child `_BaseCampaignBudgetServiceRestTransport` for base REST transport with inner classes `_BaseMETHOD` (defined in `rest_base.py`).
- public child `CampaignBudgetServiceRestTransport` for sync REST transport with inner classes `METHOD` derived from the parent's corresponding `_BaseMETHOD` classes (defined in `rest.py`).
