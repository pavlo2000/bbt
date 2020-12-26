from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


default_wd_func = webdriver.Remote
default_wd_args = []
default_wd_kwargs = {
    'command_executor': 'http://127.0.0.1:4444/wd/hub',
    'desired_capabilities': DesiredCapabilities.CHROME
}

