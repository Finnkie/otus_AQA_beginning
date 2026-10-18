import pytest
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.webdriver import LocalWebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


BASE_URL = "https://demo.prestashop.com"

# замедленный режим
SLOWMO = 0.0


def pytest_addoption(parser):
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        choices=["chrome", "firefox"],
        help="Браузер для запуска тестов: chrome или firefox",
    )
    parser.addoption(
        "--base-url",
        action="store",
        default=BASE_URL,
        help="Базовый URL магазина PrestaShop",
    )
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Запуск браузера без графического интерфейса",
    )
    parser.addoption(
        "--slowmo",
        action="store",
        default=0.0,
        type=float,
        help="Пауза в секундах перед каждым действием (наглядный прогон)",
    )


def pytest_configure(config):
    global SLOWMO
    SLOWMO = config.getoption("--slowmo")


def driver_factory(browser_name: str, headless: bool) -> LocalWebDriver:
    if browser_name == "chrome":
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument("--headless=new")
        options.add_argument("--window-size=1920,1080")
        options.page_load_strategy = "eager"
        return webdriver.Chrome(options=options)

    if browser_name == "firefox":
        options = webdriver.FirefoxOptions()
        if headless:
            options.add_argument("-headless")
        options.page_load_strategy = "eager"
        return webdriver.Firefox(options=options)

    raise ValueError(f"Неизвестный браузер: {browser_name}")


def framelive_is_ready(driver):
    for frame in driver.find_elements(By.ID, "framelive"):
        src = frame.get_attribute("src") or ""
        if ".demo.prestashop.com" in src and "//fo.demo" not in src:
            return src
    return False


def open_page(driver, url):
    for _ in range(3):
        try:
            driver.get(url)
            return
        except TimeoutException:
            continue


def resolve_shop_url(driver):
    for _ in range(3):
        open_page(driver, BASE_URL)
        try:
            src = WebDriverWait(driver, 30).until(framelive_is_ready)
            return src.split("/en")[0]
        except TimeoutException:
            continue
    raise RuntimeError("Не удалось получить адрес демо-магазина с demo.prestashop.com")


@pytest.fixture
def driver(request):
    browser = driver_factory(
        request.config.getoption("--browser"),
        request.config.getoption("--headless"),
    )
    browser.set_page_load_timeout(60)
    yield browser
    browser.quit()


@pytest.fixture
def base_url(driver, request):
    url = request.config.getoption("--base-url").rstrip("/")
    if url == BASE_URL:
        return resolve_shop_url(driver)
    return url
