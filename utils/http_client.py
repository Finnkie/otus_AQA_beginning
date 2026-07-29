import requests
import settings

class HttpRequests:
    def __init__(self, base_url: str):
        self.base_url = base_url

    def request(self, method, path: str, body: dict = None, headers: dict = None, code: int = 200):
        response = requests.request(method, f'{ВОТ СЮДА}', headers=headers, data=body)

    