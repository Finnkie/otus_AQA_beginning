import pytest
from utils.http_client import HttpRequests


# Позитивный тест на получения случайной собаки
def test_get_random_dog():
    client = HttpRequests()
    response = client.get("/breeds/image/random", code=200)
    data = response.json()
    assert data["status"] == "success"
    assert "https://images.dog.ceo/breeds/" in data["message"] and data["message"].endswith(".jpg")
    print(f"\nОтвет: {data}")


# Позитивный тест на получения всех пород
def test_get_all_breed():
    client = HttpRequests()
    response = client.get("/breeds/list/all", code=200)
    data = response.json()
    assert data["status"] == "success"
    assert isinstance(data["message"], dict)
    print(f"\nОтвет: {data}")
    # сохраняем дату для следующего теста:
    return list(data["message"].keys())


# Позитивный тест на получения фото собаки по ВСЕМ ДОСТУПНЫМ породам
@pytest.mark.parametrize("breed", test_get_all_breed())
def test_get_image_by_breed(breed):
    client = HttpRequests()
    response = client.get(f"/breed/{breed}/images/random", code=200)
    data = response.json()
    assert data["status"] == "success"
    assert "https://images.dog.ceo/breeds/" in data["message"] and data["message"].endswith(".jpg")
    print(f"\nОтвет: {data}")


# Позитивный тест на получения фото собаки по породе
# Отдельная проверка по 3 породам на случай, если получение списка пород не работает
@pytest.mark.parametrize("breed", [
    "airedale",
    "boxer",
    "wolfhound",
])
def test_get_image_by_3_breed(breed):
    client = HttpRequests()
    response = client.get(f"/breed/{breed}/images/random", code=200)
    data = response.json()
    assert data["status"] == "success"
    assert "https://images.dog.ceo/breeds/" in data["message"] and data["message"].endswith(".jpg")
    print(f"\nОтвет: {data}")


# Позитивный тест на получения списка случайных собак
# Ограничение - 50 собак за запрос
@pytest.mark.parametrize("dogs_number, status, expected_number", [
    (1, "success", 1),
    (23, "success", 23),
    (50, "success", 50),
])
def test_random_dogs_positived(dogs_number, status, expected_number):
    client = HttpRequests()
    response = client.get(f"/breeds/image/random/{dogs_number}", code=200)
    data = response.json()
    
    assert data["status"] == status
    assert isinstance(data["message"], list)
    assert len(data["message"]) == expected_number
    
    if status == "success":
        print(f"\nОтвет: {data}")
        for url in data["message"]:
            assert url.startswith("https://images.dog.ceo/breeds/")
            assert url.endswith(".jpg")


# Негативный тест на получение списка случайных собак
@pytest.mark.parametrize("dogs_number", [-10, 0])
def test_zero_negative_dogs_with_xfail(dogs_number):
    client = HttpRequests()
    response = client.get(f"/breeds/image/random/{dogs_number}", code=None)
    
    if response.status_code == 200:
        pytest.xfail(f"БАГ JIRA-T1002: Для {dogs_number}. Код ответа: 200, ожидаемый: 400. Ответ: {response.json()}")
    
    assert response.status_code == 400

