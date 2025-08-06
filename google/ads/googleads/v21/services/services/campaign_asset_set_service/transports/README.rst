
transport inheritance structure
_______________________________

`CampaignAssetSetServiceTransport` is the ABC for all transports.
- public child `CampaignAssetSetServiceGrpcTransport` for sync gRPC transport (defined in `grpc.py`).
- public child `CampaignAssetSetServiceGrpcAsyncIOTransport` for async gRPC transport (defined in `grpc_asyncio.py`).
- private child `_BaseCampaignAssetSetServiceRestTransport` for base REST transport with inner classes `_BaseMETHOD` (defined in `rest_base.py`).
- public child `CampaignAssetSetServiceRestTransport` for sync REST transport with inner classes `METHOD` derived from the parent's corresponding `_BaseMETHOD` classes (defined in `rest.py`).
