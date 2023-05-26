# Overview

This module provides a simple Python interface to interact with the Serial API. It allows you to easily perform common operations such as uploading process data, initializing identifiers, and checking the server connection. The latest version of the library can be downloaded [here](https://github.com/serialmfg/serial-py)

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
- json
- os

# Usage

1. Get API key from [documentation page](https://api.serial.io/docs/none/#authentication)

2. Generate a station ID from process builder in the serial web app. 
![Generate Station Id](https://xblmulqojemwvkwbkajj.supabase.co/storage/v1/object/public/serial-assets-public/generate_process_id.png)

3. Implement python script: 
```python
from serialmfg import *

API_KEY = "<YOUR_API_KEY>"
STATION_ID = None # or "<YOUR_STATION_ID>" # (Station ID is optional)

# 1) Setup
serial = Serial(api_key=API_KEY, station_id=STATION_ID)
response = serial.check_connection()

print(response.status_code, response.text)

# 2) Initialize New Serial Number (Optional)
my_identifier = Identifier(identifier="<sn_or_lot_code>", component="<component_name>")
response = serial.initialize_identifier(my_identifier)

print(response.status_code, response.text)

# 3) Add Data
my_process = Process(identifier="<your_sn_or_lot_code>", process_id="<your_process_id>")
my_process.add_parameter(key_name="<your_key_name>", value=1234, unit="<your_unit>")
my_process.add_image(key_name="<your_key_name>", path="<your_file_path>")
my_process.add_file(key_name="<your_key_name>", path="<your_file_path>")

# 4) Upload
response = serial.upload_process_data(my_process)

print(response.status_code, response.text)
```

# Classes

## **Serial**

A class representing the Serial.io API connection.

```python
Serial(api_key, station_id=None, base_url=BASE_URL)
```

### Constructor Parameters
| Parameter | Type | Description | Required |
| --- | --- | --- | --- |
| `api_key` | str | The API key for authentication. | Yes |
| `station_id` | str | The ID of the station. | No |
| `base_url` | str | The base URL for the API. | No |

### Methods
  - `set_station_id(station_id)`: Sets the station ID for the Station object.
    | Parameter | Type | Description | Required |
    | --- | --- | --- | --- |
    | `station_id` | str | The ID of the station. | Yes |

  - `upload_process_data(process)`: Uploads process data to the server.
    | Parameter | Type | Description | Required |
    | --- | --- | --- | --- |
    | `process` | Process | A `Process` object containing the data to be uploaded. | Yes |

  - `initialize_identifier(identifier_object)`: Initializes the identifier on the server.
    | Parameter | Type | Description | Required |
    | --- | --- | --- | --- |
    | `identifier_object` | Identifier | An `Identifier` object. | Yes |

  - `check_connection()`: Checks if the server is active and if the station ID is valid.



## **Identifier**

A class representing the identifier object.

```python
Identifier(identifier, component, part_number=None)
```

### Constructor Parameters
| Parameter | Type | Description | Required |
| --- | --- | --- | --- |
| `identifier` | str | The identifier for the object. | Yes |
| `component` | str | The component for the object. | Yes |
| `part_number` | str | The part number for the object. | No |



## **Process**

A class representing the process data to be uploaded to the API.

```python
Process(identifier)
```

### Constructor Parameters
| Parameter | Type | Description | Required |
| --- | --- | --- | --- |
| `identifier` | str | The identifier for the process data. | Yes |

### Methods
- `add_link(identifier)`: Adds a linked component to the process data.
    | Parameter | Type | Description | Required |
    | --- | --- | --- | --- |
    | `identifier` | str | The identifier for the linked component. | Yes |

- `add_parameter(key_name, value, usl=None, lsl=None, unit=None)`: Adds a parameter to the process data.
    | Parameter | Type | Description | Required |
    | --- | --- | --- | --- |
    | `key_name` | str | The key name of the parameter. | Yes |
    | `value` | float/str | The value of the parameter. | Yes |
    | `usl` | float | The upper specification limit of the parameter. | No |
    | `lsl` | float | The lower specification limit of the parameter. | No |
    | `unit` | str | The unit of measurement for the parameter. | No |

- `add_image(key_name, path)`: Adds an image to the process data.
    | Parameter | Type | Description | Required |
    | --- | --- | --- | --- |
    | `key_name` | str | The key name of the image. | Yes |
    | `path` | str | The path to the image file. | Yes |

- `add_file(key_name, path)`: Adds a file to the process data.
    | Parameter | Type | Description | Required |
    | --- | --- | --- | --- |
    | `key_name` | str | The key name of the file. | Yes |
    | `path` | str | The path to the file. | Yes |

- `set_pass_fail(is_pass)`: Overrides the pass / fail status of the process.
    | Parameter | Type | Description | Required |
    | --- | --- | --- | --- |
    | `is_pass` | bool | The pass status of the process data. | Yes |

