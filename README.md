# Тесты PrestaShop

## Работа с базой данных MySQL (ветка bd_hw)

Фреймворк подключается к MySQL через PyMySQL и работает с таблицей
клиентов `ps_customer`.

Запуск тестов:

```bash
pytest tests/test_customer_db.py -v
```

Параметры подключения (значения по умолчанию в скобках):

```bash
pytest tests/test_customer_db.py --host 127.0.0.1 --port 3306 \
    --database prestashop --user root --password admin
```

Поднять базу для тестов можно в docker:

```bash
docker run -d --name bd-hw-mysql -e MARIADB_ROOT_PASSWORD=admin \
    -e MARIADB_DATABASE=prestashop -p 3306:3306 mariadb:10.11
```

и создать таблицу `ps_customer` (SQL ниже в разделе «CREATE TABLE ps_customer»,
можно сохранить в schema.sql и выполнить):

```bash
docker exec -i bd-hw-mysql mariadb -uroot -padmin prestashop < schema.sql
```

### Как устроен фреймворк

- `conftest.py` — опции подключения (`--host`, `--port`, `--database`,
  `--user`, `--password`) и session-фикстура `connection`: одно соединение
  на весь прогон, `autocommit`, словарный курсор.
- `lib/db.py` — функции работы с клиентами, все запросы параметризованы:
  - `create_customer(connection, customer_data) -> int` — вставка клиента,
    возвращает id созданной записи;
  - `get_customer(connection, customer_id) -> dict | None` — клиент по id;
  - `update_customer(connection, customer_id, updates) -> int` — обновление
    полей, возвращает число изменённых строк;
  - `delete_customer(connection, customer_id) -> int` — удаление, возвращает
    число удалённых строк.
- `tests/test_customer_db.py` — сценарии: создание клиента и проверка по id,
  обновление firstname/lastname/email, негативные тесты обновления и удаления
  несуществующего клиента, удаление существующего.

### CREATE TABLE ps_customer

```sql
CREATE TABLE IF NOT EXISTS ps_customer (
  id_customer INT UNSIGNED NOT NULL AUTO_INCREMENT,
  id_shop_group INT UNSIGNED NOT NULL DEFAULT 1,
  id_shop INT UNSIGNED NOT NULL DEFAULT 1,
  id_gender INT UNSIGNED NOT NULL DEFAULT 0,
  id_default_group INT UNSIGNED NOT NULL DEFAULT 3,
  id_risk INT UNSIGNED NOT NULL DEFAULT 1,
  company VARCHAR(255) DEFAULT NULL,
  siret VARCHAR(14) DEFAULT NULL,
  ape VARCHAR(5) DEFAULT NULL,
  firstname VARCHAR(255) NOT NULL,
  lastname VARCHAR(255) NOT NULL,
  email VARCHAR(254) NOT NULL,
  passwd VARCHAR(255) NOT NULL,
  last_passwd_gen DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  birthday DATE DEFAULT NULL,
  newsletter TINYINT(1) UNSIGNED NOT NULL DEFAULT 0,
  ip_registration_newsletter VARCHAR(15) DEFAULT NULL,
  newsletter_date_add DATETIME DEFAULT NULL,
  optin TINYINT(1) UNSIGNED NOT NULL DEFAULT 0,
  website VARCHAR(128) DEFAULT NULL,
  outstanding_allow_amount DECIMAL(20,6) NOT NULL DEFAULT 0,
  show_public_prices TINYINT(1) UNSIGNED NOT NULL DEFAULT 0,
  max_payment_days INT UNSIGNED NOT NULL DEFAULT 60,
  secure_key VARCHAR(32) NOT NULL DEFAULT '-1',
  note TEXT,
  active TINYINT(1) UNSIGNED NOT NULL DEFAULT 1,
  is_guest TINYINT(1) UNSIGNED NOT NULL DEFAULT 0,
  deleted TINYINT(1) UNSIGNED NOT NULL DEFAULT 0,
  date_add DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  date_upd DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id_customer),
  UNIQUE KEY customer_email (email, id_shop)
);
```
