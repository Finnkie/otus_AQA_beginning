import pytest
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

# Официальное демо PrestaShop: лендинг отдаёт сам магазин в iframe
# с временным адресом вида https://some-name.demo.prestashop.com
DEMO_LAUNCHER_URL = "https://demo.prestashop.com"


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
        default=DEMO_LAUNCHER_URL,
        help="Базовый URL магазина PrestaShop",
    )
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Запуск браузера без графического интерфейса",
    )


def create_driver(browser_name: str, headless: bool):
    """Создаёт драйвер для выбранного браузера."""
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


def resolve_demo_shop_url(browser_name: str, headless: bool) -> str:
    """Возвращает адрес магазина с лендинга официального демо.

    demo.prestashop.com показывает магазин в iframe #framelive,
    адрес магазина выдаётся временный и появляется не сразу -
    ждём, пока лендинг создаст демо-инстанс и заполнит iframe.
    """
    driver = create_driver(browser_name, headless)
    try:
        for _ in range(3):
            driver.get(DEMO_LAUNCHER_URL)
            try:
                src = WebDriverWait(driver, 30).until(
                    lambda d: _framelive_src(d)
                )
                return src.split("/en")[0]
            except TimeoutException:
                continue
        raise RuntimeError(
            "Не удалось получить адрес демо-магазина с demo.prestashop.com"
        )
    finally:
        driver.quit()


def _framelive_src(driver):
    """Адрес магазина из iframe либо False, если он ещё не готов."""
    for frame in driver.find_elements(By.ID, "framelive"):
        src = frame.get_attribute("src") or ""
        if ".demo.prestashop.com" in src and "//fo.demo" not in src:
            return src
    return False


@pytest.fixture
def driver(request):
    """Запускает выбранный браузер и закрывает его после теста."""
    browser_name = request.config.getoption("--browser")
    headless = request.config.getoption("--headless")
    browser = create_driver(browser_name, headless)
    browser.set_page_load_timeout(30)
    yield browser
    browser.quit()


@pytest.fixture
def base_url(request):
    """Базовый URL магазина из опции --base-url.

    Если передан лендинг официального демо, определяем по нему
    реальный (временный) адрес магазина. Демо выдаёт инстансы
    с коротким временем жизни, поэтому адрес определяем заново
    перед каждым тестом.
    """
    url = request.config.getoption("--base-url").rstrip("/")
    if url == DEMO_LAUNCHER_URL:
        browser_name = request.config.getoption("--browser")
        headless = request.config.getoption("--headless")
        return resolve_demo_shop_url(browser_name, headless)
    return url


@pytest.fixture
def wait(driver):
    """Явное ожидание для использования в тестах."""
    return WebDriverWait(driver, 15)


@pytest.fixture
def admin_url(driver, base_url, wait):
    """Открывает страницу логина в админку и возвращает её адрес.

    По заданию админка доступна по /administration. На официальном
    демо она расположена по /admin-dev/index.php?controller=AdminLogin,
    поэтому при 404 пробуем запасной путь.
    """
    url = f"{base_url}/administration"
    driver.get(url)
    if "404" in (driver.title or ""):
        url = f"{base_url}/admin-dev/index.php?controller=AdminLogin"
        driver.get(url)
    wait.until(lambda d: d.find_elements(By.CSS_SELECTOR, "input[name='email']"))
    return url
