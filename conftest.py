import pytest
from utils.http_client import HttpRequests
import settings


# Фикстура для DogCEO API
@pytest.fixture
def dog_api_client():
    return HttpRequests(settings.BASE_URL_DOGCEO)


# Фикстура для получения списка всех пород (ID) из DogCEO API.
# Используется вместо вызова тестовой функции внутри параметризации
@pytest.fixture
def all_breeds(dog_api_client):
    response = dog_api_client.get("/breeds/list/all", code=200)
    data = response.json()
    assert data["status"] == "success"
    assert isinstance(data["message"], dict)
    return list(data["message"].keys())


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
