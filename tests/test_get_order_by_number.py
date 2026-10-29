import pytest
import requests
import allure

from url import Url

@allure.epic('Управление заказами')
@allure.feature('Получение заказа по его номеру')
class TestGetOrderByNumber:

    @allure.title('Успешное получение заказа по его номеру трека')
    def test_success_get_order_by_number(self):
        with allure.step('Создать тестовый заказ и получить его трек-номер'):
            order_payload = {
                "firstName": "Петр",
                "lastName": "Петров",
                "address": "Смоленск",
                "metroStation": 2,
                "phone": "+79991112233",
                "rentTime": 2,
                "deliveryDate": "2026-11-15",
                "comment": "Позвонить за час",
                "color": [],
            }
            create_url = f"{Url.BASIC_URL}{Url.CREATE_ORDER}"
            order_response = requests.post(create_url, json=order_payload)
            track_number = order_response.json()["track"]

        with allure.step('Отправить GET-запрос для получения заказа по треку'):
            get_order_url = f"{Url.BASIC_URL}/api/v1/orders/track"
            response = requests.get(get_order_url, params={"t": track_number})

        with allure.step('Проверить код ответа 200'):
            assert response.status_code == 200
            
        with allure.step('Проверить, что в ответе содержится объект order'):
            assert "order" in response.json()
            assert isinstance(response.json()["order"], dict)

    @allure.title('Попытка получения заказа без указания номера трека')
    def test_get_order_without_number(self):
        with allure.step('Отправить GET-запрос с пустым параметром трека'):
            get_order_url = f"{Url.BASIC_URL}/api/v1/orders/track"
            response = requests.get(get_order_url, params={"t": ""})

        with allure.step('Проверить код ошибки 400'):
            assert response.status_code == 400
            
        with allure.step('Проверить сообщение о недостатке данных'):
            assert "Недостаточно данных для поиска" in response.json()["message"]

    @allure.title('Попытка получения заказа по несуществующему номеру трека')
    def test_get_order_with_non_existent_number(self):
        with allure.step('Отправить GET-запрос с несуществующим номером трека'):
            get_order_url = f"{Url.BASIC_URL}/api/v1/orders/track"
            invalid_track = 999999999
            response = requests.get(get_order_url, params={"t": invalid_track})

        with allure.step('Проверить код ошибки 404'):
            assert response.status_code == 404
            
        with allure.step('Проверить сообщение, что заказ не найден'):
            assert 'Заказ не найден' in response.json()["message"]
