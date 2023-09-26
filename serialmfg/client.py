import requests
DEFAULT_BASE_URL = "https://api.serial.io"

class Client:
    def __init__(self):
        """
        Initializes a new Serial Client

        Args: 
        - debug: Boolean to turn on debug logging

        Returns:
        - A new Serial client

        Once initialized, it should be passed an api_key to handle requests,
        as well optionally receiving a station id and new base url (which defaults
        to the default serial api url of https://api.serial.io)
        """
        self.debug = False 
        self.api_key = None 
        self.station_id = None
        self.base_url = DEFAULT_BASE_URL
        self.allow_component_instance_creation = False

    def make_api_request(self, endpoint, method, params=None, data=None):
        if method == "GET":
            response = self._get(endpoint, params)
        elif method == "POST":
            response = self._post(endpoint, data)
        elif method == "PUT":
            response = self._put(endpoint, data)
        elif method == "PATCH":
            response = self._patch(endpoint, data)
        elif method == "DELETE":
            response = self._delete(endpoint, data)
        else:
            print(f"{method} is not supported by the serial python library")
            return None
        return response 
    
    def _log(self, message):
        if self.debug:
            print(f"DEBUG: {message}")

    def _get(self, endpoint, params=None):
        self._log(f"GET request to {endpoint} with params {params}")
        response = requests.get(f"{self.base_url}{endpoint}", params=params, headers={'Authorization': f'Bearer {self.api_key}'})
        response.raise_for_status()
        return response.json()

    def _post(self, endpoint, data=None):
        self._log(f"POST request to {endpoint} with data {data}")
        response = requests.post(f"{self.base_url}{endpoint}", json=data, headers={'Authorization': f'Bearer {self.api_key}'})
        response.raise_for_status()
        return response.json()

    def _put(self, endpoint, data=None):
        self._log(f"PUT request to {endpoint} with data {data}")
        response = requests.put(f"{self.base_url}{endpoint}", json=data, headers={'Authorization': f'Bearer {self.api_key}'})
        response.raise_for_status()
        return response.json()

    def _patch(self, endpoint, data=None):
        self._log(f"PATCH request to {endpoint} with data {data}")
        response = requests.patch(f"{self.base_url}{endpoint}", json=data, headers={'Authorization': f'Bearer {self.api_key}'})
        response.raise_for_status()
        return response.json()

    def _delete(self, endpoint, data=None):
        self._log(f"DELETE request to {endpoint} with data {data}")
        response = requests.delete(f"{self.base_url}{endpoint}", json=data, headers={'Authorization': f'Bearer {self.api_key}'})
        response.raise_for_status()
        return response.json()


client = Client()

