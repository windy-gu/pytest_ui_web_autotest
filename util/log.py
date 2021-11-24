import os
import sys
import time
import platform
import logging.handlers
from colorama import Fore, Style


class Log():
    """日志模块，在log路径下生成log文件，以小时分割。同时控制台也会打印，当使用使用unittest添加用例调用HTMLTest报告模块时
    控制台的输出内容会被HTMLTest报告模块接受而不再控制台显示
    """

    def __init__(self, name='log'):
        self.logger = logging.getLogger(name)

    def _print_console(self, level, message: str):
        # 创建一个log
        # log_file_path = (os.path.dirname(os.path.dirname(__file__))) + '/log/' \
        #                 + time.strftime('%Y-%m-%d') + '.log'  # log文件目录

        # logger = logging.getLogger(__name__)

        # 设置日志记录级别
        self.logger.setLevel(logging.DEBUG)

        # 创建一个handler，设置输出日志的级别，且设置输出日志的格式，用于写入日志文件
        # FILE_HANDLER = logging.FileHandler(log_file_path, 'a', encoding='utf-8')
        # FILE_HANDLER.setLevel(logging.DEBUG)
        # FILE_HANDLER.setFormatter(logging.Formatter('%(asctime)s - %(filename)s - %(name)s - %(levelname)s - %(message)s', "%Y-%m-%d %H:%M:%S"))

        # 再创建一个handler，设置输出日志的级别，且设置输出日志的格式，用于输出到控制台
        CONSOLE_HANDLER = logging.StreamHandler()
        CONSOLE_HANDLER.setLevel(logging.DEBUG)
        CONSOLE_HANDLER.setFormatter(logging.Formatter('%(asctime)s - %(funcName)s - %(name)s - %(levelname)s - %(message)s', "%Y-%m-%d %H:%M:%S"))

        # 给log添加handler
        # self.logger.addHandler(FILE_HANDLER)
        if "pytest" not in sys.modules:  # 目前在pytest中会存在重复打印日志的情况
            self.logger.addHandler(CONSOLE_HANDLER)

        if level == 'info':
            self.logger.info(Fore.GREEN + message + Style.RESET_ALL)
        elif level == 'debug':
            self.logger.debug(message)
        elif level == 'warn':
            self.logger.warning(Fore.YELLOW + message + Style.RESET_ALL)
        elif level == 'error':
            self.logger.error(Fore.RED + message + Style.RESET_ALL)
        elif level == 'critical':
            self.logger.critical(Fore.LIGHTRED_EX + message + Style.RESET_ALL)
        elif level == 'print':
            self.logger.debug(message)

        # 删除Handler避免重复输出log
        # self.logger.removeHandler(FILE_HANDLER)
        self.logger.removeHandler(CONSOLE_HANDLER)

        # FILE_HANDLER.close()
        CONSOLE_HANDLER.close()

    def debug(self, message):
        self._print_console('debug', message)

    def info(self, message):
        self._print_console('info', message)

    def warn(self, message):
        self._print_console('warn', message)

    def error(self, message):
        self._print_console('error', message)

    def critical(self, message):
        self._print_console('critical', message)

    def print(self, message):
        self._print_console('print', message)
