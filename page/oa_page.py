from poium import Page, PageElement, PageElements, NewPageElement
from util.page_by_keiven import Element

class OAPage(Page):

    # https://oa.wownow.net/wui/index.html#/?logintype=1&_key=q6nnev
    login_name = NewPageElement(id_='loginid', describe='登录名')
    login_password = NewPageElement(id_='userpassword', describe='登录密码')
    login_btn = NewPageElement(id_='submit', describe='登录_btn')

    door = NewPageElement(xpath='//*[@id="container"]/div/div[2]/div[1]/div/div[2]/div[1]/div[2]', describe='门户')
    liucheng = NewPageElement(xpath='//*[@id="portal-intro1"]/div/div/div/div[1]/div/div[2]', describe='流程')
    my_request = NewPageElement(xpath='//*[@id="menuScrollWrapper"]/div/div[1]/ul/li[4]/div', describe='我的请求')
    overtime_application = NewPageElement(xpath='//div[contains(text(),"S-app 加班申请")]', describe='加班申请')
    rest_application = NewPageElement(xpath='//div[contains(text(),"S-app 请休假申请")]', describe='休假申请')

    data = NewPageElement(xpath='//tbody/tr/td[2]')  # 加班list数据

#     //*[@id="container"]/div/div[2]/div[1]/div/div[2]/div[1]/div[2]
# //*[@id="weatop_6xexsw_1610351227143"]/div[2]/div/div[3]/div[2]/div[2]/div/div[1]/div/div/div/div/div/div/div/span/div[2]/table/tbody/tr[1]/td[2]



# 已办事宜 https://oa.wownow.net/wui/index.html#/main/workflow/listDone?menuIds=1,90&_key=93vuhu



class NewOAPage(Element):
    login_name = NewPageElement(id_='loginid', describe='登录名')
    login_password = NewPageElement(id_='userpassword', describe='登录密码')
    login_btn = NewPageElement(id_='submit', describe='登录_btn')


