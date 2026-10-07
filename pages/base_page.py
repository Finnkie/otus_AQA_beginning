import time

import pytest
import conftest
from conftest import open_page
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait


class BasePage:
    """Базовая страница: хранит драйвер и общие помощники для всех страниц."""

    # Блок выбора валюты в верхнем меню (классическая и новая темы)
    CURRENCY_BLOCK = [
        "#_desktop_currency_selector",
        ".ps-currencyselector",
        ".currency-selector",
    ]
    PRODUCT_PRICE = ".product-miniature__price"

    def __init__(self, driver, base_url):
        self.driver = driver
        self.base_url = base_url
        self.wait = WebDriverWait(driver, 15)

    def open(self, path):
        """Открывает страницу магазина по относительному пути или полному URL."""
        if path.startswith("http"):
            open_page(self.driver, path)
        else:
            open_page(self.driver, f"{self.base_url}{path}")

    def find(self, selector):
        """Явно ждёт появления элемента на странице."""
        return self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, selector))
        )

    def find_all(self, selector):
        return self.driver.find_elements(By.CSS_SELECTOR, selector)

    def pause(self):
        """Пауза перед действием - режим slowmo для наглядного прогона."""
        if conftest.SLOWMO:
            time.sleep(conftest.SLOWMO)

    def fill(self, selector, text):
        self.pause()
        element = self.find(selector)
        element.clear()
        element.send_keys(text)

    def click(self, element):
        """Скроллит к элементу и кликает; если элемент перекрыт - кликает через JS."""
        self.pause()
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", element
        )
        try:
            element.click()
        except ElementClickInterceptedException:
            self.driver.execute_script("arguments[0].click();", element)

    def click_and_wait_url(self, element, url_part):
        self.click(element)
        self.wait.until(EC.url_contains(url_part))

    # ---------- общее для витрины: цены и валюта ----------

    def currency_block(self):
        """Возвращает блок выбора валюты или None, если валюта в магазине одна."""
        for selector in self.CURRENCY_BLOCK:
            blocks = self.find_all(selector)
            if blocks:
                return blocks[0]
        return None

    def switch_currency(self, currency_symbol):
        """Переключает валюту в верхнем меню на вариант с нужным символом ($ или €)."""
        block = self.currency_block()
        if block is None:
            pytest.skip("В магазине включена только одна валюта, переключение недоступно")

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

    def product_prices(self):
        """Возвращает список цен товаров на странице."""
        prices = self.wait.until(
            EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, self.PRODUCT_PRICE)
            )
        )
        return [price.text.strip() for price in prices]
