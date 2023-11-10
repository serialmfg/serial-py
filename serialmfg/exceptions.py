class SerialAPIException(Exception):
    """Exception raised for errors in the Serial API call.

    Attributes:
        message -- explanation of the error
        status_code -- HTTP status code from the response
    """

    def __init__(self, message, status_code=None):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)
    
    def __str__(self):
        if self.status_code:
            return f"APIException {self.status_code}: {self.message}"
        else:
            return f"APIException: {self.message}"
