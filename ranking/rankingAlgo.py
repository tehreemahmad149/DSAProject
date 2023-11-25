import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string
import re
import json
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

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

# Path provided to the folder containing the JSON files locally
folder_path = 'testdataForRanking/testfolder/'

# Function to extract content from all the objects in every JSON file
def extract_content_from_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        try:
            data = json.load(file)
            # Extracting "content" field
            if isinstance(data, list):
                for obj in data:
                    content_item = obj.get('content', '')
                    if content_item:
                        # Lowercasing the parsed content
                        content = content_item.lower()

                        # Remove special characters
                        content = remove_special_characters(content)

                        yield content
            else:
                print(f"No content found in file {file_path}")
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON in file {file_path}: {e}")

# Collect content from all files
all_content = []
for filename in os.listdir(folder_path):
    file_path = os.path.join(folder_path, filename)
    if os.path.isfile(file_path) and filename.endswith('.json'):
        all_content.extend(list(extract_content_from_json(file_path)))

# User query
user_query = "Tell me about narrow prosecution."

# TF-IDF Vectorization
vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
tfidf_matrix = vectorizer.fit_transform(all_content)

# TF-IDF Vectorization for the user query
query_vector = vectorizer.transform([user_query])

# Calculate cosine similarity
cosine_similarities = cosine_similarity(query_vector, tfidf_matrix)

# Get document ranks based on similarity
document_ranks = list(enumerate(cosine_similarities[0]))

# Sort documents by rank
sorted_documents = sorted(document_ranks, key=lambda x: x[1], reverse=True)

# Print ranked documents
print("Ranked Documents:")
for index, score in sorted_documents:
    print(f"Document {index + 1}: Similarity Score = {score}")
