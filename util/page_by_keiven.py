# author:windy
# datetime:2021/4/14 6:13 下午
# software: PyCharm
from util.log import Log
import platform
from functools import wraps
from time import sleep, time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.support.select import Select
from poium.common.exceptions import FindElementTypesError
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.touch_actions import TouchActions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

log = Log()
# 可以识别的定位类型

LOCATOR_LIST = {
    # selenium
    'css': By.CSS_SELECTOR,
    'id_': By.ID,
    'name': By.NAME,
    'xpath': By.XPATH,
    'link_text': By.LINK_TEXT,
    'partial_link_text': By.PARTIAL_LINK_TEXT,
    'tag': By.TAG_NAME,
    'class_name': By.CLASS_NAME,
    # appium
    'ios_uiautomation': MobileBy.IOS_UIAUTOMATION,
    'ios_predicate': MobileBy.IOS_PREDICATE,
    'ios_class_chain': MobileBy.IOS_CLASS_CHAIN,
    'android_uiautomator': MobileBy.ANDROID_UIAUTOMATOR,
    'android_viewtag': MobileBy.ANDROID_VIEWTAG,
    'android_data_matcher': MobileBy.ANDROID_DATA_MATCHER,
    'android_view_matcher': MobileBy.ANDROID_VIEW_MATCHER,
    'windows_uiautomation': MobileBy.WINDOWS_UI_AUTOMATION,
    'accessibility_id': MobileBy.ACCESSIBILITY_ID,
    'image': MobileBy.IMAGE,
    'custom': MobileBy.CUSTOM,
}


