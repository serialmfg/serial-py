"""
This file contains the PartNumber class and the PartNumbers class.
"""
from ..api_client import APIClient
from ..exceptions import SerialAPIException
class PartNumberNotFound(SerialAPIException):
    """
    Exception for when a Part Number is not found
    """
    pass

class PartNumbers:
    """
    A class for part number data methods
    """
    @staticmethod
    def get(part_number, component_id=None):
        """
        Get part number data

        Args:
        - part_number (str): Part Number
        - component_id? (str): Component ID - may be needed if part number is not unique

        Returns:
        - A PartNumber object
        """
        client = APIClient()
        query_params = {
            'part_number': part_number
        }
        response = client.make_api_request('/part-numbers', 'GET', query_params)
        if not response:
            raise PartNumberNotFound('Part Number not found')
        if len(response) > 1 and not component_id:
            raise SerialAPIException('Multiple Part Numbers found. Please specify a component ID')
        return PartNumber(response[0])

    @staticmethod
    def create(part_number, component_id, description=None):
        """
        Create a part number

        Args:
        - part_number (str): Part Number
        - component_id (str): Component ID
        - description? (str): Description

        Returns:
        - A PartNumber object
        """
        client = APIClient()
        data = {
            'part_number': part_number,
            'component_id': component_id
        }
        if description:
            data['description'] = description
        response = client.make_api_request('/part-numbers', 'POST', data=data)
        if not response:
            raise SerialAPIException('Part Number not created')
        return PartNumber(response)

    @staticmethod
    def get_or_create_part_number(part_number, component_id, description=None):
        """
        Get or create a part number

        Args:
        - part_number (str): Part Number
        - component_id (str): Component ID
        - description? (str): Description

        Returns:
        - A PartNumber object
        """
        try:
            return PartNumbers.get(part_number, component_id)
        except PartNumberNotFound:
            return PartNumbers.create(part_number, component_id, description)

class PartNumber:
    """
    A class for part number data methods
    """
    def __init__(self, data):
        """
        Initialize a PartNumber object
        Args:
        - data (dict): Part Number data as defined in the API docs
        """
        self.data = data

