"""
Run all tests for the Drug Tariff Master application.
"""
import unittest
import sys
from pathlib import Path


if __name__ == "__main__":
    # Discover and run all tests
    loader = unittest.TestLoader()
    start_dir = Path(__file__).resolve().parent
    suite = loader.discover(start_dir)

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Exit with non-zero code if tests failed
    sys.exit(not result.wasSuccessful()) 