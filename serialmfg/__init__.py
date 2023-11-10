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
from . import config

def set_api_key(key):
    config.api_key = key

def set_base_url(url):
    config.base_url = url

# Export the functions so that they can be used as serial.set_api_key, etc.
__all__ = ['set_api_key', 'set_base_url', ...]
