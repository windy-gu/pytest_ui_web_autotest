# author:windy
# datetime:2021/4/21 15:09 下午
# software: PyCharm
import os
import time
import warnings
from time import sleep
from util.log import Log
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import NoAlertPresentException
from appium.webdriver.common.touch_action import TouchAction as MobileTouchAction

log = Log()


class PageBrowser(object):
    """
    Implement the APIs with javascript,
    and selenium/appium extension APIs。
    """

    def __init__(self, driver, url=None):
        """
        :param driver: `selenium.webdriver.WebDriver` Selenium webdriver instance
        :param url: `str`
        Root URI to base any calls to the ``PageObject.get`` method. If not defined
        in the constructor it will try and look it from the webdriver object.
        """
        self.driver = driver
        self.root_uri = url if url else getattr(self.driver, 'url', None)

    def quit(self):
        log.info('关闭浏览器')
        self.driver.quit()

    def close(self):
        log.info('关闭当前窗口')
        self.driver.close()

    def get(self, uri):
        """
        :param uri:  URI to GET, based off of the root_uri attribute.
        """
        root_uri = self.root_uri or ''
        self.driver.get(root_uri + uri)
        log.info('打开网页：{}'.format(uri))
        self.driver.implicitly_wait(5)
        log.info('设置全局隐式等待时间：5s')

    def run_script(self, js=None, *args):
        """
        run JavaScript script
        """
        warnings.warn("use execute_script instead",
                      DeprecationWarning, stacklevel=2)
        if js is None:
            raise ValueError("Please input js script")
        else:
            self.driver.execute_script(js, *args)

    def execute_script(self, js=None, *args):
        """
        Execute JavaScript scripts.
        """
        if js is None:
            raise ValueError("Please input js script")

        return self.driver.execute_script(js, *args)

    def window_scroll(self, width=None, height=None):
        """
        JavaScript API, Only support css positioning
        Setting width and height of window scroll bar.
        """
        if width is None:
            width = "0"
        if height is None:
            height = "0"
        js = "window.scrollTo({w},{h});".format(w=str(width), h=(height))
        self.execute_script(js)

    @property
    def get_title(self):
        """
        JavaScript API
        Get page title.
        """
        js = 'return document.title;'
        return self.execute_script(js)

    @property
    def get_url(self):
        """
        JavaScript API
        Get page URL.
        """
        js = "return document.URL;"
        return self.execute_script(js)

    def switch_to_frame(self, frame_reference):
        """
        selenium API
        Switches focus to the specified frame, by id, name, or webelement.
        """
        warnings.warn("use driver.elem.switch_to_frame() instead",
                      DeprecationWarning, stacklevel=2)
        self.driver.switch_to.frame(frame_reference)

    def switch_to_parent_frame(self):
        """
        selenium API
        Switches focus to the parent context.
        Corresponding relationship with switch_to_frame () method.
        """
        self.driver.switch_to.parent_frame()

    @property
    def new_window_handle(self):
        """
        selenium API
        Getting a handle to a new window.
        """
        all_handle = self.window_handles
        return all_handle[-1]

    @property
    def current_window_handle(self):
        """
        selenium API
        Returns the handle of the current window.
        """
        return self.driver.current_window_handle

    @property
    def window_handles(self):
        """
        selenium API
        Returns the handles of all windows within the current session.
        """
        return self.driver.window_handles

    def switch_to_window(self, handle):
        """
        selenium API
        Switches focus to the specified window.
        """
        self.driver.switch_to.window(handle)

    def screenshots(self, path=None, filename=None):
        """
        selenium API
        Saves a screenshots of the current window to a PNG image file
        :param path: The path to save the file
        :param filename: The file name
        """
        if path is None:
            path = os.getcwd()
        if filename is None:
            filename = str(time.time()).split(".")[0] + ".png"
        file_path = os.path.join(path, filename)
        self.driver.save_screenshot(file_path)

    def get_cookies(self):
        """
        Returns a set of dictionaries, corresponding to cookies visible in the current session.
        """
        return self.driver.get_cookies()

    def get_cookie(self, name):
        """
        Returns information of cookie with ``name`` as an object.
        """
        return self.driver.get_cookie(name)

    def add_cookie(self, cookie_dict: dict):
        """
        Adds a cookie to your current session.
        Usage:
            add_cookie({'name' : 'foo', 'value' : 'bar'})
        """
        if isinstance(cookie_dict, dict):
            self.driver.add_cookie(cookie_dict)
            log.info('Add cookie:' + str(cookie_dict))
        else:
            raise TypeError("Wrong cookie type.")

    def add_cookies(self, cookie_list: list):
        """
        Adds a cookie to your current session.
        Usage:
            cookie_list = [
                {'name' : 'foo', 'value' : 'bar'},
                {'name' : 'foo', 'value' : 'bar'}
            ]
            add_cookie(cookie_list)
        """
        if isinstance(cookie_list, list):
            for cookie in cookie_list:
                self.add_cookie(cookie)
            log.info('Add cookies:' + str(cookie_list))

        else:
            raise TypeError("Wrong cookie type.")

    def delete_cookie(self, name):
        """
        Deletes a single cookie with the given name.
        """
        self.driver.delete_cookie(name)
        log.info("Delete kry:{all} cookie".format(all=name))

    def delete_all_cookies(self):
        """
        Delete all cookies in the scope of the session.
        Usage:
            self.delete_all_cookies()
        """
        self.driver.delete_all_cookies()
        log.info("Delete all cookies")

    def switch_to_app(self):
        """
        appium API
        Switch to native app.
        """
        self.driver.switch_to.context('NATIVE_APP')

    def switch_to_web(self, context=None):
        """
        appium API
        Switch to web view.
        """
        if context is not None:
            self.driver.switch_to.context(context)
        else:
            all_context = self.driver.contexts
            for context in all_context:
                if "WEBVIEW" in context:
                    self.driver.switch_to.context(context)
                    break
            else:
                raise NameError("No WebView found.")

    def accept_alert(self):
        """
        selenium API
        Accept warning box.
        """
        self.driver.switch_to.alert.accept()
        log.info('Accept current alert')

    def dismiss_alert(self):
        """
        selenium API
        Dismisses the alert available.
        """
        self.driver.switch_to.alert.dismiss()
        log.info('Dismiss current alert')

    def alert_is_display(self):
        """
        selenium API
        Determines if alert is displayed
        """
        try:
            self.driver.switch_to.alert
        except NoAlertPresentException:
            return False
        else:
            return True

    @property
    def get_alert_text(self):
        """
        selenium API
        Get warning box prompt information.
        """
        text = self.driver.switch_to.alert.text
        log.info('Get current alert text:{}'.format(text))
        return text

    def move_to_element(self, elem):
        """
        selenium API
        Moving the mouse to the middle of an element
        """
        warnings.warn("use driver.elem.move_to_element() instead",
                      DeprecationWarning, stacklevel=2)
        ActionChains(self.driver).move_to_element(elem).perform()

    def click_and_hold(self, elem):
        """
        selenium API
        Holds down the left mouse button on an element.
        """
        warnings.warn("use driver.elem.click_and_hold() instead",
                      DeprecationWarning, stacklevel=2)
        ActionChains(self.driver).click_and_hold(elem).perform()

    def move_by_offset(self, x, y):
        """
        selenium API
        Moving the mouse to an offset from current mouse position.

        :Args:
         - x: X offset to move to, as a positive or negative integer.
         - y: Y offset to move to, as a positive or negative integer.
        """
        ActionChains(self.driver).move_by_offset(x, y).perform()

    def release(self):
        """
        selenium API
        Releasing a held mouse button on an element.
        """
        ActionChains(self.driver).release().perform()

    def context_click(self, elem):
        """
        selenium API
        Performs a context-click (right click) on an element.
        """
        warnings.warn("use driver.elem.context_click() instead",
                      DeprecationWarning, stacklevel=2)
        ActionChains(self.driver).context_click(elem).perform()

    def drag_and_drop_by_offset(self, elem, x, y):
        """
        selenium API
        Holds down the left mouse button on the source element,
           then moves to the target offset and releases the mouse button.
        :param elem: The element to mouse down.
        :param x: X offset to move to.
        :param y: Y offset to move to.
        """
        warnings.warn("use driver.elem.drag_and_drop_by_offset(x, y) instead",
                      DeprecationWarning, stacklevel=2)
        ActionChains(self.driver).drag_and_drop_by_offset(elem, xoffset=x, yoffset=y).perform()

    def refresh_element(self, elem, timeout=10):
        """
        selenium API
        Refreshes the current page, retrieve elements.
        """
        warnings.warn("use driver.elem.refresh_element() instead",
                      DeprecationWarning, stacklevel=2)
        try:
            timeout_int = int(timeout)
        except TypeError:
            raise ValueError("Type 'timeout' error, must be type int() ")

        for i in range(timeout_int):
            if elem is not None:
                try:
                    elem
                except StaleElementReferenceException:
                    self.driver.refresh()
                else:
                    break
            else:
                sleep(1)
        else:
            raise TimeoutError("stale element reference: element is not attached to the page document.")

    def top(self, elem, x, y, count):
        """
        appium API
        Perform a tap action on the element
        """
        action = MobileTouchAction(self.driver)
        action.tap(elem, x, y, count).perform()

    def press(self, elem, x, y, pressure):
        """
        appium API
        Begin a chain with a press down action at a particular element or point
        """
        action = MobileTouchAction(self.driver)
        action.press(elem, x, y, pressure).perform()

    def long_press(self, elem, x, y, duration):
        """
        appium API
        Begin a chain with a press down that lasts `duration` milliseconds
        """
        action = MobileTouchAction(self.driver)
        action.long_press(elem, x, y, duration).perform()

    def swipe(self, start_x, start_y, end_x, end_y, duration=None):
        """
        appium API
        Swipe from one point to another point, for an optional duration.
        """
        self.driver.swipe(start_x, start_y, end_x, end_y, duration)
