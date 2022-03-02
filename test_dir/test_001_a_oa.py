import os
import sys
import time
import pytest
import datetime
from page.oa_page import OAPage
from util.log import Log
from selenium.webdriver.common.keys import Keys
from os.path import dirname, abspath
from util.web_page_element import Element
sys.path.insert(0, dirname(dirname(abspath(__file__))))


"""
    测试案例，oa登录页面，统计操作人上个月加班时长和调休时长
    这里作为一个public的方法作为所有需要在boss中进行操作的前置方法
"""

log = Log()


# def teardown_module(browser):
#     browser.browser_close()


def test_oa_001_login(browser, url='https://oa.wownow.net/wui/index.html#/?logintype=1&_key=q6nnev',
                      account='guxiaofeng', psw='gxf4843860.'):
    """

    :param browser:
    :param url: 执行自动化的URL地址
    :param account: 账号
    :param psw: 密码
    :return:
    """
    page = OAPage(browser)
    page.get(url)

    # login
    page.login_name = account
    page.login_password = psw
    page.login_btn.click()


def test_oa_002_get_overtime_by_month(browser):
    """
    获取加班工时的testcase
    :param browser:
    :return:
    """
    over_time = auto_choose_style_by_value(browser, style_value='OVER_TIME')
    log.print("加班工时：" + str(over_time))


def test_oa_003_get_day_off_by_month(browser):
    """
    获取调休工时的testcase
    :param browser:
    :return:
    """
    day_off_time = auto_choose_style_by_value(browser, style_value='DAY_OFF')
    # 在进行调休时长获取时，会出现点击不跳转的情况
    log.print("调休工时：" + str(day_off_time))


def auto_choose_style_by_value(browser, style_value: str):
    page = OAPage(browser)
    # 进入：流程 - 我的请求 - S-app 加班申请
    page.door.click_and_hold()
    time.sleep(1)
    page.liucheng.click()
    # page.get("https://oa.wownow.net/wui/index.html#/main/workflow/listMine")
    page.my_request.click()
    time.sleep(1)
    page.my_request.click()

    if style_value == 'OVER_TIME':
        log.print("进入统计加班时间流程")
        page.overtime_application.click()

        # 查询指定条件的加班申请&获取符合条件的数据
        page.search_input.send_keys(get_last_month())
        page.search_input.send_keys(Keys.ENTER)
        time.sleep(1.5)
        list_int = int(str(page.list_operator_count.get_attribute("textContent"))[1: -1])
        time.sleep(1)
        if list_int == 0:
            log.info('{last_month}无数据，统计下一个月数据'.format(last_month=get_last_month()))
            page.clear_search_input_text.click()
            page.search_input.send_keys(time.strftime("%Y-%m"))
            page.search_input.send_keys(Keys.ENTER)
            time.sleep(1.5)
            list_int = int(str(page.list_operator_count.get_attribute("textContent"))[1: -1])
            return operator_by_list(browser, list_int=list_int, style_value=style_value)
        else:
            return operator_by_list(browser, list_int=list_int, style_value=style_value)

    elif style_value == 'DAY_OFF':
        log.print("进入统计调休时间流程")
        page.day_off_application.click()

        # 查询指定条件的加班申请&获取符合条件的数据
        page.search_input.send_keys(get_last_month())
        page.search_input.send_keys(Keys.ENTER)
        time.sleep(1.5)
        list_int = int(str(page.list_operator_count.get_attribute("textContent"))[1: -1])
        time.sleep(1)
        return operator_by_list(browser, list_int=list_int, style_value=style_value)

    else:
        raise Exception('输入style_value，错误。请核对后再执行。当前输入style_value值：%s' % style_value)


