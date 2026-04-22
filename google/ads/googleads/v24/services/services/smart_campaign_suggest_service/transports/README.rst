
transport inheritance structure
_______________________________

`SmartCampaignSuggestServiceTransport` is the ABC for all transports.
- public child `SmartCampaignSuggestServiceGrpcTransport` for sync gRPC transport (defined in `grpc.py`).
- public child `SmartCampaignSuggestServiceGrpcAsyncIOTransport` for async gRPC transport (defined in `grpc_asyncio.py`).
- private child `_BaseSmartCampaignSuggestServiceRestTransport` for base REST transport with inner classes `_BaseMETHOD` (defined in `rest_base.py`).
- public child `SmartCampaignSuggestServiceRestTransport` for sync REST transport with inner classes `METHOD` derived from the parent's corresponding `_BaseMETHOD` classes (defined in `rest.py`).
