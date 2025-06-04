
transport inheritance structure
_______________________________

`CampaignBidModifierServiceTransport` is the ABC for all transports.
- public child `CampaignBidModifierServiceGrpcTransport` for sync gRPC transport (defined in `grpc.py`).
- public child `CampaignBidModifierServiceGrpcAsyncIOTransport` for async gRPC transport (defined in `grpc_asyncio.py`).
- private child `_BaseCampaignBidModifierServiceRestTransport` for base REST transport with inner classes `_BaseMETHOD` (defined in `rest_base.py`).
- public child `CampaignBidModifierServiceRestTransport` for sync REST transport with inner classes `METHOD` derived from the parent's corresponding `_BaseMETHOD` classes (defined in `rest.py`).
