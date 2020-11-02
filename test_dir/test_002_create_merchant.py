import sys
import time
import os
import pytest
from poium import Page
from poium.common import logging
from os.path import dirname, abspath
from test_dir.test_001_boss_login import check_boss_login
sys.path.insert(0, dirname(dirname(abspath(__file__))))
from page.boss_page import HomePage, CustomerCenterPage


"""
    测试案例，Boss-创建商户
"""


def setup():
    pass


def test_create_merchant(browser, test_url='https://boss-uat.lifekh.com/boss#/home'):
    page_home = HomePage(browser)
    page_customer_center = CustomerCenterPage(browser)
    page_home.get(test_url)
    time.sleep(1)
    check_boss_login(browser, test_url)
    current_url = browser.current_url
    if current_url == test_url:
        page_home.customer_center.click()
        page_customer_center.merchant_management.click()
        page_customer_center.merchant_list.click()
        page_customer_center.add_merchant.click()

        # 商户基本信息
        page_customer_center.merchant_name_en = '12345'
        page_customer_center.merchant_name_zh = '12345'
        page_customer_center.merchant_name_cb = '12345'
        page_customer_center.merchant_style_person.click()
        page_customer_center.merchant_charge_name = 'auto-test'
        page_customer_center.merchant_charge_surname = 'UI'
        page_customer_center.merchant_certificate_type.click()
        page_customer_center.merchant_passport.click()
        page_customer_center.merchant_certificate_no = '1234567'
        page_customer_center.merchant_certificate_photo = '/Users/windy/Downloads/test_photo/tofu.jpeg'
        page_customer_center.merchant_statue_open.click()
        time.sleep(1)

        # 业务协议
        page_customer_center.merchant_business_yumnow.click()
        page_customer_center.merchant_connect_name = '111111'
        page_customer_center.merchant_connect_surname = '111111'
        page_customer_center.merchant_connect_phoneNo = '111111'
        page_customer_center.merchant_contract_photo = '/Users/windy/Downloads/test_photo/tofu.jpeg'
        time.sleep(1)

        # 管理账号信息
        page_customer_center.merchant_login_phoneNo = '1111112'
        page_customer_center.merchant_email = '1111112'
        page_customer_center.merchant_user_name = '1111112'
        page_customer_center.merchant_password = '1111112'
        page_customer_center.merchant_password_second = '1111112'
        time.sleep(1)

        page_customer_center.merchant_submit.click()

    else:
        print('failure')
    assert browser.title == 'boss管理后台'


if __name__ == '__main__':
    file_name = os.path.split(__file__)[-1]
    pytest.main(['-s', './{}'.format(file_name)])
