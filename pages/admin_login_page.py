import logging

import allure
from conftest import open_page
from pages.base_page import BasePage
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


logger = logging.getLogger(__name__)


class AdminLoginPage(BasePage):
    H1 = "h1"
    EMAIL_INPUT = "input[name='email']"
    PASSWORD_INPUT = "input[name='passwd']"
    SUBMIT_BUTTON = "button[type='submit']"
    FORGOT_PASSWORD_LINK = ".show-forgot-password"
    STAY_LOGGED_IN = "#stay_logged_in"

    def __init__(self, driver, base_url):
        super().__init__(driver, base_url)
        self.admin_path = "/administration"

    @allure.step("Открываем страницу логина в админку")
    def open_login_page(self):

        if ".demo.prestashop.com" in self.base_url:
            self.admin_path = "/admin-dev/index.php?controller=AdminLogin"
            self.open(self.admin_path)
        else:
            self.open("/administration")
            if not self._login_form_appeared():
                self.admin_path = "/admin-dev/index.php?controller=AdminLogin"
                self.open(self.admin_path)
        WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, self.PASSWORD_INPUT))
        )

    def _login_form_appeared(self):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "input[type='password']")
                )
            )
            return True
        except TimeoutException:
            return False

    @allure.step("Входим в админку под {email}")
    def login(self, email, password):
        """Входит в админку и ждёт редиректа на панель управления."""
        email_input = self.wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, self.EMAIL_INPUT))
        )
        self.pause()
        email_input.clear()
        email_input.send_keys(email)
        self.driver.find_element(By.CSS_SELECTOR, self.PASSWORD_INPUT).send_keys(
            password
        )

        # Нажимаем первую видимую кнопку входа
        for button in self.find_all(self.SUBMIT_BUTTON):
            if button.is_displayed():
                button.click()
                break

        self.wait.until(EC.url_contains("AdminDashboard"))
        logger.info("Вход выполнен, открылась панель управления")

    @allure.step("Проверяем, что мы в админке")
    def is_logged_in(self):
        return "AdminDashboard" in self.driver.current_url

    @allure.step("Выходим из админки")
    def logout(self):
        """Выходит из админки по ссылке из шапки и ждёт форму логина."""

        try:
            logout_link = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "a[href*='logout']"))
            )
        except TimeoutException:
            logger.info("Ссылка выхода не найдена, перезагружаем дашборд")
            open_page(self.driver, f"{self.base_url}{self.admin_path}")
            logout_link = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "a[href*='logout']"))
            )
        logout_url = logout_link.get_attribute("href")
        admin_dir = f"{self.base_url}{self.admin_path}".split("/index.php")[0]
        open_page(self.driver, logout_url)

        # Разлогин выполнен: снова открыта форма логина
        try:
            WebDriverWait(self.driver, 30).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, self.EMAIL_INPUT))
            )
        except Exception:
            # демо иногда отвечает 502 - пробуем ещё раз открыть страницу логина
            open_page(self.driver, f"{admin_dir}/login")
            WebDriverWait(self.driver, 30).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, self.EMAIL_INPUT))
            )
        logger.info("Выход выполнен")
        return "AdminDashboard" not in self.driver.current_url
