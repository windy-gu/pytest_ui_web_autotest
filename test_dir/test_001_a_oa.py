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
    page.overtime_application.click()
    page.search_input.send_keys("2021-06")
    # page.search_button.click()

    time.sleep(1)
    need_list = []
    for n in range(10):
        xpath = '//tbody[@class="ant-table-tbody"]/tr['+str(n+1)+']/td[2]'
        old_handle = browser.current_window_handle
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
        long = NewPageElement(xpath=overtime_long).text
        date = NewPageElement(xpath=overtime_date).text
        need_list.append(name + '_' + long + '_' + date)
        print(need_list)

        browser.close()
        browser.switch_to_window(old_handle)

        if n+1 >= 11:
            break
    print(need_list)
    time.sleep(3)


if __name__ == '__main__':
    file_name = os.path.split(__file__)[-1]
    pytest.main(['-s', './{}'.format(file_name)])
