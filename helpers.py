import random
import string
import requests
from url import Url

def generate_random_string(length=10):
    
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))

def register_new_courier_and_return_login_password():
    
    login_pass = []

    login = generate_random_string(10)
    password = generate_random_string(10)
    first_name = generate_random_string(10)

    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }

    url = f"{Url.BASIC_URL}{Url.CREATE_COURIER}"
    response = requests.post(url, json=payload)

    if response.status_code == 201:
        login_pass.append(login)
        login_pass.append(password)
        login_pass.append(first_name)

    return login_pass
