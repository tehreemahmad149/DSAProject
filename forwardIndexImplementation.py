# forwardIndexImplementation.py
import json
import os
import sys
from forwardIndex import ForwardIndex
from utils.utils import process_content_generator, generate_unique_doc_id

# Set the default encoding to 'utf-8'
sys.stdout.reconfigure(encoding='utf-8')

# Set console encoding to 'utf-8' (for Windows)
os.system('chcp 65001')

forward_index = ForwardIndex()

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

                        # Add document to the forward index
                        forward_index.add_document(article_id, tokens)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON in file {file_path}: {e}")

# Iterating over each file in the folder for the forward index implementation
for filename in os.listdir(folder_path):
    file_path = os.path.join(folder_path, filename)
    if os.path.isfile(file_path) and filename.endswith('.json'):
        extract_content_and_id_from_json(file_path)

# Save the forward index to a TXT file with improved formatting
output_file_path_txt = 'forward_index.txt'

with open(output_file_path_txt, 'w', encoding='utf-8') as txtfile:
    # Write header for the forward index file
    txtfile.write("Document ID\tKeywords\n")

    # Write each document ID, its associated keywords
    for doc_id, keywords in forward_index.index.items():
        keyword_str = ', '.join(map(str, keywords))
        txtfile.write(f"Document ID: {doc_id}\n")
        txtfile.write(f"Keywords: {keyword_str}\n")

        # Add a separator line
        txtfile.write('-' * 40 + '\n')
        # Skip 3 lines
        txtfile.write('\n' * 3)

# Save the lexicon to a separate TXT file
lexicon_file_path_txt = 'lexicon.txt'
with open(lexicon_file_path_txt, 'w', encoding='utf-8') as lexfile:
    # Write header for the lexicon file
    lexfile.write("Word ID\tWord\n")

    # Write lexicon to the lexicon file in sorted order
    for word in forward_index.lexicon:
        word_id = forward_index.get_word_id(word)
        lexfile.write(f"{word_id}\t{word}\n")

print(f"Forward index saved to {output_file_path_txt}")
print(f"Lexicon saved to {lexicon_file_path_txt}")