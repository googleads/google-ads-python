
transport inheritance structure
_______________________________

`CampaignFeedServiceTransport` is the ABC for all transports.
- public child `CampaignFeedServiceGrpcTransport` for sync gRPC transport (defined in `grpc.py`).
- public child `CampaignFeedServiceGrpcAsyncIOTransport` for async gRPC transport (defined in `grpc_asyncio.py`).
- private child `_BaseCampaignFeedServiceRestTransport` for base REST transport with inner classes `_BaseMETHOD` (defined in `rest_base.py`).
- public child `CampaignFeedServiceRestTransport` for sync REST transport with inner classes `METHOD` derived from the parent's corresponding `_BaseMETHOD` classes (defined in `rest.py`).
