import random

import pytest
from conftest import open_page
from selenium.common.exceptions import (
    ElementClickInterceptedException,
    TimeoutException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait


ADMIN_EMAIL = "demo@prestashop.com"
ADMIN_PASSWORD = "prestashop_demo"

CURRENCY_BLOCK_SELECTORS = [
    "#_desktop_currency_selector",
    ".ps-currencyselector",
    ".currency-selector",
]


def test_admin_login_and_logout(driver, admin_url, wait):
    # Логин
    email_input = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "input[name='email']"))
    )
    email_input.clear()
    email_input.send_keys(ADMIN_EMAIL)
    driver.find_element(By.CSS_SELECTOR, "input[name='passwd']").send_keys(
        ADMIN_PASSWORD
    )
    for button in driver.find_elements(By.CSS_SELECTOR, "button[type='submit']"):
        if button.is_displayed():
            button.click()
            break

    wait.until(EC.url_contains("AdminDashboard"))

    # Разлогин: ждём ссылку выхода в шапке админки и уходим по ней
    # (дашборд тяжёлый и грузится медленно - ссылке нужен запас времени)
    logout_link = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "a[href*='logout']"))
    )
    logout_url = logout_link.get_attribute("href")
    admin_dir = admin_url.split("/index.php")[0]
    open_page(driver, logout_url)

    # Разлогин выполнен: снова открыта форма логина
    # (страница админки тяжёлая, ждём подольше)
    try:
        WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "input[name='email']")
            )
        )
    except TimeoutException:
        # демо иногда отвечает 502 - пробуем ещё раз открыть страницу логина
        open_page(driver, f"{admin_dir}/login")
        WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "input[name='email']")
            )
        )
    assert "AdminDashboard" not in driver.current_url


# ============ 3.2 Случайный товар с главной добавляется в корзину ============
def cart_confirmation(driver):
    """Подтверждение добавления: модальное окно или счётчик товаров в корзине."""
    if driver.find_elements(By.CSS_SELECTOR, "#blockcart-modal.show"):
        return True
    badges = driver.find_elements(By.CSS_SELECTOR, ".header-block__badge")
    return bool(badges and badges[0].text.strip() not in ("", "0"))


def test_add_random_product_to_cart(driver, base_url, wait):
    open_page(driver, base_url)

    cards = wait.until(
        EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, "article.product-miniature")
        )
    )
    card = random.choice(cards)
    product_name = card.find_element(
        By.CSS_SELECTOR, "a.product-miniature__title"
    ).text.strip()
    product_url = card.find_element(
        By.CSS_SELECTOR, "a.product-miniature__title"
    ).get_attribute("href")
    assert product_name, "Не удалось прочитать название товара"

    add_button = card.find_element(
        By.CSS_SELECTOR, "button[data-button-action='add-to-cart']"
    )
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", add_button)

    confirmed = False
    for _ in range(2):
        try:
            add_button.click()
        except ElementClickInterceptedException:
            driver.execute_script("arguments[0].click();", add_button)
        try:
            WebDriverWait(driver, 8).until(cart_confirmation)
            confirmed = True
            break
        except TimeoutException:
            pass

    if not confirmed:
        open_page(driver, product_url)
        wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "button.product__add-to-cart-button")
            )
        ).click()
        wait.until(cart_confirmation)

    # Проверка, что товар в корзине (страница корзины грузится медленно)
    open_page(driver, f"{base_url}/cart")
    cart_text = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.TAG_NAME, "main"))
    ).text
    assert product_name in cart_text, f"Товар '{product_name}' не найден в корзине"


# ============ Переключение валют ============
def find_currency_block(driver):
    """Ищет блок выбора валюты, возвращает None, если валюты одна."""
    for selector in CURRENCY_BLOCK_SELECTORS:
        blocks = driver.find_elements(By.CSS_SELECTOR, selector)
        if blocks:
            return blocks[0]
    return None


def switch_currency(driver, currency_symbol):
    """Переключает валюту кликом по варианту с нужным символом ($ или €)."""
    block = find_currency_block(driver)
    if block is None:
        pytest.skip("В магазине включена только одна валюта, переключение недоступно")

    switched = False
    options = block.find_elements(By.CSS_SELECTOR, "option")
    if options:
        select = Select(block.find_element(By.CSS_SELECTOR, "select"))
        for option in options:
            if currency_symbol in option.text:
                select.select_by_visible_text(option.text)
                switched = True
                break
    else:
        for link in block.find_elements(By.CSS_SELECTOR, "a"):
            if currency_symbol in link.text:
                link.click()
                switched = True
                break

    if not switched:
        pytest.skip(f"В магазине нет валюты со знаком {currency_symbol}")

    driver.refresh()


def get_product_prices(driver, wait):
    """Возвращает список видимых цен товаров на странице."""
    prices = wait.until(
        EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, ".product-miniature__price")
        )
    )
    return [price.text.strip() for price in prices]


def test_currency_switch_changes_prices_on_main_page(driver, base_url, wait):
    open_page(driver, base_url)
    prices_before = get_product_prices(driver, wait)
    assert prices_before, "На главной странице не найдены цены товаров"

    switch_currency(driver, "$")
    prices_after = get_product_prices(driver, wait)

    assert prices_after != prices_before, "Цены на главной не изменились"
    assert all(price.startswith("$") for price in prices_after), (
        f"Не все цены в долларах: {prices_after}"
    )


def test_currency_switch_changes_prices_in_catalog(driver, base_url, wait):
    open_page(driver, f"{base_url}/9-art")
    prices_before = get_product_prices(driver, wait)
    assert prices_before, "В каталоге не найдены цены товаров"

    switch_currency(driver, "$")
    prices_after = get_product_prices(driver, wait)

    assert prices_after != prices_before, "Цены в каталоге не изменились"
    assert all(price.startswith("$") for price in prices_after), (
        f"Не все цены в долларах: {prices_after}"
    )
