import json
import os
import time
import hashlib  # Import hashlib for SHA-256
from class_forwardIndex import ForwardIndex
from utils.utils import process_content_generator, generate_unique_doc_id

def hash_string(string):
    # Calculate SHA-256 hash of the input string
    sha256 = hashlib.sha256()
    sha256.update(string.encode('utf-8'))
    return sha256.hexdigest()

def extract_metadata_from_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        try:
            # Load JSON data from the file
            data = json.load(file)

            # Check if data is a list
            if isinstance(data, list):
                metadata_list = []
                for obj_index, obj in enumerate(data):
                    # Extract metadata from each object in the list
                    json_id = obj.get('id', '')
                    json_url = obj.get('url', '')

                    if json_id and json_url:
                        # Use SHA-256 hash as the document ID
                        doc_id = hash_string(f"{json_id}_{json_url}")
                        metadata_list.append({'doc_id': doc_id, 'json_id': json_id, 'json_url': json_url})

                if metadata_list:
                    return metadata_list
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON in file {file_path}: {e}")
    return []

#start time measurement
start = time.time()

# Path to the folder containing JSON files
folder_path = "/home/gosal/Documents/DSA/project/DSAProject/testFiles/"

# Create an instance of the ForwardIndex class
forward_index = ForwardIndex()

# Metadata list to store information
metadata_list = []

# Iterate over each file
for filename in os.listdir(folder_path):
    file_path = os.path.join(folder_path, filename)
    # Check if the item is a file and has a '.json' extension
    if os.path.isfile(file_path) and filename.endswith('.json'):
        # Extract content and document IDs from each JSON file
        metadata_list.extend(extract_metadata_from_json(file_path))

# Save metadata to a JSON file
metadata_file_path_json = '/home/gosal/Documents/DSA/project/DSAProject/metadata.json'
with open(metadata_file_path_json, 'w', encoding='utf-8') as metadata_file:
    json.dump(metadata_list, metadata_file, indent=2)

print(f"Metadata saved to {metadata_file_path_json}")


end = time.time()
print(end - start)