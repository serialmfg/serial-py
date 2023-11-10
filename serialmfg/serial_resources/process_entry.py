"""
This module contains the ProcessEntry class and ProcessEntries class.
"""
import os
import mimetypes
from datetime import datetime
from ..api_client import APIClient 
from .dataset import Datasets 
from .component_instance import ComponentInstance
from .component_instance_link import ComponentInstanceLink

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
        # TODO: debug logging
        #print(f"Creating process entry object with data: {process_entry_data}")
        self.client = APIClient() 
        self.data = process_entry_data
        self.process_id = process_entry_data["process_id"] 
        self.id = process_entry_data["id"] 
        self.component_instance_id = process_entry_data["unique_identifier_id"]

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
        # TODO: debug logging
        #print(f"Adding text data: {dataset_name} with value: {value} and expected value: {expected_value}")
        dataset = None
        try:
            dataset = Datasets.get(dataset_name, "TEXT", self.process_id)
        except Exception as e:
            dataset = Datasets.create(dataset_name, "TEXT", self.process_id)
        data = {"type": "TEXT", "dataset_id": dataset.dataset_id, "value": value}
        return self.client.make_api_request(f"/processes/entries/{self.id}", "PUT", data=data)

    def add_number(self, dataset_name, value, usl=None, lsl=None, unit=None):
        """
        Add numerical data to a process entry

        Args: 
        - dataset_name: User facing name of the dataset
        - value: The value to be submitted
        - usl?: Optional argument to override the dataset's upper spec limit
        - lsl?: Optional argument to override the dataset's lower spec limit
        - unit?: Optional argument to create the dataset's unit
        
        Returns:
        - API response for adding numerical data
        """
        # TODO: debug logging
        #print(f"Adding numerical data: {dataset_name} with value: {value} and usl: {usl} & lsl: {lsl}")
        dataset = None
        try:
            dataset = Datasets.get(dataset_name, "NUMERICAL", self.process_id)
        except Exception as e:
            extra_params = {}
            if usl:
                extra_params["usl"] = usl
            if lsl:
                extra_params["lsl"] = lsl
            if unit:
                extra_params["unit"] = unit

            dataset = Datasets.create(dataset_name, "NUMERICAL", self.process_id, extra_params=extra_params)
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
        # TODO: debug logging
        #print(f"Adding file data: {dataset_name} with path: {path} and file name: {file_name}")
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
        # TODO: debug logging
        #print(f"Adding image data: {dataset_name} with path: {path} and file name: {file_name}")
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
        dataset = None
        try:
            dataset = Datasets.get(dataset_name, dataset_type, self.process_id)
        except Exception as e:
            dataset = Datasets.create(dataset_name, dataset_type, self.process_id)
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
        dataset = None
        try:
            dataset = Datasets.get(dataset_name, "BOOLEAN", self.process_id)
        except Exception as e:
            dataset = Datasets.create(dataset_name, "BOOLEAN", self.process_id)
        data = {"type": "BOOLEAN", "dataset_id": dataset.dataset_id, "value": value, "expected_value": expected_value}
        return self.client.make_api_request(f"/processes/entries/{self.id}", "PUT", data=data)
    
    def add_link(self, dataset_name, child_identifier, break_prior_links=False):
        """
        Creates a link between a parent and a child at this specific
        process_entry

        Args:
        - dataset_name: User facing name for the link
        - child_identifier: Identifier for the child component instance to be linked
        - break_prior_links?: Boolean for whether to break prior links

        Returns:
        - New component instance link
        """
        # TODO: debug logging
        #print(f"Adding link: {dataset_name} with child identifier: {child_identifier}")
        child_component_instance_params = {
                "identifier": child_identifier
                }
        link_params = {
                "name": dataset_name
                }
        child_component_instance = self.client.make_api_request("/components/instances",
                                                                "GET",
                                                                params=child_component_instance_params)[0]

        link_dataset = self.client.make_api_request("/datasets",
                                                    "GET",
                                                    params=link_params)[0]
        process_entry_id = self.id
        data = {
                "parent_component_instance_id": self.component_instance_id, 
                "child_component_instance_id": child_component_instance["id"],
                "dataset_id": link_dataset["id"],
                "process_entry_id": process_entry_id,
                "break_prior_links": break_prior_links,
                }
        new_link = ComponentInstanceLink(self.client.make_api_request("/components/instances/links", "PUT", data=data)) 
        return new_link

    def submit(self, cycle_time=None, is_pass=None):
        """
        Mark a process entry as completed

        Args: 
        - cycle_time?: Optional number for seconds elapsed since the last cycle 
        finished for this process.
        - is_pass?: Optional boolean for indicating whether the process passed for
        this entry
        this entry

        Returns:
        - API response for submitting a process entry
        """
        data = {}
        if cycle_time is not None:
            data["cycle_time"] = cycle_time
        if is_pass is not None: 
            data["is_pass"] = is_pass
        data["is_complete"] = True

        self.data = self.client.make_api_request(f"/processes/entries/{self.id}", "PATCH", data=data)
        return self.data

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
        client = APIClient()
        entry = client.make_api_request("/processes/entries", "GET", params={"id":id})[0]
        return ProcessEntry(entry)

    @staticmethod
    def create(process_id, component_instance=None, component_instance_id=None, component_instance_identifier=None, station_id=None):
        """
        Creates a process entry

        Args:
        - process_id: Process id 
        - component_instance?: Component instance object 
        - component_instance_id?: Component instance id (is overriden by component_instance)
        - component_instance_identifier?: Component instance identifier (is overriden by component_instance & component_instance_id)

        Returns:
        - A process entry Python object
        """
        client = APIClient()
        if component_instance:
            component_instance_id = component_instance.data["id"]
        if not component_instance_id and not component_instance_identifier:
            raise Exception("ComponentInstance id cannot be null, please pass in a valid one")
        if component_instance_identifier:
            component_instance_id = ComponentInstances.get(component_instance_identifier).data["id"]
        data = {"component_instance_id": component_instance_id, "process_id": process_id}
        if station_id:
            data["station_id"] = station_id
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
        client = APIClient()
        entries = client.make_api_request("/processes/entries", "GET", params=query_params)
        entry_object_list = [ProcessEntry(entry) for entry in entries]
        return entry_object_list

