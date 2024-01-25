import serialmfg as serial

serial.set_station_id('YOUR_STATION_ID')
serial.set_api_key('YOUR_API_KEY')

# Creating a component instance
my_component_instance = serial.ComponentInstances.create(
    identifier='ABC-1234', 
    component_name='YOUR_COMPONENT_NAME'
)

# Creating a process entry
my_process_entry = serial.ProcessEntries.create(
    process_id='YOUR_PROCESS_ID', 
    component_instance_identifier='ABC-1234'
)

# Adding data to a process entry
my_process_entry.add_text(dataset_name="Foo", value="Bar")
my_process_entry.add_number(dataset_name="Pi Approx", value=3.141, lsl=3.1, usl=3.2)

# Submitting a process entry
my_process_entry.submit()