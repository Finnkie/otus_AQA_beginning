import pytest
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.webdriver import LocalWebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


BASE_URL = "https://demo.prestashop.com"


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
    """Открывает страницу, не падая на медленной загрузке демо.

    Демо-магазин часто грузится с таймаутом - пробуем загрузить страницу
    ещё раз (зависший запрос не мешает новой попытке). Нужные элементы
    мы всё равно ждём явными ожиданиями.
    """
    for _ in range(3):
        try:
            driver.get(url)
            return
        except TimeoutException:
            continue


def resolve_base_url(browser_name: str, headless: bool) -> str:
    driver = driver_factory(browser_name, headless)
    try:
        for _ in range(3):
            driver.get(BASE_URL)
            try:
                src = WebDriverWait(driver, 30).until(framelive_is_ready)
                return src.split("/en")[0]
            except TimeoutException:
                continue
        raise RuntimeError(
            "Не удалось получить адрес демо-магазина с demo.prestashop.com"
        )
    finally:
        driver.quit()


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
def base_url(request):
    url = request.config.getoption("--base-url").rstrip("/")
    if url == BASE_URL:
        browser_name = request.config.getoption("--browser")
        headless = request.config.getoption("--headless")
        return resolve_base_url(browser_name, headless)
    return url


@pytest.fixture
def wait(driver):
    return WebDriverWait(driver, 15)


@pytest.fixture
def admin_url(driver, base_url, wait):
    url = f"{base_url}/administration"
    open_page(driver, url)
    if "404" in (driver.title or ""):
        url = f"{base_url}/admin-dev/index.php?controller=AdminLogin"
        open_page(driver, url)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='email']")))
    return url
