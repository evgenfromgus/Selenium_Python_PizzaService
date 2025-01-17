import logging

import allure
from selenium.webdriver.support import expected_conditions as ec

from final.base.base_page import BasePage
from final.configuration.links import Links
from final.models.bonus_models import BonusDataModel

logger = logging.getLogger(__name__)


class BonusPage(BasePage):
    PAGE_URL = Links.BONUS_URL
    USER_NAME_FIELD = ("id", "bonus_username")
    USER_PHONE_FIELD = ("id", "bonus_phone")
    SUBMIT_BUTTON = ("class name", "woocommerce-Button")
    SUCCESS_MESSAGE = ("xpath", "//div[@id='bonus_main']/h3")

    def is_title_correct(self, expected_title):
        with allure.step(f"Проверка заголовка страницы: {expected_title}"):
            actual_title = BasePage.get_page_title(self.driver)
            assert actual_title == expected_title
            logger.info(f"Проверка заголовка страницы: {actual_title}")

    def fill_bonus_data(self, name: str, phone: str):
        with allure.step(f"Заполнение формы бонусной программы: {name}, {phone}"):
            data = BonusDataModel(name=name, phone=phone)
            logger.info(f"Заполнение формы бонусной программы: {data}")
            self.wait.until(
                ec.visibility_of_element_located(self.USER_NAME_FIELD)
            ).send_keys(data.name)
            self.wait.until(
                ec.visibility_of_element_located(self.USER_PHONE_FIELD)
            ).send_keys(data.phone)
            self.wait.until(
                ec.visibility_of_element_located(self.SUBMIT_BUTTON)
            ).click()
            self.wait.until(ec.alert_is_present()).accept()

    def is_success_message(self, message: str):
        with allure.step(f"Проверка сообщения об успехе: {message}"):
            self.wait.until(
                ec.text_to_be_present_in_element(self.SUCCESS_MESSAGE, message)
            )
            logger.info(f"Проверка сообщения об успехе: {message}")
