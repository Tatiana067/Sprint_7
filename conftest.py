import pytest
import requests
import allure
from helpers import generate_random_string, register_new_courier_and_return_login_password
from url import Url

@pytest.fixture
def create_and_delete_courier():
    """Фикстура для изолированного теста создания курьера.
    Генерирует уникальные данные и гарантированно удаляет курьера после теста.
    """
    courier_data = {}

    def _create_payload():
        courier_data["login"] = generate_random_string()
        courier_data["password"] = generate_random_string()
        courier_data["firstName"] = generate_random_string()
        return courier_data

    yield _create_payload

    with allure.step("Удаление курьера, созданного в ходе теста"):
        login_url = f"{Url.BASIC_URL}{Url.LOGIN_COURIER}"
        login_payload = {
            "login": courier_data.get("login"),
            "password": courier_data.get("password")
        }
        login_response = requests.post(login_url, json=login_payload)
        courier_id = login_response.json().get("id")
        
        # Удаляем только если id успешно получен
        if courier_id:
            delete_url = f"{Url.BASIC_URL}{Url.CREATE_COURIER}/{courier_id}"
            requests.delete(delete_url)


@pytest.fixture
def order_and_courier_setup():
    """Глобальная фикстура для сквозных тестов.
    Автоматически регистрирует курьера, создает заказ, находит его ID и удаляет курьера после теста.
    """
    # 1. Регистрируем курьера и авторизуемся для получения его ID
    courier_data = register_new_courier_and_return_login_password()
    login_payload = {
        "login": courier_data[0],
        "password": courier_data[1]
    }
    login_url = f"{Url.BASIC_URL}{Url.LOGIN_COURIER}"
    login_response = requests.post(login_url, json=login_payload)
    
    # Заменяем assert на обычную проверку и вызов ошибки RuntimeError
    if login_response.status_code != 200:
        raise RuntimeError(f"Не удалось залогинить курьера: {login_response.text}")
        
    courier_id = login_response.json().get("id")

    # 2. Создаем тестовый заказ
    order_payload = {
        "firstName": "Тест",
        "lastName": "Тестов",
        "address": "Москва",
        "metroStation": 1,
        "phone": "+79999999999",
        "rentTime": 1,
        "deliveryDate": "2026-12-12",
        "comment": "коммент",
        "color": [],
    }
    create_order_url = f"{Url.BASIC_URL}{Url.CREATE_ORDER}"
    order_response = requests.post(create_order_url, json=order_payload)
    
    if order_response.status_code != 201:
        raise RuntimeError(f"Не удалось создать заказ: {order_response.text}")
        
    track = order_response.json().get("track")

    # 3. Получаем реальный ID заказа по его трек-номеру
    get_order_url = f"{Url.BASIC_URL}/api/v1/orders/track"
    get_order_response = requests.get(get_order_url, params={"t": track})
    
    if get_order_response.status_code != 200:
        raise RuntimeError(f"Не удалось найти заказ по треку: {get_order_response.text}")
        
    order_id = get_order_response.json().get("order", {}).get("id")

    # Передаем словарь с ID в тело теста
    yield {"courier_id": courier_id, "order_id": order_id}

    # 4. Блок очистки — выполняется строго после окончания теста
    if courier_id:
        with allure.step("Удаление курьера, созданного фикстурой order_and_courier_setup"):
            delete_url = f"{Url.BASIC_URL}{Url.CREATE_COURIER}/{courier_id}"
            requests.delete(delete_url)

