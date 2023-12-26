import json
import os
import time
import hashlib  # Import hashlib for SHA-256
from .class_forwardIndex import ForwardIndex
from .utils.utils import process_content_generator, generate_unique_doc_id       


def load_metadata(metadata_file_path_json):
    try:
        with open(metadata_file_path_json, 'r', encoding='utf-8') as metadata_file:
            metadata_dict = json.load(metadata_file)
        return metadata_dict
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON in file {metadata_file_path_json}: {e}")
        return {}

def display_metadata(metadata_dict, doc_ids=None):
    if doc_ids is None:
        doc_ids = metadata_dict.keys()

    for doc_id in doc_ids:
        if doc_id in metadata_dict:
            metadata = metadata_dict[doc_id]
            json_id = metadata.get('json_id', '')
            json_url = metadata.get('json_url', '')
            print(f"Document ID: {doc_id}")
            print(f"json_id: {json_id}")
            print(f"json_url: {json_url}")
            print("-" * 20)

def extract_metadata_from_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        try:
            # Load JSON data from the file
            data = json.load(file)

            # Check if data is a list
            if isinstance(data, list):
                metadata_dict = {}
                for obj_index, obj in enumerate(data):
                    # Extract metadata from each object in the list
                    json_id = obj.get('id', '')
                    json_url = obj.get('url', '')

                    if json_id and json_url:
                        # Use SHA-256 hash as the document ID
                        # doc_id = hash_string(f"{json_id}_{json_url}")

                        # Generate a unique document ID based on the file name and object index
                        file_name = os.path.splitext(os.path.basename(file_path))[0]
                        article_id = generate_unique_doc_id(file_name, obj_index)

                        doc_id = hashlib.sha256(article_id.encode()).hexdigest()
                        metadata_dict[doc_id] = {'json_id': json_id, 'json_url': json_url}

                if metadata_dict:
                    return metadata_dict
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON in file {file_path}: {e}")
    return []

#start time measurement
start = time.time()

# Path to the folder containing JSON files
folder_path = r"C:\Users\user\Documents\GitHub\DSA\myproject\myapi\testFiles"

# Create an instance of the ForwardIndex class
forward_index = ForwardIndex()

# Metadata list to store information
metadata_dict = {}

# Iterate over each file
for filename in os.listdir(folder_path):
    file_path = os.path.join(folder_path, filename)
    # Check if the item is a file and has a '.json' extension
    if os.path.isfile(file_path) and filename.endswith('.json'):
        # Extract content and document IDs from each JSON file
        metadata_dict.update(extract_metadata_from_json(file_path))

# Save metadata to a JSON file
metadata_file_path_json = r"C:\Users\user\Documents\GitHub\DSA\myproject\myapi\metadata.json"
with open(metadata_file_path_json, 'w', encoding='utf-8') as metadata_file:
    json.dump(metadata_dict, metadata_file, indent=2)

print(f"Metadata saved to {metadata_file_path_json}")

end = time.time()
print(end - start)