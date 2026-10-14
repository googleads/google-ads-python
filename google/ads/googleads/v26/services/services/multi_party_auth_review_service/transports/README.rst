
transport inheritance structure
_______________________________

``MultiPartyAuthReviewServiceTransport`` is the ABC for all transports.

- public child ``MultiPartyAuthReviewServiceGrpcTransport`` for sync gRPC transport (defined in ``grpc.py``).
- public child ``MultiPartyAuthReviewServiceGrpcAsyncIOTransport`` for async gRPC transport (defined in ``grpc_asyncio.py``).
- private child ``_BaseMultiPartyAuthReviewServiceRestTransport`` for base REST transport with inner classes ``_BaseMETHOD`` (defined in ``rest_base.py``).
- public child ``MultiPartyAuthReviewServiceRestTransport`` for sync REST transport with inner classes ``METHOD`` derived from the parent's corresponding ``_BaseMETHOD`` classes (defined in ``rest.py``).
