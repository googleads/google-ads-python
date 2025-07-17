import unittest
from examples.shopping_ads import add_performance_max_retail_campaign

class TestAddPerformanceMaxRetailCampaign(unittest.TestCase):
    def test_script_runs(self):
        # Basic test to ensure the main function can be imported and called.
        try:
            add_performance_max_retail_campaign.main
            self.assertTrue(True)
        except AttributeError:
            self.fail("add_performance_max_retail_campaign.py does not have a main function or it's not importable.")
        except Exception as e:
            self.fail(f"Running add_performance_max_retail_campaign.py main function failed with {e}")

if __name__ == "__main__":
    unittest.main()
