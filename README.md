# pytest_ui_web_autotest
pytest-ui-web自动化框架

###安装相关依赖

pip freeze > requirements.txt  //将环境的当前包列表记录到 requirements.txt

pip install -r requirements.txt //根据rf.txt安装项目依赖包

###元素定位详解


###运行执行


###pytest相关
@pytest.fixture(scope='module')来定义框架，scope的参数有以下几种
function 每一个用例都执行
class 每个类执行
module 每个模块执行(函数形式的用例)
session  每个session只运行一次，在自动化测试时，登录步骤可以使用该session



###其他
Google driver 下载地址：http://chromedriver.storage.googleapis.com/index.html
mac系统chromedriver应该放的位置！/usr/local/bin
win系统chromedriver存放到python目录即可