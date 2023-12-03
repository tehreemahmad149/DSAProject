from class_forwardIndex import ForwardIndex
from implementation_forwardIndex import load_config, build_forward_index
import implementation_invertedindex 

if __name__ == "__main__":

    config = load_config()
    
    # Get folder_path, output_file_path_txt, and lexicon_file_path_txt from config.json
    folder_path = config.get('folder_path', '')
    output_file_path_txt = config.get('output_file_path_txt', 'forward_index.txt')
    lexicon_file_path_txt = config.get('lexicon_file_path_txt', 'lexicon.txt')

    # Create an instance of the ForwardIndex class
    forward_index_instance = ForwardIndex()

    # Call the main building function for the forward index
    build_forward_index(folder_path, forward_index_instance)

    # Save the forward index and lexicon to TXT files
    forward_index_instance.save_forwardIndex_to_txt(output_file_path_txt)
    forward_index_instance.save_lexicon_to_txt(lexicon_file_path_txt)

    #create inverted index
    inverted_index = implementation_invertedindex.InvertedIndex()
    inverted_index.build_inverted_index(implementation_invertedindex.forward_index_file_path, implementation_invertedindex.lexicon_file_path) #add in forward index, lexicon path
    inverted_index.write_to_file(implementation_invertedindex.inverted_index_file_path) #add in inverted index path
    
    # Display success messages for all 
    print(f"Forward index saved to {output_file_path_txt}")
    print(f"Lexicon saved to {lexicon_file_path_txt}")
    print(f"Inverted index saved to {implementation_invertedindex.inverted_index_file_path}")


#Test search for inverted index
    search_keyword = 'oregonianoregonlive'  # Replace with the keyword you want to search
    result = inverted_index.search(search_keyword)
    print(f"Documents containing '{search_keyword}': {', '.join(result)}")


    exit
