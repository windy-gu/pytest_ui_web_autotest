from util.web_page_browser import PageBrowser
from util.web_page_element import Element

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
    
    element_location_css = Element(css='.s_ipt', describe='css定位描述内容')
    element_location_id = Element(id_='kw', describe='id元素描述内容')
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
    
    css详细定位
    1）通过class定位
    2）通过id定位
    3）通过标签名定位
    4）通过标签层级关系定位
    5）通过属性定位
    6）组合定位
    7）更多定位方法
    
    def __init__(self, timeout=5, describe="undefined", index=0, **kwargs):
    Element(xx='xx')
    
"""


class BossLoginPage(PageBrowser):
    # boss登录页面元素
    boss_login_name = Element(xpath='//input[@placeholder="用户名" and @type="text"]', describe='登录用户名')
    boss_login_password = Element(xpath='//input[@placeholder="密码" and @type="password"]', describe='密码')
    login_button = Element(xpath='//span[contains(text(),"点我登录")]', describe='点我登录')
    google_code = Element(xpath='//input[@placeholder="Google验证码" and @type="text"]', describe='Google验证码')
    login_confirm_button = Element(xpath='//button[@type="button" and @class="ivu-btn ivu-btn-primary"]',
                                          describe='二次验证登录_确认')


class HomePage(PageBrowser):
    # 切换boss登录语言元素
    language_button_span = Element(xpath='//a[@class="lan"]/span', describe='语言button_span')
    language_text_span = Element(xpath='//a[@class="lan"]/span/span', describe='语言text_span')
    language_selector_zh = Element(xpath='//div[contains(text(), "中文")]', describe='语言_切换选项_中文')
    language_selector_en = Element(xpath='//div[contains(text(), "English")]', describe='语言_切换选项_English')

    # 首页左侧导航栏元素
    customer_center = Element(xpath='//*[@class="main-menu-list"]/li[1]', describe='客户中心')
    yumnow_management = Element(xpath='//*[@class="main-menu-list"]/li[2]', describe='外卖管理')
    distribution_management = Element(xpath='//*[@class="main-menu-list"]/li[3]', describe='配送管理')
    order_management = Element(xpath='//*[@class="main-menu-list"]/li[4]', describe='订单管理')
    marketing_management = Element(xpath='//*[@class="main-menu-list"]/li[5]', describe='平台营销')
    system_configuration = Element(xpath='//*[@class="main-menu-list"]/li[6]', describe='系统配置')


class CustomerCenterPage(PageBrowser):
    # 客户中心 - 次级导航栏元素
    member_management = Element(xpath='//span[contains(text(),"会员管理")]', describe='会员管理')
    merchant_management = Element(xpath='//span[contains(text(),"商户管理")]', describe='商户管理')
    merchant_list = Element(xpath='//span[contains(text(),"商户列表")]', describe='商户列表')
    add_merchant = Element(xpath='//span[contains(text(),"新增")]', describe='+ 新增（商户）btn')

    # 商户基本信息
    merchant_name_en = Element(xpath='//*[@class="ivu-card-body"]/div/div[1]/div/div/div/input', describe='商户名称_en', index=0)
    merchant_name_zh = Element(xpath='//*[@class="ivu-card-body"]/div/div[2]/div/div/div/input', describe='商户名称_zh', index=0)
    merchant_name_cb = Element(xpath='//*[@class="ivu-card-body"]/div/div[3]/div/div/div/input', describe='商户名称_cb', index=0)
    merchant_style_person = Element(xpath='//*[@class="ivu-card-body"]/div/div[4]/div/div/label[1]', describe='商户类型_个体商户', index=0)
    merchant_style_enterprise = Element(xpath='//*[@class="ivu-card-body"]/div/div[4]/div/div/label[2]', describe='商户类型_企业商户', index=0)
    merchant_charge_name = Element(xpath='//*[@class="ivu-card-body"]/div/div[5]/div[1]/div/div[1]/div/input', describe='负责人_名称', index=0)
    merchant_charge_surname = Element(xpath='//*[@class="ivu-card-body"]/div/div[5]/div[1]/div/div[2]/div/input', describe='负责人_姓', index=0)
    merchant_certificate_type = Element(xpath='//*[@class="ivu-card-body"]/div/div[5]/div[2]/div/div', describe='证件类型', index=0)
    merchant_identity_card = Element(xpath='//*[@class="ivu-card-body"]/div/div[5]/div[2]/div/div/div[2]/ul[2]/li[1]', describe='身份证', index=0)
    merchant_passport = Element(xpath='//*[@class="ivu-card-body"]/div/div[5]/div[2]/div/div/div[2]/ul[2]/li[2]', describe='护照', index=0)
    merchant_certificate_no = Element(xpath='//*[@class="ivu-card-body"]/div/div[5]/div[3]/div/div/div/input', describe='证件号码', index=0)
    merchant_certificate_photo = Element(xpath='//*[@class="ivu-upload-input"]', describe='证件照片', index=0)
    merchant_statue_open = Element(xpath='//*[@class="ivu-card-body"]/div/div[6]/div/div/label[1]/span/input', describe='状态_启用', index=0)
    merchant_statue_close = Element(xpath='//*[@class="ivu-card-body"]/div/div[6]/div/div/label[2]/span/input', describe='状态_停用', index=0)

    # 业务协议
    merchant_business_yumnow = Element(xpath='//label[contains(text(),"外卖业务")]', describe='外卖业务')
    merchant_business_tinhnow = Element(xpath='//label[contains(text(),"电商业务")]', describe='电商业务')
    merchant_business_OTA = Element(xpath='//label[contains(text(),"OTA")]', describe='OTA')
    merchant_connect_name = Element(xpath='//*[@class="ivu-form ivu-form-label-right"]/div[2]/div[2]/div/div[2]/div/div[1]/div/input', describe='联系人_名称')
    merchant_connect_surname = Element(xpath='//*[@class="ivu-form ivu-form-label-right"]/div[2]/div[2]/div/div[2]/div/div[2]/div/input', describe='联系人_姓')
    merchant_connect_phoneNo = Element(xpath='//*[@class="ivu-form ivu-form-label-right"]/div[2]/div[2]/div/div[3]/div/div/div[2]/input', describe='联系电话')
    merchant_contract_photo = Element(xpath='//*[@class="ivu-form ivu-form-label-right"]/div[2]/div[2]/div/div[4]/div/div/div[1]/div/input', describe='合同扫描件')

    # 管理账号信息
    merchant_login_phoneNo = Element(xpath='//*[@class="ivu-form ivu-form-label-right"]/div[3]/div[2]/div/div[1]/div/div/div[2]/input', describe='登录手机号')
    merchant_email = Element(xpath='//*[@class="ivu-form ivu-form-label-right"]/div[3]/div[2]/div/div[2]/div/div/div/input', describe='邮箱')
    merchant_user_name = Element(xpath='//*[@class="ivu-form ivu-form-label-right"]/div[3]/div[2]/div/div[3]/div/div/div/input', describe='用户名')
    merchant_password = Element(xpath='//*[@class="ivu-form ivu-form-label-right"]/div[3]/div[2]/div/div[4]/div/div/div/input', describe='登录密码')
    merchant_password_second = Element(xpath='//*[@class="ivu-form ivu-form-label-right"]/div[3]/div[2]/div/div[5]/div/div/div/input', describe='确认密码')

    # 添加商户 - 操作btn
    merchant_back = Element(xpath='//*[@class="pub_btns"]/button[1]', describe='返回')
    merchant_submit = Element(xpath='//*[@class="pub_btns"]/button[2]', describe='提交')


class DeliveryManagementPage(PageBrowser):
    # 外卖管理 - 次级导航栏元素
    store_management = Element(xpath='//span[contains(text(),"门店管理")]', describe='门店管理')
    order_management = Element(xpath='//span[contains(text(),"订单管理")]', describe='订单管理')
    statement_management = Element(xpath='//span[contains(text(),"报表管理")]', describe='报表管理')
    financial_management = Element(xpath='//span[contains(text(),"财务管理")]', describe='财务管理')
    marketing_management = Element(xpath='//span[contains(text(),"营销管理")]', describe='营销管理')
    gift_management = Element(xpath='//span[contains(text(),"赠品管理")]', describe='赠品管理')
    page_setting = Element(xpath='//span[contains(text(),"页面管理")]', describe='页面管理')

    # 门店管理 - 第二次级导航栏元素
    store_ranking = Element(xpath='//span[contains(text(),"付费排名")]', describe='付费排名')
    business_scope = Element(xpath='//span[contains(text(),"经营范围")]', describe='经营范围')
    store_list = Element(xpath='//span[contains(text(),"门店列表")]', describe='门店列表')
    store_authority_management = Element(xpath='//span[contains(text(),"门店权限管理")]', describe='门店权限管理')
    goods_label_management = Element(xpath='//span[contains(text(),"商品标签管理")]', describe='商品标签管理')

    # 门店管理 - 添加门店 - 相关元素
    add_store = Element(xpath='//span[contains(text(),"新增")]', describe='+ 新增（门店）btn')
    add_store_relate_merchant = Element(xpath='//input[@class="请选择"]', describe='+ 新增（门店）btn')

    # 订单管理 - 外卖管理 - 全部
    wait_accept_order_tab = Element(xpath='//*[@class="filter-form-button ivu-btn ivu-btn-default"]/span[contains(text(),"等待商家接单")]', describe='等待商家接单tab')
    accept_order_tab = Element(xpath='//*[@class="filter-form-button ivu-btn ivu-btn-default"]/span[contains(text(),"商家已接单")]', describe='商家已接单tab')
    order_no_input = Element(xpath='//label[@class="ivu-form-item-label"]/span[contains(text(),"订单号")]/../following-sibling::div/div/input', describe='订单编号input')
    search_btn = Element(xpath='//*[@class="ivu-btn ivu-btn-primary"]/span[contains(text(),"查询")]', describe='查询')

    # 订单管理 - 外卖管理 - 全部 - list
    opera_list = Element(xpath='//td/div[@class="ivu-table-cell"]', describe='操作list')
    ord_detail_list = Element(xpath='//td/div[@class="ivu-table-cell"]/div/button/span[contains(text(),"详情")]', describe='详情btn')
    ord_cancer_list = Element(xpath='//td/div[@class="ivu-table-cell"]/div/button/span[contains(text(),"取消订单")]', describe='取消订单btn')
    ord_accept_list = Element(xpath='//td/div[@class="ivu-table-cell"]/div/button/span[contains(text(),"代接单")]', describe='代接单btn')


class CreateStore(PageBrowser):
    pass



