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
"""Tests for upload_enhanced_conversions_for_web example."""

import io
import unittest
from unittest import mock

from examples.remarketing import upload_enhanced_conversions_for_web
from google.ads.googleads.client import GoogleAdsClient

# Precomputed UTF-8 SHA-256 hex digests for normalized test vectors.
SHA256_MARY_JANE = (
    "e3a62fcabda79e1b70db99ef77d0e0af36d27e3c48bce714fac085d5058d945a"
)
SHA256_MARYJANE_NO_SPACE = (
    "f08f448a5e7a9dc3619bb7c129f6a7d5fc6af002cea17ad71dfdc1c68f4d4e0e"
)
SHA256_DE_LA_CRUZ = (
    "341a715580af4bbc3c3bff363245177e84fbc38c4a77d3047edeb6bee38495aa"
)
SHA256_PHONE_E164 = (
    "c5383c2eeada28210d27f011bc127d4f9562cf38ff0c9bba33dd45ae79b9fe7c"
)
SHA256_ALEX2_GMAIL = (
    "3663dbed96fe29729d2e1ba646b09559bb3dec9c73124bb70a3bea135ee5546b"
)
SHA256_JANEDOE_GOOGLEMAIL = (
    "338abf9ef1c8793cadc7bcf51ed595338eb727ed9e06ce3d91d566d60b975937"
)
SHA256_NON_GMAIL = (
    "f109a2a632fbcea5fc82049f50beed3d8621bf9034399f437fb622222acccdac"
)
SHA256_GMAIL_COM_AU = (
    "c29fe01237251dc9819c62998ab22afa6ddb5561a92cc2f7532689c906857c46"
)
SHA256_SUB_GMAIL = (
    "ac235b1865e9771f525d8cf77753255f5b9b64a5e4d02cb1722534251da9e505"
)
SHA256_MULTI_AT = (
    "6f877fa31df550e08b64aba5566f94167dd7c50df37ed6e33e389b9ee7f62c80"
)
SHA256_NO_AT = (
    "a2598686ba7440dd1a92f18ab059cae1ff50982200a9350636b2bc8927398fbc"
)
SHA256_ALEX = "4135aa9dc1b842a653dea846903ddb95bfb8c5a10c504a7fa16e10bc31d1fdf0"
SHA256_QUINN = (
    "c512ca0c5c1e71be19f3356821e56732b5fb3ac894b0dbc5846d0b6920106fb3"
)


