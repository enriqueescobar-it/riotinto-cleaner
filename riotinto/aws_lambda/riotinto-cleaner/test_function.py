"""
    :module_name: test_function
    :module_summary: tests for the function implementation
    :module_author: Enrique Escobar
"""

import unittest
from function import lambda_handler

class TestLambdaFunction(unittest.TestCase):
    def test_lambda_handler(self):
        event = {}
        context = None
        response = lambda_handler(event, context)
        self.assertEqual(response['statusCode'], 200)
        self.assertIn('Hello from Lambda', response['body'])


if __name__ == '__main__':
    unittest.main()

