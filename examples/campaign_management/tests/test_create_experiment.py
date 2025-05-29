import unittest
from unittest import mock
import argparse
import uuid
import sys

# Mock Google Ads Client and Exception if not available in the environment
try:
    from google.ads.googleads.client import GoogleAdsClient
    from google.ads.googleads.errors import GoogleAdsException
    from google.protobuf import field_mask_pb2
except ImportError:
    GoogleAdsClient = mock.MagicMock()
    GoogleAdsException = type('GoogleAdsException', (Exception,), {})
    field_mask_pb2 = mock.MagicMock() # Mock FieldMask if protobuf is not available

# Import the module to be tested
from examples.campaign_management import create_experiment as ce_script

class TestCreateExperiment(unittest.TestCase):

    @mock.patch.object(GoogleAdsClient, "load_from_storage")
    def setUp(self, mock_load_from_storage):
        self.mock_google_ads_client = mock.MagicMock(spec=GoogleAdsClient)
        self.mock_google_ads_client.configure_mock(version="v19")
        mock_load_from_storage.return_value = self.mock_google_ads_client

        self.mock_experiment_service = mock.MagicMock()
        self.mock_experiment_arm_service = mock.MagicMock()
        self.mock_campaign_service = mock.MagicMock()

        self.mock_google_ads_client.get_service.side_effect = lambda service_name, version="v19": {
            "ExperimentService": self.mock_experiment_service,
            "ExperimentArmService": self.mock_experiment_arm_service,
            "CampaignService": self.mock_campaign_service,
        }.get(service_name)

        # Mock path generation
        self.mock_experiment_service.experiment_path.side_effect = lambda cid, eid: f"customers/{cid}/experiments/{eid}"
        self.mock_campaign_service.campaign_path.side_effect = lambda cid, camp_id: f"customers/{cid}/campaigns/{camp_id}"
        
        # Mock uuid.uuid4 for predictable naming
        self.mock_uuid_patcher = mock.patch("uuid.uuid4", return_value=mock.Mock(hex="testuuid"))
        self.mock_uuid = self.mock_uuid_patcher.start()

        # Mock get_type for operations and FieldMask
        self.mock_google_ads_client.get_type.side_effect = self._get_type_mock

        # Store created mock objects for assertions if needed by _get_type_mock
        self.mock_experiment_op = mock.MagicMock()
        self.mock_experiment_arm_op = mock.MagicMock()
        self.mock_campaign_op = mock.MagicMock()
        self.mock_field_mask = mock.MagicMock(spec=field_mask_pb2.FieldMask)
        
        # Pre-configure mock FieldMask if possible
        if hasattr(field_mask_pb2, "FieldMask"):
             self.mock_field_mask = field_mask_pb2.FieldMask()


    def _get_type_mock(self, type_name, version=None):
        if type_name == "ExperimentOperation":
            return self.mock_experiment_op
        elif type_name == "ExperimentArmOperation":
            return self.mock_experiment_arm_op
        elif type_name == "CampaignOperation":
            return self.mock_campaign_op
        elif type_name == "FieldMask": # For protobuf_helpers.field_mask utility
            return self.mock_field_mask
        # Add other types if needed by the script
        mock_type = mock.MagicMock()
        mock_type.name = type_name # For debugging
        return mock_type


    def tearDown(self):
        self.mock_uuid_patcher.stop()

    def test_create_experiment_resource(self):
        customer_id = "123"
        mock_mutate_response = mock.MagicMock()
        mock_result = mock.MagicMock()
        mock_result.resource_name = f"customers/{customer_id}/experiments/exp123"
        mock_mutate_response.results = [mock_result]
        self.mock_experiment_service.mutate_experiments.return_value = mock_mutate_response

        # Mock the Experiment object that will be created
        mock_experiment_obj = self.mock_google_ads_client.get_type("Experiment", version="v19")

        experiment_resource_name = ce_script.create_experiment_resource(
            self.mock_google_ads_client, customer_id
        )

        self.mock_experiment_service.mutate_experiments.assert_called_once()
        call_args = self.mock_experiment_service.mutate_experiments.call_args
        self.assertEqual(call_args[1]['customer_id'], customer_id)
        self.assertEqual(len(call_args[1]['operations']), 1)
        # self.assertEqual(call_args[1]['operations'][0], self.mock_experiment_op) # This might be too strict if op is created inside
        
        # Check attributes of the created experiment inside the operation
        created_experiment_in_op = call_args[1]['operations'][0].create
        self.assertTrue(created_experiment_in_op.name.startswith(f"Test Experiment #{self.mock_uuid.hex}"))
        self.assertEqual(created_experiment_in_op.type_, self.mock_google_ads_client.enums.ExperimentTypeEnum.SEARCH_CUSTOM)
        self.assertEqual(created_experiment_in_op.suffix, f"[TEST_{self.mock_uuid.hex[:4]}]")
        self.assertEqual(created_experiment_in_op.status, self.mock_google_ads_client.enums.ExperimentStatusEnum.SETUP)


        self.assertEqual(experiment_resource_name, f"customers/{customer_id}/experiments/exp123")

    def test_create_experiment_arms(self):
        customer_id = "123"
        base_campaign_id = "bcamp1"
        experiment_resource_name = f"customers/{customer_id}/experiments/exp123"
        
        mock_mutate_response = mock.MagicMock()
        # Two results, one for control, one for treatment (draft campaign)
        mock_result_control = mock.MagicMock()
        mock_result_control.resource_name = f"customers/{customer_id}/experimentArms/arm_control"
        mock_result_treatment = mock.MagicMock()
        mock_result_treatment.resource_name = f"customers/{customer_id}/experimentArms/arm_treatment"
        # The draft campaign is part of the treatment arm's response
        mock_result_treatment.treatment_experiment_arm.campaign = f"customers/{customer_id}/campaigns/draft_camp1"
        mock_mutate_response.results = [mock_result_control, mock_result_treatment]
        self.mock_experiment_arm_service.mutate_experiment_arms.return_value = mock_mutate_response

        # Mock ExperimentArm objects
        mock_exp_arm_control = self.mock_google_ads_client.get_type("ExperimentArm", version="v19")
        mock_exp_arm_treatment = self.mock_google_ads_client.get_type("ExperimentArm", version="v19")

        control_arm_name, treatment_arm_name, draft_campaign_rsrc_name = ce_script.create_experiment_arms(
            self.mock_google_ads_client, customer_id, base_campaign_id, experiment_resource_name
        )

        self.mock_campaign_service.campaign_path.assert_called_once_with(customer_id, base_campaign_id)
        
        self.mock_experiment_arm_service.mutate_experiment_arms.assert_called_once()
        call_args = self.mock_experiment_arm_service.mutate_experiment_arms.call_args
        self.assertEqual(call_args[1]['customer_id'], customer_id)
        self.assertEqual(call_args[1]['response_content_type'], self.mock_google_ads_client.enums.ResponseContentTypeEnum.MUTABLE_RESOURCE)
        self.assertEqual(len(call_args[1]['operations']), 2) # Control and Treatment

        # Check control arm details
        control_op_create = call_args[1]['operations'][0].create
        self.assertEqual(control_op_create.experiment, experiment_resource_name)
        self.assertEqual(control_op_create.name, "control_arm")
        self.assertEqual(control_op_create.control, True)
        self.assertEqual(control_op_create.traffic_split, 50)
        self.assertEqual(len(control_op_create.campaigns), 1)
        self.assertEqual(control_op_create.campaigns[0], f"customers/{customer_id}/campaigns/{base_campaign_id}")

        # Check treatment arm details
        treatment_op_create = call_args[1]['operations'][1].create
        self.assertEqual(treatment_op_create.experiment, experiment_resource_name)
        self.assertEqual(treatment_op_create.name, "treatment_arm")
        self.assertEqual(treatment_op_create.control, False)
        self.assertEqual(treatment_op_create.traffic_split, 50)
        self.assertEqual(len(treatment_op_create.campaigns), 1) # Initially empty, draft created by API
        self.assertTrue(treatment_op_create.name.startswith("treatment_arm"))


        self.assertEqual(draft_campaign_rsrc_name, f"customers/{customer_id}/campaigns/draft_camp1")
        self.assertEqual(control_arm_name, f"customers/{customer_id}/experimentArms/arm_control")
        self.assertEqual(treatment_arm_name, f"customers/{customer_id}/experimentArms/arm_treatment")


    @mock.patch("google.protobuf.field_mask_pb2.FieldMask")
    def test_modify_draft_campaign(self, mock_field_mask_constructor):
        customer_id = "123"
        draft_campaign_resource_name = f"customers/{customer_id}/campaigns/draft_camp1"
        
        mock_field_mask_instance = self.mock_field_mask # Use the one from setUp
        mock_field_mask_constructor.return_value = mock_field_mask_instance
        
        mock_mutate_response = mock.MagicMock()
        self.mock_campaign_service.mutate_campaigns.return_value = mock_mutate_response

        # Mock Campaign object for the update
        mock_campaign_obj = self.mock_google_ads_client.get_type("Campaign", version="v19")

        ce_script.modify_draft_campaign(
            self.mock_google_ads_client, customer_id, draft_campaign_resource_name
        )

        self.mock_campaign_service.mutate_campaigns.assert_called_once()
        call_args = self.mock_campaign_service.mutate_campaigns.call_args
        self.assertEqual(call_args[1]['customer_id'], customer_id)
        self.assertEqual(len(call_args[1]['operations']), 1)
        
        campaign_op = call_args[1]['operations'][0]
        self.assertEqual(campaign_op.update.resource_name, draft_campaign_resource_name)
        self.assertTrue(campaign_op.update.name.endswith(f"_modified_{self.mock_uuid.hex[:4]}"))
        
        # Check that FieldMask was called with "name"
        # This depends on how protobuf_helpers.field_mask works or if it's used.
        # If it's directly field_mask_pb2.FieldMask(paths=["name"]), then mock_field_mask_constructor
        # would have paths=["name"]
        # For a direct mock, we check if paths was set on the instance.
        if hasattr(self.mock_field_mask, "paths"): # If it's a real FieldMask or a good mock
            self.assertIn("name", self.mock_field_mask.paths)
        else: # Fallback if it's a generic MagicMock
            mock_field_mask_constructor.assert_called_once_with(paths=["name"])


    @mock.patch.object(ce_script, "create_experiment_resource")
    @mock.patch.object(ce_script, "create_experiment_arms")
    @mock.patch.object(ce_script, "modify_draft_campaign")
    @mock.patch("argparse.ArgumentParser")
    @mock.patch("builtins.print") # To suppress print statements if any
    def test_main_flow(
        self, mock_print, mock_argparse, mock_modify_draft, mock_create_arms, mock_create_exp
    ):
        customer_id = "123"
        base_campaign_id = "bcamp1"
        mock_args = argparse.Namespace(customer_id=customer_id, base_campaign_id=base_campaign_id)
        mock_argparse.return_value.parse_args.return_value = mock_args

        # Mock return values
        exp_resource_name = f"customers/{customer_id}/experiments/exp1"
        mock_create_exp.return_value = exp_resource_name
        
        control_arm_rsrc = f"customers/{customer_id}/experimentArms/ctrl1"
        treatment_arm_rsrc = f"customers/{customer_id}/experimentArms/treat1"
        draft_camp_rsrc = f"customers/{customer_id}/campaigns/draft1"
        mock_create_arms.return_value = (control_arm_rsrc, treatment_arm_rsrc, draft_camp_rsrc)

        ce_script.main(self.mock_google_ads_client, customer_id, base_campaign_id)

        mock_create_exp.assert_called_once_with(self.mock_google_ads_client, customer_id)
        mock_create_arms.assert_called_once_with(
            self.mock_google_ads_client, customer_id, base_campaign_id, exp_resource_name
        )
        mock_modify_draft.assert_called_once_with(
            self.mock_google_ads_client, customer_id, draft_camp_rsrc
        )
        self.mock_experiment_service.schedule_experiment.assert_called_once_with(
            resource_name=exp_resource_name
        )
        mock_print.assert_any_call(f"Experiment {exp_resource_name} with draft campaign {draft_camp_rsrc} scheduled.")


    @mock.patch("argparse.ArgumentParser")
    @mock.patch("builtins.print")
    @mock.patch("sys.exit")
    def test_main_exception_handling(self, mock_sys_exit, mock_print, mock_argparse):
        customer_id = "123"
        base_campaign_id = "bcamp1"
        mock_args = argparse.Namespace(customer_id=customer_id, base_campaign_id=base_campaign_id)
        mock_argparse.return_value.parse_args.return_value = mock_args

        # Create a mock GoogleAdsException instance
        mock_failure = mock.MagicMock()
        mock_error = mock.MagicMock()
        mock_error.message = "Test API error"
        mock_failure.errors = [mock_error]
        google_ads_exception_instance = GoogleAdsException()
        google_ads_exception_instance._failure = mock_failure
        google_ads_exception_instance.request_id = "test_req_id"

        # Make one of the core functions raise the exception
        self.mock_experiment_service.mutate_experiments.side_effect = google_ads_exception_instance
        
        # We need to call the actual main function of the script, not the mocked one in test_main_flow
        # The script's main calls GoogleAdsClient.load_from_storage, which is already mocked in setUp
        
        # We are testing the main function in ce_script
        ce_script.main(self.mock_google_ads_client, customer_id, base_campaign_id)

        # Check that error was printed
        printed_error = False
        for call in mock_print.call_args_list:
            if "Test API error" in str(call[0]):
                printed_error = True
                break
        self.assertTrue(printed_error, "GoogleAdsException error message was not printed.")
        mock_sys_exit.assert_called_once_with(1)


if __name__ == "__main__":
    unittest.main()
