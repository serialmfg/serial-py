"""
DEPRECATED, WILL BE REMOVED IN FUTURE RELEASE
"""
import requests
from warnings import warn

BASE_URL = "https://api.serial.io"


class Serial:
    def __init__(self, api_key, station_id=None, base_url=BASE_URL):
        """
        Initializes a new Station object.

        Args:
        - api_key: The API key for authentication.
        - station_id: The ID of the station.

        Returns:
        - A new Station object.
        """
        self.api_key = api_key
        self.station_id = station_id
        self.base_url = base_url
        warn('''
        The "Serial" object is being deprecated and will be removed in future releases.
        Please begin migrating to the new interface provided from `from serialmfg import client`.
        ''')


    def set_station_id(self, station_id):
        """
        Sets the station ID for the Station object.

        Args:
        - station_id: The ID of the station.
        """
        self.station_id = station_id

    def upload_process_data(self, process):
        """
        Uploads process data to the server.

        Args:
        - process: A ProcessData object containing the data to be uploaded.

        Returns:
        - A requests.Response object representing the server's response.
        """

        endpoint = self.base_url + "/process-data"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        payload = process.build_payload(station_id=self.station_id)
        response = requests.post(endpoint, headers=headers, files=payload)
        return response
    
    def initialize_identifier(self, identifier_object):
        """
        Initializes the identifier on the server.

        Returns:
        - A requests.Response object representing the server's response.
        """
        endpoint = self.base_url + "/identifier"
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        payload = {
            "identifier": identifier_object.identifier,
            "component": identifier_object.component,
            "part_number": identifier_object.part_number,
        }
        response = requests.post(endpoint, headers=headers, json=payload)
        return response
    
    def check_connection(self):
        """
        Checks to see if the server is active and if the station ID is valid

        Returns:
        - A requests.Response object representing the server's response.
        """
        endpoint = self.base_url + "/connection"
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        payload = {
            "station_id": self.station_id
        }
        response = requests.post(endpoint, headers=headers, json=payload)
        return response

    def station_id(self):
        return self.station_id

    def api_key(self):
        return self.api_key


