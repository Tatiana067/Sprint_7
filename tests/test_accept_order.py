import pytest
import requests
import allure

from url import Url

@allure.epic('Управление заказами')
@allure.feature('Принятие заказа курьером')
class TestAcceptOrder:

    @allure.title('Успешное принятие заказа курьером')
    def test_success_accept_order(self, order_and_courier_setup):
        with allure.step('Получить ID заказа и ID курьера из фикстуры'):
            order_id = order_and_courier_setup["order_id"]
            courier_id = order_and_courier_setup["courier_id"]

        with allure.step('Отправить PUT-запрос на принятие заказа'):
            url = f"{Url.BASIC_URL}{Url.ACCEPT_ORDER}{order_id}"
            params = {"courierId": courier_id}
            response = requests.put(url, params=params)

        with allure.step('Проверить код ответа 200'):
            assert response.status_code == 200
            
        with allure.step("Проверить тело ответа {'ok': true}"):
            assert response.json() == {"ok": True}

    @allure.title('Попытка принятия заказа без ID курьера')
    def test_accept_order_without_courier_id(self, order_and_courier_setup):
        with allure.step('Получить ID заказа из фикстуры'):
            order_id = order_and_courier_setup["order_id"]

        with allure.step('Отправить PUT-запрос без параметра courierId'):
            url = f"{Url.BASIC_URL}{Url.ACCEPT_ORDER}{order_id}"
            response = requests.put(url)

        with allure.step('Проверить код ошибки 400'):
            assert response.status_code == 400
            
        with allure.step('Проверить сообщение о недостатке данных'):
            assert response.json()["message"] == 'Недостаточно данных для поиска'

    @allure.title('Попытка принятия заказа с несуществующим ID курьера')
    def test_accept_order_with_invalid_courier_id(self, order_and_courier_setup):
        with allure.step('Получить ID заказа из фикстуры'):
            order_id = order_and_courier_setup["order_id"]

        with allure.step('Отправить PUT-запрос с несуществующим courierId'):
            url = f"{Url.BASIC_URL}{Url.ACCEPT_ORDER}{order_id}"
            params = {"courierId": 999999}
            response = requests.put(url, params=params)

        with allure.step('Проверить код ошибки 404'):
            assert response.status_code == 404
            
        with allure.step('Проверить сообщение, что курьер не найден'):
            assert response.json()["message"] == 'Курьера с таким id не существует'

    @allure.title('Попытка принятия заказа без указания ID заказа в пути')
    def test_accept_order_without_order_id(self, order_and_courier_setup):
        with allure.step('Получить ID курьера из фикстуры'):
            courier_id = order_and_courier_setup["courier_id"]

        with allure.step('Отправить PUT-запрос без ID заказа в URL-пути'):
            url = f"{Url.BASIC_URL}{Url.ACCEPT_ORDER}"
            params = {"courierId": courier_id}
            response = requests.put(url, params=params)

        with allure.step('Проверить код ошибки 400'):
            assert response.status_code == 400

        with allure.step('Проверить сообщение о недостатке данных'):
            assert response.json()["message"] == 'Недостаточно данных для поиска'

    @allure.title('Попытка принятия заказа с несуществующим ID заказа')
    def test_accept_order_with_invalid_order_id(self, order_and_courier_setup):
        with allure.step('Получить ID курьера из фикстуры'):
            courier_id = order_and_courier_setup["courier_id"]

        with allure.step('Отправить PUT-запрос с несуществующим ID заказа'):
            url = f"{Url.BASIC_URL}{Url.ACCEPT_ORDER}999999"
            params = {"courierId": courier_id}
            response = requests.put(url, params=params)

        with allure.step('Проверить код ошибки 404'):
            assert response.status_code == 404
            
        with allure.step('Проверить сообщение, что заказ не найден'):
            assert response.json()["message"] == 'Заказа с таким id не существует'

    @allure.title('Попытка принятия заказа, который уже взят в работу')
    def test_cannot_accept_order_already_in_work(self, order_and_courier_setup):
        with allure.step('Получить ID заказа и ID курьера из фикстуры'):
            order_id = order_and_courier_setup["order_id"]
            courier_id = order_and_courier_setup["courier_id"]
            url = f"{Url.BASIC_URL}{Url.ACCEPT_ORDER}{order_id}"
            params = {"courierId": courier_id}

        with allure.step('Первый раз принять заказ курьером'):
            requests.put(url, params=params)

        with allure.step('Повторно отправить запрос на принятие того же заказа'):
            response = requests.put(url, params=params)

        with allure.step('Проверить код ошибки конфликта 409'):
            assert response.status_code == 409

        with allure.step('Проверить сообщение, что заказ уже в работе'):
            assert response.json()["message"] == "Этот заказ уже в работе"
