import logging
import time

import allure
from selenium.webdriver.support import expected_conditions as ec

from final.base.base_page import BasePage
from final.configuration.links import Links

logger = logging.getLogger(__name__)


class PizzaItemPage(BasePage):
    PAGE_URL = Links.PIZZA_URL
    ADD_CART_BUTTON = ("css selector", '[data-product_id="419"].add_to_cart_button')

    @allure.step("Добавление пиццы в корзину")
    def add_to_cart(self):
        self.wait.until(ec.element_to_be_clickable(self.ADD_CART_BUTTON)).click()
        logger.info(f"Нажата кнопка добавить в корзину")


class CartPage(BasePage):
    PAGE_URL = Links.CART_URL

    CODE_FIELD = ("id", "coupon_code")
    SUBMIT_BUTTON = ("css selector", "button[value='Применить купон']")
    MESSAGE = ("css selector", "div.woocommerce-message[role='alert']")
    NEGATIVE_MESSAGE = ("xpath", "//ul[@role='alert']/li")
    MOVE_TO_PAYMENT_BUTTON = (
        "css selector",
        ".wc-proceed-to-checkout .checkout-button",
    )
    TOTAL_PRICE = ("xpath", "//tr[@class='cart-subtotal']//bdi")
    PRICE_WITH_PROMO = ("xpath", "//tr[@class='order-total']//bdi")
    CARD_UPDATE_BUTTON = ("xpath", "//button[@value='Обновить корзину']")

    def insert_valide_promocode(self, code, text):
        with allure.step(
            f"Ввод валидного промокода {code} и проверка на сообщение об успехе {text}"
        ):
            code_field = self.wait.until(ec.element_to_be_clickable(self.CODE_FIELD))
            code_field.click()
            logger.info(f"Клик на поле промокода")
            time.sleep(3)
            code_field.send_keys(code)
            logger.info(f"Введен промокод {code}")
            time.sleep(3)
            self.wait.until(
                ec.visibility_of_element_located(self.SUBMIT_BUTTON)
            ).click()
            logger.info(f"Нажата кнопка применить купон")
            self.wait.until(ec.text_to_be_present_in_element(self.MESSAGE, text))
            logger.info(f"Сообщение {text}")

    def insert_invalide_promocode(self, code, text):
        with allure.step(
            f"Ввод невалидного промокода {code} и проверка на сообщение об ошибке {text}"
        ):
            code_field = self.wait.until(ec.element_to_be_clickable(self.CODE_FIELD))
            code_field.click()
            time.sleep(3)
            code_field.send_keys(code)
            time.sleep(3)
            logger.info(f"Введен промокод {code}")
            self.wait.until(
                ec.visibility_of_element_located(self.SUBMIT_BUTTON)
            ).click()
            logger.info(f"Нажата кнопка применить купон")
            self.wait.until(
                ec.text_to_be_present_in_element(self.NEGATIVE_MESSAGE, text)
            )
            logger.info(f"Сообщение {text}")

    @allure.step("Переход на страницу оплаты")
    def move_to_payment(self):
        self.wait.until(
            ec.visibility_of_element_located(self.MOVE_TO_PAYMENT_BUTTON)
        ).click()
        logger.info("Переход на страницу оплаты")

    @allure.step("Проверка корректности расчета промокода")
    def check_discount(self):
        self.wait.until(ec.presence_of_element_located(self.TOTAL_PRICE))
        self.wait.until(ec.presence_of_element_located(self.PRICE_WITH_PROMO))
        total_price = float(
            self.wait.until(ec.presence_of_element_located(self.TOTAL_PRICE))
            .text.replace("₽", "")
            .replace(",", ".")
            .strip()
        )
        promo_price = float(
            self.wait.until(ec.presence_of_element_located(self.PRICE_WITH_PROMO))
            .text.replace("₽", "")
            .replace(",", ".")
            .strip()
        )
        logger.info(f"Общая стоимость: {total_price}")
        discount = total_price * 0.10  # 10% от общей стоимости
        expected_total = total_price - discount
        logger.info(f"Скидка 10%: {discount}")
        logger.info(f"Ожидаемая сумма со скидкой 10%: {expected_total}")
        assert promo_price == expected_total

    @allure.step("Получение общей стоимости")
    def get_total_price(self):
        total_price = float(
            self.wait.until(ec.presence_of_element_located(self.TOTAL_PRICE))
            .text.replace("₽", "")
            .replace(",", ".")
            .strip()
        )
        logger.info(f"Общая стоимость: {total_price}")
        return total_price

    @allure.step("Проверка то сумма со скидкой не изменяется")
    def is_total_unchanged(self):
        self.wait.until(ec.presence_of_element_located(self.TOTAL_PRICE))
        self.wait.until(ec.presence_of_element_located(self.PRICE_WITH_PROMO))
        total_price = float(
            self.wait.until(ec.presence_of_element_located(self.TOTAL_PRICE))
            .text.replace("₽", "")
            .replace(",", ".")
            .strip()
        )
        promo_price = float(
            self.wait.until(ec.presence_of_element_located(self.PRICE_WITH_PROMO))
            .text.replace("₽", "")
            .replace(",", ".")
            .strip()
        )
        logger.info(f"Общая стоимость: {total_price}")
        assert promo_price == total_price

    def test_pizza_in_cart(self, pizza_name, boarder_name):
        with allure.step("Проверка наличия пиццы и бортика в корзине"):
            pizza_selector = (
                "xpath",
                f"//td[@class='product-name']/a[contains(text(), '{pizza_name}')]",
            )
            board_selector = (
                "xpath",
                f"//dl[@class='variation']//p[contains(text(), '{boarder_name}')]",
            )
            quantity_selector = (
                "xpath",
                f"//label[contains(text(), '{pizza_name}')]/following-sibling::input",
            )

            pizza_present = self.wait.until(
                ec.visibility_of_element_located(pizza_selector)
            )
            logger.info("Пицца '%s' найдена в корзине.", pizza_name)

            cheesy_crust_present = False
            if boarder_name is not None:
                cheesy_crust_present = self.wait.until(
                    ec.visibility_of_element_located(board_selector)
                )
                logger.info("Начинка '%s' найдена.", boarder_name)

            quantity = self.wait.until(
                ec.presence_of_element_located(quantity_selector)
            )
            quantity_value = quantity.get_attribute("value")  # Используем get_attribute
            logger.info("Количество пиццы в корзине: %s", quantity_value)

            return pizza_present, cheesy_crust_present, quantity_value

    def update_quanity(self, pizza_name, quantity_value):
        with allure.step("Обновление количества пиццы в корзине"):
            quantity_selector = (
                "xpath",
                f"//label[contains(text(), '{pizza_name}')]/following-sibling::input",
            )
            quantity_input = self.wait.until(
                ec.presence_of_element_located(quantity_selector)
            )
            quantity_input.click()
            quantity_input.clear()
            quantity_input.send_keys(quantity_value)
            logger.info("Количество пиццы в корзине обновлено")

    @allure.step("Обновление корзины")
    def confirm_card_update(self):
        self.wait.until(ec.element_to_be_clickable(self.CARD_UPDATE_BUTTON)).click()
        logger.info("Корзина обновлена")

    def delete_pizza_from_cart(self, pizza_name):
        with allure.step(f"Удаление пиццы из корзины {pizza_name}"):
            time.sleep(1)
            delete_button = (
                "xpath",
                f"//tr[td[contains(@class,'product-name')]/a[contains(text(),'{pizza_name}')]]//td[@class='product-remove']/a",
            )
            self.wait.until(ec.visibility_of_element_located(delete_button)).click()
            logger.info("Пицца '%s' удалена из корзины", pizza_name)
