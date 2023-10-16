import requests
import serial


class APIClient:
    """
    A class to handle API requests to the Serial API
    Attributes:
    - api_key: The API key to use for requests
    - base_url: The base url to use for requests
    Methods:
    - make_api_request: Makes an API request to the Serial API
    """
    def __init__(self, api_key, base_url):
        """
        Initializes a new API Client

        Returns:
        - A new API client

        Once initialized, it should be passed an api_key to handle requests,
        as well optionally receiving a station id and new base url (which defaults
        to the default serial api url of https://api.serial.io)
        """
        self._api_key = api_key 
        self._base_url = base_url 

    def make_api_request(self, endpoint, method, params=None, data=None, files=None):
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
        if serial.debug:
            print(f"DEBUG: {message}")

    def _get(self, endpoint, params=None):
        self._log(f"GET request to {endpoint} with params {params}")
        response = requests.get(f"{self._base_url}{endpoint}", params=params, headers={'Authorization': f'Bearer {self._api_key}'})
        return response

    def _post(self, endpoint, data=None):
        self._log(f"POST request to {endpoint} with data {data}")
        response = requests.post(f"{self._base_url}{endpoint}", json=data, headers={'Authorization': f'Bearer {self._api_key}'})
        return response

    def _post_files(self, endpoint, files):
        self._log(f"POST request to {endpoint} with file") 
        response = requests.post(f"{self._base_url}{endpoint}", files=files, headers={'Authorization': f'Bearer {self._api_key}'})
        return response

    def _put(self, endpoint, data=None):
        self._log(f"PUT request to {endpoint} with data {data}")
        response = requests.put(f"{self._base_url}{endpoint}", json=data, headers={'Authorization': f'Bearer {self._api_key}'})
        return response

    def _patch(self, endpoint, data=None):
        self._log(f"PATCH request to {endpoint} with data {data}")
        response = requests.patch(f"{self._base_url}{endpoint}", json=data, headers={'Authorization': f'Bearer {self._api_key}'})
        return response

    def _delete(self, endpoint, data=None):
        self._log(f"DELETE request to {endpoint} with data {data}")
        response = requests.delete(f"{self._base_url}{endpoint}", json=data, headers={'Authorization': f'Bearer {self._api_key}'})
        return response

