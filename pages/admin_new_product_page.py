import logging

import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from pages.base_page import BasePage


logger = logging.getLogger(__name__)


# админка: форма создания нового товара
class AdminNewProductPage(BasePage):
    NAME_INPUTS = [
        "#name_1",
        "input[name='name_1']",
        "input[placeholder*='product name']",
    ]
    PRICE_INPUTS = [
        "#price_ttc_short",
        "#price_tec_short",
        "input[name='price']",
    ]
    SAVE_BUTTONS = [
        "button[name='submitAddProductAndStay']",
        "button[name='submitAddProduct']",
        "form button[type='submit']",
    ]

    def _find_first(self, selectors):
        for selector in selectors:
            inputs = self.find_all(selector)
            if inputs:
                return inputs[0]
        return None

    @allure.step("Ждём форму создания товара")
    def wait_form(self):
        WebDriverWait(self.driver, 30).until(
            lambda d: self._find_first(self.NAME_INPUTS)
        )

    @allure.step("Создаём товар '{name}' с ценой {price}")
    def create_product(self, name, price):
        """Создаёт товар с названием и ценой, ждёт сохранения."""
        logger.info("Создаём товар: %s (цена %s)", name, price)
        name_input = self.wait_form()
        name_input.clear()
        name_input.send_keys(name)

        price_input = self._find_first(self.PRICE_INPUTS)
        if price_input:
            price_input.clear()
            price_input.send_keys(price)

        save_button = self._find_first(self.SAVE_BUTTONS)
        self.click(save_button)

        WebDriverWait(self.driver, 30).until(
            lambda d: bool(
                d.find_elements(By.CSS_SELECTOR, ".toast.show, .alert-success")
            )
        )
