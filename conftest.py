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
