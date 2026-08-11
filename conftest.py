import pytest
from utils.http_client import HttpRequests
import settings


# Фикстура для DogCEO API
@pytest.fixture
def dog_api_client():
    return HttpRequests(settings.BASE_URL_DOGCEO)


# Фикстура для Open Brewery API
@pytest.fixture
def brewery_api_client():
    return HttpRequests(settings.BASE_URL_BREWERY)


# Фикстура для JSON Placeholder API
@pytest.fixture
def json_api_client():
    return HttpRequests(settings.BASE_URL_JSON)


# ===========  Для test_module.py

def pytest_addoption(parser):
    parser.addoption(
        "--url",
        action="store",
        default="https://ya.ru",
    )
    parser.addoption(
        "--status_code",
        action="store",
        default=200,
        type=int,
    )

@pytest.fixture
def url(request):
    return request.config.getoption("--url")

@pytest.fixture
def status_code(request):
    return request.config.getoption("--status_code")
