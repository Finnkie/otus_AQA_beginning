import allure
from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class CatalogPage(BasePage):
    PAGE_PATH = "/9-art"
    H1 = "h1"
    BREADCRUMB = ".breadcrumb"
    PRODUCT_CARDS = "article.product-miniature"
    SORT_DROPDOWN = ".products__sort-dropdown"
    PAGINATION = ".products__pagination"

    @allure.step("Открываем каталог Art")
    def open_catalog(self):
        self.open(self.PAGE_PATH)

    @allure.step("Читаем заголовок каталога")
    def title(self):
        return self.find(self.H1).text.strip()
