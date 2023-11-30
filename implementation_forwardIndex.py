import json
import os
import sys
from class_forwardIndex import ForwardIndex
from utils.utils import process_content_generator, generate_unique_doc_id

# Set the default encoding for standard output to 'utf-8'
sys.stdout.reconfigure(encoding='utf-8')

# Set console encoding to 'utf-8' (for Windows)
os.system('chcp 65001')

# Create an instance of the ForwardIndex class
forward_index = ForwardIndex()

folder_path = 'C:\\Users\\user\\Documents\\GitHub\\DSAProject\\testFiles'

# Function to extract content and document IDs from each JSON file
def extract_content_and_id_from_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        try:
            # Load JSON data from the file
            data = json.load(file)
            
            if isinstance(data, list):
                # Iterate over each object in the list
                for obj_index, obj in enumerate(data):
                    # Extract content from the 'content' field of the object
                    content_item = obj.get('content', '')
                    
                    # Process content and generate a unique document ID
                    if content_item:
                        file_name = os.path.splitext(os.path.basename(file_path))[0]
                        article_id = generate_unique_doc_id(file_name, obj_index)
                        tokens = process_content_generator(content_item)
                        
                        # Add the document to the forward index
                        forward_index.add_document(article_id, tokens)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON in file {file_path}: {e}")

# Iterate over each file
for filename in os.listdir(folder_path):
    file_path = os.path.join(folder_path, filename)
    # Check if the item is a file and has a '.json' extension
    if os.path.isfile(file_path) and filename.endswith('.json'):
        extract_content_and_id_from_json(file_path)

output_file_path_txt = 'forward_index.txt'

# Write the forward index to a TXT file (line by line)
with open(output_file_path_txt, 'w', encoding='utf-8') as txtfile:
    # Iterate over each document in the forward index
    for doc_id, keywords in forward_index.index.items():
        keyword_str = ', '.join(map(str, keywords))
        # Write document ID and associated keywords to the output file
        txtfile.write(f"Document ID: {doc_id}\n")
        txtfile.write(f"Keywords: {keyword_str}\n")

lexicon_file_path_txt = 'lexicon.txt'

# Writing the lexicon to a TXT file in sorted order based on word IDs
with open(lexicon_file_path_txt, 'w', encoding='utf-8') as lexfile:
    lexfile.write("Word ID\tWord\n")
    sorted_lexicon = sorted(forward_index.get_lexicon(), key=forward_index.get_word_id)
    # Iterate over each word in the lexicon
    for word in sorted_lexicon:
        word_id = forward_index.get_word_id(word)
        lexfile.write(f"{word_id}\t{word}\n")

# Display success messages
print(f"Forward index saved to {output_file_path_txt}")
print(f"Lexicon saved to {lexicon_file_path_txt}")