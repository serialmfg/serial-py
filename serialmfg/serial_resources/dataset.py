"""
This file contains the Dataset class and the Datasets class.
"""
import serialmfg as serial
from ..api_client import APIClient

class Datasets:
    """
    A class for dataset data methods
    """
    @staticmethod
    def get(name, data_type, process_id=None):
        """
        Gets a dataset, if it exists
        
        Args:
        - name: Dataset name
        - data_type: Dataset data type
        - process_id?: Process ID

        Returns:
        - A dataset Python object 
        """
        client = APIClient(serial.api_key, serial.base_url)
        query_params = {"name": name, "data_type": data_type}
        if process_id:
            query_params["process_id"] = process_id
        if serial.debug:
            print(f"Getting dataset with type {data_type}: {name}")
        return Dataset(client.make_api_request("/datasets", "GET", params=query_params)[0])

class Dataset:
    """
    A dataset object python object
    """
    def __init__(self, dataset_data):
        """
        Args:
        - dataset_data: A dataset object, as defined at
        https://docs.serial.io/api-reference/datasets/get-dataset
        
        Returns:
        - A dataset Python object, which holds the api object at data, the dataset name at name, the dataset id at dataset_id and the (field) id at id
        """
        self.data = dataset_data
        self.name = dataset_data["dataset"]["name"]
        self.id = dataset_data["id"]
        self.dataset_id = dataset_data["dataset"]["id"]

