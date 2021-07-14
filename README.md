# pytest_ui_web_autotest
pytest-ui-web自动化框架

###安装相关依赖

    pip freeze > requirements.txt  //将环境的当前包列表记录到 requirements.txt
    pip install -r requirements.txt //根据rf.txt安装项目依赖包

###元素定位详解

    
    实例内容以 https:www.baidu.com 搜索输入框input/百度一下button
    selenium
    'css': By.CSS_SELECTOR,
    'id': By.ID,
    'name': By.NAME,
    'xpath': By.XPATH,
    'link_text': By.LINK_TEXT,
    'partial_link_text': By.PARTIAL_LINK_TEXT,
    'tag': By.TAG_NAME,
    'class_name': By.CLASS_NAME
    
    element_location_css = Element(css='.s_ipt', describe='css定位描述内容')
    element_location_id = Element(id='kw', describe='id元素描述内容')
    element_location_name = Element(name='kw', describe='name元素描述内容')
    element_location_xpath = Element(xpath='//*[@id="kw"]', describe='XPath定位描述内容')
    element_location_link_text = Element(link_text='百度一下', describe='link_text描述内容')
    element_location_partial_link_text = Element(partial_link_text='百度一', describe='元素描述内容')
    element_location_tag = Element(tag='input', describe='元素描述内容')
    element_location_class_name = Element(class_name='s_ipt', describe='元素描述内容')
    
    XPath详细定位
    1）绝对路径定位  通过开发者工具 - 选中需要定位的元素 - Copy - Copy XPath
    2）利用元素属性定位
        xpath='//*[@id="kw"]'  -- 获取当前页面中id="kw"的元素
        xpath='//input[@id="kw"]'  -- 获取当前页面中某个input标签下id="kw"的元素
        不局限id/name/class,任何属性都可以使用
        
    3）层级与属性结合
        若元素本身没有可以唯一标识的属性值，可以通过查找其上一级元素（同5示例）
        
    4）使用逻辑运算符
        如果一个属性值不能唯一区分一个元素，可以使用逻辑运算符连接多个属性来查找元素
        xpath='//input[@id="kw" and @class="s_ipt"]' 
        
    5）使用contains方法 
        contains方法用于匹配一个属性中包含的字符串
        xpath='//span[contains(@class, "s_ipt_wr")/input]' 
        contains方法只取了class属性中的"s_ipt_wr"部分
        
    6）使用text()方法
        text()用于匹配显示文本信息，实现了partial link定位的效果
        xpath='//a[text(), "新闻"]' 
        xpath='//span[contains(text(),"商户管理")]'  span标签内文字内容包含"商户管理"
    
    css详细定位 - 后续需要补充
    1）通过class定位
    2）通过id定位
    3）通过标签名定位
    4）通过标签层级关系定位
    5）通过属性定位
    6）组合定位
    7）更多定位方法
    
    def __init__(self, timeout=5, describe="undefined", index=0, **kwargs):
    Element(xx='xx')
    


###运行执行
    待补充

###pytest相关
    @pytest.fixture(scope='module')来定义框架，scope的参数有以下几种
    function 每一个用例都执行
    class 每个类执行
    module 每个模块执行(函数形式的用例)
    session  每个session只运行一次，在自动化测试时，登录步骤可以使用该session

###JS操作 - 一般当前HTML页面无法通过常规selenium方法进行操作时，可以通过js进行替代操作

####1）增加&赋值
    给id为nice的元素 增加 title属性并赋值为“测试title”
    js='document.getElementById("nice").setAttribute("title","测试title")'

####2）删除 - 适用场景：一些时间控件或者编辑操作页面，存在一些无法直接send_keys进行直接输入
    给id为nice的元素 删除 title属性
    js='document.getElementById("nice").removeAttribute("title")'

####3）获取信息
    获取id为nice的元素 title属性的值
    js='document.getElementById("nice").getAttribute("title")'

####4）修改
    修改id为nice的元素 title属性的值
    js='document.getELementById("nice").title="测试"'


###其他
    Google driver 下载地址：http://chromedriver.storage.googleapis.com/index.html
    mac系统chromedriver应该放的位置！/usr/local/bin
    win系统chromedriver存放到python目录即可