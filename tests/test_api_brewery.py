import pytest
from utils.http_client import HttpRequests
from pydantic import BaseModel, field_validator
from typing import Optional

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
        print(f"\nПолучен ID: {brewery_id}")
        return brewery_id

    class BrewerySchema(BaseModel):
        id: str
        name: str
        brewery_type: str
        address_1: Optional[str] = None
        address_2: Optional[str] = None
        address_3: Optional[str] = None
        city: str
        state_province: Optional[str] = None
        postal_code: Optional[str] = None
        country: str
        longitude: Optional[float] = None
        latitude: Optional[float] = None
        phone: Optional[str] = None
        website_url: Optional[str] = None
        state: Optional[str] = None
        street: Optional[str] = None
        
        @field_validator('longitude')
        def validate_longitude(cls, v):
            if v is not None:
                assert -180 <= v <= 180, "longitude вне допустимого диапазона"
            return v
        
        @field_validator('latitude')
        def validate_latitude(cls, v):
            if v is not None:
                assert -90 <= v <= 90, "latitude вне допустимого диапазона"
            return v
        
        @field_validator('brewery_type')
        def validate_brewery_type(cls, v):
            allowed_types = ["micro", "brewpub", "regional", "large", "planning", "closed"]
            assert v in allowed_types, f"Неизвестный тип: {v}"
            return v

    # Позитивный тест пивоварню по id из фикстуры, проверка по pydantic
    def test_get_random_brewery(self, brewery_client, random_brewery_id):
        response = brewery_client.get(f"/breweries/{random_brewery_id}", code=200)
        data = response.json()
        print(data)
        assert isinstance(data, dict)
        # Валидация через Pydantic
        brewery = self.BrewerySchema(**data)
        # id для второго теста
        assert brewery.id == random_brewery_id


    # Позитивный тест на рандомную пивоварню, проверка по pydantic
    def test_get_brewery_by_id(self, brewery_client):
        response = brewery_client.get(f"/breweries/random", code=200)
        data = response.json()
        
        assert isinstance(data, list)
        
        self.BrewerySchema(**data[0])


    # Позитивный тест
    @pytest.mark.parametrize("per_page, expected_min_count", [
        (1, 1), 
        (50, 1),
        (200, 1),
    ])
    def test_search_breweries_positive(self, brewery_client, per_page, expected_min_count):
        search_query = "brew"
        response = brewery_client.get(f"/breweries/search?query={search_query}&per_page={per_page}", code=200)
        data = response.json()

        # Проверяем, что ответ - список
        assert isinstance(data, list), "Ответ должен быть списком"

        # Проверяем, что количество результатов не меньше ожидаемого
        # (для запроса "brew" их точно будет больше 0)
        assert len(data) >= expected_min_count, (
            f"Ожидалось минимум {expected_min_count} результатов, получено {len(data)}"
        )

        # Проверяем, что количество результатов не превышает 50 (ограничение API)
        assert len(data) <= 50, "Количество результатов не должно превышать 50"

        # Проверяем структуру каждого результата
        for brewery in data:
            # Проверяем наличие обязательных полей
            assert "id" in brewery, "У результата нет поля id"
            assert "name" in brewery, "У результата нет поля name"
            # Проверяем, что в названии есть искомая подстрока (регистронезависимо)
            assert search_query.lower() in brewery["name"].lower(), (
                f"Название '{brewery['name']}' не содержит '{search_query}'"
            )

        print(f"\nПоиск по '{search_query}' вернул {len(data)} пивоварен")


    # # Негативный тест
    # @pytest.mark.parametrize("per_page", [
    #     0,    # Некорректное значение (0)
    #     -20,  # Некорректное значение (отрицательное)
    # ])
    # def test_search_breweries_negative(self, brewery_client, per_page):
    #     search_query = "brew"
    #     response = brewery_client.get(f"/breweries/search?query={search_query}&per_page={per_page}", code=200)
    #     data = response.json()

    #     # Проверяем, что API не падает и возвращает список
    #     assert isinstance(data, list), "Ответ должен быть списком"

    #     # Проверяем, что список пуст (API игнорирует некорректные per_page)
    #     assert len(data) == 0, (
    #         f"Для per_page={per_page} ожидался пустой список, получено {len(data)} результатов"
    #     )

    #     print(f"\n✅ Для per_page={per_page} API вернул пустой список (корректное поведение)")