
transport inheritance structure
_______________________________

`CampaignExtensionSettingServiceTransport` is the ABC for all transports.
- public child `CampaignExtensionSettingServiceGrpcTransport` for sync gRPC transport (defined in `grpc.py`).
- public child `CampaignExtensionSettingServiceGrpcAsyncIOTransport` for async gRPC transport (defined in `grpc_asyncio.py`).
- private child `_BaseCampaignExtensionSettingServiceRestTransport` for base REST transport with inner classes `_BaseMETHOD` (defined in `rest_base.py`).
- public child `CampaignExtensionSettingServiceRestTransport` for sync REST transport with inner classes `METHOD` derived from the parent's corresponding `_BaseMETHOD` classes (defined in `rest.py`).
