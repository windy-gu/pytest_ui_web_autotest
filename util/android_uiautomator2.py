# author:windy
# datetime:2021/10/20 3:56 下午
# software: PyCharm

import uiautomator2 as u2
from util.log import Log

log = Log()


class AppDevice():

    def __init__(self, source):
        # 直接把u2.Device的属性字典复制过来
        self.d = u2.connect(source)
        log.info('连接Android设备成功，设备号or地址:{}'.format(source))

    def app_start(self, package_name: str):
        self.d.app_start(package_name)
        log.info(f'启动app:[ {package_name} ]')

    def app_stop(self, package_name: str):
        self.d.app_stop(package_name)
        log.info(f'关闭app:[ {package_name} ]')

    def app_stop_all(self, excludes: list):
        if len(excludes) < 1:
            self.d.app_stop_all()
            log.info(f'关闭所有app')
        else:
            self.d.app_stop_all(excludes=excludes)
            log.info(f'关闭所有app，除了：[{excludes}]')

    def app_info(self, package_name):
        """
        获取指定app的相关信息
        example
        {'packageName': 'com.chaos.superapp',
        'mainActivity': 'com.chaos.module_app.BaseRouteActivity',
        'label': 'WOWNOW',
        'versionName': '2.21.0',
        'versionCode': 81,
        'size': 67705997}
        :param package_name:app 对应的包名
        :return:
        """
        temp = self.d.app_info(package_name)
        log.info(f'app信息：[{temp}]')
        return temp

    def app_restart(self, package_name, activity=None):
        log.info(f'重启app:[ {package_name} ]')
        self.app_stop(package_name)
        self.app_start(package_name, activity)
        self.app_wait(package_name)


if __name__ == '__main__':
    #
    d = AppDevice('WSZPZDSCZTIVJ7E6')
    # d.app_info('')
    d.app_stop_all(['com.chaos.superapp'])
    # print(d.info)

