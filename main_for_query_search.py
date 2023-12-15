#this file will be the main interface of the program.
#the user will search the query prompted here and then this file will trigger the ranking file and retrieve and show the relevant documents.   
from ranking import Ranking
from main import ForwardIndex, InvertedIndex
import time
from utils.utils import process_content_generator

#start time measurement
start = time.time()

# Create instances of ForwardIndex and InvertedIndex
forward_index_instance = ForwardIndex()
inverted_index_instance = InvertedIndex()

# Load data from JSON files
forward_index_instance.load_from_json('FI.json')
inverted_index_instance.load_from_json('II.json')

# Create an instance of the Ranking class
ranking_instance = Ranking(forward_index_instance, inverted_index_instance)

user_input = input("Enter a sentence: ")
print("You entered:", user_input)

query = process_content_generator(user_input)
ranked_documents = ranking_instance.rank_documents(query)

# # Display the ranked documents
# for doc_id, score in ranked_documents:
#     print(f"Document ID: {doc_id}, Score: {score}")

end = time.time()
print(f"time to rank and return the relevant documents: {end - start}")