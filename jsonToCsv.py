import os
import json
import csv

# Path to the directory containing JSON files
path_to_json = 'C:\\Users\\user\\Documents\\dataset\\dataset\\newsdata'
# Output directory to store CSV files
output_directory = 'C:\\Users\\user\\Documents\\dataset\\dataset\\output_csv'

# Create the output directory if it doesn't exist
os.makedirs(output_directory, exist_ok=True)

# Find all JSON files in the input directory
json_files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.json')]

# Iterate over JSON files
for js in json_files:
    with open(os.path.join(path_to_json, js)) as json_file:
        try:
            # Load JSON data
            json_data = json.load(json_file)

            # Assuming the JSON structure is a list of items
            records = []
            for item in json_data:
                record = {
                    'id': item.get('id', ''),
                    'date': item.get('date', ''),
                    'source': item.get('source', ''),
                    'title': item.get('title', ''),
                    'content': item.get('content', '').replace('\n', ' '),  # Replace newline characters with space
                    'author': item.get('author', ''),
                    'url': item.get('url', ''),
                    'published': item.get('published', ''),
                    'published_utc': item.get('published_utc', ''),
                    'collection_utc': item.get('collection_utc', '')
                }
                records.append(record)

            # Generate a unique filename based on the 'id' field
            cleaned_id = ''.join(c for c in records[0]['id'] if c.isalnum())  # Remove non-alphanumeric characters
            filename = os.path.join(output_directory, f"{cleaned_id}_{js}.csv")

            print(f"Processing {filename}")

            # Write all records to a CSV file
            with open(filename, 'w', newline='', encoding='utf-8') as output_file:
                csv_writer = csv.DictWriter(output_file, fieldnames=records[0].keys())
                csv_writer.writeheader()
                csv_writer.writerows(records)

        except Exception as e:
            print(f"Error processing file {js}: {e}")