def retry_find_web_element(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        parent = args[0]
        driver = parent.driver
        by = kwargs.pop('by', None) or args[1]
        value = kwargs.pop('value', None) or args[2]
        visible = kwargs.pop('visible', False)
        delay = kwargs.pop('delay', 0.5)
        timeout = kwargs.pop('timeout', 5)
        interval = kwargs.pop('interval', 0.5)

        # 计算重试次数
        retry_count = int(float(timeout) / float(interval))
        # 延迟查找元素
        if delay:
            sleep(delay)
        # 重试次数小于1时，不重试，找不到直接抛异常
        if retry_count < 1:
            el = func(parent, by, value)
            if visible:
                WebDriverWait(
                    driver, timeout
                ).until(
                    EC.visibility_of(el), message=f'By:[ {by} ] value:[ {value} ]'
                )
            return Element(driver=driver, web_element=el)

        # 重试查找元素，元素存在时返回，找不到时重试直到timeout后抛出异常
        for i in range(retry_count):
            try:
                if i > 0:
                    sleep(interval)
                el = func(parent, by, value)
                if visible:
                    WebDriverWait(
                        driver, timeout
                    ).until(
                        EC.visibility_of(el), message=f'By:[ {by} ] value:[ {value} ]'
                    )
                return Element(driver=driver, web_element=el)
            except NoSuchElementException:
                if i == (retry_count - 1):
                    raise
                continue

        return wrapper


def retry_find_webelements(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        parent = args[0]
        driver = parent.driver
        by = kwargs.pop('by', None) or args[1]
        value = kwargs.pop('value', None) or args[2]
        delay = kwargs.pop('delay', 0.5)
        timeout = kwargs.pop('timeout', 10)
        interval = kwargs.pop('interval', 0.5)

        # 计算重试次数
        retry_count = int(float(timeout) / float(interval))
        # 延迟查找元素
        if delay:
            sleep(delay)

        # 重试次数小于1时，不重试，找不到直接抛异常
        if retry_count < 1:
            elements = func(parent, by, value)
            if not elements:
                raise NoSuchElementException(f'By:[ {by} ] value:[ {value} ]')
            return Elements(driver=driver, web_elements=elements)

        # 重试查找元素，元素存在时返回，找不到时重试直到timeout后抛出异常
        for i in range(retry_count):
            if i > 0:
                sleep(interval)
            elements = func(parent, by, value)
            if not elements:
                if i == (retry_count - 1):
                    raise NoSuchElementException(f'By:[ {by} ] value:[ {value} ]')
                continue
            return Elements(driver=driver, web_elements=elements)

    return wrapper


class Element(WebElement):
    def __init__(self,
                 visible: bool = None,
                 driver: WebDriver = None,
                 web_element: WebElement = None,
                 delay: float = 0.5,
                 timeout: float = 5,
                 interval: float = 0.5,
                 describe: str = 'undefined',
                 index: int = 0,
                 **kwargs):
        if driver:
            self.driver = driver
        if web_element:
            # 直接把WebElement的属性字典复制过来
            self.__dict__.update(web_element.__dict__)
        if not kwargs:
            raise ValueError("Please specify a locator")
        if len(kwargs) > 1:
            raise ValueError("Please specify only one locator")

        self.kwargs = kwargs
        self.by, self.value = next(iter(kwargs.items()))
        self.visible = visible
        self.delay = delay
        self.timeout = timeout  # 根据timeout和interval的数值，用于计算重试次数
        self.interval = interval  # 每次间隔时间
        self.desc = describe
        self.index = index

        if self.by not in LOCATOR_LIST.keys():
            raise FindElementTypesError("Element positioning of type '{}' is not supported.".format(self.by))

    def __retry_find_element(self):
        if (not self.by) or (not self.value):
            raise Exception('元素定位类型/值，不允许为空')

        # 根据timeout和interval的数值，计算重新定位次数
        retry_count = int(float(self.timeout))/int(float(self.interval))

        # 重试次数<1时，不重试，找不到直接抛异常
        if retry_count < 1:
            el = self.driver.find_element(self.by, self.value)
            self.__dict__.update(el.__dict__)
            if self.visible:
                WebDriverWait(
                    self.driver, self.timeout
                ).until(
                    EC.visibility_of(self), message=f'By:[{self.by}] value[{self.value} ]'
                )
            return self

        # 重新查找元素，元素存在时返回，找不到时重试直到timeout后抛出异常
        for i in range(int(retry_count)):
            try:
                if i > 0:
                    sleep(self.interval)
                el = self.driver.find_element(self.by, self.value)
                self.__dict__.update(el.__dict__)
                if self.visible:
                    WebDriverWait(
                        self.driver, self.timeout
                    ).until(
                        EC.visibility_of(self), message=f'By:[{self.by}] value[{self.value} ]'
                    )
                return self

            except NoSuchElementException:
                if i == (retry_count - 1):
                    raise
                continue

    def __get__(self, instance, owner):
        if instance is None:
            raise Exception('类没有被实例化')
        self.driver = instance.driver
        return self.__retry_find_element()

    def __set__(self, instance, value):
        raise Exception('通过send_keys()来实现输入操作吧')

    def find_element(self, by, value, **kwargs):
        """查找元素

        Args:
            by(By): 定位类型
            value(str): 定位值
            visible(bool): 是否等待可见，default=False
            delay(float): 延迟时间，default=0.5
            timeout(float): 查找超时时间，default=10
            interval(float): 重试查找间隔时间，default=0.5

        Returns:
            Element
        """
        return super().find_element(by, value)

    def textarea_value(self):
        """获取textarea元素的值"""
        return self.get_attribute('value')

    def scroll_into_view(self):
        """
        使用元素处于用户可视区域
        :return:
        """
        js = 'arguments[0].scrollIntoView(true);'
        self.driver.execute_script(js, self)

    def save_screenshot(self, filename, frequency=0.5):
        """保存元素截图

        :param filename:  截图名称
        :param frequency: 读取图片complete属性的频率
        :return:
        """
        end_time = time() + self.timeout

        while not bool(self.get_attribute('complete')):
            sleep(frequency)
            if time() > end_time:
                raise TimeoutException('CONTENT:Image loading is not complete')

        return self.screenshot(filename)

    def select_by_value(self, value):
        """Selenium Select API"""
        Select(self).select_by_value(value)

    def select_by_visible_text(self, text):
        """Selenium Select API"""
        Select(self).select_by_visible_text(text)

    def select_by_index(self, index):
        """Selenium Select API"""
        Select(self).select_by_index(index)

    def move_here(self):
        """Selenium ActionChains API"""
        ActionChains(self.driver).move_to_element(self).perform()

    def click_by_action(self):
        ActionChains(self.driver).move_to_element(self).click(self).perform()

    def click_and_hold(self):
        """Selenium ActionChains API"""
        ActionChains(self.driver).click_and_hold(self).perform()

    def double_click(self):
        """Selenium ActionChains API"""
        ActionChains(self.driver).double_click(self).perform()

    def context_click(self):
        """Selenium ActionChains API"""
        ActionChains(self.driver).context_click(self).perform()

    def drag_and_drop_by_offset(self, x, y):
        """Selenium ActionChains API"""
        ActionChains(self.driver).drag_and_drop_by_offset(self, xoffset=x, yoffset=y).perform()

    def tap(self, center=True):
        """
        Selenium TouchActions API
        webview专用，单次点触，触控坐标为元素的左上角
        """
        if center:
            self.tap_center()
        else:
            TouchActions(self.driver).tap(self).perform()

    def tap_offset(self, xoffset, yoffset):
        """
        Selenium TouchActions API
        webview专用，单次点触，触控坐标是元素的左上角+偏移量

        Args:
            xoffset (int): x轴偏移量
            yoffset (int): y轴偏移量
        """
        location = self.location
        xcoord = int(location['x']) + int(xoffset)
        ycoord = int(location['y']) + int(yoffset)
        TouchActions(self.driver).tap_and_hold(xcoord, ycoord).release(xcoord, ycoord).perform()

    def tap_center(self):
        """
        Selenium TouchActions API
        webview专用，单次点触，触控坐标为元素的正中间
        """
        size = self.size
        height = int(size['height']) / 2
        width = int(size['width']) / 2
        self.tap_offset(width, height)

    def scroll_here(self):
        TouchActions(self.driver).scroll_from_element(self, 0, self.size['height']).perform()

    def hide(self):
        js = "arguments[0].style.display='none';"
        self.driver.execute_script(js, self)
        
    def __elements(self, key, value):
        elems = self.driver.find_elements(by=key, value=value)
        return elems

    def __find_element(self, elem):
        """
        Find if the element exists.
        """
        for i in range(self.timeout):
            try:
                elems = self.__elements(elem[0], elem[1])
            except Exception:
                elems = []

            if len(elems) == 1:
                log.info("✅ Find element: {by}={value} ".format(
                    by=elem[0], value=elem[1]))
                break
            elif len(elems) > 1:
                log.info("❓ Find {n} elements through: {by}={value}".format(
                    n=len(elems), by=elem[0], value=elem[1]))
                break
            else:
                sleep(1)
        else:
            error_msg = "❌ Find 0 elements through: {by}={value}".format(by=elem[0], value=elem[1])
            log.error(error_msg)
            raise NoSuchElementException(error_msg)

    def __get_element(self, by, value):
        """
        Judge element positioning way, and returns the element.
        """

        # selenium
        if by == "id_":
            self.__find_element((By.ID, value))
            elem = self.driver.find_elements_by_id(value)[self.index]
        elif by == "name":
            self.__find_element((By.NAME, value))
            elem = self.driver.find_elements_by_name(value)[self.index]
        elif by == "class_name":
            self.__find_element((By.CLASS_NAME, value))
            elem = self.driver.find_elements_by_class_name(value)[self.index]
        elif by == "tag":
            self.__find_element((By.TAG_NAME, value))
            elem = self.driver.find_elements_by_tag_name(value)[self.index]
        elif by == "link_text":
            self.__find_element((By.LINK_TEXT, value))
            elem = self.driver.find_elements_by_link_text(value)[self.index]
        elif by == "partial_link_text":
            self.__find_element((By.PARTIAL_LINK_TEXT, value))
            elem = self.driver.find_elements_by_partial_link_text(value)[self.index]
        elif by == "xpath":
            self.__find_element((By.XPATH, value))
            elem = self.driver.find_elements_by_xpath(value)[self.index]
        elif by == "css":
            self.__find_element((By.CSS_SELECTOR, value))
            elem = self.driver.find_elements_by_css_selector(value)[self.index]

        # appium 暂时不支持
        # elif by == "ios_uiautomation":
        #     self.__find_element((MobileBy.IOS_UIAUTOMATION, value))
        #     elem = self.driver.find_elements_by_ios_uiautomation(value)[self.index]
        # elif by == "ios_predicate":
        #     self.__find_element((MobileBy.IOS_PREDICATE, value))
        #     elem = self.driver.find_elements_by_ios_predicate(value)[self.index]
        # elif by == "ios_class_chain":
        #     self.__find_element((MobileBy.IOS_CLASS_CHAIN, value))
        #     elem = self.driver.find_elements_by_ios_class_chain(value)[self.index]
        # elif by == "android_uiautomator":
        #     self.__find_element((MobileBy.ANDROID_UIAUTOMATOR, value))
        #     elem = self.driver.find_elements_by_android_uiautomator(value)[self.index]
        # elif by == "android_viewtag":
        #     self.__find_element((MobileBy.ANDROID_VIEWTAG, value))
        #     elem = self.driver.find_elements_by_android_viewtag(value)[self.index]
        # elif by == "android_data_matcher":
        #     self.__find_element((MobileBy.ANDROID_DATA_MATCHER, value))
        #     elem = self.driver.find_elements_by_android_data_matcher(value)[self.index]
        # elif by == "accessibility_id":
        #     self.__find_element((MobileBy.ACCESSIBILITY_ID, value))
        #     elem = self.driver.find_elements_by_accessibility_id(value)[self.index]
        # elif by == "android_view_matcher":
        #     self.__find_element((MobileBy.ANDROID_VIEW_MATCHER, value))
        #     elem = self.driver.find_elements_by_android_view_matcher(value)[self.index]
        # elif by == "windows_uiautomation":
        #     self.__find_element((MobileBy.WINDOWS_UI_AUTOMATION, value))
        #     elem = self.driver.find_elements_by_windows_uiautomation(value)[self.index]
        # elif by == "image":
        #     self.__find_element((MobileBy.IMAGE, value))
        #     elem = self.driver.find_elements_by_image(value)[self.index]
        # elif by == "custom":
        #     self.__find_element((MobileBy.CUSTOM, value))
        #     elem = self.driver.find_elements_by_custom(value)[self.index]
        # else:
        #     raise FindElementTypesError(
        #         "Please enter the correct targeting elements")

        # 此注释内容未是否显示框框
        # if Browser.show is True:
        #     try:
        #         style_red = 'arguments[0].style.border="2px solid #FF0000"'
        #         style_blue = 'arguments[0].style.border="2px solid #00FF00"'
        #         style_null = 'arguments[0].style.border=""'
        #
        #         for _ in range(2):
        #             self.driver.execute_script(style_red, elem)
        #             sleep(0.1)
        #             self.driver.execute_script(style_blue, elem)
        #             sleep(0.1)
        #         self.driver.execute_script(style_blue, elem)
        #         sleep(0.5)
        #         self.driver.execute_script(style_null, elem)
        #     except WebDriverException:
        #         pass

        return elem

    def clear(self):
        """Clears the text if it's a text entry element."""
        elem = self.__get_element(self.by, self.value)
        log.info("clear element: 类型{} 值{}  desc：{}".format(self.by, self.value, self.desc))
        elem.clear()

    def send_keys(self, input_value):
        """
        Simulates typing into the element.
        """
        elem = self.__get_element(self.by, self.value)
        log.info("🖋 input element: {} 类型{} 值{}  desc：{}".format(input_value, self.by, self.value, self.desc))
        elem.send_keys(input_value)

    def click(self):
        """Clicks the element."""
        elem = self.__get_element(self.by, self.value)
        log.info("🖱 click element: 类型{} 值{}  desc：{}".format(self.by, self.value, self.desc))
        elem.click()

    def submit(self):
        """Submits a form."""
        elem = self.__get_element(self.by, self.value)
        log.info("submit element: 类型{} 值{}  desc：{}".format(self.by, self.value, self.desc))
        elem.submit()

    @property
    def tag_name(self):
        """This element's ``tagName`` property."""
        elem = self.__get_element(self.by, self.value)
        tag_name = elem.tag_name
        log.info("get element tag_name:{} - 类型{} 值{}  desc：{}".format(tag_name, self.by, self.value, self.desc))
        return tag_name

    @property
    def text(self):
        """Clears the text if it's a text entry element."""
        elem = self.__get_element(self.by, self.value)
        text = elem.text
        log.info("get element text:{} -  类型{} 值{}  desc：{}".format(text, self.by, self.value, self.desc))
        return text

    @property
    def size(self):
        """The size of the element."""
        elem = self.__get_element(self.by, self.value)
        size = elem.size
        log.info("get element size:{} -  类型{} 值{}  desc：{}".format(size, self.by, self.value, self.desc))
        return size

    def get_property(self, name):
        """
        Gets the given property of the element.
        """
        elem = self.__get_element(self.by, self.value)
        return elem.get_property(name)

    def get_attribute(self, name):
        """Gets the given attribute or property of the element."""
        elem = self.__get_element(self.by, self.value)
        return elem.get_attribute(name)

    def is_displayed(self):
        """Whether the element is visible to a user."""
        elem = self.__get_element(self.by, self.value)
        return elem.is_displayed()

    def is_selected(self):
        """
        Returns whether the element is selected.

        Can be used to check if a checkbox or radio button is selected.
        """
        elem = self.__get_element(self.by, self.value)
        return elem.is_selected()

    def is_enabled(self):
        """Returns whether the element is enabled."""
        elem = self.__get_element(self.by, self.value)
        return elem.is_enabled()

    def switch_to_frame(self):
        """
        selenium API
        Switches focus to the specified frame
        """
        elem = self.__get_element(self.by, self.value)
        self.driver.switch_to.frame(elem)

    def move_to_element(self):
        """
        selenium API
        Moving the mouse to the middle of an element
        """
        elem = self.__get_element(self.by, self.value)
        ActionChains(self.driver).move_to_element(elem).perform()

    def click_and_hold(self):
        """
        selenium API
        Holds down the left mouse button on an element.
        """
        elem = self.__get_element(self.by, self.value)
        ActionChains(self.driver).click_and_hold(elem).perform()

    def double_click(self):
        """
        selenium API
        Holds down the left mouse button on an element.
        """
        elem = self.__get_element(self.by, self.value)
        ActionChains(self.driver).double_click(elem).perform()

    def context_click(self):
        """
        selenium API
        Performs a context-click (right click) on an element.
        """
        elem = self.__get_element(self.by, self.value)
        ActionChains(self.driver).context_click(elem).perform()

    def drag_and_drop_by_offset(self, x, y):
        """
        selenium API
        Holds down the left mouse button on the source element,
           then moves to the target offset and releases the mouse button.
        :param x: X offset to move to.
        :param y: Y offset to move to.
        """
        elem = self.__get_element(self.by, self.value)
        ActionChains(self.driver).drag_and_drop_by_offset(elem, xoffset=x, yoffset=y).perform()

    def refresh_element(self, timeout=10):
        """
        selenium API
        Refreshes the current page, retrieve elements.
        """
        try:
            timeout_int = int(timeout)
        except TypeError:
            raise ValueError("Type 'timeout' error, must be type int() ")

        elem = self.__get_element(self.by, self.value)
        for i in range(timeout_int):
            if elem is not None:
                try:
                    elem
                except Exception:
                    self.driver.refresh()
                else:
                    break
            else:
                sleep(1)
        else:
            raise TimeoutError("stale element reference: element is not attached to the page document.")

    def select_by_value(self, value):
        """
        selenium API
        Select all options that have a value matching the argument. That is, when given "foo" this
           would select an option like:

           <option value="foo">Bar</option>

           :Args:
            - value - The value to match against

           throws NoSuchElementException If there is no option with specisied value in SELECT
        """
        select_elem = self.__get_element(self.by, self.value)
        Select(select_elem).select_by_value(value)

    def select_by_index(self, index):
        """
        selenium API
        Select the option at the given index. This is done by examing the "index" attribute of an
           element, and not merely by counting.

           :Args:
            - index - The option at this index will be selected

           throws NoSuchElementException If there is no option with specisied index in SELECT
        """
        select_elem = self.__get_element(self.by, self.value)
        Select(select_elem).select_by_index(index)

    def select_by_visible_text(self, text):
        """
        selenium API
        Select all options that display text matching the argument. That is, when given "Bar" this
           would select an option like:

            <option value="foo">Bar</option>

           :Args:
            - text - The visible text to match against

            throws NoSuchElementException If there is no option with specisied text in SELECT
        """
        select_elem = self.__get_element(self.by, self.value)
        Select(select_elem).select_by_visible_text(text)

    def set_text(self, keys):
        """
        appium API
        Sends text to the element.
        """
        elem = self.__get_element(self.by, self.value)
        elem.set_text(keys)
        return self

    @property
    def location_in_view(self):
        """
        appium API
        Gets the location of an element relative to the view.
        Returns:
            dict: The location of an element relative to the view
        """
        elem = self.__get_element(self.by, self.value)
        return elem.location_in_view()

    def set_value(self, value):
        """
        appium API
        Set the value on this element in the application
        """
        elem = self.__get_element(self.by, self.value)
        elem.set_value(value)
        return self

    def input(self, text=""):
        elem = self.__get_element(self.by, self.value)
        elem.send_keys(text)

    def enter(self):
        elem = self.__get_element(self.by, self.value)
        elem.send_keys(Keys.ENTER)

    def select_all(self):
        elem = self.__get_element(self.by, self.value)
        if platform.system().lower() == "darwin":
            elem.send_keys(Keys.COMMAND, "a")
        else:
            elem.send_keys(Keys.CONTROL, "a")

    def cut(self):
        elem = self.__get_element(self.by, self.value)
        if platform.system().lower() == "darwin":
            elem.send_keys(Keys.COMMAND, "x")
        else:
            elem.send_keys(Keys.CONTROL, "x")

    def copy(self):
        elem = self.__get_element(self.by, self.value)
        if platform.system().lower() == "darwin":
            elem.send_keys(Keys.COMMAND, "c")
        else:
            elem.send_keys(Keys.CONTROL, "c")

    def paste(self):
        elem = self.__get_element(self.by, self.value)
        if platform.system().lower() == "darwin":
            elem.send_keys(Keys.COMMAND, "v")
        else:
            elem.send_keys(Keys.CONTROL, "v")

    def backspace(self):
        elem = self.__get_element(self.by, self.value)
        elem.send_keys(Keys.BACKSPACE)

    def delete(self):
        elem = self.__get_element(self.by, self.value)
        elem.send_keys(Keys.DELETE)

    def tab(self):
        elem = self.__get_element(self.by, self.value)
        elem.send_keys(Keys.TAB)

    def space(self):
        elem = self.__get_element(self.by, self.value)
        elem.send_keys(Keys.SPACE)


class Elements(list):

    @property
    def count(self):
        return len(self)

    def __init__(self,
                 by: By = None,
                 value: str = None,
                 driver: WebDriver = None,
                 web_elements: list = None,
                 delay: float = 0.5,
                 timeout: float = 10,
                 interval: float = 0.5):
        if driver:
            self.driver = driver
        if web_elements:
            self.extend(web_elements)
        self.by = by
        self.value = value
        self.delay = delay
        self.timeout = timeout
        self.interval = interval

    def __retry_find(self):
        if (not self.by) or (not self.value):
            raise Exception('元素定位信息不允许为空')

        # 计算重试次数
        retry_count = int(float(self.timeout) / float(self.interval))
        # 延迟查找元素
        if self.delay:
            sleep(self.delay)

        # 重试次数小于1时，不重试，找不到直接抛异常
        if retry_count < 1:
            elements = self.driver.find_elements(self.by, self.value)
            if not elements:
                raise NoSuchElementException(f'By:[ {self.by} ] value:[ {self.value} ]')
            self.extend(elements)
            return self

        # 重试查找元素，元素存在时返回，找不到时重试直到timeout后抛出异常
        for i in range(retry_count):
            if i > 0:
                sleep(self.interval)
            elements = self.driver.find_elements(self.by, self.value)
            if not elements:
                if i == (retry_count - 1):
                    raise NoSuchElementException(f'By:[ {self.by} ] value:[ {self.value} ]')
                continue
            self.extend(elements)
            return self

    def __get__(self, instance, owner):
        if instance is None:
            raise Exception('持有类没有实例化')

        self.driver = instance.driver
        return self.__retry_find()

    def __set__(self, instance, value):
        raise NotImplementedError('老老实实send_keys()吧')

    def __getitem__(self, index: int):
        item = super().__getitem__(index)
        if isinstance(item, Element):
            return item
        elif isinstance(item, WebElement):
            return Element(driver=self.driver, web_element=item)
        else:
            raise Exception(f'仅支持uitesttoolkit.Element和selenium.WebElement，object:[ {item} ]')




