import sys
import time
import os
import pytest
from poium import Page
from poium.common import logging
from os.path import dirname, abspath
from util.public_util import random_text_base_date, get_phone_number_cambodia
from test_dir.test_001_boss_login import check_boss_login
sys.path.insert(0, dirname(dirname(abspath(__file__))))
from page.boss_page import HomePage, YumnowManagementPage


"""
    测试案例，Boss端外卖代接单，代完成订单
"""


def setup():
    pass


def test_replace_accept_finish(browser, boss_delivery_order_url='https://boss-uat.lifekh.com/boss/order/delivery-order'):
    page_home = HomePage(browser)
    page_yumnow_management = YumnowManagementPage(browser)
    page_home.get(boss_delivery_order_url)
    time.sleep(1)
    check_boss_login(browser, boss_delivery_order_url)
    current_url = browser.current_url
    if current_url == boss_delivery_order_url:
        page_home.yumnow_management.click()
        page_yumnow_management.store_management.click()
        page_yumnow_management.store_list.click()
        page_yumnow_management.add_merchant.click()

        # 账号信息
        page_yumnow_management.merchant_name_en = random_text_base_date(pre='UITest_Merchant', suffix='en')
        page_yumnow_management.merchant_name_zh = random_text_base_date(pre='UITest_Merchant', suffix='zh')
        page_yumnow_management.merchant_name_cb = random_text_base_date(pre='UITest_Merchant', suffix='cb')
        page_yumnow_management.merchant_style_person.click()
        page_yumnow_management.merchant_charge_name = 'Tester'
        page_yumnow_management.merchant_charge_surname = 'UI'
        page_yumnow_management.merchant_certificate_type.click()
        page_yumnow_management.merchant_passport.click()
        page_yumnow_management.merchant_certificate_no = 'UITest_12345678'
        page_yumnow_management.merchant_certificate_photo = '/Users/windy/Downloads/test_photo/tofu.jpeg'
        page_yumnow_management.merchant_statue_open.click()
        time.sleep(1)

        # 门店信息
        page_yumnow_management.merchant_business_yumnow.click()
        page_yumnow_management.merchant_connect_name = 'Tester'
        page_yumnow_management.merchant_connect_surname = 'UI'
        page_yumnow_management.merchant_connect_phoneNo = '010111222'
        page_yumnow_management.merchant_contract_photo = '/Users/windy/Downloads/test_photo/tofu.jpeg'
        time.sleep(1)

        # 管理账号信息
        page_yumnow_management.merchant_login_phoneNo = get_phone_number_cambodia(prefix=False)
        page_yumnow_management.merchant_email = '111222333@qq.com'
        page_yumnow_management.merchant_user_name = random_text_base_date(pre='UITester')
        page_yumnow_management.merchant_password = '123456'
        page_yumnow_management.merchant_password_second = '123456'
        time.sleep(1)

        page_yumnow_management.merchant_submit.click()

        time.sleep(5)

    else:
        print('failure')
    assert browser.title == 'boss管理后台'


if __name__ == '__main__':
    file_name = os.path.split(__file__)[-1]
    pytest.main(['-s', './{}'.format(file_name)])
