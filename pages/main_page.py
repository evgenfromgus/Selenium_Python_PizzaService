import logging
import time

import allure
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.select import Select

from final.base.base_page import BasePage
from final.configuration.links import Links

logger = logging.getLogger(__name__)


class MainPage(BasePage):
    PAGE_URL = Links.PIZZERIA_URL
    FIRST_PIZZA_ADD_BUTTON = ("xpath", "(//a[@data-product_id='423'])[2]")
    SECOND_PIZZA_ADD_BUTTON = ("xpath", "(//a[@data-product_id='425'])[2]")
    LEFT_SLIDER_BUTTON = ("xpath", "(//a[@aria-label='previous'])")
    RIGHT_SLIDER_BUTTON = ("xpath", "(//a[@aria-label='next'])")
    PIZZA_INFO = ("xpath", "(//img[contains(@src, 'pexels-natasha-filippovskaya')])[2]")
    BROAD_SELECT = ("id", "board_pack")
    ADD_TO_CART_BUTTON = (By.XPATH, "//button[@name='add-to-cart']")

    @allure.step("Проверка заголовка страницы")
    def is_title_correct(self):
        assert BasePage.get_page_title(self) == "Pizzeria — Пиццерия"
        logger.info("Проверка заголовка страницы выполнена.")

    @allure.step("Добавление первой пиццы в корзину")
    def add_first_pizza_to_cart(self):
        add_button = self.wait.until(
            ec.presence_of_element_located(self.FIRST_PIZZA_ADD_BUTTON)
        )
        actions = ActionChains(self.driver)
        time.sleep(2)
        actions.move_to_element(add_button).click().perform()
        logger.info("Первая пицца добавлена в корзину.")
        time.sleep(2)

    @allure.step("Добавление второй пиццы в корзину")
    def add_second_pizza_to_cart(self):
        add_button = self.wait.until(
            ec.presence_of_element_located(self.SECOND_PIZZA_ADD_BUTTON)
        )
        actions = ActionChains(self.driver)
        actions.move_to_element(add_button).click().perform()
        logger.info("Вторая пицца добавлена в корзину.")

    @allure.step("Перемещение слайдера влево")
    def left_slider_click(self):
        logger.info("Ожидание появления элемента для слайдера влево.")
        left_slider = self.wait.until(
            ec.visibility_of_element_located(self.LEFT_SLIDER_BUTTON)
        )
        logger.info("Кнопка слайдера влево найдена, выполнение клика.")
        actions = ActionChains(self.driver)
        actions.move_to_element(left_slider).click().perform()
        logger.info("Клик по слайдеру влево выполнен.")

    @allure.step("Перемещение слайдера вправо")
    def right_slider_click(self):
        logger.info("Ожидание появления элемента для слайдера вправо.")
        right_slider = self.wait.until(
            ec.presence_of_element_located(self.RIGHT_SLIDER_BUTTON)
        )
        logger.info("Кнопка слайдера вправо найдена, выполнение клика.")
        actions = ActionChains(self.driver)
        actions.move_to_element(right_slider).click().perform()
        logger.info("Клик по слайдеру вправо выполнен.")

    @allure.step("Просмотр информации о пицце")
    def pizza_info(self):
        logger.info("Ожидание появления элемента пиццы.")
        self.wait.until(ec.visibility_of_element_located(self.PIZZA_INFO)).click()
        logger.info("Пицца найдена, выполнение клика.")

    def broad_pack_search(self, broad_name: str):
        with allure.step(f"Поиск бортика {broad_name}"):
            logger.info("Ожидание появления элемента с выбором бортика.")

            board_pack_element = self.wait.until(
                ec.visibility_of_element_located(self.BROAD_SELECT)
            )

            select = Select(board_pack_element)
            logger.info("Поиск бортика с названием: %s", broad_name)

            for option in select.options:
                if broad_name in option.text:
                    logger.info("Бортик '%s' найден, выполнение клика.", option.text)
                    select.select_by_visible_text(option.text)
                    logger.info("Бортик '%s' выбран.", broad_name)
                    break
            else:
                logger.warning("Бортик с названием '%s' не найден.", broad_name)

    @allure.step("Добавление товара в корзину")
    def add_to_cart_with_boarder(self):
        logger.info("Ожидание появления кнопки добавления товара в корзину.")
        self.wait.until(ec.presence_of_element_located(self.ADD_TO_CART_BUTTON)).click()
        logger.info("Товар добавлен в корзину.")
