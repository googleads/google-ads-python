
transport inheritance structure
_______________________________

`YouTubeVideoUploadServiceTransport` is the ABC for all transports.
- public child `YouTubeVideoUploadServiceGrpcTransport` for sync gRPC transport (defined in `grpc.py`).
- public child `YouTubeVideoUploadServiceGrpcAsyncIOTransport` for async gRPC transport (defined in `grpc_asyncio.py`).
- private child `_BaseYouTubeVideoUploadServiceRestTransport` for base REST transport with inner classes `_BaseMETHOD` (defined in `rest_base.py`).
- public child `YouTubeVideoUploadServiceRestTransport` for sync REST transport with inner classes `METHOD` derived from the parent's corresponding `_BaseMETHOD` classes (defined in `rest.py`).
