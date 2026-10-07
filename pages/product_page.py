from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage


class ProductPage(BasePage):
    """Карточка товара."""

    H1 = "h1"
    BREADCRUMB = ".breadcrumb"
    PRICE_BLOCK = ".product__prices-block .product__price"
    QUANTITY_INPUT = "#quantity_wanted"
    ADD_TO_CART_BUTTON = "button.product__add-to-cart-button"
    CART_MODAL = "#blockcart-modal"

    def open_product(self, product_url):
        self.open(product_url)

    def title(self):
        return self.find(self.H1).text.strip()

    def price(self):
        return self.find(self.PRICE_BLOCK).text.strip()

    def add_to_cart(self):
        """Добавляет товар в корзину и ждёт подтверждения."""
        add_button = self.wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, self.ADD_TO_CART_BUTTON)
            )
        )
        self.click(add_button)
        self.wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, self.CART_MODAL))
        )
