# Copyright 2022 Google LLC
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
"""Wrapper classes used to modify the behavior of response objects."""

from dataclasses import dataclass, field
import grpc # Used for grpc.Call, grpc.Future, grpc.RpcError, grpc.StatusCode
import time # Not directly used in this file, but often imported with grpc
from typing import (
    Any,
    Callable,
    Iterator,
    Optional,
    Sequence,
    Tuple,
    TypeVar,
    Union,
)
from types import SimpleNamespace # For _UnaryStreamWrapper._cache original structure

from google.protobuf.message import Message
from google.ads.googleads import util


# Type variable for standard protobuf messages
DefaultMessageType = TypeVar("DefaultMessageType", bound=Message)
# Type variable for proto-plus messages (can be Any if no common base type other than object)
ProtoPlusMessageType = TypeVar("ProtoPlusMessageType")
# Generic type for add_done_callback results
T = TypeVar("T")

# Response type can be either a standard protobuf message or a proto-plus message
StreamedResponseItemType = Union[DefaultMessageType, ProtoPlusMessageType, Any]
UnaryResponseItemType = Union[DefaultMessageType, ProtoPlusMessageType, Any]


@dataclass
class _UnaryStreamResponseCache:
    """Cache for unary stream responses, holding the initial response object."""
    initial_response_object: Optional[StreamedResponseItemType] = None


class _UnaryStreamWrapper(grpc.Call, grpc.Future):
    """Wraps a gRPC Call object for unary-stream responses to handle potential
    failures during iteration and apply proto-plus conversions.
    """
    _underlay_call: grpc.Call
    _failure_handler: Callable[[grpc.Call], None]
    _exception: Optional[Exception]
    _use_proto_plus: bool
    _cache: _UnaryStreamResponseCache

    def __init__(
        self,
        underlay_call: grpc.Call,
        failure_handler: Callable[[grpc.Call], None],
        use_proto_plus: bool = False,
    ) -> None:
        super().__init__() # grpc.Call and grpc.Future do not require args for __init__
        self._underlay_call = underlay_call
        self._failure_handler = failure_handler
        self._exception = None
        self._use_proto_plus = use_proto_plus
        # Initialize cache to store the first message for logging purposes.
        self._cache = _UnaryStreamResponseCache()

    def initial_metadata(self) -> Optional[Sequence[Tuple[str, Union[str, bytes]]]]:
        return self._underlay_call.initial_metadata()

    def trailing_metadata(self) -> Optional[Sequence[Tuple[str, Union[str, bytes]]]]:
        # BUG: This seems to incorrectly return initial_metadata.
        # Should be: return self._underlay_call.trailing_metadata()
        return self._underlay_call.initial_metadata()

    def code(self) -> Optional[grpc.StatusCode]:
        return self._underlay_call.code()

    def details(self) -> Optional[str]:
        return self._underlay_call.details()

    def debug_error_string(self) -> Optional[str]:
        return self._underlay_call.debug_error_string()

    def cancelled(self) -> bool:
        return self._underlay_call.cancelled()

    def running(self) -> bool:
        return self._underlay_call.running()

    def done(self) -> bool:
        return self._underlay_call.done()

    def result(self, timeout: Optional[float] = None) -> Any:
        # For a stream, result() typically raises an error or is not used.
        # Iteration is the primary way to get data.
        return self._underlay_call.result(timeout=timeout)

    def exception(self, timeout: Optional[float] = None) -> Optional[Union[grpc.RpcError, Exception]]:
        if self._exception:
            return self._exception
        else:
            return self._underlay_call.exception(timeout=timeout)

    def traceback(self, timeout: Optional[float] = None) -> Any: # returns traceback.TracebackException
        return self._underlay_call.traceback(timeout=timeout)

    def add_done_callback(self, fn: Callable[[grpc.Future], T]) -> None:
        # The parameter to the callback `fn` is the Future itself.
        return self._underlay_call.add_done_callback(fn)

    def add_callback(self, callback: Callable[[grpc.Future], Any]) -> None:
        # This method is on grpc.Future. The callback receives the future.
        return self._underlay_call.add_callback(callback) # type: ignore

    def is_active(self) -> bool:
        return self._underlay_call.is_active()

    def time_remaining(self) -> Optional[float]:
        return self._underlay_call.time_remaining()

    def cancel(self) -> bool:
        return self._underlay_call.cancel()

    def __iter__(self) -> Iterator[StreamedResponseItemType]:
        return self

    def __next__(self) -> StreamedResponseItemType:
        try:
            message: Any = next(self._underlay_call)
            if self._cache.initial_response_object is None:
                self._cache.initial_response_object = message

            if self._use_proto_plus:
                return message # type: ignore
            else:
                return util.convert_proto_plus_to_protobuf(message) # type: ignore
        except StopIteration:
            raise
        except Exception as e_call: # Catch exceptions from the underlying call
            try:
                # Attempt to handle the failure using the provided handler
                self._failure_handler(self._underlay_call)
            except Exception as e_handler:
                # If the handler itself raises an exception, store it and re-raise
                self._exception = e_handler
                raise e_handler
            # If failure_handler did not raise, but we are in exception block from next(),
            # it means the original error from next() should be raised or handled.
            # Storing the original call exception if not already handled by failure_handler.
            if not self._exception : self._exception = e_call if isinstance(e_call, grpc.RpcError) else grpc.RpcError(str(e_call)) # Ensure RpcError
            raise self._exception # type: ignore


    def get_cache(self) -> _UnaryStreamResponseCache:
        return self._cache


