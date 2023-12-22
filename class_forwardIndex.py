import json
import os
import re

class ForwardIndex:
    def __init__(self):
        # Initialize attributes
        self.index = {}           # Document ID to (keywords, frequencies, positions) mapping
        self.lexicon = {}     # Set of unique keywords in the entire dataset
        self.next_word_id = 1     # Counter for generating unique word IDs
    
    def add_document(self, doc_id, keywords):
        # Add document to the index with associated keywords, frequencies, and positions
        frequencies = {}  # Define frequency dictionary
        positions = {}    # Define positions dictionary
        # Add frequencies and positions for each keyword
        for position, word in enumerate(keywords):
            if word not in frequencies:
                frequencies[word] = 1
                positions[word] = [position]
            else:
                frequencies[word] += 1
                positions[word].append(position)

        self.index[doc_id] = (keywords, frequencies, positions)

        # Update lexicon with the new unique words from the document, 
        # assigning Word IDs and incrementing them
        for word in set(keywords):
            if word not in self.lexicon:
                self.lexicon[word] = (self.next_word_id) 
                self.next_word_id += 1
        print("add doc call finished\n")

    def get_info_for_document(self, doc_id):
        # Return all information (keywords, frequencies, positions) 
        # associated with a specific document ID
        return self.index.get(doc_id, ((), {}, {}))

    def get_original_document_id(self, ranked_document_id):
        # Retrieving original document ID based on ranking (not yet implemented)
        pass

    def get_lexicon(self):
        # Return the lexicon dictionary
        return self.lexicon

    def get_word_id(self, word):
        # Return the word ID for a given keyword
        return self.lexicon.get(word, (None, None))[0]


    def save_forwardIndex_to_json(self, output_file_path):
        # Save the forward index to a TXT file
        with open(output_file_path, 'w', encoding='utf-8') as json_file:
            data_list = []
            for doc_id, (keywords, frequencies, positions) in self.index.items():
                # Converting keywords to string
                keyword_str = ', '.join(map(str, keywords))
                frequencies_str = list(map(str, frequencies))
                positions_str = list(map(str, positions))
                data = {"Document ID": doc_id, "Keywords": keyword_str, "Frequencies": frequencies_str, "Positions": positions_str}
                data_list.append(data)
            json.dump(data_list, json_file, indent=2)


    def save_lexicon_to_json(self, lexicon_file_path):
        # Save the lexicon to a TXT file
        with open(lexicon_file_path, 'w', encoding='utf-8') as json_file:
            lexicon_list = []
            for word, word_id in self.lexicon.items():
                data = {"Word ID": word_id, "Word": word}
                lexicon_list.append(data)
                
            with open(lexicon_file_path, 'w', encoding='utf-8') as json_file:
                json.dump(lexicon_list, json_file, indent=2)


<<<<<<< Updated upstream
=======

def load_config(config_path='config.json'):
# Load configuration from config.json
    if os.path.exists(config_path):
        with open(config_path, 'r') as config_file:
            return json.load(config_file)
    # Throw error otherwise
    else:
    # Throw error otherwise
        print(f"Config file {config_path} not found. Using default configuration.")
        return {}
        
def build_forward_index(folder_path, forward_index):
    # Build the forward index by processing JSON files in the specified folder and getting content
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path) and filename.endswith('.json'):
            print("build forward call finished\n")
            extract_content_and_id_from_json(file_path, forward_index)
            

def extract_content_and_id_from_json(file_path, forward_index):
    # Extract content and document ID from each object in a JSON file and add the document to the forward index
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            if isinstance(data, list):
                for obj_index, obj in enumerate(data):
                    # Get content and title
                    content_item = obj.get('content', '')
                    # creating Document length, for debugging purpose
                    doc_length = len(content_item)
                    title = obj.get('title', '')  # Add this line to extract the title
                    if content_item:
                        # Generate a unique document ID based on the file name and object index
                        file_name = os.path.splitext(os.path.basename(file_path))[0]
                        article_id = generate_unique_doc_id(file_name, obj_index)
                        # Process the content and add the document to the forward index
                        tokens = process_content_generator(content_item)
                        tokenized_title = process_content_generator(title)
                        print("extract data call finished\n")
                        forward_index.add_document(article_id, tokens, tokenized_title, doc_length)  # Update this line
    except json.JSONDecodeError as error:
        print(f"Error decoding JSON in file {file_path}: {error}")
    except Exception as e:
        print(f"An unexpected error occurred in file {file_path}: {e}")
>>>>>>> Stashed changes
