from selenium.webdriver.common.by import By
from util.web_page_browser import PageBrowser
from util.web_page_element import Element


class BaiduPage(PageBrowser):
    search_input = Element(id='kw', describe='搜索框')
    news = Element(link_text='新闻', describe='新闻')
    search_button = Element(id='su', describe='搜索按钮')
    settle_buttom = Element(id='s-usersetting-top', describe='设置按钮')
    advanced_search = Element(xpath='//*[@id="s-user-setting-menu"]/div/a[2]', describe='高级搜索')
    time_selected_default = Element(xpath='//*[@id="adv-setting-gpc"]/div/div[1]/span', describe='时间')
    word_selected_default = Element(xpath='//*[@id="adv-setting-gpc"]/div/div[1]/span', describe='文档格式')
    tiem_selector_list_week = Element(link_text='最近一周', describe='最近一周')
    # search_button1 = Element(By.ID='su', describe='搜索按钮')



