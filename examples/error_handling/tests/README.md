# Tests for Error Handling Examples

This directory contains unit tests for the Python examples in the `examples/error_handling` directory.

## Prerequisites

Ensure you have Python installed. It's recommended to use a virtual environment.

## Installation

1.  Navigate to the `examples/error_handling/tests` directory:
    ```bash
    cd examples/error_handling/tests
    ```
2.  Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```
    (If you are in the parent `examples/error_handling` directory, you can also run `pip install -r tests/requirements.txt`)

## Running Tests

To run all tests in this directory, navigate to the root of the repository (the directory containing the `examples` folder) and run the following command:

```bash
python -m unittest discover -s examples/error_handling/tests -p "test_*.py"
```

Alternatively, you can run individual test files. For example, to run tests for `handle_keyword_policy_violations.py`:

1.  Navigate to the root of the repository.
2.  Run:
    ```bash
    python -m unittest examples.error_handling.tests.test_handle_keyword_policy_violations
    ```

This will execute the test cases defined in `test_handle_keyword_policy_violations.py`.
