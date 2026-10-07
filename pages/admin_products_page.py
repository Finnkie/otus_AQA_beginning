from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from pages.base_page import BasePage


class AdminProductsPage(BasePage):
    """Раздел администратора: список товаров (Каталог -> Товары)."""

    PRODUCTS_PATH = "/admin-dev/index.php/sell/catalog/products"
    PRODUCTS_TABLE = "#product_catalog_list"
    TABLE_ROWS = "#product_catalog_list tbody tr"
    NAME_FILTER = "input[name='filter_column_name']"
    SEARCH_BUTTON = "button[name='productsFilterSubmit']"
    NEW_PRODUCT_LINK = "a[href*='products/new'], a[href*='addproduct']"
    ROW_ACTIONS_MENU = ".dropdown-toggle, [data-toggle='dropdown']"
    DELETE_LINK = "a[href*='deleteproduct'], a[onclick*='delete']"

    def open_products(self):
        self.open(self.PRODUCTS_PATH)
        self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, self.PRODUCTS_TABLE))
        )

    def search_product(self, name):
        """Ищет товар по названию в списке."""
        name_filter = self.find(self.NAME_FILTER)
        name_filter.clear()
        name_filter.send_keys(name)
        name_filter.send_keys(Keys.ENTER)
        # ждём перезагрузку таблицы
        WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, self.PRODUCTS_TABLE))
        )

    def rows(self):
        return self.find_all(self.TABLE_ROWS)

    def has_product(self, name):
        """Есть ли товар с таким названием в списке (после поиска)."""
        self.search_product(name)
        return name.lower() in self.driver.find_element(
            By.CSS_SELECTOR, self.PRODUCTS_TABLE
        ).text.lower()

    def open_new_product(self):
        """Открывает форму создания товара, возвращает страницу формы."""
        from pages.admin_new_product_page import AdminNewProductPage

        self.click(self.find(self.NEW_PRODUCT_LINK))
        new_product_page = AdminNewProductPage(self.driver, self.base_url)
        new_product_page.wait_form()
        return new_product_page

    def delete_product(self, name):
        """Удаляет товар из списка: ищем его, открываем меню действий, подтверждаем."""
        self.search_product(name)
        rows = self.rows()
        if not rows:
            return False

        # у строки открываем меню действий и выбираем удаление
        self.click(rows[0].find_element(By.CSS_SELECTOR, self.ROW_ACTIONS_MENU))
        delete_link = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, self.DELETE_LINK))
        )
        self.click(delete_link)

        # подтверждение: нативный confirm() или модальное окно
        try:
            alert = WebDriverWait(self.driver, 5).until(
                lambda d: d.switch_to.alert
            )
            alert.accept()
        except Exception:
            confirm_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, ".modal.show .btn-primary, .modal-footer .btn-primary")
                )
            )
            self.click(confirm_button)
        return True
