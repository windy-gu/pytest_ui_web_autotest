# author:windy
# datetime:2021/4/13 4:58 下午
# software: PyCharm

import time
from util.log import Log
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.support.wait import WebDriverWait

log = Log()


class Driver(WebDriver):
    def __init__(self, web_driver: WebDriver):
        # 直接把WebDriver的属性字典复制过来
        self.__dict__ == web_driver.__dict__
        # self.wait = D

    @staticmethod
    def chrome(**kwargs):
        from driver.browserdriver import chrome_driver
        wd = chrome_driver(**kwargs)
        return Driver(wd)


    @staticmethod
    def firefox(**kwargs):
        pass

    def get(self, url):
        log.info(f'打开网址，url:[ {url} ]')
        super().get(url)

    def sleep(self, secs: float = 1):
        log.info(f'等待 {secs}s')
        time.sleep(secs)

    def clear_local_storage(self):
        log.info('清空localStorage')
        js = 'window.localStorage.clear();'
        self.execute_script(js)

    def window_scroll(self, width=None, height=None):
        """
        JavaScript API, Only support css positioning
        Setting width and height of window scroll bar.
        """
        if width is None:
            width = "0"
        if height is None:
            height = "0"
        js = f'window.scrollTo({str(width)},{str(height)});'
        self.execute_script(js)

    def get_title(self):
        js = 'return document.title;'
        return self.execute_script(js)

    def get_url(self):
        js = "return document.URL;"
        return self.execute_script(js)

    def accept_alert(self):
        self.switch_to.alert.accept()

    def dismiss_alert(self):
        self.switch_to.alert.dismiss()

    def alert_is_display(self):
        try:
            self.switch_to.alert
        except NoAlertPresentException:
            return False
        else:
            return True

    def get_alert_text(self):
        return self.switch_to.alert.text

    def move_by_offset(self, x, y):
        """Selenium API
        Moving the mouse to an offset from current mouse position.

        Args:
            x: X offset to move to, as a positive or negative integer.
            y: Y offset to move to, as a positive or negative integer.
        """
        ActionChains(self).move_by_offset(x, y).perform()

    def release(self):
        """Selenium API, Releasing a held mouse button on an element"""
        ActionChains(self).release().perform()

