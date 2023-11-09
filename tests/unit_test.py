import sys
from dotenv import find_dotenv, load_dotenv
import os
sys.path.append('../serial')
import time
import serialmfg as serial
from .constants import NEW_IDENTIFIER_SAMPLE_DATA, SAMPLE_NEW_LINK, EXISTING_IDENTIFIER_DATA, SAMPLE_TEXT_DATA, SAMPLE_NUMBER_DATA, SAMPLE_IMAGE_DATA, SAMPLE_BOOLEAN_DATA, SAMPLE_ENTRY_DATA, SAMPLE_DATASET_DATA, SAMPLE_FILE_DATA

load_dotenv(find_dotenv()) # relative path to .env file
API_KEY = os.getenv('ZUPLO_API_KEY') # put your own API key here
BASE_URL = os.getenv('BASE_URL') # Put your own url here 
EXISTING_IDENTIFIER = "test-1691540942131"
UNEDITED_IDENTIFIER = "test-1696629404"

serial.set_api_key(API_KEY)
serial.set_base_url(BASE_URL)

existing_component_instance = serial.ComponentInstances.get(EXISTING_IDENTIFIER) 
new_component_instance = serial.ComponentInstances.create(f"test-{int(time.time())}", component_name="Test Process Upload Component")

new_process_entry = serial.ProcessEntries.create(process_id="51718ea4-a274-4455-bde3-e4216e1ecd96", component_instance=existing_component_instance) 

existing_process_entry = serial.ProcessEntries.get('114b846e-5d5e-4f96-87d2-6c029192053a')

def test_get_instance():
    for key, value in existing_component_instance.data.items():
        assert key in EXISTING_IDENTIFIER_DATA.keys()
        if key not in ["id", "status", "identifier", "created_at", "last_updated_at", "completed_at"]:
            assert value == EXISTING_IDENTIFIER_DATA[key]

def test_create_instance():
    for key, value in new_component_instance.data.items():
        assert key in NEW_IDENTIFIER_SAMPLE_DATA.keys()
        if key not in ["id", "identifier", "created_at", "last_updated_at"]:
            assert value == NEW_IDENTIFIER_SAMPLE_DATA[key]
        
def test_list_instances():
    component_instance_list = serial.ComponentInstances.list({"status": "DEFECTIVE"})
    for instance in component_instance_list:
        assert instance.data["status"] == "DEFECTIVE"

class DummyProcessEntry: 
    def __init__(self):
        self.id = "1963ff32-cfb8-48a9-9a6d-41c7bfdcb67c"

def test_create_link():
    process_entry = DummyProcessEntry()
    new_link = new_component_instance.add_link("Test PyLibLinking dataset", UNEDITED_IDENTIFIER, process_entry=process_entry) 
    print(new_link)
    for key, value in new_link.data["new_link"].items():
        assert key in SAMPLE_NEW_LINK["new_link"].keys()
        if key not in ["id", "created_at", "removed_at", "unique_identifier_id"]:
            assert value == SAMPLE_NEW_LINK["new_link"][key]

def test_list_process_entries():
    process_entry_list = serial.ProcessEntries.list({"component_instance_id": "0372a807-b15f-47f9-acf9-d9a3301673ec"}) 
    for entry in process_entry_list:
        assert entry.data["unique_identifier_id"] == "0372a807-b15f-47f9-acf9-d9a3301673ec"

def test_get_process_entries():
    existing_process_entry = serial.ProcessEntries.get("e6ff9f24-8435-4ed7-9b4a-0f4b860ac1fc") 
    assert existing_process_entry.id == "e6ff9f24-8435-4ed7-9b4a-0f4b860ac1fc"

def test_create_process_entries():
    assert new_process_entry.process_id == "51718ea4-a274-4455-bde3-e4216e1ecd96"
    assert new_process_entry.data["unique_identifier_id"] == "95db48e1-99ad-4e35-a86b-fa0beca5f313"

