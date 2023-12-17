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

# def get_barrel_id(query, barrels):
#     for word in query:
#         wordId= forward_index_instance.get_word_id(word)
#         print(wordId)
#         if(wordId):
#             barrels.append(get_barrel_for_word_id(wordId))

def split_json_by_word_id(input_path, output_folder):
    with open(input_path, 'r') as input_file:
        data = json.load(input_file)

    # Assuming the JSON file contains an array of objects
    if not isinstance(data, dict):
        raise ValueError("Input JSON should contain a dictionary of objects.")

    # Create a dictionary to store data for each barrel
    barrels_data = {}

    # Iterate through the data to determine the barrels and store data in respective dictionaries
    for key, value in data.items():
        word_id = int(value["Word ID"])
        barrel_name = get_barrel_for_word_id(word_id)

        # Check if the barrel dictionary exists, if not, create it
        if barrel_name not in barrels_data:
            barrels_data[barrel_name] = {}

        # Add the data to the barrel dictionary
        barrels_data[barrel_name][key] = value

    # Iterate through the barrels and write the dictionaries to respective files
    for barrel_name, barrel_data in barrels_data.items():
        output_path = os.path.join(output_folder, f"{barrel_name}.json")

        with open(output_path, 'w') as output_file:
            json.dump(barrel_data, output_file, indent=1)


input_file_path = '/home/gosal/Documents/DSA/project/DSAProject/II.json'
output_folder_path = '/home/gosal/Documents/DSA/project/DSAProject/barrel_created/'

split_json_by_word_id(input_file_path, output_folder_path)

# End time measurement
end = time.time()
print(end - start)
