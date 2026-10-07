"""Новые сценарии: регистрация покупателя и валюта из верхнего меню."""
import random

from pages.main_page import MainPage
from pages.registration_page import RegistrationPage


# ============ Регистрация нового пользователя ============
def test_register_new_user(driver, base_url):
    registration_page = RegistrationPage(driver, base_url)
    registration_page.open_registration()

    email = f"autotest{random.randint(1000, 9999)}@example.com"
    registration_page.register(
        firstname="Autotest",
        lastname="Testerov",
        email=email,
        password="Autotest123!",
    )

    assert registration_page.is_registered(), (
        f"Регистрация пользователя {email} не завершилась переходом в личный кабинет"
    )


# ============ Переключение валюты из верхнего меню ============
def test_switch_currency_from_top_menu(driver, base_url):
    main_page = MainPage(driver, base_url)
    main_page.open_main()

    prices_before = main_page.product_prices()
    assert prices_before, "На главной не найдены цены товаров"

    main_page.switch_currency("$")
    prices_after = main_page.product_prices()

    assert prices_after != prices_before, "Цены на главной не изменились"
    assert all(price.startswith("$") for price in prices_after), (
        f"Не все цены в долларах: {prices_after}"
    )
