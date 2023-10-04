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
