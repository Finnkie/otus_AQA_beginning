import logging

import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from pages.base_page import BasePage


logger = logging.getLogger(__name__)


# Регистрация пользователя
class RegistrationPage(BasePage):
    PAGE_PATH = "/registration"
    H1 = "h1"
    FORM = "form#customer-form"
    FIRSTNAME = "input[name='firstname']"
    LASTNAME = "input[name='lastname']"
    EMAIL = "input[name='email']"
    PASSWORD = "input[name='password']"
    GDPR_CHECKBOX = "input[name='psgdpr']"
    PRIVACY_CHECKBOX = "input[name='customer_privacy']"
    SUBMIT_BUTTON = "button[data-link-action='save-customer']"

    @allure.step("Открываем страницу регистрации")
    def open_registration(self):
        self.open(self.PAGE_PATH)

    @allure.step("Регистрируем пользователя {email}")
    def register(self, firstname, lastname, email, password):
        logger.info("Регистрируем пользователя: %s", email)
        self.fill(self.FIRSTNAME, firstname)
        self.fill(self.LASTNAME, lastname)
        self.fill(self.EMAIL, email)
        self.fill(self.PASSWORD, password)
        # Соглашения оформлены скрытыми чекбоксами - кликаем через JS
        for selector in [self.GDPR_CHECKBOX, self.PRIVACY_CHECKBOX]:
            for checkbox in self.find_all(selector):
                if not checkbox.is_selected():
                    self.driver.execute_script("arguments[0].click();", checkbox)
        self.click(self.find(self.SUBMIT_BUTTON))

    @allure.step("Проверяем переход в личный кабинет")
    def is_registered(self):
        try:
            WebDriverWait(self.driver, 30).until(EC.url_contains("my-account"))
            logger.info("Регистрация успешна")
            return True
        except Exception:
            logger.warning("Перехода в личный кабинет не случилось")
            return False
