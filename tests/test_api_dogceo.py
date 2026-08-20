import pytest
import requests


# Позитивный тест на получения случайной собаки
def test_get_random_dog(dog_api_client):
    response = dog_api_client.get("/breeds/image/random", code=200)
    data = response.json()
    assert data["status"] == "success"
    assert data["message"].startswith("https://images.dog.ceo/breeds/")
    assert data["message"].endswith(".jpg")


# Позитивный тест на получения всех пород
def test_get_all_breed(dog_api_client):
    response = dog_api_client.get("/breeds/list/all", code=200)
    data = response.json()
    assert data["status"] == "success"
    assert isinstance(data["message"], dict)
    # Список пород не пустой
    assert len(data["message"]) > 0


# Позитивный тест на получения фото собаки по ВСЕМ ДОСТУПНЫМ породам
# Список пород (ID) получаем через фикстуру all_breeds
def test_get_image_by_all_breeds(dog_api_client, all_breeds):
    assert len(all_breeds) > 0, "Список пород пуст"
    failed_breeds = []
    for breed in all_breeds:
        data = None
        # До 3 попыток: разовый сетевой сбой (таймаут и т.п.) не должен валить тест
        for attempt in range(3):
            try:
                response = dog_api_client.get(f"/breed/{breed}/images/random", code=200)
                data = response.json()
                break
            except requests.exceptions.RequestException:
                continue
        if data is None:
            failed_breeds.append(f"{breed} (сетевая ошибка)")
            continue
        try:
            assert data["status"] == "success"
            assert data["message"].startswith("https://images.dog.ceo/breeds/")
            assert data["message"].endswith(".jpg")
        except AssertionError:
            failed_breeds.append(breed)
    assert not failed_breeds, f"Для пород не получено валидное фото: {failed_breeds}"


# Позитивный тест на получения фото собаки по породе
# Отдельная проверка по 3 породам на случай недоступности списка пород
@pytest.mark.parametrize(
    "breed",
    [
        "airedale",
        "boxer",
        "wolfhound",
    ],
)
def test_get_image_by_3_breed(dog_api_client, breed):
    response = dog_api_client.get(f"/breed/{breed}/images/random", code=200)
    data = response.json()
    assert data["status"] == "success"
    assert data["message"].startswith("https://images.dog.ceo/breeds/")
    assert data["message"].endswith(".jpg")


# Позитивный тест на получения списка случайных собак
# Ограничение - 50 собак за запрос
@pytest.mark.parametrize(
    "dogs_number, status, expected_number",
    [
        (1, "success", 1),
        (23, "success", 23),
        (50, "success", 50),
    ],
)
def test_random_dogs_positived(dog_api_client, dogs_number, status, expected_number):
    response = dog_api_client.get(f"/breeds/image/random/{dogs_number}", code=200)
    data = response.json()

    assert data["status"] == status
    assert isinstance(data["message"], list)
    assert len(data["message"]) == expected_number

    if status == "success":
        for url in data["message"]:
            assert url.startswith("https://images.dog.ceo/breeds/")
            assert url.endswith(".jpg")


# Негативный тест на получение списка случайных собак
# Зашит ложно-положительный ответ с кодом 200 по багу
@pytest.mark.parametrize("dogs_number", [-10, 0])
def test_zero_negative_dogs_with_xfail(dog_api_client, dogs_number):
    response = dog_api_client.get(f"/breeds/image/random/{dogs_number}", code=None)

    if response.status_code == 200:
        pytest.xfail(
            f"БАГ JIRA-T1002: Для {dogs_number}. Код ответа: 200, ожидаемый: 400."
            f"Ответ: {response.json()}"
        )

    assert response.status_code == 400
