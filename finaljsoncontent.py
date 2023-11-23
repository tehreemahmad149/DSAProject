import os
import json

def read_json_files():
    folder_path = '\\Users\\tehre\\OneDrive\\Documents\\JSONFILES'

    # List all files in the folder
    file_list = os.listdir(folder_path)

    # Filter only JSON files
    json_files = [file for file in file_list if file.endswith('.json')]

    for json_file in json_files:
        file_path = os.path.join(folder_path, json_file)
        
        # Read JSON file
        with open(file_path, 'r') as file:
            try:
                data = json.load(file)  # Use json.load to read from file
                for obj in data:
                    if 'content' in obj:
                        content = obj['content']
                        yield content
                    else:
                        print("The 'content' key not found in the JSON object.")
            except json.JSONDecodeError as e:
                print(f"Error decoding {json_file}: {e}")

for content in read_json_files():
    print(content)
    print('\n\n\n\n')#to know that the article has ended.....terminating characters
