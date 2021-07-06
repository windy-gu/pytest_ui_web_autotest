import os
import sys
import hmac
import time
import base64
import struct
import pytest
import hashlib
from time import sleep
from poium.common import logging
from os.path import dirname, abspath
sys.path.insert(0, dirname(dirname(abspath(__file__))))
from page.oa_page import OAPage
from selenium.webdriver.common.keys import Keys
from poium import Page, PageElement, PageElements, NewPageElement


"""
    测试案例，Boss登录页面
    这里作为一个public的方法作为所有需要在boss中进行操作的前置方法
"""


def test_oa_login(browser, url='https://oa.wownow.net/wui/index.html#/?logintype=1&_key=q6nnev',
                  account='guxiaofeng', psw='gxf4843860.'):
    page = OAPage(browser)
    page.get(url)
    page.login_name = account
    page.login_password = psw
    page.login_btn.click()
    page.door.click_and_hold()
    time.sleep(1)
    page.liucheng.click()
    page.my_request.click()
    time.sleep(1)
    page.my_request.click()
    page.overtime_application.click()
    page.search_input.send_keys("2020")
    page.search_input.send_keys(Keys.ENTER)
    list_int = int(str(page.list_operator_count.get_attribute("textContent"))[1: -1])

    time.sleep(1)
    get_info_from_list(browser, list_int=list_int)
    time.sleep(3)


def get_info_from_list(browser, list_int: int):
    """

    :param browser:
    :param list_int:
    :return:
    """
    page = OAPage(browser)
    need_list = []
    hour = 0
    outside_loop = int(list_int/10)
    inside_loop = list_int % 10

    print(outside_loop)
    print(inside_loop)

    if outside_loop == 0:
        hour = hour + get_info(browser, loop=inside_loop)
        # pass
    else:
        for i in range(outside_loop+1):
            if i < outside_loop:
                hour = hour + get_info(browser, loop=10)

            else:
                hour = hour + get_info(browser, loop=inside_loop)
    print("加班工时：" + str(hour))


def get_info(browser, loop: int):
    hour = 0
    for n in range(loop):
        xpath = '//tbody[@class="ant-table-tbody"]/tr[' + str(n + 1) + ']/td[2]'
        old_handle = browser.current_window_handle  # 获取在点击-list数据前，当前浏览器的handle值
        NewPageElement(xpath=xpath, describe='list_' + str(n + 1)).click()  # 加班list数据
        time.sleep(3)
        all_handles = browser.window_handles  # 获取在点击-list数据后，当前浏览器的handles值
        for i in range(len(all_handles)):
            if old_handle == all_handles[i]:
                pass
            else:
                browser.switch_to_window(all_handles[i])
        time.sleep(1)
        person_xpath = '//tbody/tr[5]/td[4]/div[1]'
        overtime_long = '//tbody/tr[11]/td[4]/div[1]'
        overtime_date = '//tbody/tr[13]/td[4]/div[1]'

        name = NewPageElement(xpath=person_xpath).text
        time.sleep(1)
        long = NewPageElement(xpath=overtime_long).text
        time.sleep(1)
        date = NewPageElement(xpath=overtime_date).text
        # need_list.append(name + '_' + long + '_' + date)
        hour = hour + float(long)
        # print(need_list)

        browser.close()
        time.sleep(1)
        browser.switch_to_window(old_handle)
        time.sleep(1)

        return float(long)


if __name__ == '__main__':
    a = 23
    print(a/10)
    print(a % 10)
    file_name = os.path.split(__file__)[-1]
    pytest.main(['-s', './{}'.format(file_name)])
