"""
This module contains the operator class and its methods.
"""
from ..api_client import APIClient
from ..exceptions import SerialAPIException

class Operator:
    """
    This class contains the methods for the operator API.
    """

    def __init__(self, operator_data):
        """ 
        Args:
            operator_data (dict): The operator data.
        """
        self.data = operator_data
        self.api_client = APIClient()

class Operators:
    """
    This class contains the data methods for operators 
    """

    @staticmethod
    def get(first_name=None, last_name=None, pin=None):
        """
        Get operators.

        Args:
            first_name (str): The first name of the operator.
            last_name (str): The last name of the operator.
            pin (str): The pin of the operator.
        Returns:
            A single operator object
        """
        client = APIClient()
        params = {}
        if first_name:
            params['first_name'] = first_name
        if last_name:
            params['last_name'] = last_name
        if pin:
            params['pin'] = pin
        operator_data = client.make_api_request('/operators', "GET", params=params)
        if len(operator_data) == 0:
            raise SerialAPIException("No operator found")
        if len(operator_data) > 1:
            raise SerialAPIException("Multiple operators found")
        return Operator(operator_data[0])


