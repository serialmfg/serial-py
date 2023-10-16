"""
This module contains the ProcessEntry class and ProcessEntries class.
"""
import serialmfg as serial
import os
import mimetypes
from datetime import datetime
from ..api_client import APIClient 
from .dataset import Datasets 

class ProcessEntry:
    """
    A process entry Python object
    """
    def __init__(self, process_entry_data): 
        """
        Creates a new Process Entry
        
        Args:
        - process_entry_data: A process entry object, as defined at
        https://docs.serial.io/api-reference/process-entries/get-process-entry

        Returns:
        - A newly created process entry Python object, which holds the api object at data, the process id at process_id and the id at id
        """
        if serial.debug:
            print(f"Creating process entry object with data: {process_entry_data}")
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
        - expected_value?: Optional argument to pass an expected value. If the 
        values are the same, it would be considered a passing test result

        Returns:
        - API response for adding text data
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
        - usl?: Optional argument to override the dataset's upper spec limit
        - lsl?: Optional argument to override the dataset's lower spec limit
        
        Returns:
        - API response for adding numerical data
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
        - file_name?: Optional argument to override the file name

        Returns:
        - API response for adding file data
        """
        if serial.debug:
            print(f"Adding file data: {dataset_name} with path: {path} and file name: {file_name}")
        return self._upload_file(dataset_name, path, file_name, "FILE")

    def add_image(self, dataset_name, path, file_name=None):
        """
        Add image data to a process entry

        Args: 
        - dataset_name: User facing name of the dataset
        - path: Path to the file on your file system
        - file_name?: Optional argument to override the file name

        Returns:
        - API response for adding image data
        """
        if serial.debug:
            print(f"Adding image data: {dataset_name} with path: {path} and file name: {file_name}")
        return self._upload_file(dataset_name, path, file_name, "IMAGE")
    
    def _upload_file(self, dataset_name, path, file_name, dataset_type):
        """
        Uploads a file to the serial server

        Args:
        - dataset_name: User facing name of the dataset
        - path: Path to the file on your file system
        - file_name: None-able argument to override the file name
        - dataset_type: Type of dataset to be uploaded (IMAGE or FILE)
        """
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

        Returns:
        - API response for adding boolean data
        """
        dataset = serial.Datasets.get(dataset_name, "CHECKBOX", self.process_id)
        data = {"type": "BOOLEAN", "dataset_id": dataset.dataset_id, "value": value, "expected_value": expected_value}
        return self.client.make_api_request(f"/processes/entries/{self.id}", "PUT", data=data)
    
    def submit(self, cycle_time=None, is_pass=None, is_complete=None):
        """
        Mark a process entry as completed

        Args: 
        - cycle_time?: Optional number for seconds elapsed since the last cycle 
        finished for this process.
        - is_pass?: Optional boolean for indicating whether the process passed for
        this entry
        - is_complete?: Optional boolean for indicating whether the process is complete
        this entry

        Returns:
        - API response for submitting a process entry
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
    """
    A class for process entry data methods
    """
    @staticmethod
    def get(id):
        """
        Gets a process entry, if it exists
        
        Args:
        - id: Process entry id

        Returns:
        - A process entry Python object
        """
        client = APIClient(serial.api_key, serial.base_url)
        entry = client.make_api_request("/processes/entries", "GET", params={"id":id})[0]
        return ProcessEntry(entry)

    @staticmethod
    def create(process_id, component_instance=None, component_instance_id=None):
        """
        Creates a process entry

        Args:
        - process_id: Process id 
        - component_instance?: Component instance object 
        - component_instance_id?: Component instance id (is overriden by component_instance)

        Returns:
        - A process entry Python object
        """
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
        Lists process entries

        Args:
        - query_params: Query parameters for filtering process entries as defined at
        https://docs.serial.io/api-reference/process-entries/get-process-entries

        Returns:
        - A list of process entry Python objects, as defined above 
        """
        client = APIClient(serial.api_key, serial.base_url)
        entries = client.make_api_request("/processes/entries", "GET", params=query_params)
        entry_object_list = [ProcessEntry(entry) for entry in entries]
        return entry_object_list

