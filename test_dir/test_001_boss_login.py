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
from page.boss_page import BossLoginPage, HomePage


"""
    测试案例，Boss登录页面
    这里作为一个public的方法作为所有需要在boss中进行操作的前置方法
"""


def test_boss_login(browser, url='https://boss-uat.lifekh.com/boss#/login',
                    account='jmeter', psw='Jmeter123', google_key='BONOHGS6QNHS7V4Y'):
    page = BossLoginPage(browser)
    page.get(url)
    page.boss_login_name = account
    page.boss_login_password = psw
    page.login_button.click()
    google_code = google_security_code(google_key)
    page.google_code = google_code
    page.login_confirm_button.click()
    sleep(2)
    change_language(browser, language='zh')
    assert browser.title == 'boss管理后台'


def google_security_code(key: str):
    """
    获取实时Google身份验证器密码
    :param key:密钥
    :return:
    """
    secret_key = base64.b32decode(key, True)
    intervals_no = int(time.time()) // 30
    msg = struct.pack(">Q", intervals_no)
    h = hmac.new(secret_key, msg, hashlib.sha1).digest()
    o = ord(chr(h[19])) & 15
    h = (struct.unpack(">I", h[o:o + 4])[0] & 0x7fffffff) % 1000000
    google_code = '%06d' % h
    return google_code


def change_language(browser, language='zh'):
    """

    :param browser:
    :param language:
    :return:
    """
    page = HomePage(browser)
    language_text = page.language_text_span.text
    if language == language_text:
        logging.info('当前Boss语言，与所需执行的语言一致。当前Boss语言：{}，所需切换的语言：{}。'.format(language_text, language))
    else:
        logging.info('当前Boss语言，与所需执行的语言不一致。当前Boss语言：{}，所需切换的语言：{}。'.format(language_text, language))
        logging.info('进行切换Boss语言操作。')
        page.language_button_span.click()
        if language == 'zh':
            page.language_selector_zh.click()
        else:
            page.language_selector_en.click()


def check_boss_login(browser, url, need_login=True):
    if url != browser.current_url:
        logging.info('测试URL地址为重定向到Boss登录地址')
        if need_login is True:
            logging.info('need_login：{}，执行Boss登录流程'.format(need_login))
            test_boss_login(browser=browser)
        else:
            logging.info('need_login：{}，不执行Boss登录流程'.format(need_login))
    else:
        logging.info('测试URL地址与当前URL地址一致')


if __name__ == '__main__':
    key = google_security_code('ZAE5JSMSOYMEYAY5')
    print(key)
    file_name = os.path.split(__file__)[-1]
    pytest.main(['-s', './{}'.format(file_name)])
