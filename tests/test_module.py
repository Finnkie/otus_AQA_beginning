import requests

# test_module.py --url=https://mail.ru --status_code=200

def test_url_status(url, status_code):
    response = requests.get(url, timeout=10)
    assert response.status_code == status_code, (
        f"Ожидался статус {status_code} для {url}, "
        f"получен {response.status_code}"
    )
