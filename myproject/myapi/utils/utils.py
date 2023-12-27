import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import string
import re
from spellchecker import SpellChecker

# Using NLTK for tokenization, stopwords
nltk.download('punkt')
nltk.download('stopwords')

# Define a set of stopwords and punctuation for text processing
stop_words = set(stopwords.words('english'))
punctuation = set(string.punctuation)

# Initialize the Porter Stemmer and SpellChecker
stemmer = PorterStemmer()
spell = SpellChecker()

# Function to remove special characters from text using regular expressions
def remove_special_characters(text):
    return re.sub(r'[^A-Za-z0-9\s]', '', text)

def process_content_generator(content):
    print("Processing content...")
    # Check if content is None or empty
    if content is None or not content.strip():
        print("Content is None or empty.")
        return []

    # Convert text to lowercase and remove special characters
    content = content.lower()
    content = remove_special_characters(content)

    # Tokenize the content
    tokens = word_tokenize(content)

    # Filter out stopwords, punctuation, and stem based on spell-checked words
    meaningful_tokens = []
    for word in tokens:
        if word.isalpha() and word not in stop_words and word not in punctuation:
            corrected_word = spell.correction(word)
            if corrected_word is not None:
                stemmed_word = stemmer.stem(corrected_word)
                meaningful_tokens.append(stemmed_word)

    print("Processed tokens:", meaningful_tokens)
    return meaningful_tokens

# Function to generate unique document IDs based on json file name and object index
def generate_unique_doc_id(file_name, obj_index):
    return f"{file_name}_{obj_index}"