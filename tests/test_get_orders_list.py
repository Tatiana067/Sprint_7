import requests
import allure

from url import Url

@allure.epic('Управление заказами')
@allure.feature('Получение списка заказов')
class TestGetOrdersList:

    @allure.title('Успешное получение списка всех заказов')
    def test_get_orders_list_returns_list_of_orders(self):
        with allure.step('Отправить GET-запрос для получения списка заказов'):
            url = Url.BASIC_URL + Url.PLACE_LIST_ORDER
            response = requests.get(url)

        with allure.step('Проверить код ответа 200'):
            assert response.status_code == 200

        with allure.step('Проверить, что ключ orders присутствует в ответе'):
            assert "orders" in response.json()

        with allure.step('Проверить, что значение ключа orders является списком (list)'):
            assert isinstance(response.json()["orders"], list)
