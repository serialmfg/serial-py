from datetime import datetime

class ProcessEntry:
    def __init__(self, client, component_instance, process_id): 
        """
        Creates a new Process Entry
        
        Args:
        - client: A Serial client object
        - component_instance: Component Instance object 
        - process_id: UUID for the process associated with this entry

        Returns:
        - A newly created process entry
        """
        self.client = client
        self.process_id = process_id
        self.component_instance = component_instance 
        self.start_timestamp = datetime.now()
        self.operator_pin = None 
        # Implement setting of process entry id
        self.id = None

    def add_text(self, dataset_name, value, expected_value=None):
        """
        Add text data to a process entry

        Args: 
        - dataset_name: User facing name of the dataset
        - value: The value to be submitted
        - expected_value: Optional argument to pass an expected value. If the 
        values are the same, it would be considered a passing test result
        """
        if self.client.debug:
            print(f"Adding text data: {dataset_name} with value: {value} and expected value: {expected_value}")
        pass
    def add_number(self, dataset_name, value, usl=None, lsl=None):
        """
        Add numerical data to a process entry

        Args: 
        - dataset_name: User facing name of the dataset
        - value: The value to be submitted
        - usl: Optional argument to override the dataset's upper spec limit
        - lsl: Optional argument to override the dataset's lower spec limit
        """
        if self.client.debug:
            print(f"Adding text data: {dataset_name} with value: {value} and expected value: {expected_value}")
        pass

    def add_file(self, dataset_name, path):
        """
        Add file data to a process entry

        Args: 
        - dataset_name: User facing name of the dataset
        - path: Path to the file on your file system
        """
        pass
    
    def add_boolean(self, dataset_name, value, expected_value=None):
        """
        Add boolean data to a process entry

        Args: 
        - dataset_name: User facing name of the dataset
        - value: The value to be submitted
        - expected_value: Optional argument to pass an expected value. If the 
        values are the same, it would be considered a passing test result
        """
        pass
    
    def submit(self, auto_cycle_time=True, cycle_time=None, is_pass=None):
        """
        Mark a process entry as completed

        Args: 
        - auto_cycle_time: Optional boolean to automatically calculate the cycle
        time based on when the process entry was created
        - cycle_time: Optional number for seconds elapsed since the last cycle
        finished for this process.
        - is_pass: Optional boolean for indicating whether the process passed for
        this entry
        """
        pass
