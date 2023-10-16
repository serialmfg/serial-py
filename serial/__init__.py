"""serialmfg Module
Exports 3 data classes (they are not initialized, and simply provide 
users with ways to access underlying data structures)
ComponentInstances
ProcessEntries
Datasets

Exports 3 deprecated classes
Serial (for managing connections)
Identifier (for creating component instances)
Process (for creating process entries)
"""
from .identifier import Identifier
from .serial import Serial 
from .process import Process
from .serial_resources.component_instance import ComponentInstances
from .serial_resources.process_entry import ProcessEntries
from .serial_resources.dataset import Datasets

api_key = None
base_url = "https://api.serial.io"
station_id = None
debug = False
