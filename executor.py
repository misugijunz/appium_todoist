import argparse
import unittest
from coverage.tests.functionals import FunctionalsUtil
from coverage.configs import TEST_CASES

parser = argparse.ArgumentParser(description='Process test with options.')
parser.add_argument('--token', required=True)
parser.add_argument('--module',
                    help='Function module to be tested eg: Projects',
                    default='projects')
parser.add_argument('--email',
                    help='email to log in to app', required=True)
parser.add_argument('--password',
                    help='email to log in to app', required=True)
parsed_obj = parser.parse_args()

if __name__ == '__main__':
    test_module = parsed_obj.module.lower()
    test_cases = TEST_CASES[test_module]
    test_suite = FunctionalsUtil.get_test_suite(test_module, test_cases,
                                                parsed_obj.token,
                                                parsed_obj.username,
                                                parsed_obj.password)
    runner = unittest.TextTestRunner()
    runner(test_suite)