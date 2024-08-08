# -*- coding: utf-8 -*-
# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from google.api_core import gapic_v1
from google.api_core import retry as retries
from typing import Any, Callable, Iterable, Iterator, Sequence, Tuple, Union

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore

from google.ads.googleads.v17.services.types import batch_job_service


class ListBatchJobResultsPager:
    """A pager for iterating through ``list_batch_job_results`` requests.

    This class thinly wraps an initial
    :class:`google.ads.googleads.v17.services.types.ListBatchJobResultsResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``results`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListBatchJobResults`` requests and continue to iterate
    through the ``results`` field on the
    corresponding responses.

    All the usual :class:`google.ads.googleads.v17.services.types.ListBatchJobResultsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., batch_job_service.ListBatchJobResultsResponse],
        request: batch_job_service.ListBatchJobResultsRequest,
        response: batch_job_service.ListBatchJobResultsResponse,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (:class:`google.ads.googleads.v17.services.types.ListBatchJobResultsRequest`):
                The initial request object.
            response (:class:`google.ads.googleads.v17.services.types.ListBatchJobResultsResponse`):
                The initial response object.
            retry (google.api_core.retry.Retry): Designation of what errors,
                if any, should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = batch_job_service.ListBatchJobResultsRequest(request)
        self._response = response
        self._retry = retry
        self._timeout = timeout
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterable[batch_job_service.ListBatchJobResultsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(
                self._request,
                retry=self._retry,
                timeout=self._timeout,
                metadata=self._metadata,
            )
            yield self._response

    def __iter__(self) -> Iterator[batch_job_service.BatchJobResult]:
        for page in self.pages:
            yield from page.results

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)