from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from pages.base_page import BasePage


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

    def open_registration(self):
        self.open(self.PAGE_PATH)

    def register(self, firstname, lastname, email, password):
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

    def is_registered(self):
        try:
            WebDriverWait(self.driver, 30).until(EC.url_contains("my-account"))
            return True
        except Exception:
            return False
