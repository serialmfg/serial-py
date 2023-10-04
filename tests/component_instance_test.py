import sys
sys.path.append('../serial')
import time
import serial

API_KEY = "zpka_*" # put your own API key here
BASE_URL = "https://serial-main-6819932.d2.zuplo.dev" # Put your own url here 
EXISTING_IDENTIFIER = "test-1691540942131"

serial.api_key = API_KEY
serial.base_url = BASE_URL
serial.debug = True

existing_component_instance = serial.ComponentInstances.get(EXISTING_IDENTIFIER) 
new_component_instance = serial.ComponentInstances.create(f"test-{int(time.time())}", component_name="Test Process Upload Component")

new_process_entry = serial.ProcessEntries.create(process_id="51718ea4-a274-4455-bde3-e4216e1ecd96", component_instance=existing_component_instance) 

existing_process_entry = serial.ProcessEntries.get('114b846e-5d5e-4f96-87d2-6c029192053a')

def test_get_instance():
    assert existing_component_instance.data == {}

def test_create_instance():
    assert new_component_instance.data == {}

def test_list_instances():
    assert serial.ComponentInstances.list({"component_id": "96f59fb6-a801-4cc6-9b50-17e21f181482"}) == []

class DummyProcessEntry: 
    def __init__(self):
        self.id = "1963ff32-cfb8-48a9-9a6d-41c7bfdcb67c"

def test_create_link():
    process_entry = DummyProcessEntry()
    assert new_component_instance.add_link("Test PyLibLinking dataset", EXISTING_IDENTIFIER, process_entry=process_entry) == {} 

def test_list_process_entries():
    assert serial.ProcessEntries.list({"component_instance_id": "0372a807-b15f-47f9-acf9-d9a3301673ec"}) == []

def test_get_process_entries():
    assert serial.ProcessEntries.get("e6ff9f24-8435-4ed7-9b4a-0f4b860ac1fc") == {}

def test_create_process_entries():
    assert new_process_entry == {}

def test_add_text():
    assert existing_process_entry.add_text("New Dataset", "Bob's Burgers") == {}

def test_add_number():
    assert existing_process_entry.add_number("New Dataset", 1.5, usl=2, lsl=1) == {}

def test_add_file():
    existing_process_entry.add_file("New Dataset", "/Users/clarke/repos/serial-py/tests/test.txt", "files")

def test_add_image():
    new_process_entry = serial.ProcessEntries.create(process_id="800ed422-7c4f-4010-be8f-43954d112801", component_instance=existing_component_instance)
    new_process_entry.add_file("testImage", "/Users/clarke/repos/serial-py/tests/image.png", "images")

def test_add_boolean():
    new_process_entry = serial.ProcessEntries.create(process_id="9ecb9747-22d9-49eb-b5c1-1d9fff3fa6b8", component_instance=existing_component_instance)
    assert new_process_entry.add_boolean("Pass Fail Criteria", True, False)== {}

def test_complete_entry():
    new_process_entry = serial.ProcessEntries.create(process_id="9ecb9747-22d9-49eb-b5c1-1d9fff3fa6b8", component_instance=existing_component_instance)
    assert new_process_entry.submit(cycle_time=50, is_pass=True, is_complete=True)== {}
