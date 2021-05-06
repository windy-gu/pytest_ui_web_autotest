from selenium.webdriver.common.by import By
from util.web_page_browser import PageBrowser
from util.web_page_element import Element


# class BaiduPage(Page):
#     search_input = NewPageElement(id_='kw', describe='搜索框')
#     search_button = NewPageElement(id_='su', describe='搜索按钮')

class BaiduPage(PageBrowser):
    search_input = Element(id='kw', describe='搜索框')
    search_button = Element(id='su', describe='搜索按钮')
    # search_button1 = Element(By.ID='su', describe='搜索按钮')



