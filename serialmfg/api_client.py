import requests
from . import config

class SingletonMeta(type):
    """
    This is a thread-safe implementation of Singleton.
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

class APIClient(metaclass=SingletonMeta):
    def __init__(self):
        # The init method should only be called once.
        if not config.api_key or not config.base_url:
            raise ValueError("API client requires an API key and base URL")

        self.session = requests.Session()
        self.update_headers()

    def update_headers(self):
        if config.api_key:
            self.session.headers.update({'Authorization': f'Bearer {config.api_key}'})

    def make_api_request(self, endpoint, method, params=None, data=None, files=None):
        self.update_headers()
        if method == "GET":
            response = self._get(endpoint, params)
        elif method == "POST" and not files:
            response = self._post(endpoint, data=data)
        elif method == "POST" and files:
            response = self._post_files(endpoint, files=files)
        elif method == "PUT":
            response = self._put(endpoint, data)
        elif method == "PATCH":
            response = self._patch(endpoint, data)
        elif method == "DELETE":
            response = self._delete(endpoint, data)
        else:
            print(f"{method} is not supported by the serial python library")
            return None
        
        if not response.ok:
            self._error(response.text)
            response.raise_for_status()
            return None
        return response.json()
    
    def _error(self, message):
        print(f"ERROR: {message}")

    def _log(self, message):
        # TODO: debug logging
        #print(f"DEBUG: {message}")

    def _get(self, endpoint, params=None):
        self._log(f"GET request to {endpoint} with params {params}")
        response = self.session.get(f"{config.base_url}{endpoint}", params=params) 
        return response

    def _post(self, endpoint, data=None):
        self._log(f"POST request to {endpoint} with data {data}")
        response = self.session.post(f"{config.base_url}{endpoint}", json=data) 
        return response

    def _post_files(self, endpoint, files):
        self._log(f"POST request to {endpoint} with file") 
        response = self.session.post(f"{config.base_url}{endpoint}", files=files)
        return response

    def _put(self, endpoint, data=None):
        self._log(f"PUT request to {endpoint} with data {data}")
        response = self.session.put(f"{config.base_url}{endpoint}", json=data)
        return response

    def _patch(self, endpoint, data=None):
        self._log(f"PATCH request to {endpoint} with data {data}")
        response = self.session.patch(f"{config.base_url}{endpoint}", json=data)
        return response

    def _delete(self, endpoint, data=None):
        self._log(f"DELETE request to {endpoint} with data {data}")
        response = self.session.delete(f"{config.base_url}{endpoint}", json=data)
        return response

