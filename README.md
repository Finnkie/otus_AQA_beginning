# Selenium UI-тесты PrestaShop: PageObject + логирование + Allure

Автотесты магазина PrestaShop на pytest + Selenium WebDriver по шаблону PageObject,
с логированием действий и отчётностью Allure.

## Установка

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Для построения отчёта нужен allure CLI (потребуется Java):

```bash
sudo apt install default-jre-headless
# allure CLI: скачать tgz с https://github.com/allure-framework/allure2/releases
# и добавить bin/allure в PATH
```

## Запуск тестов и отчёт

```bash
pytest                  # тесты прогоняются, результаты пишутся в allure-results/
allure serve allure-results   # поднимет отчёт в браузере
```

Каталог результатов задан в `pytest.ini` (`--alluredir=allure-results`),
поэтому достаточно просто запустить pytest, а затем `allure serve`.

Прочие опции: `--browser firefox`, `--headless`, `--slowmo 0.5`,
`--base-url https://my-prestashop.example.com`.

## Что где лежит

```
conftest.py          # фикстуры driver/base_url, настройка logging,
                     # hook: скриншот и лог браузера при падении теста
pages/               # страницы магазина (PageObject)
  base_page.py       #   базовая страница: шаги allure, логгер, ожидания
  ...                #   остальные страницы с @allure.step на методах
tests/               # тесты с @allure.title
allure-results/      # результаты прогона (в git не попадают)
```

## Как устроено

**Логирование.** Каждая страница держит свой логгер (`logging.getLogger(__name__)`),
действия (открытие страниц, заполнение полей, ключевые сценарии) пишутся
в консоль уровнем INFO с временем и именем модуля. Настройка формата —
в `pytest_configure` в conftest.py.

**Шаги allure.** Методы PageObject украшены `@allure.step("...")`, поэтому
в отчёте действия страницы показываются вложенными шагами теста.
Сами тесты украшены `@allure.title("...")` — понятные русские названия в отчёте.

**Скриншот при падении.** Хук `pytest_runtest_makereport` в conftest.py
ловит момент падения теста, снимает скриншот (`driver.get_screenshot_as_png`)
и прикладывает его к отчёту через `allure.attach`, вместе с консольным
логом браузера.

## Особенности официального демо

Тесты по умолчанию идут против `https://demo.prestashop.com` (магазин выдаётся
на временном адресе — фикстура определяет его сама). Демо нестабильно:
тяжёлые страницы (админка, корзина) и POST-запросы иногда отвечают 502 —
в отчёте это видно по скриншоту падения, тесты достаточно перезапустить.
Валютных тестов два: на демо включена одна валюта, они пропускаются.
