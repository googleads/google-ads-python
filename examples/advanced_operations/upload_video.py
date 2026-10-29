#!/usr/bin/env python
# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""This example illustrates how to upload videos to YouTube."""

import argparse
import itertools
import sys
from typing import Iterator

from google.api_core.exceptions import GoogleAPICallError
from google.api_core.resumable_transfer import ResumableUploadSession

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
from google.ads.googleads.v26.services.services.google_ads_service import (
    GoogleAdsServiceClient,
)
from google.ads.googleads.v26.services.types.google_ads_service import (
    SearchGoogleAdsStreamResponse,
)
from google.ads.googleads.v26.services.services.you_tube_video_upload_service.client import (
    YouTubeVideoUploadServiceClient,
)
from google.ads.googleads.v26.services.types.youtube_video_upload_service import (
    CreateYouTubeVideoUploadRequest,
    CreateYouTubeVideoUploadResponse,
)


def main(
    client: GoogleAdsClient, customer_id: str, video_file_path: str
) -> None:
    """The main method that uploads a video and retrieves its state.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.
        video_file_path: the absolute path to a video file on your machine.
    """

    # [START upload_video_1]
    yt_service: YouTubeVideoUploadServiceClient = client.get_service(
        "YouTubeVideoUploadService"
    )

    create_upload_request: CreateYouTubeVideoUploadRequest = client.get_type(
        "CreateYouTubeVideoUploadRequest"
    )
    create_upload_request.customer_id = customer_id
    create_upload_request.you_tube_video_upload.video_title = "Test Video"
    create_upload_request.you_tube_video_upload.video_description = (
        "Test Video Description"
    )
    create_upload_request.you_tube_video_upload.video_privacy = (
        client.enums.YouTubeVideoPrivacyEnum.UNLISTED
    )

    upload_session: ResumableUploadSession = (
        yt_service.create_you_tube_video_upload(request=create_upload_request)
    )
    video_upload_resource_name: str
    with open(video_file_path, "rb") as stream:
        response: CreateYouTubeVideoUploadResponse = upload_session.upload(
            stream
        )
        video_upload_resource_name = response.resource_name
        print(f"Created YouTube video upload: {video_upload_resource_name}")
    # [END upload_video_1]

    # [START upload_video_3]
    # Retrieve the metadata of the newly uploaded video.
    query: str = f"""
        SELECT
          you_tube_video_upload.resource_name,
          you_tube_video_upload.video_id,
          you_tube_video_upload.state
        FROM you_tube_video_upload
        WHERE you_tube_video_upload.resource_name = '{video_upload_resource_name}'"""

    ga_service: GoogleAdsServiceClient = client.get_service("GoogleAdsService")
    stream: Iterator[SearchGoogleAdsStreamResponse] = ga_service.search_stream(
        customer_id=customer_id, query=query
    )

    for row in itertools.chain.from_iterable(
        batch.results for batch in stream
    ):
        print(
            f"Video with ID {row.you_tube_video_upload.video_id} was found in "
            f"state {row.you_tube_video_upload.state}."
        )
    # [END upload_video_3]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Uploads a video to YouTube using Google Ads API."
    )
    # The following argument(s) should be provided to run the example.
    parser.add_argument(
        "-c",
        "--customer_id",
        type=str,
        required=True,
        help="The Google Ads customer ID.",
    )
    parser.add_argument(
        "-v",
        "--video_file_path",
        type=str,
        required=True,
        help="The path to a video file to upload to YouTube.",
    )
    args: argparse.Namespace = parser.parse_args()

    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    googleads_client: GoogleAdsClient = GoogleAdsClient.load_from_storage(
        version="v26"
    )
    try:
        main(
            googleads_client,
            customer_id=args.customer_id,
            video_file_path=args.video_file_path,
        )
    except GoogleAdsException as ex:
        print(
            f'Request with ID "{ex.request_id}" failed with status '
            f'"{ex.error.code().name}" and includes the following errors:'
        )
        for error in ex.failure.errors:
            print(f'\tError with message "{error.message}".')
            if hasattr(error, "location") and error.location:
                for field_path_element in error.location.field_path_elements:
                    print(f"\t\tOn field: {field_path_element.field_name}")
        sys.exit(1)
    except GoogleAPICallError as ex:
        print(f"Resumable upload failed: {ex}")
        if getattr(ex, "upload_url", None):
            print(f"\tResumable upload URL: {ex.upload_url}")
        sys.exit(1)
