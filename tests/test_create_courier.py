import pytest
import requests
import allure

from url import Url
from data import generate_random_string

@allure.epic('Регистрация курьеров')
class TestCreateCourier:

    @allure.title('Успешное создание курьера')
    def test_success_create_courier(self, create_and_delete_courier):
        with allure.step('Создать тело запроса с валидными уникальными данными'):
            payload = create_and_delete_courier()
        
        with allure.step('Отправить POST-запрос'):
            url = Url.BASIC_URL + Url.CREATE_COURIER
            response = requests.post(url, json=payload)

        with allure.step('Проверить код ответа 201'):
            assert response.status_code == 201
            
        with allure.step("Проверить тело ответа {'ok': true}"):
            assert response.json() == {"ok": True}

    @allure.title('Создание курьера с уже существующим логином')
    def test_cannot_create_duplicate_courier(self):
        with allure.step('Создать тело запроса с данными существующего курьера superman'):
            payload = {
                "login": "superman",
                "password": "password2026",
                "firstName": "Klark",
            }
            url = Url.BASIC_URL + Url.CREATE_COURIER

        with allure.step('Отправить POST-запрос на создание дубликата'):
            response = requests.post(url, json=payload)

        with allure.step('Проверить код ошибки 409'):
            assert response.status_code == 409
            
        with allure.step('Проверить текст сообщения об ошибке'):
            assert 'Этот логин уже используется' in response.json()["message"]

    @allure.title('Создание курьера без поля login')
    def test_create_courier_without_login_returns_error(self):
        with allure.step('Создать тело запроса без поля login'):
            payload = {
                "password": generate_random_string(),
                "firstName": generate_random_string(),
            }
            url = Url.BASIC_URL + Url.CREATE_COURIER

        with allure.step('Отправить POST-запрос'):
            response = requests.post(url, json=payload)

        with allure.step('Проверить код ошибки 400'):
            assert response.status_code == 400
            
        with allure.step('Проверить текст сообщения об ошибке'):
            assert 'Недостаточно данных для создания учетной записи' in response.json()["message"]

    @allure.title('Создание курьера без поля password')
    def test_create_courier_without_password_returns_error(self):
        with allure.step('Создать тело запроса без поля password'):
            payload = {
                "login": generate_random_string(),
                "firstName": generate_random_string(),
            }
            url = Url.BASIC_URL + Url.CREATE_COURIER

        with allure.step('Отправить POST-запрос'):
            response = requests.post(url, json=payload)

        with allure.step('Проверить код ошибки 400'):
            assert response.status_code == 400
            
        with allure.step('Проверить текст сообщения об ошибке'):
            assert 'Недостаточно данных для создания учетной записи' in response.json()["message"]
