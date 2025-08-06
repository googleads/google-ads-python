
transport inheritance structure
_______________________________

`RecommendationSubscriptionServiceTransport` is the ABC for all transports.
- public child `RecommendationSubscriptionServiceGrpcTransport` for sync gRPC transport (defined in `grpc.py`).
- public child `RecommendationSubscriptionServiceGrpcAsyncIOTransport` for async gRPC transport (defined in `grpc_asyncio.py`).
- private child `_BaseRecommendationSubscriptionServiceRestTransport` for base REST transport with inner classes `_BaseMETHOD` (defined in `rest_base.py`).
- public child `RecommendationSubscriptionServiceRestTransport` for sync REST transport with inner classes `METHOD` derived from the parent's corresponding `_BaseMETHOD` classes (defined in `rest.py`).
