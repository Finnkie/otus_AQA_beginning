# Возвращает клиента по id или None, если клиента нет.
def get_customer(connection, customer_id: int) -> dict | None:
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT * FROM ps_customer WHERE id_customer = %s",
            (customer_id,),
        )
        return cursor.fetchone()


# Создаёт нового клиента, возвращает id созданной записи.
def create_customer(connection, customer_data: dict) -> int:
    columns = ", ".join(customer_data.keys())
    placeholders = ", ".join(["%s"] * len(customer_data))
    sql = f"INSERT INTO ps_customer ({columns}) VALUES ({placeholders})"

    with connection.cursor() as cursor:
        cursor.execute(sql, tuple(customer_data.values()))
        return cursor.lastrowid


# Обновляет поля клиента по id, возвращает число изменённых строк.
def update_customer(connection, customer_id: int, updates: dict) -> int:
    assignments = ", ".join(f"{column} = %s" for column in updates)
    sql = f"UPDATE ps_customer SET {assignments} WHERE id_customer = %s"
    values = tuple(updates.values()) + (customer_id,)

    with connection.cursor() as cursor:
        return cursor.execute(sql, values)


# Удаляет клиента по id, возвращает число удалённых строк.
def delete_customer(connection, customer_id: int) -> int:
    with connection.cursor() as cursor:
        return cursor.execute(
            "DELETE FROM ps_customer WHERE id_customer = %s",
            (customer_id,),
        )
