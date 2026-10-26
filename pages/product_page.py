import logging

import allure
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from pages.base_page import BasePage


logger = logging.getLogger(__name__)


class ProductPage(BasePage):
    H1 = "h1"
    BREADCRUMB = ".breadcrumb"
    PRICE_BLOCK = ".product__prices-block .product__price"
    QUANTITY_INPUT = "#quantity_wanted"
    ADD_TO_CART_BUTTON = "button.product__add-to-cart-button"

    @allure.step("Открываем карточку товара")
    def open_product(self, product_url):
        self.open(product_url)

    @allure.step("Читаем название товара")
    def title(self):
        return self.find(self.H1).text.strip()

    @allure.step("Читаем цену товара")
    def price(self):
        return self.find(self.PRICE_BLOCK).text.strip()

    @allure.step("Добавляем товар в корзину со страницы товара")
    def add_to_cart(self):
        add_button = WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, self.ADD_TO_CART_BUTTON))
        )
        for _ in range(2):
            self.click(add_button)
            try:
                WebDriverWait(self.driver, 10).until(self.cart_confirmation)
                return
            except TimeoutException:
                continue
        raise TimeoutException("Товар не добавился в корзину со страницы товара")
