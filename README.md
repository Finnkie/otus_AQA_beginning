# Selenium UI-тесты для PrestaShop

Домашнее задание: простые автотесты и основы Selenium (pytest + Selenium WebDriver).

## Установка

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Драйверы браузеров скачиваются автоматически (Selenium Manager), нужен установленный
Chrome или Firefox.

## Запуск

```bash
# Все тесты в Chrome
pytest

# В Firefox и headless-режиме
pytest --browser firefox --headless

# Против своего инстанса PrestaShop
pytest --base-url https://my-prestashop.example.com
```

Опции командной строки:

| Опция        | Значения          | Описание                                  |
|--------------|-------------------|-------------------------------------------|
| `--browser`  | `chrome`, `firefox` | Браузер для запуска тестов               |
| `--base-url` | URL               | Базовый URL магазина PrestaShop           |
| `--headless` | флаг              | Запуск браузера без GUI                   |

## Что проверяется

- `tests/test_ui_elements.py` — наличие элементов на пяти страницах: главная,
  каталог Art, карточка товара, логин в админку, регистрация.
  Все элементы ждутся явными ожиданиями (`WebDriverWait`).
- `tests/test_shop_scenarios.py` — сценарии: логин/разлогин в админку,
  добавление случайного товара с главной в корзину, смена валюты
  на главной и в каталоге.

## Особенности официального демо

По умолчанию тесты идут против `https://demo.prestashop.com`:

- демо отдаёт магазин в iframe с временным адресом — фикстура `base_url`
  сама определяет актуальный адрес магазина;
- админка демо живёт по `/admin-dev/index.php?controller=AdminLogin`,
  поэтому при 404 на `/administration` используется запасной путь;
- в демо включена только одна валюта, поэтому тесты переключения валют
  пропускаются (на инстансе с EUR и USD они выполняются полностью).
