"""Часть 2. Проверка наличия элементов на страницах PrestaShop.

Каждый тест проверяет одну страницу, не менее пяти элементов,
все элементы ждутся явным ожиданием (WebDriverWait + expected_conditions).
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


def check_elements(wait, locators):
    """Явно ждёт появления каждого элемента из списка локаторов."""
    for by, selector in locators:
        wait.until(EC.presence_of_element_located((by, selector)))


# ============ Главная страница ============
def test_main_page_has_elements(driver, base_url, wait):
    driver.get(base_url)

    check_elements(
        wait,
        [
            (By.CSS_SELECTOR, "#header"),
            (By.CSS_SELECTOR, "#header .logo"),
            (By.CSS_SELECTOR, "input[name='s']"),
            (By.CSS_SELECTOR, "#_desktop_ps_shoppingcart .blockcart"),
            (By.CSS_SELECTOR, "#_desktop_ps_customersignin a"),
            (By.CSS_SELECTOR, "#top-menu"),
            (By.CSS_SELECTOR, "footer#footer"),
        ],
    )
    # В меню есть ссылки на категории, на главной есть карточки товаров
    menu_links = driver.find_elements(By.CSS_SELECTOR, "#top-menu a")
    products = driver.find_elements(By.CSS_SELECTOR, "article.product-miniature")
    assert len(menu_links) >= 3, (
        f"Ожидалось минимум 3 пункта меню, найдено {len(menu_links)}"
    )
    assert len(products) >= 1, "На главной нет карточек товаров"


# ============ Каталог (категория Art) ============
def test_catalog_art_page_has_elements(driver, base_url, wait):
    driver.get(f"{base_url}/9-art")

    check_elements(
        wait,
        [
            (By.CSS_SELECTOR, "h1"),
            (By.CSS_SELECTOR, ".breadcrumb"),
            (By.CSS_SELECTOR, "article.product-miniature"),
            (By.CSS_SELECTOR, ".product-miniature__price"),
            (By.CSS_SELECTOR, ".products__sort-dropdown"),
            (By.CSS_SELECTOR, ".products__pagination"),
        ],
    )
    # Заголовок страницы - название категории, у товаров указаны цены
    assert driver.find_element(By.CSS_SELECTOR, "h1").text.strip() == "Art"
    prices = driver.find_elements(By.CSS_SELECTOR, ".product-miniature__price")
    assert any("€" in price.text or "$" in price.text for price in prices), (
        "У товаров в каталоге нет цен"
    )


# ============ Карточка товара ============
def test_product_page_has_elements(driver, base_url, wait):
    driver.get(base_url)

    # Переходим на карточку первого товара с главной страницы
    product_link = wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "article.product-miniature a.product-miniature__title")
        )
    )
    driver.get(product_link.get_attribute("href"))

    check_elements(
        wait,
        [
            (By.CSS_SELECTOR, "h1"),
            (By.CSS_SELECTOR, ".breadcrumb"),
            (By.CSS_SELECTOR, ".product__prices-block .product__price"),
            (By.CSS_SELECTOR, "#quantity_wanted"),
            (By.CSS_SELECTOR, "button.product__add-to-cart-button"),
        ],
    )
    # У товара есть название и цена
    title = driver.find_element(By.CSS_SELECTOR, "h1").text.strip()
    price = driver.find_element(By.CSS_SELECTOR, ".product__price").text.strip()
    assert title, "У товара нет названия"
    assert "€" in price or "$" in price, f"Некорректная цена товара: {price}"


# ============ Страница логина в админку ============
def test_admin_login_page_has_elements(driver, admin_url, wait):
    # Фикстура admin_url уже открыла страницу логина
    check_elements(
        wait,
        [
            (By.CSS_SELECTOR, "h1"),
            (By.CSS_SELECTOR, "input[name='email']"),
            (By.CSS_SELECTOR, "input[name='passwd']"),
            (By.CSS_SELECTOR, "button[type='submit']"),
            (By.CSS_SELECTOR, ".show-forgot-password"),
            (By.CSS_SELECTOR, "#stay_logged_in"),
        ],
    )


# ============ Страница регистрации ============
def test_registration_page_has_elements(driver, base_url, wait):
    driver.get(f"{base_url}/registration")

    check_elements(
        wait,
        [
            (By.CSS_SELECTOR, "h1"),
            (By.CSS_SELECTOR, "form#customer-form"),
            (By.CSS_SELECTOR, "input[name='firstname']"),
            (By.CSS_SELECTOR, "input[name='lastname']"),
            (By.CSS_SELECTOR, "input[name='email']"),
            (By.CSS_SELECTOR, "input[name='password']"),
            (By.CSS_SELECTOR, "input[name='psgdpr']"),
            (By.CSS_SELECTOR, "button[data-link-action='save-customer']"),
        ],
    )
    assert (
        driver.find_element(By.CSS_SELECTOR, "h1").text.strip() == "Create an account"
    )
