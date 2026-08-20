import pytest
from utils.http_client import HttpRequests
from schemas.brewery_schema import BrewerySchema, BreweryMetaSchema


class TestBreweryAPI:
    # Фикстура для преобразования дефолт-url клиента
    @pytest.fixture
    def brewery_client(self):
        return HttpRequests(base_url="https://api.openbrewerydb.org/v1")

    @pytest.fixture
    def random_brewery_id(self, brewery_client):
        response = brewery_client.get("/breweries/random", code=200)
        data = response.json()
        brewery_id = data[0]["id"]
        return brewery_id

    # Позитивный тест пивоварню по id из фикстуры, проверка по pydantic
    def test_get_random_brewery(self, brewery_client, random_brewery_id):
        response = brewery_client.get(f"/breweries/{random_brewery_id}", code=200)
        data = response.json()
        assert isinstance(data, dict)
        # Валидация через Pydantic
        brewery = BrewerySchema(**data)
        # id для второго теста
        assert brewery.id == random_brewery_id

    # Позитивный тест на бизнес-проверку рандомной пивоварни, проверка по pydantic
    def test_get_brewery_by_id(self, brewery_client):
        response = brewery_client.get("/breweries/random", code=200)
        data = response.json()
        assert isinstance(data, list)
        brewery = BrewerySchema(**data[0])

        # Бизнес-проверка самих данных пивоварни
        # Название - непустое, достаточной длины и содержит буквы
        assert brewery.name.strip(), "Название пивоварни пустое"
        assert len(brewery.name.strip()) >= 2
        assert any(ch.isalpha() for ch in brewery.name), (
            f"В названии нет букв: {brewery.name}"
        )
        # Телефон (если указан) содержит хотя бы одну цифру
        if brewery.phone:
            assert any(sym.isdigit() for sym in brewery.phone), (
                f"Телефон без цифр: {brewery.phone}"
            )
        # Сайт (если указан) должен быть корректным URL
        if brewery.website_url:
            assert brewery.website_url.startswith(("http://", "https://")), (
                f"Некорректный URL сайта: {brewery.website_url}"
            )

    # Позитивный тест на рандомные пивоварни списком, с pydantic
    @pytest.mark.parametrize("per_page", [1, 50, 200])
    def test_search_breweries_positive(self, brewery_client, per_page):
        search_query = "brew"
        response = brewery_client.get(
            f"/breweries/search?query={search_query}&per_page={per_page}", code=200
        )
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == per_page
        for brewery in data:
            BrewerySchema(**brewery)

    # Негативный тест
    @pytest.mark.parametrize("per_page", [0, -20, 201, 300])
    def test_search_breweries_negative(self, brewery_client, per_page):
        search_query = "brew"
        response = brewery_client.get(
            f"/breweries/search?query={search_query}&per_page={per_page}", code=422
        )
        data = response.json()
        # Проверка, что API не падает и возвращает словарь с ошибкой
        assert isinstance(data, dict)
        assert "message" in data, "В ответе нет поля message"
        assert "must be at least 1" or "not be greater than 200" in data["message"], (
            f"Ожидалось сообщение 'must be at least 1'"
            f"или 'not be greater than 200',получено: {data['message']}"
        )

    # Позитивный тест на meta-информацию
    def test_get_breweries_meta(self, brewery_client):
        response = brewery_client.get("/breweries/meta", code=200)
        data = response.json()
        # Валидация через Pydantic
        meta = BreweryMetaSchema(**data)
        # Валидация основных полей по документации
        assert meta.total > 0
        assert len(meta.by_state) > 0
        assert len(meta.by_country) > 0
        assert len(meta.by_type) > 0
