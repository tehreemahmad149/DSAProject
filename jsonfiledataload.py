import os
import json
# Increased Error Handling
def replace_problematic_characters(text):
    # Replace characters that may cause encoding issues with a placeholder
    return ''.join(char if char.isprintable() else '?' for char in text)

def read_json_files():
    # List all files in the folder
    file_list = os.listdir('C:\\Users\\user\\Documents\\dataset\\dataset')

    # Filter only JSON files
    json_files = [file for file in file_list if file.endswith('.json')]

    for json_file in json_files:
        file_path = os.path.join('C:\\Users\\user\\Documents\\dataset\\dataset', json_file)
        
        # Read JSON file
        with open(file_path, 'r', encoding='utf-8') as file:
            try:
                data = json.load(file)
                yield data
            except json.JSONDecodeError as e:
                print(f"Error decoding {json_file}: {e}")

                # If you want to continue processing other files even if one fails, you can use 'continue'
                continue

        # Move the print('\n') statement inside the loop
        print('\n')

# Example usage:
for data in read_json_files():
    try:
        # Use replace_problematic_characters to handle encoding issues
        print(replace_problematic_characters(json.dumps(data, ensure_ascii=False)))
    except UnicodeEncodeError:
        print("Cannot print some characters in this data.")
    print('\n')
