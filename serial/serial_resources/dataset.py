import serial
from ..api_client import APIClient

class Datasets:
    def __init__(self):
        pass

    @staticmethod
    def get(name, data_type, process_id=None):
        client = APIClient(serial.api_key, serial.base_url)
        query_params = {"name": name, "data_type": data_type}
        if process_id:
            query_params["process_id"] = process_id
        if serial.debug:
            print(f"Getting dataset with type {data_type}: {name}")
        return Dataset(client.make_api_request("/datasets", "GET", params=query_params)[0])

class Dataset:
    def __init__(self, dataset_data):
        self.data = dataset_data
        self.name = dataset_data["dataset"]["name"]
        self.id = dataset_data["id"]
        self.dataset_id = dataset_data["dataset"]["id"]

