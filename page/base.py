import time
from poium.page_objects import NewPageElement
from selenium.webdriver.remote.webdriver import WebDriver


class BasePage:
    """
    页面基础类
    """

    def __init__(self, driver):
        self.driver = driver

    def open_url(self, url=None):
        if url is None:
            self.driver.get(self.url)
        else:
            self.driver.get(url)

    # 通过id定位元素
    def by_id(self, id_):
        return self.driver.find_element_by_id(id_)

    # 通过name定位元素
    def by_name(self, name):
        return self.driver.find_element_by_name(name)

    # 通过class_name定位元素
    def by_class_name(self, class_name):
        return self.driver.find_element_by_class_name(class_name)

    # 通过XPath定位元素
    def by_xpath(self, xpath):
        return self.driver.find_element_by_xpath(xpath)

    # 通过CSS定位元素
    def by_css(self, css):
        return self.driver.find_element_by_css_selector(css)

    # 获取页面title
    def get_title(self):
        return self.driver.title

    # 通过xpath定位，获取text内容
    def get_text(self, xpath):
        return self.by_xpath(xpath).text

    # 执行JS
    def js(self, script):
        self.driver.execute_script(script)


class Page(NewPageElement):
    def __init__(self):
        ...


class Driver(WebDriver):
    def __init__(self, web_driver: WebDriver):
        ...


