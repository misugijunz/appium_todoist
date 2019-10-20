import unittest
from ..rest_client.clients import ProjectsClient
from .functionals import Functionals

class FunctionalsProject(unittest.TestCase, Functionals):
    
    @staticmethod
    def get_instance(testcase, token, username, password):
        obj = FunctionalsProject(testcase)
        obj.set_token(token)
        obj.set_username(username)
        obj.set_password(password)
        return obj
    
    def setUp(self):
        pass
        
    def test_create_project(self):
        assert(True)