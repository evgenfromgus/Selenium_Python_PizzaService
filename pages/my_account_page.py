import logging

import allure
from selenium.webdriver.support import expected_conditions as ec

from final.base.base_page import BasePage
from final.configuration.links import Links

logger = logging.getLogger(__name__)


class MyAccountPage(BasePage):
    PAGE_URL = Links.MY_ACCOUNT_URL
    REGISTER_BUTTON = ("xpath", "//button[text()='Зарегистрироваться']")

    @allure.step("Переход на страницу регистрации")
    def click_register_button(self):
        self.wait.until(ec.element_to_be_clickable(self.REGISTER_BUTTON)).click()
        logger.info("Переход на страницу регистрации")
