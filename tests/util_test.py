# Copyright 2019 Google LLC
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
"""Tests for the Google Ads API client library utilities."""


from importlib import import_module
from unittest import TestCase

from google.protobuf.message import Message as ProtobufMessageType
import proto

from fixtures.protobuf_fixture_pb2 import ProtobufFixture
from fixtures.proto_plus_fixture import ProtoPlusFixture
from google.ads.googleads import util
from google.ads.googleads import client

default_version = client._DEFAULT_VERSION

feed_module = import_module(
    f"google.ads.googleads.{default_version}.resources.types.feed"
)


class ConvertStringTest(TestCase):
    def test_convert_upper_case_to_snake_case(self):
        string = "GoogleAdsServiceClientTransport"
        expected = "google_ads_service_client_transport"
        result = util.convert_upper_case_to_snake_case(string)
        self.assertEqual(result, expected)

    def test_convert_snake_case_to_upper_case(self):
        string = "google_ads_service_client_transport"
        expected = "GoogleAdsServiceClientTransport"
        result = util.convert_snake_case_to_upper_case(string)
        self.assertEqual(result, expected)


class SetNestedMessageFieldTest(TestCase):
    def test_set_nested_message_field(self):
        val = "test value"
        feed = feed_module.Feed()
        util.set_nested_message_field(
            feed, "places_location_feed_data.email_address", val
        )
        self.assertEqual(feed.places_location_feed_data.email_address, val)


class GetNestedMessageFieldTest(TestCase):
    def test_get_nested_message_field(self):
        val = "test value"
        feed = feed_module.Feed()
        feed.places_location_feed_data.email_address = val
        self.assertEqual(
            util.get_nested_attr(
                feed, "places_location_feed_data.email_address"
            ),
            val,
        )


class ConvertProtoPlusToProtobufTest(TestCase):
    def test_convert_proto_plus_to_protobuf(self):
        """A proto_plus proto is converted to a protobuf one."""
        proto_plus = ProtoPlusFixture()
        converted = util.convert_proto_plus_to_protobuf(proto_plus)
        # Assert that the converted proto is an instance of the protobuf
        # protobuf message class.
        self.assertIsInstance(converted, ProtobufMessageType)

    def test_convert_proto_plus_to_protobuf_if_protobuf(self):
        """If a protobuf proto is given then it is returned to the caller."""
        protobuf = ProtobufFixture()
        converted = util.convert_proto_plus_to_protobuf(protobuf)
        self.assertEqual(protobuf, converted)

    def test_proto_plus_to_protobuf_raises_type_error(self):
        """Method raises TypeError if not given a proto_plus proto."""
        wrong_type = dict()
        self.assertRaises(
            TypeError, util.convert_proto_plus_to_protobuf, wrong_type
        )


class ConvertProtobufToProtoPlusTest(TestCase):
    def test_convert_protobuf_to_proto_plus(self):
        """A protobuf proto is converted to a proto_plus one."""
        protobuf = ProtobufFixture()
        converted = util.convert_protobuf_to_proto_plus(protobuf)
        # Assert that the converted proto is an instance of the Message
        # wrapper class.
        self.assertIsInstance(converted, proto.Message)

    def test_convert_protobuf_to_proto_plus_if_proto_plus(self):
        """If a protobuf proto is given then it is returned to the caller."""
        proto_plus = ProtoPlusFixture()
        converted = util.convert_protobuf_to_proto_plus(proto_plus)
        self.assertEqual(proto_plus, converted)

    def test_raises_type_error(self):
        """Method raises TypeError if not given a protobuf proto."""
        wrong_type = dict()
        self.assertRaises(
            TypeError, util.convert_protobuf_to_proto_plus, wrong_type
        )


class ProtoCopyFromTest(TestCase):
    def test_client_copy_from_both_proto_plus(self):
        """util.proto_copy_from works with two proto_plus proto messages."""
        destination = ProtoPlusFixture()
        origin = ProtoPlusFixture()
        origin.name = "Test"

        util.proto_copy_from(destination, origin)

        self.assertEqual(destination.name, "Test")
        self.assertIsNot(destination, origin)

    def test_client_copy_from_both_protobuf(self):
        """util.proto_copy_from works with two protobuf proto messages."""
        destination = ProtobufFixture()
        origin = ProtobufFixture()
        origin.name = "Test"

        util.proto_copy_from(destination, origin)

        self.assertEqual(destination.name, "Test")
        self.assertIsNot(destination, origin)

    def test_client_copy_from_protobuf_origin(self):
        """util.proto_copy_from works with a proto_plus dest and a protobuf origin."""
        destination = ProtoPlusFixture()
        origin = ProtoPlusFixture()
        origin = type(origin).pb(origin)
        origin.name = "Test"

        util.proto_copy_from(destination, origin)

        self.assertEqual(destination.name, "Test")
        self.assertIsNot(destination, origin)

    def test_client_copy_from_protobuf_destination(self):
        """util.proto_copy_from works with a protobuf dest and a proto_plus origin."""
        destination = ProtoPlusFixture()
        destination = type(destination).pb(destination)
        origin = ProtoPlusFixture()
        origin.name = "Test"

        util.proto_copy_from(destination, origin)

        self.assertEqual(destination.name, "Test")
        self.assertIsNot(destination, origin)

    def test_client_copy_from_different_types_proto_plus(self):
        """TypeError is raised with different types of proto_plus messasges."""
        destination = ProtobufFixture()
        destination = proto.Message.wrap(destination)
        origin = ProtoPlusFixture()
        origin.name = "Test"

        self.assertRaises(TypeError, util.proto_copy_from, destination, origin)

    def test_client_copy_from_different_types_protobuf(self):
        """TypeError is raised with different types of protobuf messasges."""
        destination = ProtoPlusFixture()
        destination = type(destination).pb(destination)
        origin = ProtobufFixture()
        origin.name = "Test"

        self.assertRaises(TypeError, util.proto_copy_from, destination, origin)

    def test_client_copy_from_different_types_protobuf_origin(self):
        """TypeError is raised with different types and protobuf origin."""
        destination = ProtoPlusFixture()
        origin = ProtobufFixture()
        origin.name = "Test"

        self.assertRaises(TypeError, util.proto_copy_from, destination, origin)

    def test_client_copy_from_non_proto_message(self):
        """ValueError is raised if an object other than a protobuf is given"""
        destination = ProtoPlusFixture()
        origin = {"name": "Test"}

        self.assertRaises(ValueError, util.proto_copy_from, destination, origin)
