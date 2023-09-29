import sys
sys.path.append('../serialmfg')
import time
from client import client 
from component_instance import ComponentInstance
from process_entry import ProcessEntry

API_KEY = "zpka_4326ceec11234dbc9a6f13db72d9cb9f_50d587d2" # put your own API key here
BASE_URL = "https://serial-main-6819932.d2.zuplo.dev" # Put your own url here 
EXISTING_IDENTIFIER = "test-1691540942131"

client.api_key = API_KEY
client.base_url = BASE_URL
client.debug = True
client.allow_component_instance_creation = True


existing_component_instance = ComponentInstance(client, EXISTING_IDENTIFIER) 
new_component_instance = ComponentInstance(client, f"test-{int(time.time())}", component_name="Test Process Upload Component")


def test_get_instance():
    assert existing_component_instance.component_instance == {}

def test_create_instance():
    assert new_component_instance.component_instance == {}

class DummyProcessEntry: 
    def __init__(self):
        self.id = "d0606301-b5eb-4b0e-b111-3e08fa1ef5ce"

def test_create_link():
    process_entry = DummyProcessEntry()
    assert new_component_instance.add_link("Test PyLibLinking dataset", EXISTING_IDENTIFIER, process_entry=process_entry) == {} 
