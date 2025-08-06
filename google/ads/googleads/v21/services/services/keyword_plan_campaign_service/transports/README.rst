
transport inheritance structure
_______________________________

`KeywordPlanCampaignServiceTransport` is the ABC for all transports.
- public child `KeywordPlanCampaignServiceGrpcTransport` for sync gRPC transport (defined in `grpc.py`).
- public child `KeywordPlanCampaignServiceGrpcAsyncIOTransport` for async gRPC transport (defined in `grpc_asyncio.py`).
- private child `_BaseKeywordPlanCampaignServiceRestTransport` for base REST transport with inner classes `_BaseMETHOD` (defined in `rest_base.py`).
- public child `KeywordPlanCampaignServiceRestTransport` for sync REST transport with inner classes `METHOD` derived from the parent's corresponding `_BaseMETHOD` classes (defined in `rest.py`).
