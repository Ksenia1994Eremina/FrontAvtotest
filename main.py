import requests
import json
import pytest
import random
import string

BASE_URL = "https://reqres.in/api"

API_KEY = "reqres-free-v1"

def get_headers():
    return {
        "x-api-key": API_KEY
    }

created_user_id = None
test_user_data = None


def generate_random_string(length=8):
    """
    Генерирует случайную строку указанной длины.
    Полезно для создания уникальных тестовых данных.
    """
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(length))


def log_request_info(method, url, data=None, response=None):
    """
    Выводит информацию о запросе и ответе для отладки.
    Помогает понять, что происходит во время выполнения тестов.
    """
    print(f"\n=== {method} Request to {url} ===")
    if data:
        print(f"Request body: {json.dumps(data, indent=2)}")
    if response:
        print(f"Status code: {response.status_code}")
        try:
            print(f"Response body: {json.dumps(response.json(), indent=2)}")
        except:
            print(f"Response body: {response.text}")
    print("=" * 50)


def test_get_users_list():
    """
    Тест GET запроса для получения списка пользователей.
    Проверяет статус-код ответа и структуру данных.
    """
    url = f"{BASE_URL}/users"

    response = requests.get(url)

    log_request_info("GET", url, response=response)


    assert response.status_code == 200, f"Ожидался статус-код 200, получен {response.status_code}"


    response_data = response.json()
    assert 'data' in response_data, "Ответ не содержит ключ 'data'"
    assert 'page' in response_data, "Ответ не содержит ключ 'page'"


    assert len(response_data['data']) > 0, "Список пользователей пуст"



def test_get_single_user():
    """
    Тест GET запроса для получения информации о конкретном пользователе.
    Проверяет статус-код ответа и данные пользователя.
    """

    user_id = 2
    url = f"{BASE_URL}/users/{user_id}"


    response = requests.get(url)


    log_request_info("GET", url, response=response)


    assert response.status_code == 200, f"Ожидался статус-код 200, получен {response.status_code}"

    response_data = response.json()
    assert 'data' in response_data, "Ответ не содержит ключ 'data'"

    user_data = response_data['data']
    assert user_data[
               'id'] == user_id, f"ID пользователя в ответе ({user_data['id']}) не соответствует запрошенному ({user_id})"
    assert 'email' in user_data, "Данные пользователя не содержат email"
    assert 'first_name' in user_data, "Данные пользователя не содержат first_name"
    assert 'last_name' in user_data, "Данные пользователя не содержат last_name"



def test_create_user():
    """
    Тест POST запроса для создания нового пользователя.
    Проверяет статус-код ответа и возвращаемые данные.
    Сохраняет ID созданного пользователя для последующих тестов.
    """
    global created_user_id, test_user_data


    test_user_data = {
        "name": f"Test User {generate_random_string()}",
        "job": "QA Engineer"
    }

    url = f"{BASE_URL}/users"


    response = requests.post(url, json=test_user_data, headers=get_headers())


    log_request_info("POST", url, test_user_data, response)


    assert response.status_code == 201, f"Ожидался статус-код 201, получен {response.status_code}"

    response_data = response.json()
    assert 'id' in response_data, "Ответ не содержит ID созданного пользователя"
    assert 'name' in response_data, "Ответ не содержит имя пользователя"
    assert response_data['name'] == test_user_data['name'], "Имя пользователя в ответе не соответствует отправленному"


    created_user_id = response_data['id']



def test_update_user_put():
    """
    Тест PUT запроса для полного обновления данных пользователя.
    Проверяет статус-код ответа и обновленные данные.
    Использует ID пользователя, созданного в предыдущем тесте.
    """
    global test_user_data


    if not created_user_id:
        pytest.skip("Пропуск теста, так как ID пользователя не был получен")


    updated_user_data = {
        "name": f"Updated User {generate_random_string()}",
        "job": "Senior QA Engineer"
    }

    url = f"{BASE_URL}/users/{created_user_id}"


    response = requests.put(url, json=updated_user_data, headers=get_headers())


    log_request_info("PUT", url, updated_user_data, response)


    assert response.status_code == 200, f"Ожидался статус-код 200, получен {response.status_code}"

    response_data = response.json()
    assert 'name' in response_data, "Ответ не содержит имя пользователя"
    assert response_data['name'] == updated_user_data[
        'name'], "Имя пользователя в ответе не соответствует отправленному"


    test_user_data = updated_user_data



