import requests
import allure

from data import generate_random_string
from url import Url

@allure.epic("Авторизация курьеров")
class TestLoginCourier:
    
    EXISTING_LOGIN = 'superman'
    EXISTING_PASSWORD = 'password2026'

    @allure.title('Успешная авторизация курьера')
    def test_success_login_courier(self):
        with allure.step('Подготовить валидные данные для входа'):
            payload = {
                "login": self.EXISTING_LOGIN, 
                "password": self.EXISTING_PASSWORD
            }

        with allure.step('Отправить POST-запрос на авторизацию'):
            url = Url.BASIC_URL + Url.LOGIN_COURIER
            response = requests.post(url, json=payload)

        with allure.step('Проверить код ответа 200'):
            assert response.status_code == 200
            
        with allure.step('Проверить, что в ответе возвращается числовой id'):
            assert 'id' in response.json()
            assert isinstance(response.json()["id"], int)

    @allure.title('Авторизация с неправильным паролем')
    def test_login_with_incorrect_password(self):
        with allure.step('Подготовить данные с неверным паролем'):
            payload = {
                "login": self.EXISTING_LOGIN, 
                "password": self.EXISTING_PASSWORD + "_wrong"
            }

        with allure.step('Отправить POST-запрос на авторизацию'):
            url = Url.BASIC_URL + Url.LOGIN_COURIER
            response = requests.post(url, json=payload)

        with allure.step('Проверить код ошибки 404'):
            assert response.status_code == 404
            
        with allure.step("Проверить сообщение, что учетная запись не найдена"):
            assert 'Учетная запись не найдена' in response.json()["message"]

    @allure.title('Авторизация с неправильным логином')
    def test_login_with_incorrect_login(self):
        with allure.step('Подготовить данные с неверным логином'):
            payload = {
                "login": self.EXISTING_LOGIN + "_wrong", 
                "password": self.EXISTING_PASSWORD
            }

        with allure.step('Отправить POST-запрос на авторизацию'):
            url = Url.BASIC_URL + Url.LOGIN_COURIER
            response = requests.post(url, json=payload)

        with allure.step('Проверить код ошибки 404'):
            assert response.status_code == 404
            
        with allure.step('Проверить сообщение, что учетная запись не найдена'):
            assert 'Учетная запись не найдена' in response.json()["message"]

    @allure.title('Авторизация под несуществующим пользователем')
    def test_login_non_existent_courier(self):
        with allure.step('Подготовить данные случайного несуществующего курьера'):
            payload = {
                "login": "non_existent_" + generate_random_string(5),
                "password": "random_password_999",
            }

        with allure.step('Отправить POST-запрос на авторизацию'):
            url = Url.BASIC_URL + Url.LOGIN_COURIER
            response = requests.post(url, json=payload)

        with allure.step('Проверить код ошибки 404'):
            assert response.status_code == 404
            
        with allure.step('Проверить сообщение, что учетная запись не найдена'):
            assert 'Учетная запись не найдена' in response.json()["message"]

    @allure.title('Авторизация без поля login')
    def test_login_without_login_returns_error(self):
        with allure.step('Подготовить тело запроса без ключа login'):
            payload = {
                "password": self.EXISTING_PASSWORD
            }

        with allure.step('Отправить POST-запрос без логина'):
            url = Url.BASIC_URL + Url.LOGIN_COURIER
            response = requests.post(url, json=payload)

        with allure.step('Проверить код ошибки 400'):
            assert response.status_code == 400
            
        with allure.step('Проверить сообщение о недостатке данных'):
            assert 'Недостаточно данных для входа' in response.json()["message"]

    @allure.title("Авторизация без поля password")
    def test_login_without_password_returns_error(self):
        with allure.step('Подготовить тело запроса без ключа password'):
            payload = {
                "login": self.EXISTING_LOGIN
            }

        with allure.step('Отправить POST-запрос без пароля'):
            url = Url.BASIC_URL + Url.LOGIN_COURIER
            response = requests.post(url, json=payload)

        with allure.step('Проверить код ошибки 400'):
            assert response.status_code == 400
            
        with allure.step('Проверить сообщение о недостатке данных'):
            assert 'Недостаточно данных для входа' in response.json()["message"]
