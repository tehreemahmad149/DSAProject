import os

from class_forwardIndex import ForwardIndex
from implementation_forwardIndex import load_config, build_forward_index

if __name__ == "__main__":
    # Load configuration settings from config.json or use default values
    config = load_config()
    
    # Extract folder_path, output_file_path_txt, and lexicon_file_path_txt from the configuration
    folder_path = config.get('folder_path', '')
    output_file_path_txt = config.get('output_file_path_txt', 'forward_index.txt')
    lexicon_file_path_txt = config.get('lexicon_file_path_txt', 'lexicon.txt')

    # Create an instance of the ForwardIndex class
    forward_index_instance = ForwardIndex()

    # Build the forward index by processing JSON files in the specified folder
    build_forward_index(folder_path, forward_index_instance)

    # Write the lexicon to a TXT file
    forward_index_instance.save_lexicon_to_txt(lexicon_file_path_txt)

    # Create a folder to store the split text files
    output_folder_path = "output_txt_files"
    os.makedirs(output_folder_path, exist_ok=True)

    # Write the forward index to multiple text files
    forward_index_instance.save_forwardIndex_to_txt(output_folder_path)

    # Display success message
    print(f"Forward index saved to {output_folder_path}/")
    exit()