def test_update_user_patch():
    """
    Тест PATCH запроса для частичного обновления данных пользователя.
    Проверяет статус-код ответа и обновленные данные.
    """

    if not created_user_id:
        pytest.skip("Пропуск теста, так как ID пользователя не был получен")


    patch_data = {
        "job": "Lead QA Engineer"
    }

    url = f"{BASE_URL}/users/{created_user_id}"


    response = requests.patch(url, json=patch_data, headers=get_headers())


    log_request_info("PATCH", url, patch_data, response)


    assert response.status_code == 200, f"Ожидался статус-код 200, получен {response.status_code}"

    response_data = response.json()
    assert 'job' in response_data, "Ответ не содержит должность пользователя"
    assert response_data['job'] == patch_data['job'], "Должность пользователя в ответе не соответствует отправленной"



def test_delete_user():
    """
    Тест DELETE запроса для удаления пользователя.
    Проверяет статус-код ответа.
    """

    if not created_user_id:
        pytest.skip("Пропуск теста, так как ID пользователя не был получен")

    url = f"{BASE_URL}/users/{created_user_id}"


    response = requests.delete(url, headers=get_headers())


    log_request_info("DELETE", url, response=response)


    assert response.status_code == 204, f"Ожидался статус-код 204, получен {response.status_code}"


    assert response.text == "", "Ответ на DELETE запрос должен быть пустым"



def test_get_nonexistent_user():
    """
    Негативный тест GET запроса для получения несуществующего пользователя.
    Проверяет, что API возвращает правильный статус-код ошибки.
    """

    user_id = 999
    url = f"{BASE_URL}/users/{user_id}"


    response = requests.get(url, headers=get_headers())


    log_request_info("GET", url, response=response)


    assert response.status_code == 404, f"Ожидался статус-код 404, получен {response.status_code}"



def test_create_user_invalid_data():
    """
    Негативный тест POST запроса с невалидными данными.
    Проверяет обработку ошибочных данных сервером.
    """

    empty_data = {}

    url = f"{BASE_URL}/users"


    response = requests.post(url, json=empty_data, headers=get_headers())


    log_request_info("POST", url, empty_data, response)


    assert response.status_code == 201, f"Ожидался статус-код 201, получен {response.status_code}"



def test_register_user_successful():
    """
    Тест POST запроса для регистрации пользователя.
    Проверяет успешную регистрацию и получение токена.
    """
    register_data = {
        "email": "eve.holt@reqres.in",
        "password": "pistol"
    }

    url = f"{BASE_URL}/register"

    response = requests.post(url, json=register_data, headers=get_headers())

    log_request_info("POST", url, register_data, response)


    assert response.status_code == 200, f"Ожидался статус-код 200, получен {response.status_code}"

    response_data = response.json()
    assert 'token' in response_data, "Ответ не содержит токен"
    assert 'id' in response_data, "Ответ не содержит ID пользователя"

def test_register_user_unsuccessful():
    """
    Негативный тест POST запроса для регистрации пользователя без указания пароля.
    Проверяет обработку ошибки сервером.
    """

    incomplete_data = {
        "email": "sydney@fife"
    }

    url = f"{BASE_URL}/register"


    response = requests.post(url, json=incomplete_data, headers=get_headers())


    log_request_info("POST", url, incomplete_data, response)


    assert response.status_code == 400, f"Ожидался статус-код 400, получен {response.status_code}"

    response_data = response.json()
    assert 'error' in response_data, "Ответ не содержит сообщение об ошибке"



if __name__ == "__main__":

    print("Запуск тестов API...")


    test_get_users_list()
    test_get_single_user()
    test_create_user()
    test_update_user_put()
    test_update_user_patch()
    test_delete_user()
    test_get_nonexistent_user()
    test_create_user_invalid_data()
    test_register_user_successful()
    test_register_user_unsuccessful()

    print("\nВсе тесты выполнены!")
