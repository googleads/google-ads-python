
transport inheritance structure
_______________________________

`CampaignServiceTransport` is the ABC for all transports.
- public child `CampaignServiceGrpcTransport` for sync gRPC transport (defined in `grpc.py`).
- public child `CampaignServiceGrpcAsyncIOTransport` for async gRPC transport (defined in `grpc_asyncio.py`).
- private child `_BaseCampaignServiceRestTransport` for base REST transport with inner classes `_BaseMETHOD` (defined in `rest_base.py`).
- public child `CampaignServiceRestTransport` for sync REST transport with inner classes `METHOD` derived from the parent's corresponding `_BaseMETHOD` classes (defined in `rest.py`).
