from util.web_page_browser import PageBrowser
from util.web_page_element import Element


class OAPage(PageBrowser):

    # https://oa.wownow.net/wui/index.html#/?logintype=1&_key=q6nnev
    login_name = Element(id='loginid', describe='登录名')
    login_password = Element(id='userpassword', describe='登录密码')
    login_btn = Element(id='submit', describe='登录_btn')

    door = Element(xpath='//*[@id="container"]/div/div[2]/div[1]/div/div[2]/div[1]/div[2]', describe='门户')
    liucheng = Element(xpath='//*[@id="portal-intro1"]/div/div/div/div[1]/div/div[2]', describe='流程')
    my_request = Element(xpath='//*[@id="menuScrollWrapper"]/div/div[1]/ul/li[4]/div', describe='我的请求')
    overtime_application = Element(xpath='//div[contains(text(),"S-app 加班申请")]', describe='加班申请')
    day_off_application = Element(xpath='//div[contains(text(),"S-app 请休假申请")]', describe='请休假申请')
    search_input = Element(xpath='//input[@class="ant-input undefined"]', index=1, describe='搜索输入框')
    rest_application = Element(xpath='//div[contains(text(),"S-app 请休假申请")]', describe='休假申请')

    list_operator_count = Element(xpath='//span[@class="ant-pagination-total-text"]', describe='需要操作数据条数')
    next_page = Element(xpath='//li[@class="ant-pagination-next"]', describe='下一页')

    data = Element(xpath='//tbody/tr/td[2]')  # 加班list数据



