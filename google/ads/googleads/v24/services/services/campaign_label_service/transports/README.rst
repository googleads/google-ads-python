
transport inheritance structure
_______________________________

`CampaignLabelServiceTransport` is the ABC for all transports.
- public child `CampaignLabelServiceGrpcTransport` for sync gRPC transport (defined in `grpc.py`).
- public child `CampaignLabelServiceGrpcAsyncIOTransport` for async gRPC transport (defined in `grpc_asyncio.py`).
- private child `_BaseCampaignLabelServiceRestTransport` for base REST transport with inner classes `_BaseMETHOD` (defined in `rest_base.py`).
- public child `CampaignLabelServiceRestTransport` for sync REST transport with inner classes `METHOD` derived from the parent's corresponding `_BaseMETHOD` classes (defined in `rest.py`).
