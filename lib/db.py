"""Функции для работы с базой данных PrestaShop.

Все функции принимают connection (pymysql-соединение) и работают
с таблицей ps_customer. Запросы параметризованы, значения подставляются
через плейсхолдеры %s.
"""


def get_customer(connection, customer_id: int) -> dict | None:
    """Возвращает клиента по id или None, если клиента нет."""
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT * FROM ps_customer WHERE id_customer = %s",
            (customer_id,),
        )
        return cursor.fetchone()


def create_customer(connection, customer_data: dict) -> int:
    """Создаёт нового клиента, возвращает id созданной записи.

    Ключи словаря customer_data - имена колонок таблицы ps_customer.
    """
    columns = ", ".join(customer_data.keys())
    placeholders = ", ".join(["%s"] * len(customer_data))
    sql = f"INSERT INTO ps_customer ({columns}) VALUES ({placeholders})"

    with connection.cursor() as cursor:
        cursor.execute(sql, tuple(customer_data.values()))
        return cursor.lastrowid


def update_customer(connection, customer_id: int, updates: dict) -> int:
    """Обновляет поля клиента по id, возвращает число изменённых строк.

    Ключи словаря updates - имена колонок, значения - новые значения.
    Для несуществующего клиента вернёт 0.
    """
    assignments = ", ".join(f"{column} = %s" for column in updates)
    sql = f"UPDATE ps_customer SET {assignments} WHERE id_customer = %s"
    values = tuple(updates.values()) + (customer_id,)

    with connection.cursor() as cursor:
        return cursor.execute(sql, values)


def delete_customer(connection, customer_id: int) -> int:
    """Удаляет клиента по id, возвращает число удалённых строк.

    Для несуществующего клиента вернёт 0.
    """
    with connection.cursor() as cursor:
        return cursor.execute(
            "DELETE FROM ps_customer WHERE id_customer = %s",
            (customer_id,),
        )
