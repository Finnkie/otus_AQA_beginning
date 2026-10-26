import logging
import random

import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage


logger = logging.getLogger(__name__)


class MainPage(BasePage):
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

    @allure.step("Открываем главную страницу")
    def open_main(self):
        self.open("/")

    @allure.step("Считаем ссылки в главном меню")
    def menu_links_count(self):
        count = len(self.find_all(self.MENU_LINKS))
        return count

    @allure.step("Собираем карточки товаров с главной")
    def product_cards(self):
        return self.wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, self.PRODUCT_CARDS))
        )

    @allure.step("Выбираем случайный товар на главной")
    def random_product_name_and_url(self):
        """Возвращает название и адрес случайного товара с главной страницы."""
        card = random.choice(self.product_cards())
        title = card.find_element(By.CSS_SELECTOR, self.PRODUCT_TITLE)
        name, url = title.text.strip(), title.get_attribute("href")
        return name, url

    @allure.step("Добавляем случайный товар с главной в корзину")
    def add_random_product_to_cart(self):
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

            logger.info("Быстрая кнопка не сработала, открываем карточку товара")
            self.open(product_url)
            product_page = ProductPage(self.driver, self.base_url)
            product_page.add_to_cart()
        return product_name
