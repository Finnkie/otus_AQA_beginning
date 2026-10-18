import random

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage


class MainPage(BasePage):
    """Главная страница магазина."""

    HEADER = "#header"
    LOGO = "#header .logo"
    SEARCH_INPUT = "input[name='s']"
    CART_BLOCK = "#_desktop_ps_shoppingcart .blockcart"
    SIGN_IN_LINK = "#_desktop_ps_customersignin a"
    TOP_MENU = "#top-menu"
    MENU_LINKS = "#top-menu a"
    FOOTER = "footer#footer"
    PRODUCT_CARDS = "article.product-miniature"
    PRODUCT_TITLE = "a.product-miniature__title"
    ADD_TO_CART_BUTTON = "button[data-button-action='add-to-cart']"

    def open_main(self):
        self.open("/")

    def menu_links_count(self):
        return len(self.find_all(self.MENU_LINKS))

    def product_cards(self):
        return self.wait.until(
            EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, self.PRODUCT_CARDS)
            )
        )

    def random_product_name_and_url(self):
        """Возвращает название и адрес случайного товара с главной страницы."""
        card = random.choice(self.product_cards())
        title = card.find_element(By.CSS_SELECTOR, self.PRODUCT_TITLE)
        return title.text.strip(), title.get_attribute("href")

    def add_random_product_to_cart(self):
        """Добавляет случайный товар с главной в корзину.

        Возвращает название добавленного товара. Быстрая кнопка может
        не сработать (товар с обязательными вариантами или скрипты ещё
        грузятся) - тогда добавляем товар с его страницы.
        """
        product_name, product_url = self.random_product_name_and_url()
        add_buttons = self.find_all(self.ADD_TO_CART_BUTTON)
        add_button = random.choice(add_buttons)

        confirmed = False
        for _ in range(2):
            self.click(add_button)
            try:
                self.wait.until(self.cart_confirmation)
                confirmed = True
                break
            except Exception:
                pass

        if not confirmed:
            from pages.product_page import ProductPage

            self.open(product_url)
            product_page = ProductPage(self.driver, self.base_url)
            product_page.add_to_cart()
        return product_name
