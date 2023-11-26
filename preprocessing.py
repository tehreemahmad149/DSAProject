import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import json
import os
import string
import re
import sys
from forwardIndex import ForwardIndex 
import csv

# Set the default encoding to 'utf-8'
sys.stdout.reconfigure(encoding='utf-8')

# Download stopwords
nltk.download('punkt')
nltk.download('stopwords')

# Set console encoding to 'utf-8' (for Windows)
os.system('chcp 65001')

# Define a set of stopwords and punctuation
stop_words = set(stopwords.words('english'))
punctuation = set(string.punctuation)

forward_index = ForwardIndex()

# Function to remove special characters using regex
def remove_special_characters(text):
    return re.sub(r'[^A-Za-z0-9\s]', '', text)

# Custom function to generate unique document IDs
def generate_unique_doc_id(file_name, obj_index):
    return f"{file_name}_{obj_index}"

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

                        # Lowercasing the parsed content
                        content = content_item.lower()

                        # Remove special characters
                        content = remove_special_characters(content)

                        # Remove stopwords and punctuation
                        tokens = [word for word in word_tokenize(content) if word.isalpha() and word not in stop_words and word not in punctuation]

                        yield article_id, tokens
            else:
                print(f"No content found in file {file_path}")
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON in file {file_path}: {e}")

# Iterating over each file in the folder
for filename in os.listdir(folder_path):
    file_path = os.path.join(folder_path, filename)
    if os.path.isfile(file_path) and filename.endswith('.json'):
        for article_id, content_tokens in extract_content_and_id_from_json(file_path):
            forward_index.add_document(article_id, content_tokens)
            # Convert the list of tokens to a string before printing
            tokenized_content_str = ', '.join(map(str, content_tokens))
            print(f"Article ID: [{article_id}], Tokenized Content: [{tokenized_content_str.encode('utf-8', 'ignore').decode('utf-8')}]")
            print("\n" * 4)

# Save the forward index to a TXT file with improved formatting
output_file_path_txt = 'forward_index.txt'

with open(output_file_path_txt, 'w', encoding='utf-8') as txtfile:
    # Write header
    txtfile.write("Document ID\tKeywords\n")

    # Write each document ID and its associated keywords
    for doc_id, keywords in forward_index.index.items():
        keyword_str = ', '.join(map(str, keywords))
        txtfile.write(f"Document ID: {doc_id}\n")
        txtfile.write(f"Keywords: {keyword_str}\n")
        # Add a separator line
        txtfile.write('-' * 40 + '\n')
        # Skip 3 lines
        txtfile.write('\n' * 3)

print(f"Forward index saved to {output_file_path_txt}")