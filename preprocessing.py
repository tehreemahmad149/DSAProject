# preprocessing.py
import json
import os
import sys
from utils.utils import process_content_generator, generate_unique_doc_id

# Set the default encoding to 'utf-8'
sys.stdout.reconfigure(encoding='utf-8')

# Set console encoding to 'utf-8' (for Windows)
os.system('chcp 65001')

# Path to the folder containing the JSON files locally
folder_path = 'C:\\Users\\user\\Documents\\dataset\\dataset'

# Function to extract content from all objects in each JSON file
def extract_content_and_id_from_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        try:
            data = json.load(file)
            if isinstance(data, list):
                for obj_index, obj in enumerate(data):
                    content_item = obj.get('content', '')
                    if content_item:
                        # Generate a unique document ID
                        file_name = os.path.splitext(os.path.basename(file_path))[0]
                        article_id = generate_unique_doc_id(file_name, obj_index)

                        # Process content using a generator
                        tokens = process_content_generator(content_item)

                        yield article_id, tokens
            else:
                print(f"No content found in file {file_path}")
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON in file {file_path}: {e}")

# Iterating over each file in the folder for preprocessing
for filename in os.listdir(folder_path):
    file_path = os.path.join(folder_path, filename)
    if os.path.isfile(file_path) and filename.endswith('.json'):
        for article_id, content_tokens in extract_content_and_id_from_json(file_path):
            # Convert the list of tokens to a string before printing
            tokenized_content_str = ', '.join(map(str, content_tokens))
            print(f"Article ID: [{article_id}], Tokenized Content: [{tokenized_content_str.encode('utf-8', 'ignore').decode('utf-8')}]")
            print("\n" * 4)
