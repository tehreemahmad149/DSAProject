'''import json
with open('jesusdaily.json', 'r') as json_file:
    data = json.load(json_file)
    print(data)'''
import os
import json
# this code will be used to load all the data from a selected json file to data variable
# will be used read all files
folder_path = 'add in the path to the folder '  #make sure to use double slash in path otherwise python will give unicode error due to escape sequences

# List all files in the folder
file_list = os.listdir(folder_path)

# Filter only JSON files
json_files = [file for file in file_list if file.endswith('.json')]

# Process each JSON file
for json_file in json_files:
    file_path = os.path.join(folder_path, json_file)
    
    # Read JSON file
    with open(file_path, 'r') as file:
        try:
            data = json.load(file)
            # Do something with the data (process, analyze, etc.)
            print(f"Content of {json_file}: {data}")
        except json.JSONDecodeError as e:
            print(f"Error decoding {json_file}: {e}")
