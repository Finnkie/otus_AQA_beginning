from pages.admin_login_page import AdminLoginPage
from pages.catalog_page import CatalogPage
from pages.main_page import MainPage
from pages.product_page import ProductPage
from pages.registration_page import RegistrationPage


# ============ Главная страница ============
def test_main_page_has_elements(driver, base_url):
    main_page = MainPage(driver, base_url)
    main_page.open_main()

    for selector in [
        main_page.HEADER,
        main_page.LOGO,
        main_page.SEARCH_INPUT,
        main_page.CART_BLOCK,
        main_page.SIGN_IN_LINK,
        main_page.TOP_MENU,
        main_page.FOOTER,
    ]:
        main_page.find(selector)

    assert main_page.menu_links_count() >= 3, "Ожидалось минимум 3 пункта меню"
    assert len(main_page.product_cards()) >= 1, "На главной нет карточек товаров"


# ============ Каталог (категория Art) ============
def test_catalog_art_page_has_elements(driver, base_url):
    catalog_page = CatalogPage(driver, base_url)
    catalog_page.open_catalog()

    for selector in [
        catalog_page.H1,
        catalog_page.BREADCRUMB,
        catalog_page.PRODUCT_CARDS,
        catalog_page.PRODUCT_PRICE,
        catalog_page.SORT_DROPDOWN,
        catalog_page.PAGINATION,
    ]:
        catalog_page.find(selector)

    assert catalog_page.title() == "Art"
    prices = catalog_page.product_prices()
    assert any("€" in price or "$" in price for price in prices), "Нет цен у товаров"


# ============ Карточка товара ============
def test_product_page_has_elements(driver, base_url):
    main_page = MainPage(driver, base_url)
    main_page.open_main()

    _, product_url = main_page.random_product_name_and_url()
    product_page = ProductPage(driver, base_url)
    product_page.open_product(product_url)

    for selector in [
        product_page.H1,
        product_page.BREADCRUMB,
        product_page.PRICE_BLOCK,
        product_page.QUANTITY_INPUT,
        product_page.ADD_TO_CART_BUTTON,
    ]:
        product_page.find(selector)

    assert product_page.title(), "У товара нет названия"
    assert "€" in product_page.price() or "$" in product_page.price(), (
        f"Некорректная цена: {product_page.price()}"
    )


# ============ Страница логина в админку ============
def test_admin_login_page_has_elements(driver, base_url):
    admin_login_page = AdminLoginPage(driver, base_url)
    admin_login_page.open_login_page()

    for selector in [
        admin_login_page.H1,
        admin_login_page.EMAIL_INPUT,
        admin_login_page.PASSWORD_INPUT,
        admin_login_page.SUBMIT_BUTTON,
        admin_login_page.FORGOT_PASSWORD_LINK,
        admin_login_page.STAY_LOGGED_IN,
    ]:
        admin_login_page.find(selector)


# ============ Страница регистрации ============
def test_registration_page_has_elements(driver, base_url):
    registration_page = RegistrationPage(driver, base_url)
    registration_page.open_registration()

    for selector in [
        registration_page.H1,
        registration_page.FORM,
        registration_page.FIRSTNAME,
        registration_page.LASTNAME,
        registration_page.EMAIL,
        registration_page.PASSWORD,
        registration_page.GDPR_CHECKBOX,
        registration_page.SUBMIT_BUTTON,
    ]:
        registration_page.find(selector)

    assert registration_page.find(registration_page.H1).text.strip() == (
        "Create an account"
    )
