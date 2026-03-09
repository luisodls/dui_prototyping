import requests

# Variables
original_example = '''
base_url = "https://data.cloud.ccp4.ac.uk/api" # Replace with actual API base URL
user = "example_user"
source_id = "upload"
data_id = "my_dataset_01"  # The {id} for this specific data entry

# Construct the endpoint URL
url = f"{base_url}/data/{user}/{source_id}/{data_id}/upload"
'''
url = 'http://localhost:8080/'

# Define the headers
cloudrun_id = "XXXX-XXXX-XXXX-XXXX"
headers = {
    "cloudrun_id": cloudrun_id
}
# Define the files to upload
# Format: 'file': ('filename', file_object)
'''files = {
    'file': ('data.mtz', open('data.mtz', 'rb'))
}'''

files = {
    'file': ('upload.me', open('upload.me', 'rb'))
}

try:
    response = requests.post(url, headers=headers, files=files)

    if response.status_code == 200:
        print("Upload Successful!")
        print(response.json())

    else:
        print(f"Upload failed with status code: {response.status_code}")
        print(response.text)

except ConnectionRefusedError:
    print("Connection Refused Err Catch")

except requests.exceptions.ConnectionError:
    print("Connection Err Catch")

finally:
    # Ensure the file is closed
    files['file'][1].close()
