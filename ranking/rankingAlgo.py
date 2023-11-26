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
    return re.sub(r'[^A-Za-z0-9\s]', '', text)

# Function to read forward_index.txt and extract document information
def read_forward_index(file_path):
    document_info = {}
    with open(file_path, 'r', encoding='utf-8') as txtfile:
        lines = txtfile.read().split('----------------------------------------\n')

        for entry in lines:
            if entry.strip():  # Skip empty entries
                # Extract document ID
                doc_id_match = re.search(r'Document ID: (.+)', entry)
                if doc_id_match:
                    doc_id = doc_id_match.group(1).strip()
                else:
                    continue

                # Extract keywords
                keywords_match = re.search(r'Keywords: (.+)', entry)
                if keywords_match:
                    keywords = keywords_match.group(1).strip().split(', ')
                    document_info[doc_id] = keywords

    return document_info


# Function to process user query
def process_user_query(query):
    tokens = [word for word in word_tokenize(query.lower()) if word.isalpha() and word not in stop_words and word not in punctuation]
    return ' '.join(map(str, tokens))

# Read document information from forward_index.txt
forward_index_path = 'forward_index.txt'
document_info = read_forward_index(forward_index_path)

# User query
user_query = "Tell me about Elizabeth Minor and the University of Tskuba."

# Process user query
user_query_tokens = process_user_query(user_query)

# Extract content and tokens from forward index
all_content_tokens = list(document_info.values())

# TF-IDF Vectorization
vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
tfidf_matrix = vectorizer.fit_transform([' '.join(map(str, tokens)) for tokens in all_content_tokens] + [user_query_tokens])

# Calculate cosine similarity
cosine_similarities = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])

# Get document ranks based on similarity
document_ranks = list(enumerate(cosine_similarities[0]))

# Sort documents by rank
sorted_documents = sorted(document_ranks, key=lambda x: x[1], reverse=True)

# Print ranked documents
print("Ranked Documents:")
for index, score in sorted_documents:
    doc_id = list(document_info.keys())[index]
    print(f"Document ID: {doc_id}, Similarity Score = {score}")
    # You can optionally print more information about the document here, e.g., content or a snippet
