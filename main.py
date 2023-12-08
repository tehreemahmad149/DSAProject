from class_forwardIndex import ForwardIndex
from implementation_forwardIndex import load_config, build_forward_index
import implementation_invertedindex

if __name__ == "__main__":

    config = load_config()
    
    # Get folder_path, output_file_path_txt, and lexicon_file_path_txt from config.json
    folder_path = config.get('folder_path', '')
    output_file_path_txt = config.get('output_file_path_txt', 'forward_index.txt')
    lexicon_file_path_txt = config.get('lexicon_file_path_txt', 'lexicon.txt')
    inverted_index_file_path_txt = config.get('inverted_index_file_path_txt', 'lexicon.txt')

    # Create an instance of the ForwardIndex class
    forward_index_instance = ForwardIndex()

    # Call the main building function for the forward index
    build_forward_index(folder_path, forward_index_instance)

    # Save the forward index and lexicon to TXT files
    forward_index_instance.save_forwardIndex_to_json(output_file_path_txt)
    forward_index_instance.save_lexicon_to_json(lexicon_file_path_txt)
    
    inverted_index = implementation_invertedindex.InvertedIndex()
    inverted_index.build_inverted_index(output_file_path_txt, lexicon_file_path_txt)
    inverted_index.save_inverted_index_to_json(inverted_index_file_path_txt)

    
    # Display success messages for all 
    print(f"Forward index saved to {output_file_path_txt}")
    print(f"Lexicon saved to {lexicon_file_path_txt}")
    print(f"Inverted index saved to {inverted_index_file_path_txt}")
    search_keyword = "captivating"
    result = inverted_index.search_inverted_index(search_keyword)
    print(f"Documents containing '{search_keyword}': {result}")


    exit
