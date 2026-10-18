from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from pages.base_page import BasePage


class CartPage(BasePage):
    """Страница корзины."""

    def open_cart(self):
        self.open("/cart")

    def has_product(self, product_name):
        """Ждёт появления товара в корзине.

        Список товаров корзины дорисовывается скриптами темы после
        загрузки страницы, поэтому ждём именно текст с названием.
        """
        return bool(
            WebDriverWait(self.driver, 30).until(
                EC.text_to_be_present_in_element(
                    (By.TAG_NAME, "main"), product_name
                )
            )
        )
