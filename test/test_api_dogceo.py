import pytest
from utils.http_client import HttpRequests


def test_get_random_dog():
    client = HttpRequests()
    response = client.get("/breeds/image/random", code=200)
    data = response.json()
    assert data["status"] == "success"
    assert "https://images.dog.ceo/breeds/" in data["message"] and data["message"].endswith(".jpg")
    print(f"\nresponse: {data}")


# Позитивный тест на получения списка случайных собак
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
        print(data)
        for url in data["message"]:
            assert url.startswith("https://images.dog.ceo/breeds/")
            assert url.endswith(".jpg")


# # Негативный тест на получение списка случайных собак
# @pytest.mark.parametrize("dogs_number, expected_status, expected_error", [
#     (-10, "error", "Не может быть отрицательным"),
#     (0, "error", "Не может быть равен 0"),
#     (51, "error", "Не может быть больше 50"),
#     (500, "error", "Не может быть больше 50"),
# ])
# def test_random_dogs_negative(dogs_number, expected_status, expected_error):
#     client = HttpRequests()
#     response = client.get(f"/breeds/image/random/{dogs_number}", code=200)
#     data = response.json()
    
#     assert data["status"] == expected_status
#     assert expected_error in data["message"].lower()
    
#     print(f"\nОжидаемая ошибка для {dogs_number} собак: {data['message']}")


# Ложно положительные результаты с Багами
@pytest.mark.parametrize("dogs_number, expected_number", [
    (-10, 1),
    (0, 1),
])
#@pytest.mark.xfail(reason="БАГ DOGCEO-T1002: Невалидные значения (0, отрицательные) обрабатываются с кодом 200")
def test_zero_negative_dogs(dogs_number, expected_number):
    # """
    # БАГ: DOGCEO-T1002 - Ожидается ошибка, но API возвращает успешный ответ с 1 собакой
    # Тест помечен как xfail (ожидаемое падение)
    # """
    # client = HttpRequests()
    # response = client.get(f"/breeds/image/random/{dogs_number}", code=200)
    # data = response.json()

    # print(f"ВОТ ОТВЕТ: {data}")
    # 
    # assert data["status"] == "success", f"БАГ DOGCEO-T1002: Для {dogs_number} ожидалась ошибка"

    client = HttpRequests()
    response = client.get(f"/breeds/image/random/{dogs_number}", code=None)
    
    # Жесткая проверка: только 400 статус считается правильным
    assert response.status_code == 400, (
        f"БАГ DOGCEO-T1002: Запрос с {dogs_number} вернул {response.status_code} вместо 400\n"
        f"Ответ: {response.json()}"
    )

    #assert len(data["message"]) == expected_number
    
    # Дополнительная проверка тела ответа
    data = response.json()
    assert data["status"] == "error"
    assert "invalid" in data["message"].lower() or "must be" in data["message"].lower()
    
    print(f"\n✅ PASSED: API корректно вернул 400 для {dogs_number}")