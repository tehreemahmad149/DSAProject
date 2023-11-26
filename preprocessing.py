import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import json
import os
import string
import re
import sys

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

# Function to remove special characters using regex
def remove_special_characters(text):
    return re.sub(r'[^A-Za-z0-9\s]', '', text)

# Path to the folder containing the JSON files locally
folder_path = 'C:\\Users\\user\\Documents\\dataset\\dataset\\newsdata'

# Function to extract content from all objects in each JSON file
def extract_content_and_id_from_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        try:
            data = json.load(file)
            if isinstance(data, list):
                for obj in data:
                    content_item = obj.get('content', '')
                    article_id = obj.get('id', '')
                    if content_item and article_id:
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
            # Convert the list of tokens to a string before printing
            tokenized_content_str = ', '.join(map(str, content_tokens))
            print(f"Article ID: [{article_id}], Tokenized Content: [{tokenized_content_str.encode('utf-8', 'ignore').decode('utf-8')}]")
            print("\n" * 4)