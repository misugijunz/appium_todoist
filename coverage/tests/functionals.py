import unittest
import importlib
class Functionals():
    def set_token(self, token):
        self.token = token
    
    def set_username(self, username):
        self.username = username
        
    def set_password(self, password):
        self.password = password

class FunctionalsUtil():
    
    @staticmethod
    def get_test_suite(module_name, test_cases, token,
                       username, password):
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
        
        