def test_add_text():
    text_data = existing_process_entry.add_text("New Dataset", "Bob's Burgers") 
    for key, value in text_data.items():
        assert key in SAMPLE_TEXT_DATA.keys()
        if key not in ["id", "created_at", "dataset_id"]: 
            assert value == SAMPLE_TEXT_DATA[key]

def test_add_number():
    number_data = existing_process_entry.add_number("New Dataset", 1.5, usl=2, lsl=1) 
    for key, value in number_data.items():
        assert key in SAMPLE_NUMBER_DATA.keys()
        if key not in ["id", "created_at", "dataset_id"]: 
            assert value == SAMPLE_NUMBER_DATA[key]

def test_add_file():
    file_data = existing_process_entry.add_file("New Dataset", "/Users/clarke/repos/serial-py/tests/test.txt")
    for key, value in file_data.items():
        assert key in SAMPLE_FILE_DATA.keys()
        if key not in ["id", "created_at", "file_id", "dataset_id"]: 
            assert value == SAMPLE_FILE_DATA[key]

def test_add_image():
    new_process_entry = serial.ProcessEntries.create(process_id="800ed422-7c4f-4010-be8f-43954d112801", component_instance=existing_component_instance)
    image_data = new_process_entry.add_image("testImage", "/Users/clarke/repos/serial-py/tests/image.png")
    for key, value in image_data.items():
        assert key in SAMPLE_IMAGE_DATA.keys()
        if key not in ["id", "created_at", "file_id", "process_entry_id"]: 
            assert value == SAMPLE_IMAGE_DATA[key]
        if key == "process_entry_id":
            assert value == new_process_entry.id

def test_add_boolean():
    new_process_entry = serial.ProcessEntries.create(process_id="9ecb9747-22d9-49eb-b5c1-1d9fff3fa6b8", component_instance=existing_component_instance)
    boolean_data = new_process_entry.add_boolean("Pass Fail Criteria", True, False)
    for key, value in boolean_data.items():
        assert key in SAMPLE_BOOLEAN_DATA.keys()
        if key not in ["id", "created_at", "process_entry_id", "dataset_id"]:
            assert value == SAMPLE_BOOLEAN_DATA[key]
        if key == "process_entry_id":
            assert value == new_process_entry.id

def test_complete_entry():
    new_process_entry = serial.ProcessEntries.create(process_id="9ecb9747-22d9-49eb-b5c1-1d9fff3fa6b8", component_instance=existing_component_instance)
    entry_data = new_process_entry.submit(cycle_time=50, is_pass=True)
    for key, value in entry_data.items():
        assert key in SAMPLE_ENTRY_DATA.keys()
        if key not in ["id", "timestamp", "created_at"]:
            assert value == SAMPLE_ENTRY_DATA[key]

def test_get_datasets():
    dataset = serial.Datasets.get("LSL Only", "NUMERICAL", process_id="9ecb9747-22d9-49eb-b5c1-1d9fff3fa6b8")
    for key, value in dataset.data.items():
        assert key in SAMPLE_DATASET_DATA.keys()

def test_create_datasets():
    dataset = serial.Datasets.create("New Dataset", "NUMERICAL", "9ecb9747-22d9-49eb-b5c1-1d9fff3fa6b8", {"lsl": -10.5})
    for key, value in dataset.data.items():
        assert key in SAMPLE_DATASET_DATA.keys()

def test_auto_create_numerical_data():
    new_process_entry = serial.ProcessEntries.create(process_id="9ecb9747-22d9-49eb-b5c1-1d9fff3fa6b8", component_instance=existing_component_instance)
    numerical_data = new_process_entry.add_number("New Dataset", 1.5, usl=2, lsl=1, unit="m")
    for key, value in numerical_data.items():
        assert key in SAMPLE_NUMBER_DATA.keys()
        if key not in ["id", "created_at", "dataset_id", "process_entry_id", "unit"]: 
            assert value == SAMPLE_NUMBER_DATA[key]
