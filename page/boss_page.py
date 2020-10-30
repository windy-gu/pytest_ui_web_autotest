from poium import Page, PageElement, PageElements, NewPageElement


"""
# selenium
    'css': By.CSS_SELECTOR,
    'id_': By.ID,
    'name': By.NAME,
    'xpath': By.XPATH,
    'link_text': By.LINK_TEXT,
    'partial_link_text': By.PARTIAL_LINK_TEXT,
    'tag': By.TAG_NAME,
    'class_name': By.CLASS_NAME
    
    实例内容以 https:www.baidu.com 搜索输入框input/百度一下button
    
    element_location_css = NewPageElement(css='.s_ipt', describe='css定位描述内容')
    element_location_id = NewPageElement(id_='kw', describe='id元素描述内容')
    element_location_name = NewPageElement(name='kw', describe='name元素描述内容')
    element_location_xpath = NewPageElement(xpath='//*[@id="kw"]', describe='XPath定位描述内容')
    element_location_link_text = NewPageElement(link_text='百度一下', describe='link_text描述内容')
    element_location_partial_link_text = NewPageElement(partial_link_text='百度一', describe='元素描述内容')
    element_location_tag = NewPageElement(tag='input', describe='元素描述内容')
    element_location_class_name = NewPageElement(class_name='s_ipt', describe='元素描述内容')
    
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
    
    css详细定位
    1）通过class定位
    2）通过id定位
    3）通过标签名定位
    4）通过标签层级关系定位
    5）通过属性定位
    6）组合定位
    7）更多定位方法
    
    
"""


class BossLoginPage(Page):
    boss_login_name = NewPageElement(xpath='//*[@id="app"]/div/div/div/div/div[2]/form/div[1]/div/div/div[2]/input',
                                     describe='登录用户名')
    boss_login_password = NewPageElement(xpath='//*[@id="app"]/div/div/div/div/div[2]/form/div[2]/div/div/div[2]/input',
                                         describe='密码')
    login_button = NewPageElement(xpath='//*[@id="app"]/div/div/div/div/div[2]/div[2]/button', describe='点我登录')
    google_code = NewPageElement(xpath='//*[@id="app"]/div/div/div/div/form/div[1]/div/div/div/input',
                                 describe='Google验证码')
    login_confirm_button = NewPageElement(xpath='//*[@id="app"]/div/div/div/div/form/div[2]/div/div/button[2]',
                                          describe='二次验证登录_确认')


class HomePage(Page):
    language_button_span = NewPageElement(xpath='//*[@id="app"]/div/div/div[3]/div/div[1]/div[3]/div/div[1]/a/span',
                                          describe='语言button_span')
    language_text_span = NewPageElement(xpath='//*[@id="app"]/div/div/div[3]/div/div[1]/div[3]/div/div[1]/a/span/span',
                                        describe='语言text_span')
    language_selector_zh = NewPageElement(xpath='//*[@class="left"]/div/div[2]/div/div[2]/div/div/div/div[1]',
                                          describe='语言_切换选项_中文')
    language_selector_en = NewPageElement(xpath='//*[@class="left"]/div/div[2]/div/div[2]/div/div/div/div[2]',
                                          describe='语言_切换选项_English')
    customer_center = NewPageElement(xpath='//*[@class="main-menu-list"]/li[1]', describe='客户中心')
    yumnow_management = NewPageElement(xpath='//*[@class="main-menu-list"]/li[2]', describe='外卖管理')
    distribution_management = NewPageElement(xpath='//*[@class="main-menu-list"]/li[3]', describe='配送管理')
    order_management = NewPageElement(xpath='//*[@class="main-menu-list"]/li[4]', describe='订单管理')
    marketing_management = NewPageElement(xpath='//*[@class="main-menu-list"]/li[5]', describe='平台营销')
    system_configuration = NewPageElement(xpath='//*[@class="main-menu-list"]/li[6]', describe='系统配置')
    member_management = NewPageElement(xpath='//span[contains(text(),"会员管理")]', describe='会员管理')
    merchant_management = NewPageElement(xpath='//span[contains(text(),"商户管理")]', describe='商户管理')
    merchant_list = NewPageElement(xpath='//span[contains(text(),"商户列表")]', describe='商户列表')
    add_merchant = NewPageElement(xpath='//span[contains(text(),"新增")]', describe='+新增（商户）btn')


class CustomerCenterPage(Page):
    member_management = NewPageElement(xpath='//span[contains(text(),"会员管理")]', describe='会员管理')
    merchant_management = NewPageElement(xpath='//span[contains(text(),"商户管理")]', describe='商户管理')
    merchant_list = NewPageElement(xpath='//span[contains(text(),"商户列表")]', describe='商户列表')
    add_merchant = NewPageElement(xpath='//span[contains(text(),"新增")]', describe='+新增（商户）btn')


class CreateStore(Page):
    pass




