import requests
import pytest
import allure

from helpers import register_new_courier_and_return_login_password
from url import Url

@allure.epic('Регистрация курьеров')
@allure.feature('Удаление курьера')
class TestDeleteCourier:

    @allure.title('Успешное удаление курьера')
    def test_success_delete_courier(self):
        with allure.step('Зарегистрировать нового курьера'):
            courier_data = register_new_courier_and_return_login_password()
        
        with allure.step('Авторизоваться для получения ID курьера'):
            login_payload = {
                "login": courier_data[0], 
                "password": courier_data[1]
            }
            login_url = Url.BASIC_URL + Url.LOGIN_COURIER
            login_response = requests.post(login_url, json=login_payload)
            courier_id = login_response.json()["id"]

        with allure.step('Отправить DELETE-запрос на удаление курьера'):
            delete_url = f"{Url.BASIC_URL}/api/v1/courier/{courier_id}"
            response = requests.delete(delete_url)

        with allure.step('Проверить код ответа 200'):
            assert response.status_code == 200
            
        with allure.step("Проверить тело ответа {'ok': true}"):
            assert response.json() == {"ok": True}

    @allure.title('Попытка удаления курьера с несуществующим ID')
    def test_delete_courier_with_non_existent_id(self):
        with allure.step("Сформировать запрос с несуществующим ID"):
            non_existent_id = 9999999
            delete_url = f"{Url.BASIC_URL}/api/v1/courier/{non_existent_id}"
        
        with allure.step('Отправить DELETE-запрос'):
            response = requests.delete(delete_url)

        with allure.step('Проверить код ошибки 404'):
            assert response.status_code == 404
            
        with allure.step('Проверить сообщение, что курьер не найден'):
            assert response.json()["message"] == 'Курьера с таким id нет'

    @allure.title('Попытка удаления курьера без указания ID')
    def test_delete_courier_without_id(self):
        with allure.step('Сформировать URL без ID курьера'):
            delete_url = f"{Url.BASIC_URL}/api/v1/courier/"
        
        with allure.step('Отправить DELETE-запрос'):
            response = requests.delete(delete_url)

        with allure.step('Проверить код ошибки 400'):
            assert response.status_code == 400

        with allure.step('Проверить сообщение о недостатке данных'):
            assert response.json()["message"] == 'Недостаточно данных для удаления курьера'