class _UnaryUnaryWrapper(grpc.Call, grpc.Future):
    """Wraps a gRPC Call object for unary-unary responses to apply proto-plus
    conversions if specified.
    """
    _underlay_call: grpc.Call
    _use_proto_plus: bool
    # _exception is not set or used in this class's current exception() method.
    # If it were intended, it would be: _exception: Optional[grpc.RpcError] = None

    def __init__(self, underlay_call: grpc.Call, use_proto_plus: bool = False) -> None:
        super().__init__()
        self._underlay_call = underlay_call
        self._use_proto_plus = use_proto_plus

    def initial_metadata(self) -> Optional[Sequence[Tuple[str, Union[str, bytes]]]]:
        return self._underlay_call.initial_metadata()

    def trailing_metadata(self) -> Optional[Sequence[Tuple[str, Union[str, bytes]]]]:
        # BUG: This seems to incorrectly return initial_metadata.
        # Should be: return self._underlay_call.trailing_metadata()
        return self._underlay_call.initial_metadata()

    def code(self) -> Optional[grpc.StatusCode]:
        return self._underlay_call.code()

    def details(self) -> Optional[str]:
        return self._underlay_call.details()

    def debug_error_string(self) -> Optional[str]:
        return self._underlay_call.debug_error_string()

    def cancelled(self) -> bool:
        return self._underlay_call.cancelled()

    def running(self) -> bool:
        return self._underlay_call.running()

    def done(self) -> bool:
        return self._underlay_call.done()

    def result(self, timeout: Optional[float] = None) -> UnaryResponseItemType:
        # timeout is not used in the original _underlay_call.result() call here.
        message: Any = self._underlay_call.result(timeout=timeout)
        if self._use_proto_plus:
            return message # type: ignore
        else:
            return util.convert_proto_plus_to_protobuf(message) # type: ignore

    def exception(self, timeout: Optional[float] = None) -> Optional[grpc.RpcError]:
        # The check for self._exception is present in UnaryStreamWrapper,
        # but _exception is not an attribute of _UnaryUnaryWrapper.
        # Annotating based on current implementation:
        return self._underlay_call.exception(timeout=timeout)

    def traceback(self, timeout: Optional[float] = None) -> Any: # returns traceback.TracebackException
        return self._underlay_call.traceback(timeout=timeout)

    def add_done_callback(self, fn: Callable[[grpc.Future], T]) -> None:
        return self._underlay_call.add_done_callback(fn)

    def add_callback(self, callback: Callable[[grpc.Future], Any]) -> None:
        # This method is on grpc.Future. The callback receives the future.
        return self._underlay_call.add_callback(callback) # type: ignore

    def is_active(self) -> bool:
        return self._underlay_call.is_active()

    def time_remaining(self) -> Optional[float]:
        return self._underlay_call.time_remaining()

    def cancel(self) -> bool:
        return self._underlay_call.cancel()

    def __iter__(self) -> Iterator[UnaryResponseItemType]:
        # This implementation for a UnaryCall is unusual.
        # Typically, a unary call returns a single result, not an iterator.
        # However, to match the existing code's structure:
        # It seems to intend to make the wrapper itself iterable, yielding one item.
        # This would require __next__ to be implemented carefully.
        # The original code `return self` or `return util.convert_proto_plus_to_protobuf(self)`
        # is problematic as `self` is not an iterator of messages.
        # A correct way would be to yield the single result.
        # For now, typing based on intent of yielding one message.
        # A more robust implementation might look like:
        # yield self.result()
        # However, the current __next__ calls next(self._underlay_call) which is wrong for unary.
        # Given the __next__ is `next(self._underlay_call)`, this is likely a bug for UnaryUnary.
        # For typing, I will assume it intends to return an iterator of one item.
        # The provided __next__ is more suited for a stream.
        # Let's assume the existing __next__ is what needs to be typed, despite issues.
        return self # This makes it an iterable, __next__ will be called.


    def __next__(self) -> UnaryResponseItemType:
        # This is problematic for a Unary-Unary call.
        # next(self._underlay_call) implies _underlay_call is an iterator,
        # which is true for streaming calls but not for unary calls after completion.
        # A unary call's result should be obtained via self._underlay_call.result().
        # Annotating current code, but this is likely a bug.
        message: Any = next(self._underlay_call) # This will likely fail for a completed unary call.
        if self._use_proto_plus:
            return message # type: ignore
        else:
            return util.convert_proto_plus_to_protobuf(message) # type: ignore
