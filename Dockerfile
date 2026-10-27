# Тесты Selenium против PrestaShop в контейнере.
# Внутри нет дисплея, поэтому браузеры всегда запускаются в headless.
#
# Сборка:   docker build -t tests .
# Запуск:   docker run -it tests --browser firefox
#           docker run -it tests --browser chrome -k main
# Параметры после имени образа передаются pytest как есть
# (--browser, --slowmo, -k, путь к тестам и т.д.).
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1

# Браузеры для selenium: google-chrome (официальный deb) и firefox-esr.
# Драйверы (chromedriver/geckodriver) Selenium скачивает сам при первом запуске.
RUN apt-get update && apt-get install -y --no-install-recommends \
        wget \
        firefox-esr \
        fonts-liberation \
    && ln -sf /usr/bin/firefox-esr /usr/bin/firefox \
    && wget -q -O /tmp/chrome.deb https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
    && apt-get install -y --no-install-recommends /tmp/chrome.deb \
    && rm -f /tmp/chrome.deb \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY conftest.py pytest.ini ./
COPY pages/ pages/
COPY tests/ tests/

# Параметры из docker run добавляются к pytest;
# --headless обязателен: дисплея в контейнере нет
ENTRYPOINT ["pytest", "--headless"]
