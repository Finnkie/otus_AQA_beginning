import logging

import allure
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from pages.base_page import BasePage


logger = logging.getLogger(__name__)


# Раздел админки: список товаров
class AdminProductsPage(BasePage):
    ADMIN_PATHS = ["/administration", "/admin-dev"]
    PRODUCTS_TABLE = "#product_catalog_list"
    TABLE_ROWS = "#product_catalog_list tbody tr"
    NAME_FILTER = "input[name='filter_column_name']"
    SEARCH_BUTTON = "button[name='productsFilterSubmit']"
    NEW_PRODUCT_LINK = "a[href*='products/new'], a[href*='addproduct']"
    ROW_ACTIONS_MENU = ".dropdown-toggle, [data-toggle='dropdown']"
    DELETE_LINK = "a[href*='deleteproduct'], a[onclick*='delete']"

    @allure.step("Открываем список товаров в админке")
    def open_products(self):

        if ".demo.prestashop.com" in self.base_url:
            admin_paths = ["/admin-dev"]
        else:
            admin_paths = self.ADMIN_PATHS

        for admin_path in admin_paths:
            self.open(f"{admin_path}/index.php/sell/catalog/products")
            try:
                WebDriverWait(self.driver, 20).until(
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR, self.PRODUCTS_TABLE)
                    )
                )
                return
            except TimeoutException:
                continue
        raise TimeoutException(
            f"Не удалось открыть список товаров ни по одному из путей: {admin_paths}"
        )

    @allure.step("Ищем товар '{name}' в списке")
    def search_product(self, name):
        name_filter = self.find(self.NAME_FILTER)
        name_filter.clear()
        name_filter.send_keys(name)
        name_filter.send_keys(Keys.ENTER)
        # перезагрузка таблицы
        WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, self.PRODUCTS_TABLE))
        )

    @allure.step("Читаем строки списка товаров")
    def rows(self):
        return self.find_all(self.TABLE_ROWS)

    @allure.step("Проверяем наличие товара '{name}' в списке")
    def has_product(self, name):
        """Есть ли товар с таким названием в списке (после поиска)."""
        self.search_product(name)
        found = (
            name.lower()
            in self.driver.find_element(
                By.CSS_SELECTOR, self.PRODUCTS_TABLE
            ).text.lower()
        )
        logger.info("Товар '%s' %s в списке", name, "найден" if found else "не найден")
        return found

    @allure.step("Открываем форму создания товара")
    def open_new_product(self):
        from pages.admin_new_product_page import AdminNewProductPage

        self.click(self.find(self.NEW_PRODUCT_LINK))
        new_product_page = AdminNewProductPage(self.driver, self.base_url)
        new_product_page.wait_form()
        return new_product_page

    @allure.step("Удаляем товар '{name}' из списка")
    def delete_product(self, name):
        self.search_product(name)
        rows = self.rows()
        if not rows:
            logger.warning("Товар '%s' не найден для удаления", name)
            return False

        # у строки открываем меню действий и выбираем удаление
        self.click(rows[0].find_element(By.CSS_SELECTOR, self.ROW_ACTIONS_MENU))
        delete_link = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, self.DELETE_LINK))
        )
        self.click(delete_link)

        # подтверждение: нативный confirm() или модальное окно
        try:
            alert = WebDriverWait(self.driver, 5).until(lambda d: d.switch_to.alert)
            alert.accept()
        except Exception:
            confirm_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(
                    (
                        By.CSS_SELECTOR,
                        ".modal.show .btn-primary, .modal-footer .btn-primary",
                    )
                )
            )
            self.click(confirm_button)
        return True
