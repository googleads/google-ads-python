
transport inheritance structure
_______________________________

`CampaignCustomizerServiceTransport` is the ABC for all transports.
- public child `CampaignCustomizerServiceGrpcTransport` for sync gRPC transport (defined in `grpc.py`).
- public child `CampaignCustomizerServiceGrpcAsyncIOTransport` for async gRPC transport (defined in `grpc_asyncio.py`).
- private child `_BaseCampaignCustomizerServiceRestTransport` for base REST transport with inner classes `_BaseMETHOD` (defined in `rest_base.py`).
- public child `CampaignCustomizerServiceRestTransport` for sync REST transport with inner classes `METHOD` derived from the parent's corresponding `_BaseMETHOD` classes (defined in `rest.py`).
