#this file will be the main interface of the program.
#the user will search the query prompted here and then this file will trigger the ranking file and retrieve and show the relevant documents.   
from ranking import Ranking
from main import ForwardIndex, InvertedIndex
import time
from utils.utils import process_content_generator
from barrels import get_barrel_for_word_id
from extract_guiData import load_metadata, display_metadata
import sys

# Create instances of ForwardIndex and InvertedIndex
forward_index_instance = ForwardIndex()
inverted_index_instance = InvertedIndex()

# Load data from JSON files
forward_index_instance.load_from_json('FI.json')
forward_index_instance.load_lexicon_from_file('Lexi.json')
loaded_metadata = load_metadata("metadata.json")

# Create an instance of the Ranking class
ranking_instance = Ranking(forward_index_instance, inverted_index_instance)

user_input = input("Enter a sentence: ")
print("You entered:", user_input)

#start time measurement
start = time.time()

query = process_content_generator(user_input)

#getting the relevant documents
ranked_documents = ranking_instance.rank_documents(query)

#getting the doc_ids to display the metadata
doc_ids_to_display = []
for doc_id, score in ranked_documents:
    doc_ids_to_display.append(doc_id)

# Display the ranked documents
if loaded_metadata:
    display_metadata(loaded_metadata, doc_ids_to_display)
    for doc_id, score in ranked_documents:
        print(f"Document ID: {doc_id}, Score: {score}")

end = time.time()
print(f"time to rank and return the relevant documents: {end - start}")