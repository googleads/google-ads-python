# Tests for Billing Examples

This directory contains unit tests for the Python scripts in the `examples/billing` directory.

## Running the Tests

To run all tests in this directory, navigate to the root of the repository and run:

```bash
python -m unittest discover -s examples/billing/tests -p "test_*.py"
```

Ensure you have the Google Ads API client library installed and any necessary configurations for it if you were to run the examples themselves. For the tests, the Google Ads API is mocked, so no live calls are made.
