# main.py

from class_forwardIndex import ForwardIndex
from class_invertedIndex import InvertedIndex
from ranking import Ranking
from implementation_forwardIndex import load_config, build_forward_index

if __name__ == "__main__":
    config = load_config()

    # Get folder_path, output_file_path_txt, lexicon_file_path_txt, and inverted_index_file_path_txt from config.json
    folder_path = config.get('folder_path', '')
    output_file_path_txt = config.get('output_file_path_txt', 'forward_index.txt')
    lexicon_file_path_txt = config.get('lexicon_file_path_txt', 'lexicon.txt')
    inverted_index_file_path_txt = config.get('inverted_index_file_path_txt', 'inverted_index.txt')

    # Create an instance of the ForwardIndex class
    forward_index_instance = ForwardIndex()

    # Call the main building function for the forward index
    build_forward_index(folder_path, forward_index_instance)

    # Save the forward index and lexicon to TXT files
    forward_index_instance.save_forwardIndex_to_json(output_file_path_txt)
    forward_index_instance.save_lexicon_to_json(lexicon_file_path_txt)

    # Create an instance of the InvertedIndex class
    inverted_index_instance = InvertedIndex()

    # Build inverted index
    inverted_index_instance.build_inverted_index(output_file_path_txt, lexicon_file_path_txt)
    inverted_index_instance.save_inverted_index_to_json(inverted_index_file_path_txt)

    # Create an instance of the Ranking class
    ranking_instance = Ranking(forward_index_instance, inverted_index_instance)

    # Search for documents based on a query
    query = ["lucifer", "darkness"]
    ranked_documents = ranking_instance.rank_documents(query)

    # Display the ranked documents
    for doc_id, score in ranked_documents:
        print(f"Document ID: {doc_id}, Score: {score}")

    exit()