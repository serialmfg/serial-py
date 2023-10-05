import serial
import os
import mimetypes
from datetime import datetime
from ..api_client import APIClient 
from .dataset import Datasets 

class ProcessEntry:
    def __init__(self, process_entry_data): 
        """
        Creates a new Process Entry
        
        Args:
        - client: A Serial client object
        - component_instance: Component Instance object 
        - process_id: UUID for the process associated with this entry

        Returns:
        - A newly created process entry
        """
        self.client = APIClient(serial.api_key, serial.base_url) 
        self.data = process_entry_data
        self.process_id = process_entry_data["process_id"] 
        self.id = process_entry_data["id"] 

    def add_text(self, dataset_name, value, expected_value=None):
        """
        Add text data to a process entry

        Args: 
        - dataset_name: User facing name of the dataset
        - value: The value to be submitted
        - expected_value: Optional argument to pass an expected value. If the 
        values are the same, it would be considered a passing test result
        """
        if serial.debug:
            print(f"Adding text data: {dataset_name} with value: {value} and expected value: {expected_value}")
        dataset = serial.Datasets.get(dataset_name, "PARAMETRIC_QUALITATIVE", self.process_id)
        data = {"type": "TEXT", "dataset_id": dataset.dataset_id, "value": value}
        return self.client.make_api_request(f"/processes/entries/{self.id}", "PUT", data=data)

    def add_number(self, dataset_name, value, usl=None, lsl=None):
        """
        Add numerical data to a process entry

        Args: 
        - dataset_name: User facing name of the dataset
        - value: The value to be submitted
        - usl: Optional argument to override the dataset's upper spec limit
        - lsl: Optional argument to override the dataset's lower spec limit
        """
        if serial.debug:
            print(f"Adding numerical data: {dataset_name} with value: {value} and usl: {usl} & lsl: {lsl}")
        dataset = serial.Datasets.get(dataset_name, "PARAMETRIC_QUANTITATIVE", self.process_id)
        data = {"type": "NUMERICAL", "dataset_id": dataset.dataset_id, "value": value}
        if usl:
            data["usl"] = usl
        if lsl:
            data["lsl"] = lsl
        return self.client.make_api_request(f"/processes/entries/{self.id}", "PUT", data=data)

    def add_file(self, dataset_name, path, file_name=None):
        """
        Add file data to a process entry

        Args: 
        - dataset_name: User facing name of the dataset
        - path: Path to the file on your file system
        """
        if serial.debug:
            pass
        self._upload_file(dataset_name, path, file_name, "FILE")

    def add_image(self, dataset_name, path, file_name=None):
        """
        Add image data to a process entry

        Args: 
        - dataset_name: User facing name of the dataset
        - path: Path to the file on your file system
        """
        if serial.debug:
            pass
        self._upload_file(dataset_name, path, file_name, "IMAGE")
    
    def _upload_file(self, dataset_name, path, file_name, dataset_type):
        if not file_name:
            file_name = os.path.basename(path)
        # if in the future we need to do a better guess, we can use python-magic to determine the mimetype
        files = {'file': (file_name, open(path, 'rb'), mimetypes.guess_type(path))} 
        storage_object = self.client.make_api_request("/files", "POST", files=files)
        dataset = serial.Datasets.get(dataset_name, dataset_type, self.process_id)
        data = {"type": dataset_type, "dataset_id": dataset.dataset_id, "file_id": storage_object["name"], "file_name": file_name}
        return self.client.make_api_request(f"/processes/entries/{self.id}", "PUT", data=data)

    def add_boolean(self, dataset_name, value, expected_value):
        """
        Add boolean data to a process entry

        Args: 
        - dataset_name: User facing name of the dataset
        - value: The value to be submitted
        - expected_value: argument to pass an expected value. If the 
        values are the same, it would be considered a passing test result
        """
        dataset = serial.Datasets.get(dataset_name, "CHECKBOX", self.process_id)
        data = {"type": "BOOLEAN", "dataset_id": dataset.dataset_id, "value": value, "expected_value": expected_value}
        return self.client.make_api_request(f"/processes/entries/{self.id}", "PUT", data=data)
    
    def submit(self, cycle_time=None, is_pass=None, is_complete=None):
        """
        Mark a process entry as completed

        Args: 
        - cycle_time: Optional number for seconds elapsed since the last cycle
        finished for this process.
        - is_pass: Optional boolean for indicating whether the process passed for
        this entry
        """
        data = {}
        if cycle_time:
            data["cycle_time"] = cycle_time
        if is_pass: 
            data["is_pass"] = is_pass
        if is_complete:
            data["is_complete"] = is_complete

        return self.client.make_api_request(f"/processes/entries/{self.id}", "PATCH", data=data)

class ProcessEntries:
    def __init__(self):
        pass

    @staticmethod
    def get(id):
        client = APIClient(serial.api_key, serial.base_url)
        entry = client.make_api_request("/processes/entries", "GET", params={"id":id})[0]
        return ProcessEntry(entry)

    @staticmethod
    def create(process_id, component_instance=None, component_instance_id=None):
        client = APIClient(serial.api_key, serial.base_url)
        if component_instance:
            component_instance_id = component_instance.data["id"]
        if not component_instance_id:
            raise Exception("ComponentInstance id cannot be null, please pass in a valid one")
        data = {"component_instance_id": component_instance_id, "process_id": process_id}
        entry = client.make_api_request("/processes/entries", "POST", data=data)
        return ProcessEntry(entry)

    @staticmethod
    def list(query_params):
        """
        Can be any parameters as outlined in serial's documentation
        """
        client = APIClient(serial.api_key, serial.base_url)
        entries = client.make_api_request("/processes/entries", "GET", params=query_params)
        entry_object_list = [ProcessEntry(entry) for entry in entries]
        return entries


