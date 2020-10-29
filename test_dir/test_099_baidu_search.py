import sys
from time import sleep
from os.path import dirname, abspath
sys.path.insert(0, dirname(dirname(abspath(__file__))))
from page.baidu_page import BaiduPage


# class TestBaiduSearch:
"""
    测试案例，百度页面上搜索
"""

"""
    setup_module/teardown_module/setup_function
    teardown_function/setup/teardown有点类型unittest等
"""


def setup_module():
    print("Setup_module========")


def teardown_module():
    print("Teardown_module========")


def setup_function():
    print("Setup_function========")


def teardown_function():
    print("Teardown_function========")


def setup():
    print("Setup=====")


def teardown():
    print("Teardown========")


def test_baidu_search_case(browser, base_url):
    page = BaiduPage(browser)
    page.get(base_url)
    page.search_input = 'pytest'
    page.search_button.click()
    sleep(2)
    assert browser.title == 'pytest_百度搜索'
