import sys
import time
import os
import pytest
from poium import Page
from poium.common import logging
from os.path import dirname, abspath
from test_dir.test_001_boss_login import check_boss_login
# from test_dir.test_001_boss_login import test_boss_login
sys.path.insert(0, dirname(dirname(abspath(__file__))))
from page.boss_page import HomePage, CustomerCenter


"""
    测试案例，Boss登录页面
"""


def setup():
    pass


def test_create_merchant(browser, test_url='https://boss-uat.lifekh.com/boss#/home'):
    page_home = HomePage(browser)
    page_home.get(test_url)
    time.sleep(1)
    check_boss_login(browser, test_url)
    current_url = browser.current_url
    if current_url == test_url:
        print('pass')
    else:
        print('failure')
    assert browser.title == 'boss管理后台'


if __name__ == '__main__':
    file_name = os.path.split(__file__)[-1]
    pytest.main(['-s', './{}'.format(file_name)])
