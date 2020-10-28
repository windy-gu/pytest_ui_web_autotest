from poium import Page, PageElement, PageElements, NewPageElement


class BaiduPage(Page):
    search_input = NewPageElement(id_='kw', describe='搜索框')
    search_button = NewPageElement(id_='su1', describe='搜索按钮')

    pass