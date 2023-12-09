# main.py

import numpy as np
from class_forwardIndex import ForwardIndex
from implementation_forwardIndex import load_config, build_forward_index
import implementation_invertedindex  # Corrected import

if __name__ == "__main__":
    config = load_config()

    # Get folder_path, output_file_path_txt, and lexicon_file_path_txt from config.json
    folder_path = config.get('folder_path', '')
    output_file_path_txt = config.get('output_file_path_txt', 'forward_index.txt')
    lexicon_file_path_txt = config.get('lexicon_file_path_txt', 'lexicon.txt')
    inverted_index_file_path_txt = config.get('inverted_index_file_path_txt', 'inverted_index.txt')  # Corrected path

    # Create an instance of the ForwardIndex class
    forward_index_instance = ForwardIndex()

    # Call the main building function for the forward index
    build_forward_index(folder_path, forward_index_instance)

    # Save the forward index and lexicon to TXT files
    forward_index_instance.save_forwardIndex_to_json(output_file_path_txt)
    forward_index_instance.save_lexicon_to_json(lexicon_file_path_txt)

    inverted_index = implementation_invertedindex.InvertedIndex()  # Corrected class name
    inverted_index.build_inverted_index(output_file_path_txt, lexicon_file_path_txt)
    inverted_index.save_inverted_index_to_json(inverted_index_file_path_txt)

    # Search for documents based on a query
    query = ["must", "see", "covid"]
    ranked_documents = forward_index_instance.rank_documents(query)

    # Display the ranked documents
    for doc_id, score in ranked_documents:
        print(f"Document ID: {doc_id}, Score: {score}")

    exit