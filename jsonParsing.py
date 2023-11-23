import json
import os

# Path provided to folder containing the JSON files locally
folder_path = 'C:\\Users\\user\\Documents\\dataset\\dataset'

# Function to extract content from all the objects in every JSON file
def extract_content_from_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        try:
            data = json.load(file)
            # Extracting "content" field
            if isinstance(data, list):
                for obj in data:
                    content_item = obj.get('content', '')
                    if content_item:
                        yield content_item
            else:
                print(f"No content found in file {file_path}")
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON in file {file_path}: {e}")

# Iterating over each file in the folder
for filename in os.listdir(folder_path):
    file_path = os.path.join(folder_path, filename)
    if os.path.isfile(file_path) and filename.endswith('.json'):
        for content in extract_content_from_json(file_path):
            # Encoding content using 'utf-8'
            print(f"File: {filename}, Content: {content.encode('utf-8', 'replace')}")
            print(f"\n\n\n\n")
