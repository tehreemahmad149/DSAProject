# Import necessary modules
from ranking import Ranking
from main import ForwardIndex, InvertedIndex
from utils.utils import process_content_generator

import time

# Start time measurement
start = time.time()

# Create instances of ForwardIndex and InvertedIndex
forward_index_instance = ForwardIndex()
inverted_index_instance = InvertedIndex()

# Load data from JSON files
forward_index_instance.load_from_json('FI.json')
inverted_index_instance.load_from_json('II.json')

# Create an instance of the Ranking class
ranking_instance = Ranking(forward_index_instance, inverted_index_instance)

# Prompt the user for a search query
user_query = input("Enter your search query: ")

# Tokenize the user's query using the same process as document tokenization
tokenized_query = process_content_generator(user_query)

# Search for documents based on the user's query
ranked_documents = ranking_instance.rank_documents(tokenized_query)

# Display the ranked documents
print("After ranking, ready to display:")
for doc_id, score in ranked_documents:
    print(f"Document ID: {doc_id}, Score: {score}")

# End time measurement
end = time.time()
print("Time taken:", end - start)
