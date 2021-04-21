# author:windy
# datetime:2021/4/13 9:53 上午
# software: PyCharm

import os
import atexit
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

    :param driver_file_path:    使用项目工程的driver驱动
    :param headless:            无头模式
    :param user_agent:          自定义user_gent
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
    wd = webdriver.Chrome()

    if user_agent:  # User-agent不为空，则添加指定user-agent
        options.add_argument(f'--user-agent={user_agent}')

    DRIVER_LAST_VERSION_PATH = get_driver_file_path()
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

    atexit.register(wd.quit())  # always quit driver when done
    return wd


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
    """
    global opera_system
    driver_dir_path = os.path.abspath(os.path.join(os.path.dirname(__file__)))
    if system.lower() == 'windows':
        opera_system = 'win'
        file = 'chromedriver.exe'

    elif system.lower() == 'darwin':
        opera_system = 'mac'
        file = 'chromedriver'

    elif system.lower() == 'linux':
        opera_system = 'linux'
        file = 'chromedriver'

    else:
        raise Exception("运行操作系统，找不到对应driver驱动")

    driver_dir = os.path.join(driver_dir_path, browser, opera_system)  # # 将驱动目录，浏览器类型和操作系统，输出文件路径
    version_last = os.listdir(driver_dir)  # 获取当前最新浏览器版本号
    version_last.sort()  # 排序
    driver_file_path = os.path.join(driver_dir, version_last[-1], file)  # 将驱动文件目录，版本号和驱动文件，输出文件路径
    return driver_file_path


if __name__ == '__main__':
    # d = webdriver.Chrome()
    # d.maximize_window()
    print(get_driver_file_path())