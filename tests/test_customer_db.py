"""Тесты работы с клиентами PrestaShop (таблица ps_customer)."""
import random

import allure

from lib.db import (
    create_customer,
    delete_customer,
    get_customer,
    update_customer,
)


def make_customer_data(email_suffix=""):
    """Готовит данные нового клиента."""
    return {
        "firstname": "Иван",
        "lastname": "Тестов",
        "email": f"sql.test{random.randint(10000, 99999)}{email_suffix}@example.com",
        "passwd": "Secret123!",
        "newsletter": 0,
        "optin": 1,
        "active": 1,
    }


@allure.title("Создание нового клиента в базе")
def test_create_customer(connection):
    customer_data = make_customer_data()
    customer_id = create_customer(connection, customer_data)

    # Клиент найден по id и все переданные поля совпадают
    customer = get_customer(connection, customer_id)
    assert customer is not None, f"Клиент с id={customer_id} не найден в базе"
    assert customer["id_customer"] == customer_id
    assert customer["firstname"] == customer_data["firstname"]
    assert customer["lastname"] == customer_data["lastname"]
    assert customer["email"] == customer_data["email"]
    assert customer["active"] == 1


@allure.title("Обновление данных существующего клиента")
def test_update_customer(connection):
    customer_id = create_customer(connection, make_customer_data())

    new_data = {
        "firstname": "Пётр",
        "lastname": "Обновлённый",
        "email": f"updated{random.randint(10000, 99999)}@example.com",
    }
    updated_rows = update_customer(connection, customer_id, new_data)
    assert updated_rows == 1, "Должна быть изменена ровно одна строка"

    # Данные клиента в базе совпадают с новыми значениями
    customer = get_customer(connection, customer_id)
    assert customer["firstname"] == new_data["firstname"]
    assert customer["lastname"] == new_data["lastname"]
    assert customer["email"] == new_data["email"]


@allure.title("Негативный: обновление несуществующего клиента")
def test_update_nonexistent_customer(connection):
    nonexistent_id = 999999999

    updated_rows = update_customer(
        connection, nonexistent_id, {"firstname": "Никто"}
    )

    # Ни одна строка не изменилась, клиент с таким id не появился
    assert updated_rows == 0, "Обновление несуществующего клиента изменило строки"
    assert get_customer(connection, nonexistent_id) is None


@allure.title("Удаление существующего клиента")
def test_delete_customer(connection):
    customer_id = create_customer(connection, make_customer_data())
    assert get_customer(connection, customer_id) is not None

    deleted_rows = delete_customer(connection, customer_id)
    assert deleted_rows == 1, "Должна быть удалена ровно одна строка"

    # Клиента больше нет в базе
    assert get_customer(connection, customer_id) is None


@allure.title("Негативный: удаление несуществующего клиента")
def test_delete_nonexistent_customer(connection):
    nonexistent_id = 999999999

    deleted_rows = delete_customer(connection, nonexistent_id)

    # Удалить некого: ни одна строка не затронута
    assert deleted_rows == 0
