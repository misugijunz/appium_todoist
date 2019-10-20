import unittest
import random
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
        self.client = ProjectsClient(self.token)
        
    def test_create_project(self):
        random_no = random.randint(1, 5000)
        project_name = "Project_{}".format(random_no)
        assert_msg = "Generated project name should be same with test case: {}"
        assert_msg = assert_msg.format(project_name)
        params = {
            "name": project_name
        }
        obj = self.client.create(params)
        self.assertEqual(project_name, obj.name,
                         assert_msg)