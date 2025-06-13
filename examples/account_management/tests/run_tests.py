#!/usr/bin/env python
import unittest
import sys
import os

if __name__ == "__main__":
    # Get the directory of the current script
    current_script_dir = os.path.dirname(os.path.abspath(__file__))
    # Calculate the path to the repository root (three levels up from examples/account_management/tests)
    repo_root = os.path.abspath(os.path.join(current_script_dir, "..", "..", ".."))

    # Add the repository root to sys.path to allow imports like 'from examples....'
    if repo_root not in sys.path:
        sys.path.insert(0, repo_root)

    # Create a TestLoader instance
    loader = unittest.TestLoader()

    # Discover all tests in the current directory ('.')
    # Test files should match the pattern 'test_*.py'.
    suite = loader.discover(start_dir='.', pattern='test_*.py')

    # Create a TextTestRunner instance
    # verbosity=2 provides more detailed output
    runner = unittest.TextTestRunner(verbosity=2)

    # Run the tests
    result = runner.run(suite)

    # Exit with an appropriate status code
    # result.wasSuccessful() returns True if all tests passed
    if result.wasSuccessful():
        sys.exit(0)
    else:
        sys.exit(1)
