"""
This module contains the ProcessEntry class and ProcessEntries class.
"""
import os
import mimetypes
from concurrent.futures import ThreadPoolExecutor, as_completed
from ..api_client import APIClient 
from ..exceptions import SerialAPIException
from .. import config
from .dataset import Datasets 
from .component_instance import ComponentInstances
from ..utils.time_formatting import is_iso_timestamp

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
        self.text_data_queue = []
        self.numerical_data_queue = []
        self.file_data_queue = []
        self.boolean_data_queue = []
        self.link_data_queue = []

    def _process_queue(self):
        """
        Process all queued data submissions.
        """
        with ThreadPoolExecutor() as executor:
            # Submit each queue processing function to the executor
            futures = [
                executor.submit(self._process_text_data_queue),
                executor.submit(self._process_numerical_data_queue),
                executor.submit(self._process_file_data_queue),
                executor.submit(self._process_boolean_data_queue),
                executor.submit(self._process_link_data_queue)
            ]

            for future in as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    # Handle exceptions
                    print(f"An error occurred: {e}")
                    raise SerialAPIException(f"An error occurred: {e}")

    def add_text(self, dataset_name, value, expected_value=None):
        """
        Store text data to be added to a process entry

        Args: 
        - dataset_name: User facing name of the dataset
        - value: The value to be submitted
        - expected_value: Optional argument to pass an expected value. If the 
          values are the same, it would be considered a passing test result

        Stores:
        - Information necessary to add text data
        """
        # Store the necessary information in an internal queue or list
        self.text_data_queue.append({
            'dataset_name': dataset_name,
            'value': value,
            'expected_value': expected_value
        })

    def _process_text_data_queue(self):
        with ThreadPoolExecutor() as executor:
            futures = []
            for text_data in self.text_data_queue:
                # Submit each request to the executor
                futures.append(executor.submit(self._process_single_text_data, text_data))

            # Clear the queue once all futures are submitted
            self.text_data_queue.clear()

            for future in as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    # Handle exceptions
                    print(f"An error occurred: {e}")
                    raise SerialAPIException(f"An error occurred: {e}")

    def _process_single_text_data(self, text_data):
        # The code that processes a single text data entry
        dataset_name = text_data['dataset_name']
        value = text_data['value']
        expected_value = text_data.get('expected_value')

        dataset = Datasets.get_or_create_dataset(dataset_name, "TEXT", self.process_id)

        data = {
            "type": "TEXT",
            "dataset_id": dataset.dataset_id,
            "value": value,
            **({'expected_value': expected_value} if expected_value is not None else {})
        }

        # Make the API request
        response = self.client.make_api_request(
            f"/processes/entries/{self.id}", "PUT", data=data
        )
        return response

    def add_number(self, dataset_name, value, usl=None, lsl=None, unit=None):
        """
        Queue numerical data to be added to a process entry.

        Args: 
        - dataset_name: User facing name of the dataset
        - value: The value to be submitted
        - usl: Optional argument to override the dataset's upper spec limit
        - lsl: Optional argument to override the dataset's lower spec limit
        - unit: Optional argument to create the dataset's unit
        """
        # Append a task to the queue with all necessary information
        self.numerical_data_queue.append({
            'dataset_name': dataset_name,
            'value': value,
            'usl': usl,
            'lsl': lsl,
            'unit': unit
        })

    def _process_numerical_data_queue(self):
        """
        Process the queued numerical data submissions.
        """
        with ThreadPoolExecutor() as executor:
            futures = []
            for number_data in self.numerical_data_queue:
                # Submit each request to the executor
                futures.append(executor.submit(self._process_single_numerical_data, number_data))

            # Clear the queue once all futures are submitted
            self.numerical_data_queue.clear()

            for future in as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    # Handle exceptions
                    print(f"An error occurred: {e}")
                    raise SerialAPIException(f"An error occurred: {e}")

    def _process_single_numerical_data(self, number_data):
        # The code that processes a single numerical data entry
        dataset_name = number_data['dataset_name']
        value = number_data['value']
        usl = number_data.get('usl')
        lsl = number_data.get('lsl')
        unit = number_data.get('unit')
        extra_params = {'unit': unit, 'usl': usl, 'lsl': lsl}
            
        dataset = Datasets.get_or_create_dataset(dataset_name, "NUMERICAL", self.process_id, extra_params)
        
        data = {
            "type": "NUMERICAL",
            "dataset_id": dataset.dataset_id,
            "value": value
        }
        if usl is not None:
            data["usl"] = usl
        if lsl is not None:
            data["lsl"] = lsl

        # Make the API request
        response = self.client.make_api_request(f"/processes/entries/{self.id}", "PUT", data=data)
        return response

    def add_image(self, dataset_name, path, file_name=None):
        """
        DEPRECATED: Use add_file instead

        Args: 
        - dataset_name: User facing name of the dataset
        - path: Path to the file on your file system
        - file_name: Optional argument to override the file name
        """
        return self.add_file(dataset_name, path, file_name)

    def add_file(self, dataset_name, path, file_name=None):
        """
        Queue file data to be added to a process entry.

        Args: 
        - dataset_name: User facing name of the dataset
        - path: Path to the file on your file system
        - file_name: Optional argument to override the file name
        """
        # Queue the task with all necessary information
        self.file_data_queue.append({
            'dataset_name': dataset_name,
            'path': path,
            'file_name': file_name
        })

    def _process_file_data_queue(self):
        """
        Process the queued file data submissions.
        """
        with ThreadPoolExecutor() as executor:
            futures = []
            for file_data in self.file_data_queue:
                # Submit each file upload request to the executor
                futures.append(executor.submit(self._process_single_file_data, file_data))

            # Clear the queue once all futures are submitted
            self.file_data_queue.clear()

            for future in as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    # Handle exceptions
                    print(f"An error occurred: {e}")
                    raise SerialAPIException(f"An error occurred: {e}")

    def _process_single_file_data(self, file_data):
        # The code that processes a single file data entry
        dataset_name = file_data['dataset_name']
        path = file_data['path']
        file_name = file_data.get('file_name') or os.path.basename(path)

        response = self._upload_file(dataset_name, path, file_name, "FILE")
        return response
    
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
        mimetype = mimetypes.guess_type(path)[0]
        storage_object = self.client.make_api_request("/files", "POST", files=files)
        if mimetype.startswith("image"):
            dataset_type = "IMAGE"
        dataset = Datasets.get_or_create_dataset(dataset_name, dataset_type, self.process_id) 
        data = {"type": dataset_type, "dataset_id": dataset.dataset_id, "file_id": storage_object["name"], "file_name": file_name}
        return self.client.make_api_request(f"/processes/entries/{self.id}", "PUT", data=data)

    def add_boolean(self, dataset_name, value, expected_value):
        """
        Queue boolean data to be added to a process entry.

        Args: 
        - dataset_name: User facing name of the dataset
        - value: The value to be submitted
        - expected_value: Argument to pass an expected value.
        """
        # Append a task with all necessary information to the queue
        self.boolean_data_queue.append({
            'dataset_name': dataset_name,
            'value': value,
            'expected_value': expected_value
        })

    def _process_boolean_data_queue(self):
        """
        Process the queued boolean data submissions.
        """
        with ThreadPoolExecutor() as executor:
            futures = []
            for boolean_data in self.boolean_data_queue:
                # Submit each boolean data processing task to the executor
                futures.append(executor.submit(self._process_single_boolean_data, boolean_data))

            # Clear the queue once all futures are submitted
            self.boolean_data_queue.clear()

            for future in as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    # Handle exceptions
                    print(f"An error occurred: {e}")
                    raise SerialAPIException(f"An error occurred: {e}")

    def _process_single_boolean_data(self, boolean_data):
        # The code that processes a single boolean data entry
        dataset_name = boolean_data['dataset_name']
        value = boolean_data['value']
        expected_value = boolean_data['expected_value']

        dataset = Datasets.get_or_create_dataset(dataset_name, "BOOLEAN", self.process_id)
        
        data = {
            "type": "BOOLEAN",
            "dataset_id": dataset.dataset_id,
            "value": value,
            "expected_value": expected_value
        }

        # Make the API request
        response = self.client.make_api_request(
            f"/processes/entries/{self.id}", "PUT", data=data
        )
        return response


    def add_link(self, dataset_name, child_identifier, break_prior_links=False):
        """
        Queue a link creation between a parent and a child at this specific process entry.

        Args: 
        - dataset_name: User facing name for the link
        - child_identifier: Identifier for the child component instance to be linked
        - break_prior_links: Boolean for whether to break prior links
        """
        # Queue the task with all necessary information
        self.link_data_queue.append({
            'dataset_name': dataset_name,
            'child_identifier': child_identifier,
            'break_prior_links': break_prior_links
        })

    def _process_link_data_queue(self):
        """
        Process the queued link creation tasks.
        """
        with ThreadPoolExecutor() as executor:
            futures = []
            for link_data in self.link_data_queue:
                # Submit each link data processing task to the executor
                futures.append(executor.submit(self._process_single_link_data, link_data))

            # Clear the queue once all futures are submitted
            self.link_data_queue.clear()

            # Optional: Wait for all tasks to complete and handle results/errors
            for future in as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    # Handle exceptions
                    print(f"An error occurred: {e}")

    def _process_single_link_data(self, link_data):
        # The code that processes a single link data entry
        dataset_name = link_data['dataset_name']
        child_identifier = link_data['child_identifier']
        break_prior_links = link_data['break_prior_links']

        child_component_instance_id = ComponentInstances.get(child_identifier).data["id"]
        link_dataset = Datasets.get(dataset_name, "LINK", self.process_id)

        process_entry_id = self.id
        data = {
            "parent_component_instance_id": self.component_instance_id, 
            "child_component_instance_id": child_component_instance_id,
            "dataset_id": link_dataset.dataset_id,
            "process_entry_id": process_entry_id,
            "break_prior_links": break_prior_links,
        }

        # Make the API request
        new_link_response = self.client.make_api_request(
            "/components/instances/links", "PUT", data=data
        )
        return new_link_response

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
        try:
            self._process_queue()
        except SerialAPIException as e:
            raise SerialAPIException(f"Could not add data to process entry: {e}")

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
        entry = client.make_api_request("/processes/entries", "GET", params={"id":id})
        if len(entry) == 0:
            raise SerialAPIException(f"Could not find process entry with id: {id}")
        entry = entry[0]
        return ProcessEntry(entry)

    @staticmethod
    def create(process_id, component_instance=None, component_instance_id=None, component_instance_identifier=None, station_id=None, timestamp=None):
        """
        Creates a process entry

        Args:
        - process_id: Process id 
        - component_instance?: Component instance object 
        - component_instance_id?: Component instance id (is overriden by component_instance)
        - component_instance_identifier?: Component instance identifier (is overriden by component_instance & component_instance_id)
        - station_id?: Optional station id to override the default station id
        - timestamp?: Optional timestamp to override the default timestamp. Must be in ISO 8601 format

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
        elif config.station_id:
            data["station_id"] = config.station_id
        if timestamp:
            if not is_iso_timestamp(timestamp):
                raise Exception("Timestamp must be in ISO 8601 format")
            data["timestamp"] = timestamp
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

