import json
import os

def split_json_alphabetically(input_path, output_folder):
    with open(input_path, 'r') as input_file:
        data = json.load(input_file)

    # Assuming the JSON file contains an array of objects
    if not isinstance(data, dict):
        raise ValueError("Input JSON should contain a dictionary of objects.")

    # Create output folders if they don't exist
    for char in 'abcdefghijklmnopqrstuvwxyz':
        folder_path = os.path.join(output_folder, char)
        os.makedirs(folder_path, exist_ok=True)

        # Create a single JSON file for each alphabet
        output_path = os.path.join(folder_path, f"{char}.json")

        # Write all key-value pairs with the same starting alphabet to the file
        with open(output_path, 'w') as output_file:
            # Filter key-value pairs with the current starting alphabet
            filtered_data = {key: value for key, value in data.items() if key.startswith(char)}

            # Write the filtered data to the JSON file
            json.dump(filtered_data, output_file, indent=4)


if __name__ == "__main__":
    input_file_path = '/home/gosal/Documents/DSA/project/github_repo/DSAProject/II.json'  # Replace with your input file path
    output_folder_path = '/home/gosal/Documents/DSA/project/github_repo/DSAProject/barrel_created/'   # Replace with your desired output folder path

    split_json_alphabetically(input_file_path, output_folder_path)
