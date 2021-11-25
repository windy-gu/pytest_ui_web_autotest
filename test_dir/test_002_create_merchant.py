import sys
import time
import os
import pytest
from os.path import dirname, abspath
from test_dir.test_001_boss_login import check_boss_login
from util.public_util import random_text_base_date, get_phone_number_cambodia, get_email
sys.path.insert(0, dirname(dirname(abspath(__file__))))
from page.boss_page import HomePage, CustomerCenterPage


"""
    测试案例，Boss-创建商户
"""


def setup():
    pass


def test_create_merchant(browser, test_url='https://boss-uat.lifekh.com/boss/home'):
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
        page_customer_center.merchant_name_en = random_text_base_date(pre='UITest_Merchant', suffix='en')
        page_customer_center.merchant_name_zh = random_text_base_date(pre='UITest_Merchant', suffix='zh')
        page_customer_center.merchant_name_cb = random_text_base_date(pre='UITest_Merchant', suffix='cb')
        page_customer_center.merchant_style_person.click()
        page_customer_center.merchant_charge_name = 'UI_Tester'
        page_customer_center.merchant_certificate_type.click()
        page_customer_center.merchant_passport.click()
        page_customer_center.merchant_certificate_no = 'UITest_12345678'
        page_customer_center.merchant_certificate_photo = '/Users/windy/Downloads/photo/text.png'
        page_customer_center.merchant_statue_open.click()
        time.sleep(1)

        # 业务协议
        page_customer_center.merchant_business_first_merchant.click()
        page_customer_center.merchant_business_li_list_4.click()
        page_customer_center.merchant_connect_name = 'Tester'
        page_customer_center.merchant_connect_surname = 'UI'
        page_customer_center.merchant_connect_phoneNo = '010111222'
        page_customer_center.merchant_contract_photo = '/Users/windy/Downloads/photo/text.png'
        time.sleep(1)

        # 管理账号信息
        page_customer_center.merchant_login_phoneNo = get_phone_number_cambodia(prefix=False)
        page_customer_center.merchant_email = get_email()
        page_customer_center.merchant_user_name = random_text_base_date(pre='UITester')
        page_customer_center.merchant_password = '123456'
        page_customer_center.merchant_password_second = '123456'
        time.sleep(1)

        page_customer_center.merchant_submit.click()

        time.sleep(5)

    else:
        print('failure')
    assert browser.title == 'boss管理后台'


if __name__ == '__main__':
    file_name = os.path.split(__file__)[-1]
    pytest.main(['-s', './{}'.format(file_name)])
