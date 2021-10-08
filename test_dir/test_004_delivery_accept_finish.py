import sys
import time
import os
import pytest
from util.log import Log
from os.path import dirname, abspath
from util.public_util import MySQL
from test_dir.test_001_boss_login import check_boss_login
sys.path.insert(0, dirname(dirname(abspath(__file__))))
from page.boss_page import HomePage, DeliveryManagementPage


"""
    测试案例，Boss端外卖代接单，代完成订单
"""
log = Log()


def setup():
    pass


def test_replace_accept_finish(browser,
                               boss_delivery_order_url='https://boss-uat.lifekh.com/boss/order/delivery-order',
                               store_no: str = ''):
    page_home = HomePage(browser)
    page_delivery_management = DeliveryManagementPage(browser)
    page_home.get(boss_delivery_order_url)
    time.sleep(1)
    get_store_wait_accept_ords('MS1320194834269442048')
    check_boss_login(browser, boss_delivery_order_url)

    # 判断当前是否在外卖管理 - 订单管理 - 外卖订单页面
    if boss_delivery_order_url != browser.current_url:
        page_delivery_management.get(boss_delivery_order_url)
        log.info('打开网址：{}'.format(boss_delivery_order_url))
        time.sleep(3)

    if browser.current_url == boss_delivery_order_url:
        page_delivery_management.wait_accept_order_search.click()
        # 此处需要补充获取数据库指定门店中的待接单的商家数据

        page_delivery_management.order_no_input = '12345689'
        page_delivery_management.search_btn.click()
        time.sleep(3)
        # 待补充查询后

    else:

        print('failure')
    assert browser.title == 'boss管理后台'


def get_store_wait_accept_ords(store_no: str):
    mysql = MySQL()
    ords = mysql.select(
                 "SELECT order_no FROM `lifekh_takeaway_uat`.`takeaway_order`"
                 "WHERE `store_no` = '{}' "
                 "AND `biz_state` = '10' ORDER BY `update_time` DESC ".format(store_no))

    return ords


if __name__ == '__main__':
    get_store_wait_accept_ords('MS1430090942563762176')
    file_name = os.path.split(__file__)[-1]
    pytest.main(['-s', './{}'.format(file_name)])
