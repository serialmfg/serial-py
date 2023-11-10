# Overview

This module provides a partial Python SDK for interacting with Serial's API. 
If you need to perform actions not provided in the SDK, please reference the [API documentation](https://docs.serial.io/api-reference).
If neither the API nor the library provides you with the necessary tools, please contact [Serial Support](mailto:support@serial.io).
The latest version of the library can be downloaded [here](https://github.com/serialmfg/serial-py).

# Installation

Clone the repository from GitHub or install via pip:
```
git clone https://https://github.com/serialmfg/serial-py.git
```
or 
```
pip install serialmfg
```

# Dependencies

This project requires the following dependencies:
- requests

# Example Usage

1. Get an API key from your Serial account or admin. 

2. (Optionally) Generate a station ID from process builder in the serial web app. 
![Generate Station Id](https://xblmulqojemwvkwbkajj.supabase.co/storage/v1/object/public/serial-assets-public/generate_process_id.png)

3. Implement your script: 
```python
import serialmfg as serial

serial.set_station_id('YOUR_STATION_ID')
serial.set_api_key('YOUR_API_KEY')

# ----------- Component Instances ----------- #
# Creating a component instance
my_component_instance_1 = serial.ComponentInstances.create(identifier="identifier-1234", component_name="component-name") 

# Getting a component instance
my_component_instance_2 = serial.ComponentInstances.get(identifier="identifier-1234") 

# Listing component instances
defective_components = serial.ComponentInstances.list({"name":"component-name", "active": True}) 


# ----------- Process Entries ----------- #
# Creating a process entry
my_process_entry = serial.ProcessEntries.create(process_id="process-id", component_instance=my_component_instance_1) 
my_process_entry_2 = serial.ProcessEntries.create(process_id="process-id", component_instance_id=my_component_instance_1.data["id"])
my_process_entry_3 = serial.ProcessEntries.create(process_id="process-id", component_instance_identifier=component_instance_1.data["identifier"])

# Adding data to a process entry
my_process_entry.add_text(dataset_name="Foo", value="bar")
my_process_entry.add_number(dataset_name="Pi Approx", value=3.141, usl=3.1, lsl=3.2)
my_process_entry.add_boolean(dataset_name="PassFail Criteria", value=True, expected_value=False)
my_process_entry.add_file(dataset_name="Oven Temperatures", path="/Users/me/Downloads/oven-temp.csv", file_name="oven-temp-todays-date.csv") 
my_process_entry.add_image(dataset_name="Cat Pictures", path="/Users/me/Documents/my-cat.png", file_name="jerry.png") 
my_process_entry.add_link(dataset_name="Parent Component", child_identifier="child-component-instance", parent_identifier="parent-component-instance")

# Submitting a process entry
my_process_entry.submit(cycle_time=42, is_pass=False) #Optionally add cycle_time or process result override
```

