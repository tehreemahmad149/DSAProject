import json
import os
import time

# Function to determine the barrel based on word_id
def get_barrel_for_word_id(word_id):
    # Assuming word IDs are integers, determine the barrel based on the division
    # Each barrel contains a maximum of 1000 words
    barrel_number = word_id // 1000
    return f"barrel_{barrel_number}"

# Start time measurement
start = time.time()

def split_json_by_word_id(input_path, output_folder):
    with open(input_path, 'r') as input_file:
        data = json.load(input_file)

    # Assuming the JSON file contains an array of objects
    if not isinstance(data, dict):
        raise ValueError("Input JSON should contain a dictionary of objects.")

    # Iterate through the data to determine the barrels and write to respective files
    for key, value in data.items():
        word_id = int(value["Word ID"])
        barrel_name = get_barrel_for_word_id(word_id)
        folder_path = os.path.join(output_folder, barrel_name)
        os.makedirs(folder_path, exist_ok=True)

        output_path = os.path.join(folder_path, f"{barrel_name}.json")

        # Append the data to the existing file or create a new one
        with open(output_path, 'a') as output_file:
            json.dump({key: value}, output_file, indent=4)
            output_file.write("\n")  # Add a newline for each entry

# Replace the paths with your actual file paths
input_file_path = '/home/gosal/Documents/DSA/project/DSAProject/II.json'
output_folder_path = '/home/gosal/Documents/DSA/project/DSAProject/barrel_created/'

split_json_by_word_id(input_file_path, output_folder_path)

# End time measurement
end = time.time()
print(end - start)
