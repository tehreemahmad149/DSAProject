from class_forwardIndex import ForwardIndex
from implementation_forwardIndex import load_config, build_forward_index

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

    # Display success messages once done and exit
    print(f"Forward index saved to forward_index.txt")
    print(f"Lexicon saved to lexicon.txt")
    exit()