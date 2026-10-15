from pages.admin_products_page import AdminProductsPage
from tests.test_shop_scenarios import ADMIN_EMAIL, ADMIN_PASSWORD, login_to_admin
import random


def _open_products(driver, base_url):
    """Входит в админку и открывает список товаров."""
    login_to_admin(driver, base_url)
    products_page = AdminProductsPage(driver, base_url)
    products_page.open_products()
    return products_page


# ============ Добавление нового товара в админке ============
def test_admin_add_new_product(driver, base_url):
    products_page = _open_products(driver, base_url)

    new_product_page = products_page.open_new_product()
    product_name = f"Autotest Product {random.randint(1000, 9999)}"
    new_product_page.create_product(product_name, price="10.50")

    assert products_page.has_product(product_name), (
        f"Созданный товар '{product_name}' не найден в списке"
    )


# ============ Удаление товара из списка в админке ============
def test_admin_delete_product(driver, base_url):
    # Создаём свой товар, чтобы удалять было что
    products_page = _open_products(driver, base_url)
    new_product_page = products_page.open_new_product()
    product_name = f"Autotest Product {random.randint(1000, 9999)}"
    new_product_page.create_product(product_name, price="5.00")

    assert products_page.has_product(product_name), "Товар не создан перед удалением"

    products_page.delete_product(product_name)

    assert not products_page.has_product(product_name), (
        f"Товар '{product_name}' не удалён из списка"
    )
