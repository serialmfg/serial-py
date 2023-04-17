from serialmfg import *

API_KEY = "<YOUR_API_KEY>"
STATION_ID = "<YOUR_STATION_ID>"

# 1) Setup
serial = Serial(api_key=API_KEY)
response = serial.check_connection()
print(response.status_code, response.text)

# 2) Initialize New Serial Number (Optional)
my_identifier = Identifier(identifier="<sn_or_lot_code>", component="<component_name>")
response = serial.initialize_identifier(my_identifier)

print(response.status_code, response.text)

# 3) Add Data
my_process = Process(identifier="<your_sn_or_lot_code>")
my_process.add_parameter(key_name="<your_key_name>", value=1234, unit="<your_unit>")
my_process.add_image(key_name="<your_key_name>", path="<your_file_path>")
my_process.add_file(key_name="<your_key_name>", path="<your_file_path>")

# 4) Upload
response = serial.upload_process_data(my_process, station_id=STATION_ID)

print(response.status_code, response.text)