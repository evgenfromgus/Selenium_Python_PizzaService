import logging
from datetime import datetime, timedelta

import allure
from selenium.webdriver.support import expected_conditions as ec

from final.base.base_page import BasePage
from final.configuration.links import Links

logger = logging.getLogger(__name__)


class OrderPage(BasePage):
    PAGE_URL = Links.ORDER_URL
    NAME_FIELD = ("id", "billing_first_name")
    LAST_NAME_FIELD = ("id", "billing_last_name")
    ADDRESS_FIELD = ("id", "billing_address_1")
    CITY_FIELD = ("id", "billing_city")
    STATE_FIELD = ("id", "billing_state")
    POSTCODE_FIELD = ("id", "billing_postcode")
    PHONE_FIELD = ("id", "billing_phone")
    BANK_PAYMENT_METHOD = ("xpath", "//input[@id='payment_method_bacs']")
    DELIVERY_PAYMENT_METOD = ("xpath", "//input[@id='payment_method_cod']")
    CHECKBOX = ("xpath", "//input[@type='checkbox']")
    DELIVERY_DATA = ("id", "order_date")
    CONFIRM_ORDER_BUTTON = ("id", "place_order")
    SUCCESS_MESSAGE_ASSERT_ORDER = (
        "xpath",
        "//p[@class='woocommerce-notice woocommerce-notice--success woocommerce-thankyou-order-received']",
    )
    TOTAL_PRICE_ASSERT_ORDER = (
        "xpath",
        "//th[@scope='row' and text()='Total:']/following-sibling::td/span[@class='woocommerce-Price-amount amount']",
    )
    PHONE_ASSERT_ORDER = ("xpath", './/p[@class="woocommerce-customer-details--phone"]')
    ALL_ASSERT_ADDRESS_ORDER = ("xpath", ".//address")

    def fill_user_data(
        self, first_name, last_name, address, city, state, postcode, phone
    ):
        with allure.step(
            f"Заполнение данных пользователя в форме овормления заказа {first_name} {last_name} {address} {city} {state} {postcode} {phone}"
        ):
            self.wait.until(
                ec.visibility_of_element_located(self.NAME_FIELD)
            ).send_keys(first_name)
            logger.info(f"Заполнено имя {first_name}")
            self.wait.until(
                ec.visibility_of_element_located(self.LAST_NAME_FIELD)
            ).send_keys(last_name)
            logger.info(f"Заполненa фамилия {last_name}")
            self.wait.until(
                ec.visibility_of_element_located(self.ADDRESS_FIELD)
            ).send_keys(address)
            logger.info(f"Заполнен адрес {address}")
            self.wait.until(
                ec.visibility_of_element_located(self.CITY_FIELD)
            ).send_keys(city)
            logger.info(f"Заполнен город {city}")
            self.wait.until(
                ec.visibility_of_element_located(self.STATE_FIELD)
            ).send_keys(state)
            logger.info(f"Заполнено страна {state}")
            self.wait.until(
                ec.visibility_of_element_located(self.POSTCODE_FIELD)
            ).send_keys(postcode)
            logger.info(f"Заполнен почтовый индекс {postcode}")
            self.wait.until(
                ec.visibility_of_element_located(self.PHONE_FIELD)
            ).send_keys(phone)
            logger.info(f"Заполнен телефон {phone}")

    @allure.step("Ввод завтрашней даты в форму овормления заказа")
    def insert_delivery_data(self):
        tomorrow = datetime.now() + timedelta(days=1)
        formatted_date = tomorrow.strftime("%d.%m.%Y")
        self.wait.until(ec.visibility_of_element_located(self.DELIVERY_DATA)).send_keys(
            formatted_date
        )
        logger.info(f"Введена дата {formatted_date}")

    @allure.step("Выбор способа оплаты онлайн")
    def bank_payment(self):
        self.wait.until(ec.element_to_be_clickable(self.BANK_PAYMENT_METHOD)).click()
        logger.info("Выбран способ оплаты онлайн")

    @allure.step("Выбор способа оплаты после доставки")
    def delivery_payment(self):
        self.wait.until(ec.element_to_be_clickable(self.DELIVERY_PAYMENT_METOD)).click()
        logger.info("Выбран способ оплаты после доставки")

    @allure.step("Выбор чекбокса согласия с заказом")
    def agree_checkbox_click(self):
        self.wait.until(ec.element_to_be_clickable(self.CHECKBOX)).click()
        logger.info("Выбран чекбокс согласия с заказом")

    @allure.step("Отправка заказа")
    def submit_order(self):
        self.wait.until(ec.element_to_be_clickable(self.CONFIRM_ORDER_BUTTON)).click()

    @allure.step("Проверка оформленного заказа")
    def assertion_order(self, message, money, first_name, address, city, index, phone):
        as_message = self.wait.until(
            ec.visibility_of_element_located(self.SUCCESS_MESSAGE_ASSERT_ORDER)
        ).text
        assert as_message == message
        as_price = float(
            self.wait.until(
                ec.visibility_of_element_located(self.TOTAL_PRICE_ASSERT_ORDER)
            )
            .text.replace("₽", "")
            .replace(",", ".")
            .strip()
        )
        assert as_price == money
        logger.info("Cумма заказа совпадает с ожидаемой")

        as_name = self.wait.until(
            ec.visibility_of_element_located(self.ALL_ASSERT_ADDRESS_ORDER)
        ).text.split("\n")[0]
        assert as_name == first_name
        logger.info("Имя заказа совпадает с ожидаемым")

        as_address = self.wait.until(
            ec.visibility_of_element_located(self.ALL_ASSERT_ADDRESS_ORDER)
        ).text.split("\n")[1]
        assert as_address == address
        logger.info("Адрес заказа совпадает с ожидаемым")

        as_city = self.wait.until(
            ec.visibility_of_element_located(self.ALL_ASSERT_ADDRESS_ORDER)
        ).text.split("\n")[2]
        assert as_city == city
        logger.info("Город заказа совпадает с ожидаемым")

        as_index = self.wait.until(
            ec.visibility_of_element_located(self.ALL_ASSERT_ADDRESS_ORDER)
        ).text.split("\n")[4]
        assert as_index == index
        logger.info("Индекс заказа совпадает с ожидаемым")

        as_phone = self.wait.until(
            ec.visibility_of_element_located(self.PHONE_ASSERT_ORDER)
        ).text
        assert as_phone == phone
        logger.info("Телефон заказа совпадает с ожидаемым")
