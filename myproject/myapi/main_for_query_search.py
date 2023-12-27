#this file will be the main interface of the program.
#the user will search the query prompted here and then this file will trigger the ranking file and retrieve and show the relevant documents.   
import sys
from pathlib import Path
project_root = str(Path(__file__).resolve().parent.parent)  # Adjust the parent count based on your project structure
sys.path.append(project_root)

from myapi.ranking import Ranking
from myapi.main import ForwardIndex, InvertedIndex
import time
from myapi.utils.utils import process_content_generator
from myapi.barrels import get_barrel_for_word_id
from myapi.extract_guiData import load_metadata, display_metadata
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

# Prompt the user for a search query
user_query = input("Enter your search query: ")

#start time measurement
start = time.time()

# Tokenize the user's query using the same process as document tokenization
tokenized_query = process_content_generator(user_query)

# Search for documents based on the user's query
ranked_documents = ranking_instance.rank_documents(tokenized_query)

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