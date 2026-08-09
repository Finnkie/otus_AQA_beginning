import pytest
from utils.http_client import HttpRequests
from pydantic import BaseModel, field_validator
from typing import Dict, Optional

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

    class BreweryMetaSchema(BaseModel):
        total: int
        by_state: Dict[str, int]
        by_country: Dict[str, int]
        by_type: Dict[str, int]
        page: int = 1
        per_page: int = 50
        
        @field_validator('total')
        def validate_total(cls, v):
            assert v > 0, "total должен быть больше 0"
            return v
        
        @field_validator('page')
        def validate_page(cls, v):
            assert v >= 1, "page должен быть >= 1"
            return v
        
        @field_validator('per_page')
        def validate_per_page(cls, v):
            assert 1 <= v <= 200, "per_page должен быть между 1 и 200"
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


    # Позитивный тест на 
    @pytest.mark.parametrize("per_page", [ 1, 50, 200])
    def test_search_breweries_positive(self, brewery_client, per_page):
        search_query = "brew"
        response = brewery_client.get(f"/breweries/search?query={search_query}&per_page={per_page}", code=200)
        data = response.json()

        assert isinstance(data, list)

         # для скорости обрежем проверку по pydantic
        for brewery in data:
            assert "id" in brewery, "У результата нет поля id"
            assert "name" in brewery, "У результата нет поля name"

        assert len(data) == per_page
        print(f"\nПоиск по '{search_query}' вернул {len(data)} пивоварен")

       
    # Негативный тест
    @pytest.mark.parametrize("per_page", [0, -20])
    def test_search_breweries_negative(self, brewery_client, per_page):
        search_query = "brew"
        response = brewery_client.get(f"/breweries/search?query={search_query}&per_page={per_page}", code=422)
        data = response.json()
        print(data)
        # Проверка, что API не падает и возвращает словарь с ошибкой
        assert isinstance(data, dict)
        assert "message" in data, "В ответе нет поля message"
        assert "must be at least 1" in data["message"], (
            f"Ожидалось сообщение 'must be at least 1', получено: {data['message']}"
        )

    # Позитивный тест на meta-информацию
    def test_get_breweries_meta(self, brewery_client):
        response = brewery_client.get("/breweries/meta", code=200)
        data = response.json()
        print(f"\nОтвет: {data}")
        
        # Валидация через Pydantic
        meta = self.BreweryMetaSchema(**data)
        
        # Валидация основных полей по документации
        assert meta.total > 0
        assert len(meta.by_state) > 0
        assert len(meta.by_country) > 0
        assert len(meta.by_type) > 0