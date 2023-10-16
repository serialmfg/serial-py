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

serial.api_key = 'my_api_key'
serial.station_id = 'my_station_id' # optional

# ----------- Component Instances ----------- #

# Getting a component instance
my_component_instance_1 = serial.ComponentInstances.get(identifier="my_sn_or_lot_code_1") # Returns a ComponentInstance object

# Creating a component instance
my_component_instance_2 = serial.ComponentInstances.create(identifier="my_sn_or_lot_code_2", component="my_component_name") # Returns a ComponentInstance object

# Listing component instances
defective_components = serial.ComponentInstances.list({"status"="DEFECTIVE", "component_id"="my_component_id"}) # Returns an array of ComponentInstance objects

# Linking a component instance to a child
my_component_instance_1.add_link(child=my_component_instance_2)

# ----------- Process Entries ----------- #

# Creating a process entry
my_process_entry = serial.ProcessEntries.create(process_id="my_process_id", component_instance=my_component_instance_1) # Returns a ProcessEntry object

my_process_entry.add_text(dataset_name="Foo", value="bar")
my_process_entry.add_number(dataset_name="Pi Approx", value=3.141, usl=3.1, lsl=3.2)
my_process.add_boolean(dataset_name="PassFail Criteria", value=True, expected_value=False)
my_process_entry.add_file(dataset_name="Oven Temperatures", path="/Users/me/Downloads/oven-temp.csv", file_name="oven-temp-todays-date.csv") # File name is optional to override the provided name
my_process_entry.add_image(dataset_name="Cat Pictures", path="/Users/me/Documents/my-cat.png", file_name="jerry.png") # File name is optional to override the provided name
my_process_entry.submit(cycle_time=42, is_pass=True, is_complete=True) # Notes how long the cycle took for the entry, whether it is passing and whether the process is complete
```

