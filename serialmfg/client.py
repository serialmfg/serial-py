DEFAULT_BASE_URL = "https://api.serial.io"

class Client:
    def __init__(self, debug=False):
        """
        Initializes a new Serial Client

        Args: 
        - debug: Boolean to turn on debug logging

        Returns:
        - A new Serial client

        Once initialized, it should be passed an api_key to handle requests,
        as well optionally receiving a station id and new base url (which defaults
        to the default serial api url of https://api.serial.io)
        """
        self.api_key = None
        self.station_id = None
        self.base_url = DEFAULT_BASE_URL
        self.allow_component_instance_creation = False
        self.debug = debug

client = Client()

