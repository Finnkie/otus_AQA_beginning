# Генерация отчёта

allure serve allure-results   
(Заходить по ссылке на localhost браузере)


# Что где лежит

```
conftest.py          # фикстуры driver/base_url, настройка logging,
                     # hook: скриншот и лог браузера при падении теста
pages/               # страницы магазина (PageObject)
  base_page.py       #   базовая страница: шаги allure, логгер, ожидания
  ...                #   остальные страницы с @allure.step на методах
tests/               # тесты с @allure.title
allure-results/      # результаты прогона (в git не попадают)
```


**Логирование.** Каждая страница держит свой логгер (`logging.getLogger(__name__)`),
действия (открытие страниц, заполнение полей, ключевые сценарии) пишутся
в консоль уровнем INFO с временем и именем модуля. Настройка формата —
в `pytest_configure` в conftest.py.

**Шаги allure.** 
Перед методами в PageObject навешаны декораторы `@allure.step("...")`, поэтому
в отчёте действия страницы показываются вложенными шагами теста.
Сами тесты украшены `@allure.title("...")` — понятные русские названия в отчёте.

**Скриншот при падении.** 
Хук `pytest_runtest_makereport` в conftest.py
ловит момент падения теста, снимает скриншот (`driver.get_screenshot_as_png`)
и прикладывает его к отчёту через `allure.attach`

# Запуск в Docker

Тесты можно запускать не устанавливая браузеры и зависимости себе на машину.

Сборка образа:

```bash
docker build -t tests .
```

Внутрь образа уже установлены Python, зависимости из requirements.txt,
Google Chrome и Firefox (в контейнере нет дисплея, браузеры запускаются в headless).

Запуск тестов — всё, что указано после имени образа, передаётся pytest как есть:

```bash
docker run -it tests --browser firefox          # тесты в Firefox
docker run -it tests                            # тесты в Chrome (по умолчанию)
docker run -it tests --browser chrome -k main   # только тесты с main в имени
docker run -it tests --browser firefox --slowmo 0.5
```

Так работают все опции из conftest.py: `--browser`, `--base-url`, `--slowmo`,
плюс любые аргументы pytest (`-k`, путь к конкретному файлу тестов и т.д.).

Чтобы забрать результаты allure из контейнера на хост:

```bash
docker run --rm -v $(pwd)/allure-results:/app/allure-results tests
allure serve allure-results
```
