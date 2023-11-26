import sys
sys.path.append('C:\\Users\\user\\Documents\\GitHub\\DSAProject')
import json
import os
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from forwardIndex import ForwardIndex
from utils.utils import process_content_generator, generate_unique_doc_id

# Downloading stopwords
nltk.download('punkt')
nltk.download('stopwords')

# Define a set of stopwords and punctuation
stop_words = set(stopwords.words('english'))
punctuation = set(string.punctuation)

# Function to remove special characters using regex
def remove_special_characters(text):
    # Use regex to remove characters like \xe2\x80\x9c and @@@@@
    cleaned_text = re.sub(r'[^A-Za-z0-9\s]', '', text)
    return cleaned_text

# Read forward_index.txt and extract document information
def read_forward_index(file_path):
    document_info = {}
    with open(file_path, 'r', encoding='utf-8') as txtfile:
        lines = txtfile.readlines()
        # Skip the header
        lines = lines[1:]
        for i in range(0, len(lines), 5):
            if i + 1 < len(lines):
                doc_id_line = lines[i]
                keywords_line = lines[i + 1]

                # Extract document ID
                doc_id_parts = doc_id_line.split(":")
                if len(doc_id_parts) > 1:
                    doc_id = doc_id_parts[1].strip()
                else:
                    continue

                # Extract keywords
                keywords_parts = keywords_line.split(":")
                if len(keywords_parts) > 1:
                    keywords = keywords_parts[1].strip().split(', ')
                    document_info[doc_id] = keywords
    return document_info

# Path to the forward_index.txt file
forward_index_path = 'forward_index.txt'

# Read document information from forward_index.txt
document_info = read_forward_index(forward_index_path)

# User query
user_query = "Tell me about narrow prosecution."

# Process user query
user_query_tokens = [word for word in word_tokenize(user_query.lower()) if word.isalpha() and word not in stop_words and word not in punctuation]

# Convert user query tokens to a string before printing
user_query_str = ', '.join(map(str, user_query_tokens))
print(f"User Query: [{user_query_str}]")

# Extract content and tokens from forward index
all_content_tokens = list(document_info.values())

# TF-IDF Vectorization
vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
tfidf_matrix = vectorizer.fit_transform([' '.join(map(str, tokens)) for tokens in all_content_tokens])

# TF-IDF Vectorization for the user query
query_vector = vectorizer.transform([' '.join(map(str, user_query_tokens))])

# Calculate cosine similarity
cosine_similarities = cosine_similarity(query_vector, tfidf_matrix)

# Get document ranks based on similarity
document_ranks = list(enumerate(cosine_similarities[0]))

# Sort documents by rank
sorted_documents = sorted(document_ranks, key=lambda x: x[1], reverse=True)

# Print ranked documents
print("Ranked Documents:")
for index, score in sorted_documents:
    doc_id = list(document_info.keys())[index]
    print(f"Document ID: {doc_id}, Similarity Score = {score}")