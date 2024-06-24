import serialmfg as serial

serial.set_station_id('YOUR_STATION_ID')
serial.set_api_key('YOUR_API_KEY')

# ----------- Component Instances ----------- #

# Creating a component instance
my_component_instance = serial.ComponentInstances.create(identifier="ABC-1234", component_name="Component Name") 

# ----------- Process Entries ----------- #

# Creating a process entry
my_process_entry = serial.ProcessEntries.create(process_id="process-id", component_instance_identifier="ABC-1234") 

# Submitting a process entry
my_process_entry.submit()
