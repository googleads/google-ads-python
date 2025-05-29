import unittest
from unittest import mock
import argparse
import asyncio
import uuid
import sys

# Mock Google Ads Client and Exception if not available in the environment
try:
    from google.ads.googleads.client import GoogleAdsClient
    from google.ads.googleads.errors import GoogleAdsException
    from google.api_core import operation as api_core_operation
except ImportError:
    GoogleAdsClient = mock.MagicMock()
    GoogleAdsException = type('GoogleAdsException', (Exception,), {})
    api_core_operation = mock.MagicMock()
    api_core_operation.Operation = mock.MagicMock()


# Import the module to be tested
# This assumes the script is in the examples.campaign_management package
from examples.campaign_management import add_complete_campaigns_using_batch_job as acct_script

# Helper to reset global temporary ID counter in the script
def reset_temporary_id_counter():
    acct_script._temporary_id = -1

class TestAddCompleteCampaignsUsingBatchJob(unittest.TestCase):

    @mock.patch.object(GoogleAdsClient, "load_from_storage")
    def setUp(self, mock_load_from_storage):
        self.mock_google_ads_client = mock.MagicMock(spec=GoogleAdsClient)
        self.mock_google_ads_client.configure_mock(version="v19") # Ensure version is set
        mock_load_from_storage.return_value = self.mock_google_ads_client

        self.mock_batch_job_service = mock.MagicMock()
        self.mock_campaign_service = mock.MagicMock()
        self.mock_campaign_budget_service = mock.MagicMock()
        self.mock_ad_group_service = mock.MagicMock()
        self.mock_ad_group_ad_service = mock.MagicMock()
        self.mock_ad_group_criterion_service = mock.MagicMock()

        self.mock_google_ads_client.get_service.side_effect = lambda service_name, version="v19": {
            "BatchJobService": self.mock_batch_job_service,
            "CampaignService": self.mock_campaign_service,
            "CampaignBudgetService": self.mock_campaign_budget_service,
            "AdGroupService": self.mock_ad_group_service,
            "AdGroupAdService": self.mock_ad_group_ad_service,
            "AdGroupCriterionService": self.mock_ad_group_criterion_service,
        }.get(service_name)

        # Mock path generation
        self.mock_campaign_budget_service.campaign_budget_path.side_effect = lambda cid, bid: f"customers/{cid}/campaignBudgets/{bid}"
        self.mock_campaign_service.campaign_path.side_effect = lambda cid, camp_id: f"customers/{cid}/campaigns/{camp_id}"
        self.mock_ad_group_service.ad_group_path.side_effect = lambda cid, ag_id: f"customers/{cid}/adGroups/{ag_id}"
        self.mock_ad_group_ad_service.ad_group_ad_path.side_effect = lambda cid, ad_id: f"customers/{cid}/adGroupAds/{ad_id}"
        self.mock_ad_group_criterion_service.ad_group_criterion_path.side_effect = lambda cid, crit_id: f"customers/{cid}/adGroupCriteria/{crit_id}"

        # Mock uuid.uuid4 for predictable IDs
        self.mock_uuid_patcher = mock.patch("uuid.uuid4", return_value=mock.Mock(hex="testuuidhex"))
        self.mock_uuid = self.mock_uuid_patcher.start()

        # Mock asyncio.Event
        self.mock_event_patcher = mock.patch("asyncio.Event")
        self.mock_asyncio_event_class = self.mock_event_patcher.start()
        self.mock_asyncio_event_instance = mock.MagicMock(spec=asyncio.Event)
        self.mock_asyncio_event_instance.wait = mock.AsyncMock() # For async def wait
        self.mock_asyncio_event_class.return_value = self.mock_asyncio_event_instance
        
        # Mock google.api_core.operation.Operation
        self.mock_api_operation_patcher = mock.patch("google.api_core.operation.Operation")
        self.mock_api_operation_class = self.mock_api_operation_patcher.start()
        self.mock_api_operation_instance = mock.MagicMock(spec=api_core_operation.Operation)
        self.mock_api_operation_instance.add_done_callback = mock.MagicMock()
        self.mock_api_operation_instance.done = mock.MagicMock(return_value=False) # Default to not done
        self.mock_batch_job_service.run_batch_job.return_value = self.mock_api_operation_instance
        
        # Reset temporary ID for each test
        reset_temporary_id_counter()

    def tearDown(self):
        self.mock_uuid_patcher.stop()
        self.mock_event_patcher.stop()
        self.mock_api_operation_patcher.stop()
        reset_temporary_id_counter()

    def test_create_batch_job(self):
        mock_mutate_response = mock.MagicMock()
        mock_mutate_response.results[0].resource_name = "customers/123/batchJobs/batch_job_resource_name"
        self.mock_batch_job_service.mutate_batch_job.return_value = mock_mutate_response

        resource_name = acct_script.create_batch_job(self.mock_batch_job_service, "123")
        
        self.mock_batch_job_service.mutate_batch_job.assert_called_once()
        self.assertEqual(resource_name, "customers/123/batchJobs/batch_job_resource_name")

    def test_create_batch_job_exception(self):
        # Create a mock GoogleAdsException instance
        mock_failure = mock.MagicMock()
        mock_error = mock.MagicMock()
        mock_error.message = "Batch job creation failed"
        mock_failure.errors = [mock_error]
        google_ads_exception_instance = GoogleAdsException()
        google_ads_exception_instance._failure = mock_failure
        google_ads_exception_instance.request_id = "test_request_id"


        self.mock_batch_job_service.mutate_batch_job.side_effect = google_ads_exception_instance
        with self.assertRaises(GoogleAdsException):
            acct_script.create_batch_job(self.mock_batch_job_service, "123")

    def test_add_all_batch_job_operations(self):
        mock_operations = [mock.MagicMock(), mock.MagicMock()]
        batch_job_resource_name = "customers/123/batchJobs/test_job"
        
        self.mock_batch_job_service.add_batch_job_operations.return_value = mock.MagicMock(
            total_operations=2,
            next_sequence_token="next_token"
        )

        acct_script.add_all_batch_job_operations(
            self.mock_batch_job_service,
            mock_operations,
            batch_job_resource_name
        )
        self.mock_batch_job_service.add_batch_job_operations.assert_called_once_with(
            resource_name=batch_job_resource_name,
            sequence_token=None, # First call
            mutate_operations=mock_operations,
        )

    def test_add_all_batch_job_operations_with_sequence_token(self):
        # Simulate a scenario where not all operations are added in the first call
        mock_operations = [mock.MagicMock()] * (acct_script.MAX_OPERATIONS_PER_REQUEST + 10) # More than max
        batch_job_resource_name = "customers/123/batchJobs/test_job"

        # Mock responses for multiple calls
        self.mock_batch_job_service.add_batch_job_operations.side_effect = [
            mock.MagicMock(total_operations=acct_script.MAX_OPERATIONS_PER_REQUEST, next_sequence_token="token1"),
            mock.MagicMock(total_operations=10, next_sequence_token="token2") # Assuming token2 means done here for simplicity
        ]
        
        acct_script.add_all_batch_job_operations(
            self.mock_batch_job_service,
            mock_operations,
            batch_job_resource_name
        )
        
        self.assertEqual(self.mock_batch_job_service.add_batch_job_operations.call_count, 2)
        first_call_args = self.mock_batch_job_service.add_batch_job_operations.call_args_list[0]
        second_call_args = self.mock_batch_job_service.add_batch_job_operations.call_args_list[1]

        self.assertEqual(first_call_args[1]['sequence_token'], None)
        self.assertEqual(len(first_call_args[1]['mutate_operations']), acct_script.MAX_OPERATIONS_PER_REQUEST)
        self.assertEqual(second_call_args[1]['sequence_token'], "token1")
        self.assertEqual(len(second_call_args[1]['mutate_operations']), 10)


    def test_run_batch_job(self):
        batch_job_resource_name = "customers/123/batchJobs/test_job"
        returned_operation = acct_script.run_batch_job(self.mock_batch_job_service, batch_job_resource_name)
        self.mock_batch_job_service.run_batch_job.assert_called_once_with(resource_name=batch_job_resource_name)
        self.assertEqual(returned_operation, self.mock_api_operation_instance)

    def test_poll_batch_job(self):
        mock_op = self.mock_api_operation_instance
        mock_event = self.mock_asyncio_event_instance
        
        acct_script.poll_batch_job(mock_op, mock_event)
        mock_op.add_done_callback.assert_called_once()
        # The callback itself (set_event) should be tested by checking if event.set() is called
        # when the callback is executed.
        callback_func = mock_op.add_done_callback.call_args[0][0]
        
        # Simulate the operation completing and the callback being called
        self.assertFalse(mock_event.is_set()) # Ensure not set initially
        callback_func(mock_op) # Call the callback
        mock_event.set.assert_called_once() # Assert event was set

    @mock.patch("builtins.print")
    def test_fetch_and_print_results(self, mock_print):
        batch_job_resource_name = "customers/123/batchJobs/test_job"
        mock_result_item = mock.MagicMock()
        mock_result_item.mutate_operation_response.campaign_result.resource_name = "customers/123/campaigns/camp1"
        
        self.mock_batch_job_service.list_batch_job_results.return_value = [mock_result_item]

        acct_script.fetch_and_print_results(self.mock_batch_job_service, batch_job_resource_name)
        
        self.mock_batch_job_service.list_batch_job_results.assert_called_once_with(
            resource_name=batch_job_resource_name, page_size=acct_script.PAGE_SIZE
        )
        mock_print.assert_any_call(
            "\tMutate response for campaign with resource name "
            "'customers/123/campaigns/camp1' found."
        )

    @mock.patch.object(acct_script, "create_batch_job_operation")
    @mock.patch.object(acct_script, "build_all_operations")
    @mock.patch.object(acct_script, "add_all_batch_job_operations")
    @mock.patch.object(acct_script, "run_batch_job")
    @mock.patch.object(acct_script, "poll_batch_job")
    @mock.patch.object(acct_script, "fetch_and_print_results")
    @mock.patch("asyncio.run") # Mock asyncio.run
    @mock.patch("argparse.ArgumentParser")
    def test_main_flow(
        self, mock_argparse, mock_asyncio_run, mock_fetch, mock_poll,
        mock_run, mock_add_ops, mock_build_ops, mock_create_op
    ):
        customer_id = "1234567890"
        mock_args = argparse.Namespace(customer_id=customer_id)
        mock_argparse.return_value.parse_args.return_value = mock_args
        
        # Mock return values for the flow
        mock_batch_job_op = mock.MagicMock()
        mock_create_op.return_value = mock_batch_job_op # create_batch_job_operation
        
        mock_all_operations = [mock.MagicMock()] * 5 # build_all_operations
        mock_build_ops.return_value = mock_all_operations
        
        mock_lro = self.mock_api_operation_instance # run_batch_job
        mock_run.return_value = mock_lro

        # Simulate the main async function being called by asyncio.run
        async def mock_main_async_logic(*args, **kwargs):
            # This is where the logic of _main_async would run
            # We need to ensure poll_batch_job's event gets set to simulate completion
            # The event is created inside _main_async, so we rely on the class-level mock
            self.mock_asyncio_event_instance.set() # Simulate event being set by the callback
            await self.mock_asyncio_event_instance.wait() # Simulate waiting for it

        mock_asyncio_run.side_effect = lambda coro: asyncio.get_event_loop().run_until_complete(mock_main_async_logic())


        acct_script.main(customer_id)

        mock_create_op.assert_called_once_with(self.mock_google_ads_client, customer_id)
        mock_build_ops.assert_called_once_with(self.mock_google_ads_client, customer_id)
        mock_add_ops.assert_called_once_with(
            self.mock_batch_job_service, # This comes from client.get_service
            mock_batch_job_op.resource_name, # from create_batch_job_operation
            mock_all_operations
        )
        mock_run.assert_called_once_with(
            self.mock_batch_job_service,
            mock_batch_job_op.resource_name
        )
        mock_poll.assert_called_once() # Args are operation and event
        
        # Assert that the event's wait method was awaited
        self.mock_asyncio_event_instance.wait.assert_awaited_once()
        
        mock_fetch.assert_called_once_with(
            self.mock_batch_job_service,
            mock_batch_job_op.resource_name
        )
        
        # Ensure GoogleAdsClient was initialized
        GoogleAdsClient.load_from_storage.assert_called_once()


    @mock.patch.object(acct_script, "get_next_temporary_id")
    def test_build_campaign_budget_operation(self, mock_get_id):
        mock_get_id.return_value = -1
        op = acct_script.build_campaign_budget_operation(self.mock_google_ads_client, "123")
        self.assertIsNotNone(op.campaign_budget_operation.create.resource_name)
        self.assertTrue(op.campaign_budget_operation.create.resource_name.endswith("/-1"))

    @mock.patch.object(acct_script, "get_next_temporary_id")
    def test_build_campaign_operation(self, mock_get_id):
        mock_get_id.return_value = -2 # For campaign
        # budget_resource_name is passed, not generated here
        budget_resource_name = "customers/123/campaignBudgets/-1"
        op = acct_script.build_campaign_operation(self.mock_google_ads_client, "123", budget_resource_name)
        self.assertIsNotNone(op.campaign_operation.create.resource_name)
        self.assertTrue(op.campaign_operation.create.resource_name.endswith("/-2"))
        self.assertEqual(op.campaign_operation.create.campaign_budget, budget_resource_name)

    # Similar tests can be added for:
    # build_ad_group_operation
    # build_ad_group_ad_operation
    # build_keyword_operation

    def test_get_next_temporary_id(self):
        self.assertEqual(acct_script.get_next_temporary_id(), -1)
        self.assertEqual(acct_script.get_next_temporary_id(), -2)
        reset_temporary_id_counter() # Reset for other tests
        self.assertEqual(acct_script.get_next_temporary_id(), -1)


if __name__ == "__main__":
    unittest.main()
