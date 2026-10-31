FROM python:3.11-slim

USER root

ENV PYTHONUNBUFFERED=1

# slim-образ + необходимые зависимости
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

# Каталоги копируются с сохранением имён: pages/ -> ./pages/
COPY conftest.py pytest.ini ./
COPY pages/ pages/
COPY tests/ tests/

# --headles: контейнер без UI
ENTRYPOINT ["pytest", "--headless"]
