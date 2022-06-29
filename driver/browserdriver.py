# author:windy
# datetime:2021/4/13 9:53 上午
# software: PyCharm

import os
import re
import requests
import platform
from util.log import Log
from selenium import webdriver


log = Log()


def chrome_driver(driver_path=None,
                  headless=None,
                  user_agent=None,
                  maximize=True
                  ):

    """

    :param driver_path:         使用项目工程的driver驱动
    :param headless:            无头模式
    :param user_agent:          自定义user_agent
    :param maximize:            是否最大化窗口
    :return:
    """
    options = webdriver.ChromeOptions()
    options.headless = headless
    options.set_capability('noRetest', True)
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-infobars')  # 防止Chrome显示“Chrome正在被自动化软件控制”的通知，但似乎不会生效
    options.add_argument('--disable-popup-blocking')
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-dev-shm-usage')  # overcome limited resource problems
    options.add_argument('--start-maximized')  # open Browser in maximized mode
    options.add_argument('--no-sandbox')  # bypass OS security model

    if user_agent:  # User-agent不为空，则添加指定user-agent
        options.add_argument(f'--user-agent={user_agent}')
    DRIVER_TEMP = get_driver_file_path()
    DRIVER_LAST_VERSION_PATH = DRIVER_TEMP[0]
    DRIVER_LAST_VERSION = DRIVER_TEMP[1]

    # 判断当前Chrome是否为最新版本
    get_chrome_version_info(DRIVER_LAST_VERSION)

    executable_path = driver_path or DRIVER_LAST_VERSION_PATH

    if headless:
        log.info('无头模式启动chrome driver')
    else:
        log.info('启动chrome driver')

    wd = webdriver.Chrome(executable_path=executable_path,
                          options=options)

    if maximize:
        log.info('窗口全屏化')
        wd.maximize_window()
        log.info('浏览器名称：{}'.format(wd.capabilities["browserName"]))
        log.info('浏览器版本号：{}'.format(wd.capabilities["browserVersion"]))

    # atexit.register(wd.quit())  # always quit driver when done
    return wd


def get_chrome_version_info(current_chrome_driver_version: str):
    """
    通过获取chromedriver页面中的版本号跟本地版本，提示更新
    :param current_chrome_driver_version:
    :return:
    """
    api_url = 'http://chromedriver.storage.googleapis.com/?delimiter=/&prefix='
    download_url = 'http://chromedriver.storage.googleapis.com/index.html'
    headers = {
        'Connection': 'keep-alive',
        'Accept-Encoding': 'Accept-Encoding',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Accept': '*/*',
        'Referer': 'http://chromedriver.storage.googleapis.com/index.html',
        'Host': 'chromedriver.storage.googleapis.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/94.0.4606.81 Safari/537.36'
    }
    r = requests.get(url=api_url, headers=headers)
    text = r.text
    a_text = text.split('<Prefix>')

    # 获取到chrome中版本相关数据
    temp_text = []

    # 判断跟本地driver驱动和网页版本中驱动版本中差异
    over_version = []
    version = current_chrome_driver_version
    for i in range(len(a_text)):
        if '/</Prefix>' in a_text[i]:
            temp_text.append(a_text[i].split('/</Prefix>')[0])

    for i in range(len(temp_text)):
        temp_version_int = version.split('.')[0]
        # 获取版本号.前的数字值跟本地已有的Chrome版本号进行对比
        if '.' in temp_text[i]:
            temp_list_int = temp_text[i].split('.')[0]
            temp_int = int(temp_version_int) - int(temp_list_int)
            # 若是两个版本差值<=0，则添加在over_version中
            if temp_int <= 0:
                if version != temp_text[i]:
                    over_version.append(temp_text[i])

    if len(over_version) > 0:
        log.warn('本地Chrome浏览器驱动，可能不是最新版本。若Chrome浏览器无法启动，请手动更新Chrome驱动')
        log.warn('本地Chrome浏览器驱动版本：%s' % version)
        log.warn('当前可更新或近期的Chrome浏览器驱动版本：%s，驱动下载地址：%s' % (str(over_version), download_url))
    else:
        log.info('本地Chrome浏览器驱动，可以正常使用')


def firefox_driver():
    ...


def run_system():
    """
    返回到当前系统运行的系统，
    win系统 return windows
    mac系统 return Darwin
    linux系统 return linux
    """
    return platform.system()


def get_driver_file_path(browser: str = 'chrome'):
    """
    根据当前执行的环境，获取到工程目录下的浏览器driver路径
    """
    return driver_last_version(browser=browser, system=run_system())


def driver_last_version(browser: str = 'chrome', system: str = 'darwin'):
    """
    根据浏览器类型，输出浏览器驱动在项目工作中的路径地址
    :param browser:     浏览器类型，默认值：chrome
    :param system:      操作系统类型，默认值：darwin
    :return:
    """
    global operating_system
    driver_dir_path = os.path.abspath(os.path.join(os.path.dirname(__file__)))
    if system.lower() == 'windows':
        operating_system = 'win'
        file = 'chromedriver.exe'

    elif system.lower() == 'darwin':
        operating_system = 'mac'
        file = 'chromedriver'

    elif system.lower() == 'linux':
        operating_system = 'linux'
        file = 'chromedriver'

    else:
        raise Exception("找不到对应driver驱动")

    driver_dir = os.path.join(driver_dir_path, browser, operating_system)  # 将驱动目录，浏览器类型和操作系统，输出文件路径
    version_last = os.listdir(driver_dir)  # 根据驱动目录获取目录下浏览器版本号名称
    version_last.sort(key=lambda l: int(re.findall('\d+', l)[0]))  # 排序。优化了str字符串中，99>100排序问题
    driver_file_path = os.path.join(driver_dir, version_last[-1], file)  # 将驱动文件目录，版本号和驱动文件，输出文件路径
    # log.info('本地Chrome浏览器驱动版本List:' + str(driver_file_path))
    return driver_file_path, version_last[-1]


if __name__ == '__main__':
    print(get_driver_file_path())
