class Url:
    BASIC_URL = 'https://qa-scooter.praktikum-services.ru'
    
    CREATE_COURIER = '/api/v1/courier' # Создание курьера
    LOGIN_COURIER = '/api/v1/courier/login' # Логин курьера в системе
    CREATE_ORDER = '/api/v1/orders' # Создание заказа
    PLACE_LIST_ORDER = '/api/v1/orders' # Получить список заказов
    DELETE_COERIER = '/api/v1/courier/:id' # Удаление курьера
    ACCEPT_ORDER = '/api/v1/orders/accept/' # Принять заказ
    GET_ORDER_NUMBER = '/api/v1/orders/track' # Получить заказ по его номеру
