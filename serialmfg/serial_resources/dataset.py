"""
This file contains the Dataset class and the Datasets class.
"""
from ..api_client import APIClient

class Datasets:
    """
    A class for dataset data methods
    """
    @staticmethod
    def get(name, data_type, process_id):
        """
        Gets a dataset, if it exists
        
        Args:
        - name: Dataset name
        - data_type: Dataset data type

        Returns:
        - A dataset Python object 
        """
        client = APIClient()
        query_params = {"name": name, "type": data_type, "process_id": process_id}
        # TODO: debug logging
        print(f"Getting dataset {name} of type {data_type}")
        return Dataset(client.make_api_request("/datasets", "GET", params=query_params)[0])
    
    @staticmethod
    def create(name, data_type, process_id, extra_params=None):
        """
        Creates a dataset, if it does not exist
        
        Args:
        - name: Dataset name
        - data_type: Dataset data type
        - process_id: Process ID
        - extra_params?: Extra parameters. Valid options are: usl, lsl, & unit

        Returns:
        - A dataset Python object 
        """
        client = APIClient()
        query_params = {"name": name, "type": data_type, "process_id": process_id}
        if extra_params:
            query_params.update(extra_params)
        # TODO: debug logging
        print(f"Creating dataset with type {data_type}: {name}")
        return Dataset(client.make_api_request("/datasets", "PUT", data=query_params))

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
        print(dataset_data)
        self.name = dataset_data["name"]
        self.dataset_id = dataset_data["id"]

