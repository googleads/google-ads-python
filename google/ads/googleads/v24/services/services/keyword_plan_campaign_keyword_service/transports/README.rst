
transport inheritance structure
_______________________________

`KeywordPlanCampaignKeywordServiceTransport` is the ABC for all transports.
- public child `KeywordPlanCampaignKeywordServiceGrpcTransport` for sync gRPC transport (defined in `grpc.py`).
- public child `KeywordPlanCampaignKeywordServiceGrpcAsyncIOTransport` for async gRPC transport (defined in `grpc_asyncio.py`).
- private child `_BaseKeywordPlanCampaignKeywordServiceRestTransport` for base REST transport with inner classes `_BaseMETHOD` (defined in `rest_base.py`).
- public child `KeywordPlanCampaignKeywordServiceRestTransport` for sync REST transport with inner classes `METHOD` derived from the parent's corresponding `_BaseMETHOD` classes (defined in `rest.py`).
