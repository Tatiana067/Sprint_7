import pytest
import requests
import allure

from url import Url

@allure.epic('Управление заказами')
@allure.feature('Создание заказа')
class TestCreateOrder:

    @allure.title('Создание заказа с цветом: {color_combination}')
    @pytest.mark.parametrize(
        "color_combination",
        [
            ["BLACK"],          # Только черный цвет
            ["GREY"],           # Только серый цвет
            ["BLACK", "GREY"],  # Оба цвета
            [],                 # Без указания цвета
        ]
    )
    def test_create_order_with_various_colors(self, color_combination):
        with allure.step('Подготовить тело запроса с параметрами заказа'):
            order_payload = {
                "firstName": "Иван",
                "lastName": "Иванов",
                "address": "ул. Ленина, д. 1",
                "metroStation": 4,
                "phone": "+7 999 999 99 99",
                "rentTime": 3,
                "deliveryDate": "2026-11-30",
                "comment": "Жду у подъезда",
                "color": color_combination
            }

        with allure.step('Отправить POST-запрос на создание заказа'):
            url = Url.BASIC_URL + Url.CREATE_ORDER
            response = requests.post(url, json=order_payload)

        with allure.step('Проверить код ответа 201'):
            assert response.status_code == 201

        with allure.step('Проверить, что в ответе вернулся числовой track'):
            assert "track" in response.json()
            assert isinstance(response.json()["track"], int)
