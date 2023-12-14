#this file will be the main interface of the program.
#the user will search the query prompted here and then this file will trigger the ranking file and retrieve and show the relevant documents.   
from ranking import Ranking
from main import ForwardIndex, InvertedIndex
import time

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

# # Search for documents based on a query
query = ["young", "issue", "kiess"]
ranked_documents = ranking_instance.rank_documents(query)

# debugging
print("after ranking now ready to display")

# Display the ranked documents
for doc_id, score in ranked_documents:
    print(f"Document ID: {doc_id}, Score: {score}")

end = time.time()
print(end - start)