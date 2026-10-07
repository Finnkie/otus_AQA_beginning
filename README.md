# Selenium UI-тесты для PrestaShop (PageObject)

Автотесты магазина PrestaShop на pytest + Selenium WebDriver по шаблону PageObject.

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
pytest                          # все тесты в Chrome
pytest --browser firefox        # в Firefox
pytest --headless               # без окна браузера
pytest --slowmo 0.5             # пауза 0.5 с перед каждым действием (наглядный прогон)
pytest --base-url https://my-prestashop.example.com   # свой инстанс
```

## Структура проекта

```
conftest.py          # опции pytest, фикстуры driver и base_url, open_page
pages/               # страницы магазина (PageObject)
  base_page.py       #   базовая страница: ожидания, клики, цены, валюта
  main_page.py       #   главная страница
  catalog_page.py    #   каталог (категория Art)
  product_page.py    #   карточка товара
  cart_page.py       #   корзина
  registration_page.py     #  регистрация покупателя
  admin_login_page.py      #  логин/разлогин в админку
  admin_products_page.py   #  список товаров в админке
  admin_new_product_page.py #  форма нового товара
tests/
  test_ui_elements.py      # наличие элементов на 5 страницах
  test_shop_scenarios.py   # логин/разлогин, корзина, валюта в каталоге
  test_user_scenarios.py   # регистрация, валюта из верхнего меню
  test_admin_scenarios.py  # создание и удаление товара в админке
```

## Особенности официального демо

По умолчанию тесты идут против `https://demo.prestashop.com`:

- демо отдаёт магазин в iframe с временным адресом — фикстура `base_url`
  сама определяет актуальный адрес магазина;
- админка демо живёт по `/admin-dev/...`, при 404 на `/administration`
  страница логина использует запасной путь (креды демо:
  `demo@prestashop.com` / `prestashop_demo`);
- в демо включена только одна валюта, поэтому тесты переключения валют
  пропускаются (на инстансе с EUR и USD они выполняются полностью);
- демо нестабильно: тяжёлые страницы (админка, корзина) и POST-запросы
  иногда отвечают 502 — в таком случае тесты достаточно перезапустить.
