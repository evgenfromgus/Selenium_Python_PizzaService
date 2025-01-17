import allure
import pytest

from final.base.base_test import BaseTest
from final.configuration.faker_data import FakerData as faker
from final.constants import customer_data


@allure.feature("Процесс оформления заказа")
@pytest.mark.base_test
class TestOrderProcess(BaseTest):
    @allure.story("Пользователь оформляет заказ на пиццу и десерты")
    @allure.description(
        "Тест проверяет весь процесс оформления заказа, включая выбор пиццы, десертов, регистрацию и оформление заказа."
    )
    @allure.title("Пользователь оформляет заказ")
    def test_order_process(self):
        self.main_page.open()
        self.main_page.add_first_pizza_to_cart()
        for _ in range(3):
            self.main_page.right_slider_click()
        for _ in range(1):
            self.main_page.right_slider_click()
        self.main_page.pizza_info()
        self.main_page.broad_pack_search("Сырный")
        self.main_page.add_to_cart_with_boarder()
        self.cart_page.open()
        first_pizza = self.cart_page.test_pizza_in_cart(
            pizza_name="Как у бабушки", boarder_name=None
        )
        assert first_pizza[2] == "1"
        second_pizza = self.cart_page.test_pizza_in_cart(
            pizza_name="4 в", boarder_name="Сырный"
        )
        assert second_pizza[2] == "1"
        self.cart_page.update_quanity(pizza_name="Как у бабушки", quantity_value=2)
        self.cart_page.confirm_card_update()
        self.cart_page.delete_pizza_from_cart(pizza_name="4 в")
        self.desert_page.open()
        self.desert_page.add_desert_to_cart(desert_name="Булочка")
        self.cart_page.open()
        self.cart_page.move_to_payment()
        self.my_account_page.open()
        self.my_account_page.click_register_button()
        self.register_page.register_user(
            username=faker.username, email=faker.email, password=faker.password
        )
        self.my_account_page.open()
        self.cart_page.open()
        total_price = self.cart_page.get_total_price()
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

        self.order_page.insert_delivery_data()
        self.order_page.delivery_payment()
        self.order_page.agree_checkbox_click()
        self.order_page.submit_order()
        self.order_page.assertion_order(
            message="Спасибо! Ваш заказ был получен.",
            money=total_price,
            first_name=f'{customer_data["first_name"]} {customer_data["last_name"]}',
            address=customer_data["address"],
            city=customer_data["city"],
            index=customer_data["postcode"],
            phone=customer_data["phone"],
        )
