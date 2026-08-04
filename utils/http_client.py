import requests
from settings import BASE_URL_DOGCEO, DEFAULT_HEADERS

class HttpRequests:
    def __init__(self, base_url=BASE_URL_DOGCEO):
        self.base_url = base_url
        self.headers = DEFAULT_HEADERS.copy()
    
    def request(self, method: str, path: str, body: dict = None, headers: dict = None, code: int = 200):
        url = f"{self.base_url}{path}"

        final_headers = self.headers.copy()
        if headers:
            final_headers.update(headers)
        
        response = requests.request(
            method=method,
            url=url,
            headers=final_headers,
            json=body
        )
        
        if code:
            assert response.status_code == code, (
                f"Ожидаемый код: {code}. Получен: {response.status_code}"
                f"Ответ сервера: {response.text[:200]}"
            )
        
        return response
    
    def get(self, path: str, headers: dict = None, code: int = 200):
        return self.request("GET", path, headers=headers, code=code)
    
    def post(self, path: str, body: dict = None, headers: dict = None, code: int = 200):
        return self.request("POST", path, body=body, headers=headers, code=code)
    
    def delete(self, path: str, headers: dict = None, code: int = 200):
        return self.request("DELETE", path, headers=headers, code=code)
    
    def put(self, path: str, body: dict = None, headers: dict = None, code: int = 200):
        return self.request("PUT", path, body=body, headers=headers, code=code)