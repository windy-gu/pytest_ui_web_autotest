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
                               store_no: str = 'MS1320194834269442048'):
    page_home = HomePage(browser)
    page_delivery_management = DeliveryManagementPage(browser)
    page_home.get(boss_delivery_order_url)
    time.sleep(1)

    # 校验boss是否登录
    check_boss_login(browser, boss_delivery_order_url)

    # 判断当前是否在外卖管理 - 订单管理 - 外卖订单页面
    if boss_delivery_order_url != browser.current_url:
        page_delivery_management.get(boss_delivery_order_url)
        time.sleep(3)
    if boss_delivery_order_url == browser.current_url:
        # 进入到待门店接单流程
        page_delivery_management.wait_accept_order_tab.click()
        time.sleep(3)

        ords = get_store_wait_accept_ords(store_no)
        if len(ords) >= 1:
            log.info('当前门店：{} 存在 待接单的订单：{}'.format(store_no, str(ords)))
            for i in range(len(ords)):
                page_delivery_management.order_no_input.clear()
                page_delivery_management.order_no_input = ords[i]
                page_delivery_management.search_btn.click()
                time.sleep(3)

                # 判断操作list区域元素是否存在
                if page_delivery_management.opera_list.check_element():
                    page_delivery_management.ord_accept_list.click()
        else:
            log.info('当前门店：{} 无 待接单的订单'.format(store_no))


def get_store_wait_accept_ords(store_no: str):
    """
    获取指定门店 - 待接单的订单号
    :param store_no:门店标号
    :return:订单号，可以为空
    """
    mysql = MySQL()
    ords = mysql.select(
                 "SELECT order_no FROM `lifekh_takeaway_uat`.`takeaway_order`"
                 "WHERE `store_no` = '{}' "
                 "AND `biz_state` = '10' ORDER BY `update_time` DESC ".format(store_no))
    ords_list = []
    if isinstance(ords, list):
        for i in range(len(ords)):
            ords_list.append(ords[i]['order_no'])
    else:
        log.info('门店：{},当前无待接单订单'.format(store_no))
    return ords_list


if __name__ == '__main__':
    get_store_wait_accept_ords('MS1430090942563762176')
    file_name = os.path.split(__file__)[-1]
    pytest.main(['-s', './{}'.format(file_name)])
