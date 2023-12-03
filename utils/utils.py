import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string
import re

# Using NLTK for tokenization and stopwords
nltk.download('punkt')
nltk.download('stopwords')

# Define a set of stopwords and punctuation for text processing
stop_words = set(stopwords.words('english'))
punctuation = set(string.punctuation)

# Function to remove special characters from text using regular expressions
def remove_special_characters(text):
    return re.sub(r'[^A-Za-z0-9\s]', '', text)

# Combined Function for content processing as a generator
def process_content_generator(content):
    # Convert text to lowercase and remove special characters
    content = content.lower()
    content = remove_special_characters(content)

    # Tokenize the content and filter out stopwords and punctuation
    tokens = [word for word in word_tokenize(content) if word.isalpha() and word not in stop_words and word not in punctuation]
    return tokens

# Function to generate unique document IDs based on json file name and object index
def generate_unique_doc_id(file_name, obj_index):
    return f"{file_name}_{obj_index}"