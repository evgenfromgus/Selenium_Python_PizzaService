import pytest

from final.pages.bonus_page import BonusPage
from final.pages.cart_page import PizzaItemPage, CartPage
from final.pages.deserts_page import DesertsPage
from final.pages.main_page import MainPage
from final.pages.my_account_page import MyAccountPage
from final.pages.order_page import OrderPage
from final.pages.user_page import RegisterPage


class BaseTest:
    register_page: RegisterPage
    main_page: MainPage
    pizza_page: PizzaItemPage
    cart_page: CartPage
    bonus_page: BonusPage
    order_page: OrderPage
    desert_page: DesertsPage
    my_account_page: MyAccountPage

    @pytest.fixture(autouse=True)
    def setup(self, request, driver):
        request.cls.driver = driver

        request.cls.register_page = RegisterPage(driver)
        request.cls.main_page = MainPage(driver)
        request.cls.pizza_page = PizzaItemPage(driver)
        request.cls.cart_page = CartPage(driver)
        request.cls.bonus_page = BonusPage(driver)
        request.cls.order_page = OrderPage(driver)
        request.cls.desert_page = DesertsPage(driver)
        request.cls.my_account_page = MyAccountPage(driver)
