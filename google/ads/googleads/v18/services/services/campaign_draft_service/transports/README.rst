
transport inheritance structure
_______________________________

`CampaignDraftServiceTransport` is the ABC for all transports.
- public child `CampaignDraftServiceGrpcTransport` for sync gRPC transport (defined in `grpc.py`).
- public child `CampaignDraftServiceGrpcAsyncIOTransport` for async gRPC transport (defined in `grpc_asyncio.py`).
- private child `_BaseCampaignDraftServiceRestTransport` for base REST transport with inner classes `_BaseMETHOD` (defined in `rest_base.py`).
- public child `CampaignDraftServiceRestTransport` for sync REST transport with inner classes `METHOD` derived from the parent's corresponding `_BaseMETHOD` classes (defined in `rest.py`).
