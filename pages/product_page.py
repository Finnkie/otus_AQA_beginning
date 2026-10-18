from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from pages.base_page import BasePage


class ProductPage(BasePage):
    """Карточка товара."""

    H1 = "h1"
    BREADCRUMB = ".breadcrumb"
    PRICE_BLOCK = ".product__prices-block .product__price"
    QUANTITY_INPUT = "#quantity_wanted"
    ADD_TO_CART_BUTTON = "button.product__add-to-cart-button"

    def open_product(self, product_url):
        self.open(product_url)

    def title(self):
        return self.find(self.H1).text.strip()

    def price(self):
        return self.find(self.PRICE_BLOCK).text.strip()

    def add_to_cart(self):
        """Добавляет товар в корзину и ждёт подтверждения.

        Подтверждение - модальное окно корзины или счётчик товаров
        в шапке. Первый клик может пройти до загрузки скриптов
        магазина, поэтому пробуем дважды.
        """
        add_button = self.wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, self.ADD_TO_CART_BUTTON)
            )
        )
        for _ in range(2):
            self.click(add_button)
            try:
                WebDriverWait(self.driver, 10).until(self.cart_confirmation)
                return
            except TimeoutException:
                continue
        raise TimeoutException("Товар не добавился в корзину со страницы товара")
