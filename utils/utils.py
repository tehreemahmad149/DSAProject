# utils.py
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string
import re

# Download stopwords
nltk.download('punkt')
nltk.download('stopwords')

# Define a set of stopwords and punctuation
stop_words = set(stopwords.words('english'))
punctuation = set(string.punctuation)

# Function to remove special characters using regex
def remove_special_characters(text):
    # Using regex to remove characters like \xe2\x80\x9c and @@@@@
    return re.sub(r'[^A-Za-z0-9\s]', '', text)

# Common function for content processing as a generator
def process_content_generator(content_item):
    content = content_item.lower()
    content = remove_special_characters(content)
    tokens = [word for word in word_tokenize(content) if word.isalpha() and word not in stop_words and word not in punctuation]
    return tokens

# Custom function to generate unique document IDs
def generate_unique_doc_id(file_name, obj_index):
    return f"{file_name}_{obj_index}"