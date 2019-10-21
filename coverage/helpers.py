import os
import sys

ANDROID_BASE_CAPS = {
    'app': os.path.abspath('Todoist_v14.4.7_apkpure.com.apk'),
    'automationName': 'UIAutomator2',
    'platformName': 'Android',
    'platformVersion': os.getenv('ANDROID_PLATFORM_VERSION') or '10',
    'deviceName': os.getenv('ANDROID_DEVICE_VERSION') or 'Android Emulator',
    'appActivity': 'com.todoist.activity.HomeActivity',
    'appPackage': 'com.todoist',
    'appWaitActivity': 'com.todoist.activity.WelcomeActivity',
    'appWaitPackage': 'com.todoist'
}

EXECUTOR = 'http://127.0.0.1:4723/wd/hub'