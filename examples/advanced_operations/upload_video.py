#!/usr/bin/env python
# Copyright 2026s Google LLC
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
import os
import sys
import logging
from typing import Iterator, Iterable, List, MutableSequence

import google.auth
from google.auth.credentials import Credentials
from google.auth import impersonated_credentials

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
from google.ads.googleads.v23.services.services.google_ads_service import (
    GoogleAdsServiceClient,
)
from google.ads.googleads.v23.services.types.google_ads_service import (
    SearchGoogleAdsStreamResponse,
    GoogleAdsRow,
)

from google.ads.googleads.v23.services.services.you_tube_video_upload_service.client import (
    YouTubeVideoUploadServiceClient,
)
from google.ads.googleads.v23.services.types import youtube_video_upload_service
from google.ads.googleads.v23.services.types.youtube_video_upload_service import (
    CreateYouTubeVideoUploadRequest,
    CreateYouTubeVideoUploadResponse,
    UpdateYouTubeVideoUploadRequest,
    UpdateYouTubeVideoUploadResponse,
    RemoveYouTubeVideoUploadRequest,
    RemoveYouTubeVideoUploadResponse,
)

from google.protobuf import field_mask_pb2
from google.ads.googleads.v23.resources.types import youtube_video_upload


def main(client: GoogleAdsClient, customer_id: str, video_file_path: str) -> None:
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

    create_upload_request: CreateYouTubeVideoUploadRequest = (
        youtube_video_upload_service.CreateYouTubeVideoUploadRequest()
    )
    create_upload_request.customer_id = customer_id
    create_upload_request.you_tube_video_upload.video_title = "Test Video"
    create_upload_request.you_tube_video_upload.video_description = (
        "Test Video Description"
    )
    create_upload_request.you_tube_video_upload.video_privacy = (
        client.enums.YouTubeVideoPrivacyEnum.UNLISTED
    )

    video_upload_resource_name: str
    with open(video_file_path, "rb") as stream:
        response: CreateYouTubeVideoUploadResponse = (
            yt_service.create_you_tube_video_upload(
                stream=stream,
                request=create_upload_request,
                retry=None,
            )
        )
        print(f"Created YouTube video upload: {response.resource_name}")
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

    for row in itertools.chain.from_iterable(batch.results for batch in stream):
        video = row.you_tube_video_upload
        print(
            f"Video with ID {row.you_tube_video_upload.video_id} was found in state {row.you_tube_video_upload.state}."
        )
    # [END upload_video_3]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Lists all campaigns for specified customer."
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
    googleads_client: GoogleAdsClient = GoogleAdsClient.load_from_storage(version="v23")
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
        if hasattr(ex.error, "_response"):
            raw_res = getattr(ex.error, "_response")
            print(f"\n--- Full Response (Reflected from Proxy) ---")
            print(f"Status Code: {raw_res.status_code}")
            print(f"Headers: {raw_res.headers}")
            print(f"Body: {raw_res.text}")
            print(f"-------------------------------------------\n")

        for error in ex.failure.errors:
            print(f'\tError with message "{error.message}".')
            if hasattr(error, "location") and error.location:
                for field_path_element in error.location.field_path_elements:
                    print(f"\t\tOn field: {field_path_element.field_name}")
        sys.exit(1)
