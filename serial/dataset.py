class Dataset:
    def __init__(self, client, name):
        """
        Creates a new dataset object
        """
        self.client = client
        self.dataset = _get_dataset(name)

    def _get_dataset(self, name):
        if self.client.debug:
            print(f"Getting dataset: {identifier}")
        return self.client.make_api_request(f"/datasets?name={name}", "GET")

