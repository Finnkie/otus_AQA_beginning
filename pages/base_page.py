import logging
import time

import pytest
import conftest
from conftest import open_page
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

import allure


logger = logging.getLogger(__name__)


# Базовая страница: хранит драйвер и общие помощники для всех страниц
class BasePage:
    CURRENCY_BLOCK = [
        "#_desktop_currency_selector",
        ".ps-currencyselector",
        ".currency-selector",
    ]
    PRODUCT_PRICE = ".product-miniature__price"
    CART_BADGE = ".header-block__badge"
    CART_MODAL = "#blockcart-modal.show"

    def __init__(self, driver, base_url):
        self.driver = driver
        self.base_url = base_url
        self.wait = WebDriverWait(driver, 15)

    @allure.step("Проверяем подтверждение добавления в корзину")
    def cart_confirmation(self, driver):
        if self.find_all(self.CART_MODAL):
            return True
        badges = self.find_all(self.CART_BADGE)
        return bool(badges and badges[0].text.strip() not in ("", "0"))

    @allure.step("Открываем страницу '{path}'")
    def open(self, path):
        url = path if path.startswith("http") else f"{self.base_url}{path}"
        logger.info("Открываем страницу: %s", url)
        open_page(self.driver, url)

    @allure.step("Ищем элемент '{selector}'")
    def find(self, selector):
        logger.debug("Ожидаем элемент: %s", selector)
        return self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, selector))
        )

    def find_all(self, selector):
        return self.driver.find_elements(By.CSS_SELECTOR, selector)

    def pause(self):
        if conftest.SLOWMO:
            time.sleep(conftest.SLOWMO)

    @allure.step("Заполняем поле '{selector}' значением '{text}'")
    def fill(self, selector, text):
        logger.info("Заполняем поле %s", selector)
        self.pause()
        element = self.find(selector)
        element.clear()
        element.send_keys(text)

    @allure.step("Кликаем по элементу")
    def click(self, element):
        logger.debug("Клик по элементу: %s", element.accessible_name or element.tag_name)
        self.pause()
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", element
        )
        try:
            element.click()
        except ElementClickInterceptedException:
            logger.debug("Элемент перекрыт, кликаем через JS")
            self.driver.execute_script("arguments[0].click();", element)

    @allure.step("Кликаем и ждём в URL '{url_part}'")
    def click_and_wait_url(self, element, url_part):
        self.click(element)
        self.wait.until(EC.url_contains(url_part))

    # ---------- общее для витрины: цены и валюта ----------

    @allure.step("Ищем блок выбора валюты")
    def currency_block(self):
        for selector in self.CURRENCY_BLOCK:
            blocks = self.find_all(selector)
            if blocks:
                return blocks[0]
        return None

    @allure.step("Переключаем валюту на '{currency_symbol}'")
    def switch_currency(self, currency_symbol):
        logger.info("Переключаем валюту: %s", currency_symbol)
        block = self.currency_block()
        if block is None:
            pytest.skip(
                "В магазине включена только одна валюта, переключение недоступно"
            )

        # Ищем нужную валюту и переключаемся на неё.
        # Валюта может быть оформлена выпадающим списком или списком ссылок
        switched = False
        options = block.find_elements(By.TAG_NAME, "option")
        if options:
            select = Select(block.find_element(By.TAG_NAME, "select"))
            for option in options:
                if currency_symbol in option.text:
                    select.select_by_visible_text(option.text)
                    switched = True
                    break
        else:
            for link in block.find_elements(By.CSS_SELECTOR, "a"):
                if currency_symbol in link.text:
                    self.click(link)
                    switched = True
                    break

        if not switched:
            pytest.skip(f"В магазине нет валюты со знаком {currency_symbol}")

        # Дожидаемся обновления страницы с новыми ценами
        self.driver.refresh()

    @allure.step("Собираем цены товаров на странице")
    def product_prices(self):
        prices = self.wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, self.PRODUCT_PRICE))
        )
        price_texts = [price.text.strip() for price in prices]
        logger.info("Найдено цен: %d", len(price_texts))
        return price_texts
