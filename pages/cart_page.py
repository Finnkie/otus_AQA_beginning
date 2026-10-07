from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from pages.base_page import BasePage


class CartPage(BasePage):
    """Страница корзины."""

    MAIN = "main"

    def open_cart(self):
        self.open("/cart")

    def text(self):
        """Текст страницы корзины (грузится медленно - ждём подольше)."""
        main = WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.TAG_NAME, self.MAIN))
        )
        return main.text

    def has_product(self, product_name):
        return product_name in self.text()
