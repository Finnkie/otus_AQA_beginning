from pydantic import BaseModel, field_validator


class BrewerySchema(BaseModel):
    id: str
    name: str
    brewery_type: str
    address_1: str | None = None
    address_2: str | None = None
    address_3: str | None = None
    city: str
    state_province: str | None = None
    postal_code: str | None = None
    country: str
    longitude: float | None = None
    latitude: float | None = None
    phone: str | None = None
    website_url: str | None = None
    state: str | None = None
    street: str | None = None

    @field_validator("longitude")
    def validate_longitude(cls, v):
        if v is not None:
            assert -180 <= v <= 180, "longitude вне допустимого диапазона"
        return v

    @field_validator("latitude")
    def validate_latitude(cls, v):
        if v is not None:
            assert -90 <= v <= 90, "latitude вне допустимого диапазона"
        return v

    @field_validator("brewery_type")
    def validate_brewery_type(cls, v):
        allowed_types = [
            "micro",
            "brewpub",
            "regional",
            "large",
            "planning",
            "closed",
            "contract",
            "bar",
            "taproom",
            "nano",
            "proprietor",
        ]
        assert v in allowed_types, f"Неизвестный тип: {v}"
        return v


class BreweryMetaSchema(BaseModel):
    total: int
    by_state: dict[str, int]
    by_country: dict[str, int]
    by_type: dict[str, int]
    page: int = 1
    per_page: int = 50

    @field_validator("total")
    def validate_total(cls, v):
        assert v > 0, "total должен быть больше 0"
        return v

    @field_validator("page")
    def validate_page(cls, v):
        assert v >= 1, "page должен быть >= 1"
        return v

    @field_validator("per_page")
    def validate_per_page(cls, v):
        assert 1 <= v <= 200, "per_page должен быть между 1 и 200"
        return v