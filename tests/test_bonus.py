import allure
import pytest

from final.base.base_test import BaseTest


@pytest.mark.parametrize(
    "name, phone, expected_message",
    [
        ("Иван Иванов", "+79123456789", "Ваша карта оформлена!"),
        pytest.param(
            "Иван Иванов",
            "123456789",
            "Введен неверный формат телефона",
            marks=pytest.mark.xfail(reason="Pydantic валидация", strict=False),
        ),
        pytest.param(
            "",
            "+79123456789",
            "Поле 'Имя' обязательно для заполнения",
            marks=pytest.mark.xfail(reason="Pydantic валидация", strict=False),
        ),
        pytest.param(
            "Иван Иванов",
            "",
            "Поле 'Телефон' обязательно для заполнения",
            marks=pytest.mark.xfail(reason="Pydantic валидация", strict=False),
        ),
    ],
    ids=[
        "valid_data",
        "invalid_phone",
        "empty_name",
        "empty_phone",
    ],
)
@allure.feature("Бонусная программа")
@pytest.mark.bonus
class TestBonusPage(BaseTest):
    @allure.story("Пользователь оформляет бонусную программу")
    @allure.description(
        "Тест проверяет заполнение полей в форме подключения к бонусной программе И сравнивает сообщение"
    )
    @allure.title("Бонусная программа")
    def test_add_bonus_data(self, name, phone, expected_message):
        self.bonus_page.open()
        self.bonus_page.fill_bonus_data(name, phone)

        if expected_message == "Ваша карта оформлена!":
            self.bonus_page.is_success_message(expected_message)
        else:
            self.bonus_page.is_success_message(expected_message)
