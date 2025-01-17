import logging

import allure
from selenium.webdriver.support import expected_conditions as ec

from final.base.base_page import BasePage
from final.configuration.links import Links
from final.models.register_models import RegisterDataModel

logger = logging.getLogger(__name__)


class RegisterPage(BasePage):
    PAGE_URL = Links.REGISTER_URL
    NAME_FIELD = ("id", "reg_username")
    EMAIL_FIELD = ("id", "reg_email")
    PASS_FIELD = ("id", "reg_password")
    SUBMIT_BUTTON = ("name", "register")
    MESSAGE_ELEMENT = ("css selector", ".content-page div")

    def register_user(self, username, email, password):
        with allure.step(
            f"Заполнение формы регистрации пользователя данными: {username}, {email}, {password}"
        ):
            data = RegisterDataModel(username=username, email=email, password=password)
            logger.info(f"Регистрирую пользователя с данными: {data}")
            self.wait.until(
                ec.visibility_of_element_located(self.NAME_FIELD)
            ).send_keys(data.username)
            logger.info(f"Введено имя пользователя: {data.username}")
            self.wait.until(
                ec.visibility_of_element_located(self.EMAIL_FIELD)
            ).send_keys(data.email)
            logger.info(f"Введен email пользователя: {data.email}")
            self.wait.until(
                ec.visibility_of_element_located(self.PASS_FIELD)
            ).send_keys(data.password)
            logger.info(f"Введен пароль пользователя: {data.password}")
            self.wait.until(
                ec.visibility_of_element_located(self.SUBMIT_BUTTON)
            ).click()
            logger.info("Нажата кнопка регистрации")
            message = self.wait.until(
                ec.presence_of_element_located(self.MESSAGE_ELEMENT)
            ).text
            logger.info(f"Сообщение регистрации пользователя: {message}")
            return message
