from pages.admin_login_page import AdminLoginPage
from pages.admin_products_page import AdminProductsPage
from pages.cart_page import CartPage
from pages.catalog_page import CatalogPage
from pages.main_page import MainPage

ADMIN_EMAIL = "demo@prestashop.com"
ADMIN_PASSWORD = "prestashop_demo"


def login_to_admin(driver, base_url):
    login_page = AdminLoginPage(driver, base_url)
    login_page.open_login_page()
    login_page.login(ADMIN_EMAIL, ADMIN_PASSWORD)
    return login_page


def test_admin_login_and_logout(driver, base_url):
    login_page = login_to_admin(driver, base_url)
    assert login_page.is_logged_in(), "Не удалось войти в админку"
    assert login_page.logout(), "После выхода не открылась форма логина"


# Случайный товар с главной добавляется в корзинуу
def test_add_random_product_to_cart(driver, base_url):
    main_page = MainPage(driver, base_url)
    main_page.open_main()

    product_name = main_page.add_random_product_to_cart()

    cart_page = CartPage(driver, base_url)
    cart_page.open_cart()
    assert cart_page.has_product(product_name), (
        f"Товар '{product_name}' не найден в корзине"
    )


# Переключение валюты в каталоге
def test_currency_switch_changes_prices_in_catalog(driver, base_url):
    catalog_page = CatalogPage(driver, base_url)
    catalog_page.open_catalog()

    prices_before = catalog_page.product_prices()
    assert prices_before, "В каталоге не найдены цены товаров"

    catalog_page.switch_currency("$")
    prices_after = catalog_page.product_prices()

    assert prices_after != prices_before, "Цены в каталоге не изменились"
    assert all(price.startswith("$") for price in prices_after), (
        f"Не все цены в долларах: {prices_after}"
    )
