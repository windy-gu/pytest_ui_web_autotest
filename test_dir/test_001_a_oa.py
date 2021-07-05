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
    page.search_input.send_keys("2021-06")
    page.search_input.send_keys(Keys.ENTER)
    list_int = int(str(page.list_operator_count.get_attribute("textContent"))[1: -1])
    # page.search_button.click()

    time.sleep(1)
    need_list = []
    hour = 0
    for n in range(list_int):
        xpath = '//tbody[@class="ant-table-tbody"]/tr['+str(n+1)+']/td[2]'
        old_handle = browser.current_window_handle
        print(n)
        print(old_handle)

        NewPageElement(xpath=xpath, describe='list_'+str(n+1)).click()  # 加班list数据
        time.sleep(3)
        all_handles = browser.window_handles
        for i in range(len(all_handles)):
            if old_handle == all_handles[i]:
                pass
            else:
                browser.switch_to_window(all_handles[i])
        print(all_handles)
        time.sleep(1)
        person_xpath = '//tbody/tr[5]/td[4]/div[1]'
        overtime_long = '//tbody/tr[11]/td[4]/div[1]'
        overtime_date = '//tbody/tr[13]/td[4]/div[1]'

        name = NewPageElement(xpath=person_xpath).text
        time.sleep(1)
        long = NewPageElement(xpath=overtime_long).text
        time.sleep(1)
        date = NewPageElement(xpath=overtime_date).text
        time.sleep(1)
        need_list.append(name + '_' + long + '_' + date)
        hour = hour + float(long)
        # print(need_list)

        browser.close()
        browser.switch_to_window(old_handle)

        if n+1 >= 11:
            break
    print(need_list)
    print("你的加班工时时长：" + hour)
    time.sleep(3)
#
#
# def calculate_overtime(data: list):
#     hour = 0
#     for i in range(len(data)):
#         i[4:]
#
#
#


if __name__ == '__main__':
    list_data = ['古小锋_2.5_From 2021-06-2919:30To2021-06-2922:00',
                 '古小锋_5.0_From 2021-06-2713:30To2021-06-2718:30',
                 '古小锋_2.5_From 2021-06-2219:30To2021-06-2222:00',
                 '古小锋_1.5_From 2021-06-1719:30To2021-06-1721:00',
                 '古小锋_3.0_From 2021-06-1519:30To2021-06-1522:30',
                 '古小锋_1.5_From 2021-06-0419:30To2021-06-0421:00',
                 '古小锋_5.5_From 2021-06-0119:30To2021-06-0201:00']
    s = '共8条'
    print(s[0:-1])
    file_name = os.path.split(__file__)[-1]
    pytest.main(['-s', './{}'.format(file_name)])
