import os
import json

def read_json_files():
    # List all files in the folder
    file_list = os.listdir('\\Users\\tehre\\OneDrive\\Documents\\JSONFILES')

    # Filter only JSON files
    json_files = [file for file in file_list if file.endswith('.json')]

    for json_file in json_files:
        file_path = os.path.join('\\Users\\tehre\\OneDrive\\Documents\\JSONFILES', json_file)
        
        # Read JSON file
        with open(file_path, 'r') as file:
            try:
                data = json.load(file)
                # Do something with the data (process, analyze, etc.)
                print(f"Content of {json_file}: {data}")
                
                # Return the content of the current file
                yield data
            except json.JSONDecodeError as e:
                print(f"Error decoding {json_file}: {e}")

# Example usage:
for content in read_json_files():
    print(content)
    print('\n')
    pass
