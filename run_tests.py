import os
import sys
import unittest

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def run_tests():
    """Run all tests in the tests directory"""
    # Find all test modules in the tests directory
    test_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tests')
    test_modules = [f[:-3] for f in os.listdir(test_dir) if f.startswith('test_') and f.endswith('.py')]
    
    # Create a test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all tests to the suite
    for module_name in test_modules:
        module_path = f'tests.{module_name}'
        try:
            module = __import__(module_path, fromlist=['*'])
            suite.addTests(loader.loadTestsFromModule(module))
        except ImportError as e:
            print(f"Error importing {module_path}: {e}")
    
    # Run the tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Return True if all tests passed, False otherwise
    return result.wasSuccessful()

if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1) 