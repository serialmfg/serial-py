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
UNEDITED_IDENTIFIER = "BIKE-0002"

serial.set_api_key(API_KEY)
serial.set_base_url(BASE_URL)
serial.set_station_id("2f02d2be-ece6-410f-ad80-ffd746988870")

existing_component_instance = serial.ComponentInstances.get(EXISTING_IDENTIFIER) 
new_component_instance = serial.ComponentInstances.create(f"test-{int(time.time())}", component_name="Test Process Upload Component")

new_process_entry = serial.ProcessEntries.create(process_id="51718ea4-a274-4455-bde3-e4216e1ecd96", component_instance=existing_component_instance) 

existing_process_entry = serial.ProcessEntries.get('114b846e-5d5e-4f96-87d2-6c029192053a')

def test_get_instance():
    for key, value in existing_component_instance.data.items():
        assert key in EXISTING_IDENTIFIER_DATA.keys()
        if key == "component":
          # We need to handle component separately since component_types are changed regularly  
          for key, value in existing_component_instance.data["component"].items():
            assert key in EXISTING_IDENTIFIER_DATA["component"].keys()
            if key not in ["id", "created_at", "last_updated_at", "component_type"]:
              assert value == EXISTING_IDENTIFIER_DATA["component"][key]
        elif key not in ["id", "status", "identifier", "created_at", "last_updated_at", "completed_at"]: 
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
    for key, value in new_link.data["new_link"].items():
        assert key in SAMPLE_NEW_LINK["new_link"].keys()
        if key not in ["id", "created_at", "removed_at", "unique_identifier_id", "removal_reason", "removed_by_user_id"]:
            assert value == SAMPLE_NEW_LINK["new_link"][key]

def test_list_process_entries():
    process_entry_list = serial.ProcessEntries.list({"component_instance_id": "0372a807-b15f-47f9-acf9-d9a3301673ec"}) 
    for entry in process_entry_list:
        assert entry.data["unique_identifier_id"] == "0372a807-b15f-47f9-acf9-d9a3301673ec"

def test_get_process_entries():
    existing_process_entry = serial.ProcessEntries.get("e6ff9f24-8435-4ed7-9b4a-0f4b860ac1fc") 
    assert existing_process_entry.id == "e6ff9f24-8435-4ed7-9b4a-0f4b860ac1fc"

def test_create_process_entries():
    new_process_entry_2 = serial.ProcessEntries.create(process_id="51718ea4-a274-4455-bde3-e4216e1ecd96", component_instance=existing_component_instance, timestamp="2023-03-21T10:45:00") 

    assert new_process_entry_2.process_id == "51718ea4-a274-4455-bde3-e4216e1ecd96"
    assert new_process_entry_2.data["unique_identifier_id"] == "95db48e1-99ad-4e35-a86b-fa0beca5f313"
    assert new_process_entry_2.data["timestamp"] == "2023-03-21T10:45:00+00:00"

def test_create_process_entries_with_identifier():
    new_process_entry_2 = serial.ProcessEntries.create(process_id="51718ea4-a274-4455-bde3-e4216e1ecd96", component_instance_identifier=EXISTING_IDENTIFIER) 

    assert new_process_entry_2.process_id == "51718ea4-a274-4455-bde3-e4216e1ecd96"
    assert new_process_entry_2.data["unique_identifier_id"] == "95db48e1-99ad-4e35-a86b-fa0beca5f313"

def test_create_process_entries_with_id_and_submit():
    new_process_entry_2 = serial.ProcessEntries.create(process_id="51718ea4-a274-4455-bde3-e4216e1ecd96", component_instance_id="95db48e1-99ad-4e35-a86b-fa0beca5f313") 

    assert new_process_entry_2.process_id == "51718ea4-a274-4455-bde3-e4216e1ecd96"
    assert new_process_entry_2.data["unique_identifier_id"] == "95db48e1-99ad-4e35-a86b-fa0beca5f313"

    existing_process_entry.add_text("New Dataset", "Bob's Burgers") 
    existing_process_entry.add_number("New Dataset", 1.5, usl=5, lsl=0) 

    existing_process_entry.add_file("New Dataset", "test.txt")

    existing_process_entry.add_boolean("Pass Fail Criteria", True, False)
    existing_process_entry.submit(cycle_time=50, is_pass=True)

    assert existing_process_entry.data["cycle_time"] == 50

def test_create_process_entries_with_id_lots_of_data_and_submit():
    new_process_entry_3 = serial.ProcessEntries.create(process_id="51718ea4-a274-4455-bde3-e4216e1ecd96", component_instance_id="95db48e1-99ad-4e35-a86b-fa0beca5f313") 

    assert new_process_entry_3.process_id == "51718ea4-a274-4455-bde3-e4216e1ecd96"
    assert new_process_entry_3.data["unique_identifier_id"] == "95db48e1-99ad-4e35-a86b-fa0beca5f313"

    for i in range(100):
        new_process_entry_3.add_text("New Dataset", "Bob's Burgers") 
        new_process_entry_3.add_number("New Dataset", 1.5, usl=5, lsl=0) 

        new_process_entry_3.add_file("New Dataset", "test.txt")
        new_process_entry_3.add_boolean("Pass Fail Criteria", True, False)

    new_process_entry_3.submit(cycle_time=50, is_pass=True)

    assert new_process_entry_3.data["cycle_time"] == 50

def test_process_entry_submit_handles_failures():
    new_process_entry_3 = serial.ProcessEntries.create(process_id="51718ea4-a274-4455-bde3-e4216e1ecd96", component_instance_id="95db48e1-99ad-4e35-a86b-fa0beca5f313") 

    assert new_process_entry_3.process_id == "51718ea4-a274-4455-bde3-e4216e1ecd96"
    assert new_process_entry_3.data["unique_identifier_id"] == "95db48e1-99ad-4e35-a86b-fa0beca5f313"

    for i in range(100):
        if i == 50:
            serial.set_api_key("bad_key")
        if i == 75:
            serial.set_api_key(API_KEY)
        new_process_entry_3.add_text("New Dataset", "Bob's Burgers") 
        new_process_entry_3.add_number("New Dataset", 1.5, usl=5, lsl=0) 

        new_process_entry_3.add_file("New Dataset", "test.txt")

        new_process_entry_3.add_boolean("Pass Fail Criteria", True, False)

    try:
        new_process_entry_3.submit(cycle_time=50, is_pass=True)
    except serial.SerialAPIException as e:
        assert "Could not add data to process entry" in e.message 

def test_create_process_entries_with_identifier_and_fail():
    new_process_entry_2 = serial.ProcessEntries.create(process_id="51718ea4-a274-4455-bde3-e4216e1ecd96", component_instance_identifier=EXISTING_IDENTIFIER)

def test_get_datasets():
    dataset = serial.Datasets.get("LSL Only", "NUMERICAL", process_id="9ecb9747-22d9-49eb-b5c1-1d9fff3fa6b8")
    for key, value in dataset.data.items():
        assert key in SAMPLE_DATASET_DATA.keys()

def test_create_datasets():
    dataset = serial.Datasets.create("New Dataset", "NUMERICAL", "9ecb9747-22d9-49eb-b5c1-1d9fff3fa6b8", {"lsl": -10.5})
    for key, value in dataset.data.items():
        assert key in SAMPLE_DATASET_DATA.keys()

