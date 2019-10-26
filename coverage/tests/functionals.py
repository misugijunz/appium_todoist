import unittest
import importlib
class Functionals():

    """It is a main parent class for tests.
    
    The class defines default behaviour of automation tests
    """

    def set_token(self, token):
        """Set token for test
        
        Set generated auth token for REST http calls to endpoint
        
        :param token: auth token provided by todois
        :type token: string
        """
        self.token = token
    
    def set_username(self, username):
        """Set username for the test
        
        Username will be used to login to the app
        
        :param username: provide username to login to the app
        :type username: string
        """
        self.username = username
        
    def set_password(self, password):
        """Set password for the test
        
        Password will be used to login to the app
        
        :param password: provide password to login to the app
        :type password: string
        """
        self.password = password

class FunctionalsUtil():
    
    """A class holder of utility methods for testware
    
    Provide static convenience methods to help various scenarios of tests
    """
    
    @staticmethod
    def get_test_suite(module_name, test_cases, token,
                       username, password):
        """Returning testsuite of unittest
        
        Create test suite based on provided module_name from testware.
        
        :param module_name: module under test
        :param test_cases: test cases list of this module
        :param token: token to auth the API call
        :param username: username used for login
        :param password: password used for login
        :type module_name: string
        :type test_cases: list
        :type token: string
        :type username: string
        :type password: string
        :return: TestSuite for supplied module & test cases
        :rtype: unittest.TestSuite
        """
        python_module_name = "functionals_task"
        class_name = "FunctionalsTask"
        if module_name.lower() == "projects":
            python_module_name = "functionals_project"
            class_name = "FunctionalsProject"
        module = __import__(python_module_name,
                            globals={"__name__": __name__})
        obj = getattr(module, class_name)
        suite = unittest.TestSuite()
        for test_case in test_cases:
            test = obj.get_instance(test_case, token, username, password)
            suite.addTest(test)
        return suite
       