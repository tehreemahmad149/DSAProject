import json
import os
from implementation_forwardIndex import ForwardIndex
from utils.utils import process_content_generator, generate_unique_doc_id

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
                        file_name = os.path.splitext(os.path.basename(file_path))[0]
                        doc_id = generate_unique_doc_id(file_name, obj_index)
                        metadata_list.append({'doc_id': doc_id, 'json_id': json_id, 'json_url': json_url})
                
                if metadata_list:
                    return metadata_list

        except json.JSONDecodeError as e:
            print(f"Error decoding JSON in file {file_path}: {e}")

    return []

# Path to the folder containing JSON files
<<<<<<< Updated upstream
folder_path = "\\DSAProject\\testFiles"
=======
folder_path = "C:\\DSAProject\\testFiles"
>>>>>>> Stashed changes

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

<<<<<<< Updated upstream
# Save metadata to a TXT file
metadata_file_path_txt = '\\DSAProject\\metadata.txt'
with open(metadata_file_path_txt, 'w', encoding='utf-8') as metadata_file:
    for metadata_entry in metadata_list:
        metadata_file.write(f"Doc ID: {metadata_entry['doc_id']}\n")
        metadata_file.write(f"JSON ID: {metadata_entry['json_id']}\n")
        metadata_file.write(f"JSON URL: {metadata_entry['json_url']}\n")
=======
# Save metadata to a JSON file
metadata_file_path_json = "C:\\DSAProject\\metadata.json"
with open(metadata_file_path_json, 'w', encoding='utf-8') as metadata_file:
    json.dump(metadata_dict, metadata_file, indent=2)
>>>>>>> Stashed changes


print(f"Metadata saved to {metadata_file_path_txt}")