class TestUploadEnhancedConversionsForWeb(unittest.TestCase):
    """Tests for normalization helpers and main flow in web example."""

    def _create_client_with_mock_services(
        self, conversion_action_service, adjustment_upload_service
    ):
        client = GoogleAdsClient(
            credentials=mock.MagicMock(),
            use_proto_plus=True,
        )

        def get_service_side_effect(name):
            if name == "ConversionActionService":
                return conversion_action_service
            if name == "ConversionAdjustmentUploadService":
                return adjustment_upload_service
            raise AssertionError(f"Unexpected service requested: {name}")

        client.get_service = mock.MagicMock(side_effect=get_service_side_effect)
        return client

    def test_normalize_and_hash_preserves_internal_spaces_for_multiword_names(
        self,
    ):
        result_first = upload_enhanced_conversions_for_web.normalize_and_hash(
            "  Mary Jane  "
        )
        result_last = upload_enhanced_conversions_for_web.normalize_and_hash(
            "  De La Cruz\t"
        )

        self.assertEqual(result_first, SHA256_MARY_JANE)
        self.assertNotEqual(result_first, SHA256_MARYJANE_NO_SPACE)
        self.assertEqual(result_last, SHA256_DE_LA_CRUZ)

    def test_normalize_and_hash_removes_all_whitespace_when_requested(self):
        result = upload_enhanced_conversions_for_web.normalize_and_hash(
            " +1 800\t5550102\n", remove_all_whitespace=True
        )

        self.assertEqual(result, SHA256_PHONE_E164)

    def test_normalize_and_hash_email_strips_dots_and_plus_for_gmail_domains(
        self,
    ):
        gmail_hash = upload_enhanced_conversions_for_web.normalize_and_hash_email_address(
            "  Alex.2+MyAlias@Gmail.com "
        )
        googlemail_hash = upload_enhanced_conversions_for_web.normalize_and_hash_email_address(
            "Jane.Doe+Shopping+Extra@GOOGLEMAIL.COM"
        )

        self.assertEqual(gmail_hash, SHA256_ALEX2_GMAIL)
        self.assertEqual(googlemail_hash, SHA256_JANEDOE_GOOGLEMAIL)

    def test_normalize_and_hash_email_strips_spaces_around_at_before_matching(
        self,
    ):
        space_before_at = upload_enhanced_conversions_for_web.normalize_and_hash_email_address(
            "alex.2+tag @gmail.com"
        )
        space_after_at = upload_enhanced_conversions_for_web.normalize_and_hash_email_address(
            "alex.2+tag@ gmail.com"
        )

        self.assertEqual(space_before_at, SHA256_ALEX2_GMAIL)
        self.assertEqual(space_after_at, SHA256_ALEX2_GMAIL)

    def test_normalize_and_hash_email_preserves_dots_and_plus_for_other_domains(
        self,
    ):
        example_hash = upload_enhanced_conversions_for_web.normalize_and_hash_email_address(
            "user.name+NYC@Example.com"
        )
        cc_tld_hash = upload_enhanced_conversions_for_web.normalize_and_hash_email_address(
            "alex.2+tag@gmail.com.au"
        )
        subdomain_hash = upload_enhanced_conversions_for_web.normalize_and_hash_email_address(
            "alex.2+tag@sub.gmail.com"
        )

        self.assertEqual(example_hash, SHA256_NON_GMAIL)
        self.assertEqual(cc_tld_hash, SHA256_GMAIL_COM_AU)
        self.assertEqual(subdomain_hash, SHA256_SUB_GMAIL)

    def test_normalize_and_hash_email_skips_gmail_rules_on_invalid_at_count(
        self,
    ):
        multi_at_hash = upload_enhanced_conversions_for_web.normalize_and_hash_email_address(
            "alex.2+tag@gmail.com@example.com"
        )
        no_at_hash = upload_enhanced_conversions_for_web.normalize_and_hash_email_address(
            "alex.2+tag"
        )

        self.assertEqual(multi_at_hash, SHA256_MULTI_AT)
        self.assertEqual(no_at_hash, SHA256_NO_AT)

    @mock.patch(
        "examples.remarketing.upload_enhanced_conversions_for_web.normalize_and_hash",
        wraps=upload_enhanced_conversions_for_web.normalize_and_hash,
    )
    def test_main_uploads_enhancement_and_preserves_name_whitespace_mode(
        self, spy_normalize_and_hash
    ):
        mock_conversion_action_service = mock.MagicMock()
        mock_conversion_action_service.conversion_action_path.return_value = (
            "customers/1234567890/conversionActions/456"
        )
        mock_adjustment_service = mock.MagicMock()
        client = self._create_client_with_mock_services(
            mock_conversion_action_service, mock_adjustment_service
        )

        result_entry = client.get_type("ConversionAdjustmentResult")
        result_entry.conversion_action = (
            "customers/1234567890/conversionActions/456"
        )
        result_entry.order_id = "order-789"
        mock_adjustment_service.upload_conversion_adjustments.return_value = (
            mock.MagicMock(partial_failure_error=None, results=[result_entry])
        )

        stdout = io.StringIO()
        with mock.patch("sys.stdout", stdout):
            upload_enhanced_conversions_for_web.main(
                client=client,
                customer_id="1234567890",
                conversion_action_id="456",
                order_id="order-789",
                conversion_date_time="2026-06-01 12:32:45-08:00",
                user_agent="Mozilla/5.0",
            )

        mock_adjustment_service.upload_conversion_adjustments.assert_called_once()
        call_kwargs = (
            mock_adjustment_service.upload_conversion_adjustments.call_args.kwargs
        )
        self.assertEqual(call_kwargs["customer_id"], "1234567890")
        self.assertTrue(call_kwargs["partial_failure"])
        self.assertEqual(len(call_kwargs["conversion_adjustments"]), 1)

        adjustment = call_kwargs["conversion_adjustments"][0]
        self.assertEqual(
            adjustment.adjustment_type,
            client.enums.ConversionAdjustmentTypeEnum.ENHANCEMENT,
        )
        self.assertEqual(
            adjustment.conversion_action,
            "customers/1234567890/conversionActions/456",
        )
        self.assertEqual(adjustment.order_id, "order-789")
        self.assertEqual(
            adjustment.gclid_date_time_pair.conversion_date_time,
            "2026-06-01 12:32:45-08:00",
        )
        self.assertEqual(adjustment.user_agent, "Mozilla/5.0")

        self.assertEqual(len(adjustment.user_identifiers), 3)
        email_id, phone_id, address_id = adjustment.user_identifiers
        self.assertEqual(
            email_id.user_identifier_source,
            client.enums.UserIdentifierSourceEnum.FIRST_PARTY,
        )
        self.assertEqual(email_id.hashed_email, SHA256_ALEX2_GMAIL)
        self.assertEqual(phone_id.hashed_phone_number, SHA256_PHONE_E164)
        self.assertEqual(address_id.address_info.hashed_first_name, SHA256_ALEX)
        self.assertEqual(address_id.address_info.hashed_last_name, SHA256_QUINN)
        self.assertEqual(address_id.address_info.country_code, "US")
        self.assertEqual(address_id.address_info.postal_code, "94045")

        spy_normalize_and_hash.assert_any_call(
            "+1 800 5550102", remove_all_whitespace=True
        )
        spy_normalize_and_hash.assert_any_call("Alex")
        spy_normalize_and_hash.assert_any_call("Quinn")

        self.assertEqual(
            stdout.getvalue().strip(),
            "Uploaded conversion adjustment of "
            "customers/1234567890/conversionActions/456 for order ID order-789.",
        )

    def test_main_prints_partial_failure_error(self):
        mock_conversion_action_service = mock.MagicMock()
        mock_conversion_action_service.conversion_action_path.return_value = (
            "customers/1234567890/conversionActions/456"
        )
        mock_adjustment_service = mock.MagicMock()
        client = self._create_client_with_mock_services(
            mock_conversion_action_service, mock_adjustment_service
        )

        response = client.get_type("UploadConversionAdjustmentsResponse")
        response.partial_failure_error.code = 3
        response.partial_failure_error.message = "Invalid order ID."
        mock_adjustment_service.upload_conversion_adjustments.return_value = (
            response
        )

        stdout = io.StringIO()
        with mock.patch("sys.stdout", stdout):
            upload_enhanced_conversions_for_web.main(
                client=client,
                customer_id="1234567890",
                conversion_action_id="456",
                order_id="bad-order",
                conversion_date_time=None,
                user_agent=None,
            )

        self.assertEqual(
            stdout.getvalue().strip(),
            "Partial error encountered: Invalid order ID.",
        )


if __name__ == "__main__":
    unittest.main()
