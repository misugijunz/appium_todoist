import unittest
import os
import copy
import sys
import random
from ..rest_client.clients import TasksClient, ProjectsClient
from ..helpers import ANDROID_BASE_CAPS, EXECUTOR
from .functionals import Functionals

from time import sleep
from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction
from selenium.common.exceptions import NoSuchElementException

class FunctionalsTask(unittest.TestCase, Functionals):
    
    @staticmethod
    def get_instance(testcase, token, username, password):
        obj = FunctionalsTask(testcase)
        obj.set_token(token)
        obj.set_username(username)
        obj.set_password(password)
        return obj
    
    def _tap(self, el):
        actions = TouchAction(self.driver)
        actions.tap(el)
        actions.perform()
        
    def login_to_homepage(self):
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
        # wait until home page is loaded
        today_el_in_home_page = self.driver.find_element_by_xpath(path)

         
    def setUp(self):
        self.client = TasksClient(self.token)
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub',
                                       ANDROID_BASE_CAPS)
        self.driver.implicitly_wait(5000)
        # set up test project
        random_no = random.randint(1, 5000)
        self.project_name = "Project_{}".format(random_no)
        params = {
            "name": self.project_name
        }
        self.project_client = ProjectsClient(self.token)
        self.project = self.project_client.create(params)        
        
    def tearDown(self):
        # end the session
        self.driver.quit()
        # self.project_client.delete(self.project.id)
    
    def test_create_task_from_mobile_phone(self):
        self.login_to_homepage()
        el = self.driver.find_element_by_accessibility_id('Change the current view')
        self._tap(el)
        sleep(1.0)
        # expand project menu list
        path = "(//android.widget.ImageView[@content-desc='Expand/collapse'])[1]"
        el = self.driver.find_element_by_xpath(path)
        self._tap(el)
        # set xpath search path with text of project_name
        project_text_widget = None
        path = "//android.widget.TextView[@text='{}']".format(self.project_name)
        project_text_widget = self.driver.find_element_by_xpath(path)
        self._tap(project_text_widget)
        
        # Step 1: Create task with mobile phone
        el = self.driver.find_element_by_id("fab")
        self._tap(el)
        # add message
        random_no = random.randint(1, 5000)
        task_message = "Task_{}".format(random_no)
        path = "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/" + \
            "android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/" + \
            "androidx.drawerlayout.widget.DrawerLayout/android.view.ViewGroup/" + \
            "android.widget.FrameLayout[2]/android.widget.LinearLayout/android.view.ViewGroup/android.widget.EditText"
        self.driver.find_element_by_xpath(path).send_keys(task_message)
        # submit task
        sleep(1.0)
        el = self.driver.find_element_by_id("android:id/button1")
        self._tap(el)
        # search for test task in the list
        path = "//android.widget.TextView[@text='{}']".format(task_message)
        task_text_widget = self.driver.find_elements_by_xpath(path)
        task_text_widget_size = len(task_text_widget)
        self.assertEqual(task_text_widget_size, 1)
        print("Task {} is created".format(task_message))
        
        # Step 2: Verify task is created through API
        sleep(5.0)
        params = {
            "project_id": self.project.id
        }
        tasks = self.client.get_all(params)
        sleep(5.0)
        found = False
        for task in tasks:
            if task.content == task_message:
                found = True
                print("Task is found through API")
                break
        self.assertTrue(found)

    def test_reopen_task(self):
        # Step 1: Open mobile application
        activity = None
        activity = self.driver.current_activity;
        # assert if activity is loaded
        self.assertTrue(activity is not None)
        # login and prepare test project
        self.login_to_homepage()
        
        # Step 2: Open test project
        el = self.driver.find_element_by_accessibility_id('Change the current view')
        self._tap(el)
        sleep(1.0)
        # expand project menu list
        path = "(//android.widget.ImageView[@content-desc='Expand/collapse'])[1]"
        el = self.driver.find_element_by_xpath(path)
        self._tap(el)
        # set xpath search path with text of project_name
        project_text_widget = None
        path = "//android.widget.TextView[@text='{}']".format(self.project_name)
        project_text_widget = self.driver.find_element_by_xpath(path)
        self._tap(project_text_widget)
        # entered project view, search for header with project name to assert
        project_title_text_count = len(self.driver.find_elements_by_xpath(path))
        self.assertEqual(project_title_text_count, 1)
        
        # Step 3: Create test task
        el = self.driver.find_element_by_id("fab")
        self._tap(el)
        # add message
        random_no = random.randint(1, 5000)
        task_message = "Task_{}".format(random_no)
        path = "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/" + \
            "android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/" + \
            "androidx.drawerlayout.widget.DrawerLayout/android.view.ViewGroup/" + \
            "android.widget.FrameLayout[2]/android.widget.LinearLayout/android.view.ViewGroup/android.widget.EditText"
        self.driver.find_element_by_xpath(path).send_keys(task_message)
        # submit task
        sleep(1.0)
        el = self.driver.find_element_by_id("android:id/button1")
        self._tap(el)
        # close keyboard with back button
        self.driver.press_keycode(4);
        # search for test task in the list
        path = "//android.widget.TextView[@text='{}']".format(task_message)
        task_text_widget = self.driver.find_elements_by_xpath(path)
        task_text_widget_size = len(task_text_widget)
        self.assertEqual(task_text_widget_size, 1)
        print("Task {} is created".format(task_message))
        # get task object from api for testing following steps
        sleep(5.0)
        params = {
            "project_id": self.project.id
        }
        tasks = self.client.get_all(params)
        sleep(1.0)
        _task = None
        for task in tasks:
            if task.content == task_message:
                _task = task
                print("Task is found through API")
                break
        sleep(5.0)
        print(_task)
        
        # Step 4: complete test task
        # assume the test task is in first list, we check the check box to complete
        # search with full xpath
        path = '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/' + \
            'android.widget.FrameLayout/android.widget.FrameLayout/' + \
            'android.widget.FrameLayout/androidx.drawerlayout.widget.DrawerLayout/' + \
            'android.view.ViewGroup/android.view.ViewGroup/android.widget.FrameLayout/' + \
            'androidx.recyclerview.widget.RecyclerView/android.widget.FrameLayout[1]/' + \
            'android.widget.RelativeLayout/android.widget.CheckBox'
        el = self.driver.find_element_by_xpath(path)
        
        self._tap(el)
        # search again the test task, make sure it is not found now on the list
        # path = "//android.widget.TextView[@text='{}']".format(task_message)
        sleep(3.0)
        task_text_widgets = self.driver.find_elements_by_class_name("android.widget.TextView")
        texts = [el.text for el in task_text_widgets if el.text == task_message]
        task_text_widget_size = len(task_text_widget)
        self.assertEqual(len(texts), 0)
        print("Task {} is completed".format(task_message))
        
        # Step 5: reopen task with API
        resp = self.client.reopen(_task.id)
        # search again the test task, make sure it is not found now on the list
        sleep(3.0)
        # verify reopened task with status completed = False
        # if 402 == resp.status_code:
        _task = self.client.get(_task.id)
        sleep(3.0)
        self.assertFalse(_task.completed)
        print("Task {} is reopened and completed value is False".format(task_message))
        
        # Step 6: validate reopened task on mobile app
        path = "//android.widget.TextView[@text='{}']".format(task_message)
        task_text_widget = self.driver.find_elements_by_xpath(path)
        task_text_widget_size = len(task_text_widget)
        self.assertGreater(task_text_widget_size, 0)
        print("Task {} is reopened and can be seen at mobile app".format(task_message))
                