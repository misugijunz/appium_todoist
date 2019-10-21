import unittest
import os
import copy
import sys
import random
from ..rest_client.clients import ProjectsClient
from ..helpers import ANDROID_BASE_CAPS, EXECUTOR
from .functionals import Functionals

from time import sleep
from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction
from selenium.common.exceptions import NoSuchElementException

class FunctionalsProject(unittest.TestCase, Functionals):
    
    @staticmethod
    def get_instance(testcase, token, username, password):
        obj = FunctionalsProject(testcase)
        obj.set_token(token)
        obj.set_username(username)
        obj.set_password(password)
        return obj
    
    def _tap(self, el):
        actions = TouchAction(self.driver)
        actions.tap(el)
        actions.perform()
    
    def setUp(self):
        self.client = ProjectsClient(self.token)
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub',
                                       ANDROID_BASE_CAPS)
        self.driver.implicitly_wait(5000)
        
    def tearDown(self):
        # end the session
        self.driver.quit()
        
    def test_create_project(self):
        # Step 1 Create test project via API
        random_no = random.randint(1, 5000)
        project_name = "Project_{}".format(random_no)
        assert_msg = "Generated project name should be same with test case: {}"
        assert_msg = assert_msg.format(project_name)
        params = {
            "name": project_name
        }
        obj = self.client.create(params)
        # validate if generated project name is equal to returned object name from API
        self.assertEqual(project_name, obj.name,
                         assert_msg)
        # Step 2: Login
        # choose login by email
        el = self.driver.find_element_by_id('btn_welcome_continue_with_email')
        self._tap(el)
        # fill username/email then continue
        self.driver.find_element_by_id('email_exists_input').send_keys(self.username)
        el = self.driver.find_element_by_id('btn_continue_with_email')
        self._tap(el)
        # fill password then log in
        self.driver.find_element_by_id('log_in_password').send_keys(self.password)
        el = self.driver.find_element_by_id('btn_log_in')
        self._tap(el)
        # check if home page is loaded so it means login is successful
        today_el_in_home_page = None
        path = "//android.widget.TextView[@text='Today']"
        today_el_in_home_page = self.driver.find_element_by_xpath(path)
        # check login is successful by means of being in a home page contains "Today" text
        self.assertTrue(today_el_in_home_page is not None)
        
        # Step 3: Verify project is created in mobile app
        # click and expand sidebar
        el = self.driver.find_element_by_accessibility_id('Change the current view')
        self._tap(el)
        sleep(1.0)
        # expand project menu list
        path = "(//android.widget.ImageView[@content-desc='Expand/collapse'])[1]"
        el = self.driver.find_element_by_xpath(path)
        self._tap(el)
        # set xpath search path with text of project_name
        project_text_widget = None
        path = "//android.widget.TextView[@text='{}']".format(project_name)
        project_text_widget = self.driver.find_element_by_xpath(path)
        # check if text widget of the project is found
        self.assertTrue(project_text_widget is not None)
