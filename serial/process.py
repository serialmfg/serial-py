"""
DEPRECATED, WILL BE REMOVED IN FUTURE RELEASE
"""
import json
import os
import mimetypes
from warnings import warn

class Process:
    """
    A class representing the process data to be uploaded to the API.
    """
    def __init__(self, identifier, process_id):
        """
        DEPRECATED, WILL BE REMOVED IN A FUTURE RELEASE
        Constructor for the ProcessData class.
        
        Args:
            identifier (str): The identifier for the process data.
        """
        self.process_id = process_id
        self.links = []
        self.parameters = []
        self.images = []
        self.files = []
        self.is_pass = None
        self.identifier = identifier
        warn('''
        The "Process" object is being deprecated and will be removed in future releases.
        Please begin migrating to the new interface provided from `from serialmfg import client`.
        ''')

    def add_link(self, identifier):
        """
        Adds a linked component to the process data.
        
        Args:
            identifier (str): The identifier for the linked component.
        """
        self.links.append({
            "identifier": identifier,
        })

    def add_parameter(self, key_name, value, usl=None, lsl=None, unit=None):
        """
        Adds a parameter to the process data.
        
        Args:
            key_name (str): The key name of the parameter.
            usl (float): The upper specification limit of the parameter.
            lsl (float): The lower specification limit of the parameter.
            value (float): The value of the parameter.
            unit (str): The unit of measurement for the parameter.
        """

        # set data_type to INTEGER, NUMBER, STRING based on the type of value:
        data_type_py = type(value)

        if data_type_py in [int, float]:
            data_type = "NUMBER" if data_type_py == float else "INTEGER"
        elif data_type_py == str:
            data_type = "STRING"
            if usl is not None or lsl is not None:
                raise ValueError("usl and lsl can only be used if value is an integer or float")
        else:
            raise ValueError("data_type must be 'INTEGER', 'NUMBER', or 'STRING'")

        self.parameters.append({
            "key_name": key_name,
            "data_type": data_type,
            "usl": usl, 
            "lsl": lsl,
            "value": value,
            "unit": unit
        })

    def add_image(self, key_name, path):
        """
        Adds an image to the process data.
        
        Args:
            key_name (str): The key name of the image.
            path (str): The path to the image file.
        """
        with open(path, 'rb') as file:
            image_bytes = file.read()
            file_name = os.path.basename(file.name)
            mime_type, _ = mimetypes.guess_type(file_name)
            self.images.append({
                "key_name": key_name,
                "file_name": file_name,
                "bytes": image_bytes,
                "mime_type": mime_type
            })

    def add_file(self, key_name, path):
        """
        Adds a file to the process data.
        
        Args:
            key_name (str): The key name of the file.
            path (str): The path to the image file.
        """
        with open(path, 'rb') as file:
            file_bytes = file.read()
            file_name = os.path.basename(file.name)
            mime_type, _ = mimetypes.guess_type(file_name)
            self.files.append({
                "key_name": key_name,
                "file_name": file_name,
                "bytes": file_bytes,
                "mime_type": mime_type
            })

    def set_pass_fail(self, is_pass):
        """
        Sets the pass status of the process data.
        
        Args:
            is_pass (bool): The pass status of the process data.
        """
        self.is_pass = is_pass

    def build_payload(self, station_id):
        """
        Builds the multipart form data payload for the endpoint
        """
        serial_payload = {
            "identifier": self.identifier,
            "process_id": self.process_id,
            "station_id": station_id,
            "links": self.links,
            "parameters": self.parameters,
            "images": [],
            "files": [], 
            "is_pass": self.is_pass
        }

        for image in self.images:
            serial_payload["images"].append({
                "key_name": image["key_name"],
                "file_name": image["file_name"]
            })

        for file in self.files:
            serial_payload["files"].append({
                "key_name": file["key_name"],
                "file_name": file["file_name"]
            })

        payload = {
            "serial_payload": ("serial_payload.json", json.dumps(serial_payload), "application/json")
        }
        
        for image in self.images:
            mime_type = image["mime_type"]
            if mime_type is None:
                raise ValueError(f"Could not determine MIME type for image: {image['file_name']}")
            payload[image["file_name"]] = (image["file_name"], image["bytes"], mime_type)

        for file in self.files:
            mime_type = file["mime_type"]
            if mime_type is None:
                raise ValueError(f"Could not determine MIME type for file: {file['file_name']}")
            payload[file["file_name"]] = (file["file_name"], file["bytes"], mime_type)

        return payload
