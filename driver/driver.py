# author:windy
# datetime:2021/4/13 4:58 下午
# software: PyCharm
from selenium.webdriver.remote.webdriver import WebDriver


class Driver(WebDriver):
    def __init__(self, web_driver: WebDriver):
        self.__dict__ == web_driver.__dict__

    @staticmethod
    def chrome(**kwargs):
        ...

