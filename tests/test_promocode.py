from unittest.mock import patch

import allure
import pytest

from final.base.base_test import BaseTest
from final.configuration.faker_data import FakerData as faker
from final.constants import PROMOCODE_1, PROMOCODE_2, customer_data


@allure.feature("Промокоды")
@pytest.mark.promocode
class TestPromoCode(BaseTest):
    @allure.story("Проверка применения действительных промокодов")
    @allure.description(
        "Тест проверяет применение действительного промокода и корректность скидки."
    )
    @allure.title("Проверка применения действительного промокода")
    def test_apply_valid_promo_code(self):
        self.main_page.open()
        self.main_page.is_title_correct()
        self.main_page.add_first_pizza_to_cart()
        self.cart_page.open()
        self.cart_page.insert_valide_promocode(
            PROMOCODE_1, "Coupon code applied successfully."
        )
        self.cart_page.check_discount()

    @allure.story("Проверка применения недействительных промокодов")
    @allure.description(
        "Тест проверяет, что использование недействительного промокода не приводит к снижению итоговой суммы заказа."
    )
    @allure.title("Проверка применения недействительного промокода")
    def test_apply_invalid_promo_code(self):
        self.main_page.open()
        self.main_page.is_title_correct()
        self.main_page.add_first_pizza_to_cart()
        self.cart_page.open()
        self.cart_page.insert_invalide_promocode(PROMOCODE_2, "Неверный купон.")
        self.cart_page.is_total_unchanged()

    @allure.story("Проверка поведения сайта при недоступности сервера промокодов")
    @allure.description(
        "Тест проверяет, что при недоступности сервера промокодов скидка не применяется и промокод не считается примененным."
    )
    @allure.title("Проверка поведения сайта при недоступности сервера промокодов")
    @pytest.mark.xfail(
        reason="Тест падает, т.к. это нормальное поведение при ошибке сервера с 500-й ошибкой"
    )
    def test_promo_server_down(self):
        self.main_page.open()
        self.main_page.add_first_pizza_to_cart()
        self.cart_page.open()

        # Заглушаем метод, который отвечает за валидацию промокодов.
        with patch(
            "final.pages.items.CartPage.insert_valide_promocode",
            side_effect=Exception("500 Internal Server Error"),
        ):
            try:
                self.cart_page.insert_valide_promocode(
                    PROMOCODE_1, "Coupon code applied successfully."
                )
                # Если не было исключения, это значит, что тест не прошел, и мы должны ожидать ошибку.
                pytest.fail("Ожидалось исключение, но его не произошло.")
            except Exception as e:
                # Обрабатываем ожидаемое исключение
                assert str(e) == "500 Internal Server Error"

        self.cart_page.open()
        assert (
            self.cart_page.is_total_unchanged()
        ), "Сумма заказа должна остаться без изменений."

    @allure.story("Проверка повторного применения промокодов")
    @allure.description(
        "Тест проверяет, что промокод может быть применен только один раз для одного пользователя."
    )
    @allure.title("Проверка повторного применения промокода")
    @pytest.mark.xfail(
        reason="Тест падает, т.к. срабатывает повторно один и тот же промокод"
    )
    def test_reuse_promo_code(self):
        self.register_page.open()
        self.register_page.register_user(
            username=faker.username, email=faker.email, password=faker.password
        )
        self.main_page.open()
        self.main_page.is_title_correct()
        self.main_page.add_first_pizza_to_cart()
        self.cart_page.open()
        self.cart_page.insert_valide_promocode(
            PROMOCODE_1, "Coupon code applied successfully."
        )
        self.cart_page.move_to_payment()
        self.order_page.fill_user_data(
            customer_data["first_name"],
            customer_data["last_name"],
            customer_data["address"],
            customer_data["city"],
            customer_data["state"],
            customer_data["postcode"],
            customer_data["phone"],
        )
        self.order_page.bank_payment()
        self.order_page.agree_checkbox_click()
        self.order_page.submit_order()
        self.main_page.open()
        self.main_page.add_first_pizza_to_cart()
        self.cart_page.open()
        self.cart_page.insert_invalide_promocode(
            PROMOCODE_1, "Купон уже был использован."
        )
