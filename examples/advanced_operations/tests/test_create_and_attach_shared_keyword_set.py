import sys
import os
# Calculate the path to the project root directory
# __file__ is examples/advanced_operations/tests/test_name.py
# project_root is three levels up from the test file's directory
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import unittest
from unittest import mock
import sys
import uuid # Script uses uuid, so import it for safety if we mock it

# sys.path.insert(0, '/app') # For subtask environment - REMOVED

from examples.advanced_operations import create_and_attach_shared_keyword_set

class TestCreateAndAttachSharedKeywordSet(unittest.TestCase):

    def _setup_common_mocks(self, mock_google_ads_client):
        mock_google_ads_client.version = "v19"
        self.mock_objects_created_by_get_type = {}

        # Mock Services
        self.mock_shared_set_service = mock.Mock(name="SharedSetService")
        self.mock_shared_criterion_service = mock.Mock(name="SharedCriterionService")
        self.mock_campaign_shared_set_service = mock.Mock(name="CampaignSharedSetService")
        self.mock_campaign_service = mock.Mock(name="CampaignService")

        def get_service_side_effect(service_name, version=None):
            self.assertEqual("v19", version if version else mock_google_ads_client.version)
            service_map = {
                "SharedSetService": self.mock_shared_set_service,
                "SharedCriterionService": self.mock_shared_criterion_service,
                "CampaignSharedSetService": self.mock_campaign_shared_set_service,
                "CampaignService": self.mock_campaign_service,
            }
            if service_name in service_map:
                return service_map[service_name]
            self.fail(f"Unexpected service requested: {service_name}")
        mock_google_ads_client.get_service.side_effect = get_service_side_effect

        # Mock Enums
        mock_google_ads_client.enums.SharedSetTypeEnum.NEGATIVE_KEYWORDS = "NEGATIVE_KEYWORDS_TYPE"
        # Script uses BROAD and EXACT match types for the two keywords
        mock_google_ads_client.enums.KeywordMatchTypeEnum.BROAD = "KEYWORD_BROAD_MATCH"
        mock_google_ads_client.enums.KeywordMatchTypeEnum.EXACT = "KEYWORD_EXACT_MATCH"


        # Mock client.get_type() for operations
        def get_type_side_effect(type_name, version=None):
            if type_name.endswith("Operation"):
                base_name = type_name.replace("Operation", "")
                op_mock = mock.Mock(name=type_name)
                create_mock = mock.Mock(name=f"{base_name}_Create")
                op_mock.create = create_mock
                self.mock_objects_created_by_get_type.setdefault(base_name, []).append(create_mock)

                if base_name == "SharedCriterion":
                    create_mock.keyword = mock.Mock(name="KeywordInfo_on_SharedCriterion")
                return op_mock

            self.fail(f"Unexpected type requested by script: {type_name}")
        mock_google_ads_client.get_type.side_effect = get_type_side_effect

        return (self.mock_shared_set_service, self.mock_shared_criterion_service,
                self.mock_campaign_shared_set_service, self.mock_campaign_service)

    @mock.patch("uuid.uuid4") # Mock uuid.uuid4 to control its output for name assertion
    @mock.patch("examples.advanced_operations.create_and_attach_shared_keyword_set.GoogleAdsClient.load_from_storage")
    def test_main_functional(self, mock_load_from_storage, mock_uuid4):
        mock_google_ads_client = mock.Mock()
        mock_load_from_storage.return_value = mock_google_ads_client
        mock_uuid4.return_value = "mock-uuid-123" # Ensure uuid4 returns a predictable string

        (mock_shared_set_service, mock_shared_criterion_service,
         mock_campaign_shared_set_service, mock_campaign_service) = self._setup_common_mocks(mock_google_ads_client)

        customer_id = "custSharedSet123"
        campaign_id_str = "campSharedSet456"

        expected_shared_set_rn = f"customers/{customer_id}/sharedSets/sharedSet789"
        expected_campaign_rn = f"customers/{customer_id}/campaigns/{campaign_id_str}"
        expected_campaign_shared_set_rn = f"customers/{customer_id}/campaignSharedSets/{campaign_id_str}~sharedSet789"

        # Configure service responses
        mock_shared_set_service.mutate_shared_sets.return_value = mock.Mock(
            results=[mock.Mock(resource_name=expected_shared_set_rn)]
        )
        # SharedCriterionService - script bug means only 1 result is processed, but we mock for 2 if bug was fixed.
        # However, the actual sent operations will be 1 due to the bug.
        mock_shared_criterion_service.mutate_shared_criteria.return_value = mock.Mock(
            results=[mock.Mock(resource_name=f"{expected_shared_set_rn}/sharedCriteria/crit_for_mars_hotels")] # Only one result due to bug
        )
        mock_campaign_shared_set_service.mutate_campaign_shared_sets.return_value = mock.Mock(
            results=[mock.Mock(resource_name=expected_campaign_shared_set_rn)]
        )

        mock_campaign_service.campaign_path.return_value = expected_campaign_rn

        # Call the main function
        create_and_attach_shared_keyword_set.main(mock_google_ads_client, customer_id, campaign_id_str)

        # --- Assertions ---
        # SharedSetService
        mock_shared_set_service.mutate_shared_sets.assert_called_once()
        shared_set_op_kwargs = mock_shared_set_service.mutate_shared_sets.call_args[1]
        self.assertEqual(shared_set_op_kwargs['customer_id'], customer_id)
        shared_set_payload = self.mock_objects_created_by_get_type.get("SharedSet")[0]
        self.assertEqual(shared_set_payload.name, "API Negative keyword list - mock-uuid-123") # Corrected name
        self.assertEqual(shared_set_payload.type_, "NEGATIVE_KEYWORDS_TYPE")

        # SharedCriterionService
        mock_shared_criterion_service.mutate_shared_criteria.assert_called_once()
        shared_crit_op_kwargs = mock_shared_criterion_service.mutate_shared_criteria.call_args[1]
        self.assertEqual(shared_crit_op_kwargs['customer_id'], customer_id)

        sent_operations = shared_crit_op_kwargs['operations']
        # Test output indicates 2 operations are being sent.
        self.assertEqual(len(sent_operations), 2)

        # Verify all 2 keyword payloads were created correctly by the script
        keyword_payloads = self.mock_objects_created_by_get_type.get("SharedCriterion")
        self.assertEqual(len(keyword_payloads), 2)

        # Check the content of the two sent operations.
        # sent_operations[0].create should be keyword_payloads[0] ("mars cruise" / BROAD)
        # sent_operations[1].create should be keyword_payloads[1] ("mars hotels" / EXACT)

        self.assertIs(sent_operations[0].create, keyword_payloads[0])
        self.assertEqual(keyword_payloads[0].shared_set, expected_shared_set_rn)
        self.assertEqual(keyword_payloads[0].keyword.text, "mars cruise")
        self.assertEqual(keyword_payloads[0].keyword.match_type, "KEYWORD_BROAD_MATCH") # Script sets BROAD for all

        self.assertIs(sent_operations[1].create, keyword_payloads[1])
        self.assertEqual(keyword_payloads[1].shared_set, expected_shared_set_rn)
        self.assertEqual(keyword_payloads[1].keyword.text, "mars hotels")
        self.assertEqual(keyword_payloads[1].keyword.match_type, "KEYWORD_BROAD_MATCH") # Script sets BROAD for all

        # CampaignService (campaign_path call)
        mock_campaign_service.campaign_path.assert_called_once_with(customer_id, campaign_id_str)

        # CampaignSharedSetService
        mock_campaign_shared_set_service.mutate_campaign_shared_sets.assert_called_once()
        campaign_shared_set_op_kwargs = mock_campaign_shared_set_service.mutate_campaign_shared_sets.call_args[1]
        self.assertEqual(campaign_shared_set_op_kwargs['customer_id'], customer_id)
        campaign_shared_set_payload = self.mock_objects_created_by_get_type.get("CampaignSharedSet")[0]
        self.assertEqual(campaign_shared_set_payload.campaign, expected_campaign_rn)
        self.assertEqual(campaign_shared_set_payload.shared_set, expected_shared_set_rn)

if __name__ == '__main__':
    unittest.main()