def operator_by_list(browser, list_int: int, style_value: str):
    """

    :param browser:
    :param list_int: 待处理的list数量
    :param style_value: 加班or调休类型
    :return:
    """
    hour = 0
    # 根据查询出来的数据，自动处理需要进行循环次数和翻页次数
    outside_loop = int(list_int/10)  # 翻页次数
    inside_loop = int(list_int % 10)  # 单页循环次数

    if outside_loop == 0:
        hour = hour + get_info_by_detail(browser, loop=inside_loop, style_value=style_value)

    else:
        for i in range(outside_loop+1):
            if i < outside_loop:
                hour = hour + get_info_by_detail(browser, loop=10, style_value=style_value)

            else:
                hour = hour + get_info_by_detail(browser, loop=inside_loop, style_value=style_value)

    return hour


def get_info_by_detail(browser, loop: int, style_value: str):
    """
    点击list数据跳转到对应详情页面，获取对应加班或调休的数据信息
    :param browser:
    :param loop:
    :param style_value:
    :return:
    """
    hour = 0
    for n in range(loop):
        if style_value == 'DAY_OFF':
            xpath_state = '//tbody[@class="ant-table-tbody"]/tr[' + str(n + 1) + ']/td[5]/div[1]'
            text_state = Element(xpath=xpath_state).text
        xpath_click = '//tbody[@class="ant-table-tbody"]/tr[' + str(n + 1) + ']/td[2]/div[1]'
        old_handle = browser.current_window_handle  # 获取在点击-list数据前，当前浏览器的handle值
        Element(xpath=xpath_click, describe='list_' + str(n + 1)).click()  # 加班list数据
        time.sleep(2)
        all_handles = browser.window_handles  # 获取在点击-list数据后，当前浏览器的handles值
        old_handle_list = []
        old_handle_list.append(old_handle)

        # 用于判断当前点击是否出现新的弹窗
        if len(old_handle_list) == len(all_handles):
            Element(xpath=xpath_click+'/a[1]', describe='list_' + str(n + 1)).click()  # 加班list数据
            all_handles = browser.window_handles  # 获取在点击-list数据后，当前浏览器的handles值

        for i in range(len(all_handles)):
            if old_handle == all_handles[i]:
                pass
            else:
                browser.switch_to_window(all_handles[i])  # 用于切换到新打开的窗口
        time.sleep(1)
        if style_value == 'OVER_TIME':
            # 获取名称和加班时长数据
            person_xpath = '//tbody/tr[5]/td[4]/div[1]'
            overtime_long = '//tbody/tr[11]/td[4]/div[1]'
            # overtime_date = '//tbody/tr[13]/td[4]/div[1]'

        elif style_value == 'DAY_OFF':
            # 获取名称和调休时长数据
            if text_state == '归档':
                person_xpath = '//tbody/tr[3]/td[6]/div[1]'
                overtime_long = '//tbody/tr[13]/td[4]/div[1]'
            else:
                person_xpath = '//tbody/tr[5]/td[6]/div[1]'
                overtime_long = '//tbody/tr[16]/td[4]/div[1]'

        # name = Element(xpath=person_xpath).text
        time.sleep(0.5)
        browser.refresh()
        long = Element(xpath=overtime_long).text
        time.sleep(0.5)
        # date = Element(xpath=overtime_date).text
        # need_list.append(name + '_' + long + '_' + date)
        hour = hour + float(long)

        # 关闭detail页面切换回到list页面
        browser.close()
        time.sleep(1)
        browser.switch_to_window(old_handle)
        time.sleep(1)

    return float(hour)


def get_last_month():
    """
    此函数返回上一个月，格式：yyyy-MM
    :return:
    """
    time_now = time.strftime("%Y-%m-%d", time.localtime())
    time_now_2 = time.localtime(time.time())
    first_day = datetime.date(time_now_2.tm_year, time_now_2.tm_mon, 1)
    pre_month = str(first_day - datetime.timedelta(days=1))  # timedelta是一个不错的函数
    last_month = pre_month[0:-3]
    return last_month


if __name__ == '__main__':
    file_name = os.path.split(__file__)[-1]
    pytest.main(['-s', '-v', './{}'.format(file_name)])
