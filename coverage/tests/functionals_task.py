import unittest
import os
import copy
import sys
import random
from ..rest_client.clients import TasksClient
from ..helpers import ANDROID_BASE_CAPS, EXECUTOR
from .functionals import Functionals

from time import sleep
from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction
from selenium.common.exceptions import NoSuchElementException

class FunctionalsTask(Functionals):
    
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
    
    def setUp(self):
        self.client = TasksClient(self.token)
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub',
                                       ANDROID_BASE_CAPS)
        self.driver.implicitly_wait(5000)
        
    def tearDown(self):
        # end the session
        self.driver.quit()