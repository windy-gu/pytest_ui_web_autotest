# author:windy
# datetime:2021/4/13 9:53 上午
# software: PyCharm

import os
import platform
from selenium import webdriver


def run_system():
    """
    返回到当前系统运行的系统，
    win系统 return windows
    mac系统 return Darwin
    linux系统 return linux
    """
    return platform.system()


def get_driver_file_path():
    """
    根据当前执行的环境，获取到工程目录下的浏览器driver路径
    """
    return driver_last_version(system=run_system())


def driver_last_version(browser: str = 'chrome', system: str = 'darwin'):
    """
    根据浏览器类型，输出浏览器驱动在项目工作中的路径地址
    """
    global opera_system
    if system.lower() == 'windows':
        opera_system = 'win'
        driver_dir = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__))), browser, opera_system)
        version_last = os.listdir(driver_dir)[-1]  # 获取当前最新浏览器版本号
        file = 'chromedriver.exe'
        driver_file_path = os.path.join(driver_dir, version_last, file)  # 将驱动文件目录，版本号和驱动文件，输出文件路径
        return driver_file_path

    elif system.lower() == 'darwin':
        opera_system = 'mac'
        # 将驱动目录，浏览器类型和操作系统，输出文件路径
        driver_dir = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__))), browser, opera_system)
        version_last = os.listdir(driver_dir)[-1]  # 获取当前最新浏览器版本号
        file = 'chromedriver'
        driver_file_path = os.path.join(driver_dir, version_last, file)  # 将驱动文件目录，版本号和驱动文件，输出文件路径
        return driver_file_path

    elif system.lower() == 'linux':
        opera_system = 'linux'
        # 将驱动目录，浏览器类型和操作系统，输出文件路径
        driver_dir = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__))), browser, opera_system)
        version_last = os.listdir(driver_dir)[-1]  # 获取当前最新浏览器版本号
        file = 'chromedriver'
        driver_file_path = os.path.join(driver_dir, version_last, file)  # 将驱动文件目录，版本号和驱动文件，输出文件路径
        return driver_file_path

    else:
        raise Exception("运行操作系统，找不到对应driver驱动")


if __name__ == '__main__':
    d = webdriver.Chrome()
    d.maximize_window()
    print(get_driver_file_path())