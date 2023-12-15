import json
import os
import hashlib 
from utils.utils import process_content_generator, generate_unique_doc_id

class ForwardIndex:
    def __init__(self):
        # Initialize attributes
        self.index = {}           # Document ID to (keywords, frequencies, positions, title) mapping
        self.lexicon = {}         # Set of unique keywords in the entire dataset
        self.next_word_id = 1     # Counter for generating unique word IDs
        self.total_doc_length = 0
    
    def add_document(self, doc_id, keywords, title, doc_length):
        # Use SHA-256 hashing for the document ID
        hashed_doc_id = hashlib.sha256(doc_id.encode()).hexdigest()

        # Add document to the index with associated keywords, frequencies, positions, and title
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
            # Update total_doc_length and corpus_size
            self.total_doc_length += doc_length

        # Store title information
        self.index[hashed_doc_id] = {"Keywords": keywords, "Frequencies": frequencies, "Positions": positions, "Title": title, "Doc_length": doc_length}

        # Update lexicon with the new unique words from the document, 
        # assigning Word IDs and incrementing them
        for word in set(keywords):
            if word not in self.lexicon:
                self.lexicon[word] = self.next_word_id 
                self.next_word_id += 1

    def get_total_doc_length(self):
        return self.total_doc_length

    def save_total_doc_length(self, total_doc_length_file):
        # Save total_doc_length to a JSON file
        with open(total_doc_length_file, 'w', encoding='utf-8') as json_file:
            json.dump({"total_doc_length": self.total_doc_length}, json_file, indent=2)
    
    def load_total_doc_length(self, total_doc_length_file):
        # Load total_doc_length from a JSON file
        try:
            with open(total_doc_length_file, 'r', encoding='utf-8') as json_file:
                data = json.load(json_file)
                self.total_doc_length = data.get("total_doc_length", 0)
        except FileNotFoundError:
            # Handle the case where the file doesn't exist
            print(f"File not found: {total_doc_length_file}")
        except json.JSONDecodeError as error:
            # Handle JSON decoding errors
            print(f"Error decoding JSON in file {total_doc_length_file}: {error}")

    def get_info_for_document(self, doc_id):
        # Return all information (keywords, frequencies, positions, title) associated with a specific document ID
        return self.index.get(doc_id, {"Keywords": [], "Frequencies": {}, "Positions": {}, "Title": [], "Doc_length": 0})

    def get_lexicon(self):
        # Return the lexicon dictionary
        return self.lexicon

    def get_word_id(self, word):
        # Return the word ID for a given keyword
        return self.lexicon.get(word, None)

    def get_all_document_ids(self):
        # Return a list of all document IDs
        return list(self.index.keys())

    def save_forwardIndex_to_json(self, output_file_path):
        # Save the forward index to a JSON file
        with open(output_file_path, 'w', encoding='utf-8') as json_file:
            json.dump(self.index, json_file, indent=2)

    def save_lexicon_to_json(self, lexicon_file_path):
        # Save the lexicon to a TXT file
        with open(lexicon_file_path, 'w', encoding='utf-8') as json_file:
            lexicon_list = []
            for word, word_id in self.lexicon.items():
                data = {"Word ID": word_id, "Word": word}
                lexicon_list.append(data)
                
            with open(lexicon_file_path, 'w', encoding='utf-8') as json_file:
                json.dump(lexicon_list, json_file, indent=2)
    
    def get_document_frequency(self, term):
        # Count the number of documents containing the given term
        return sum(1 for doc_id, info in self.index.items() if term in info["Keywords"])

    def load_from_json(self, file_path):
        with open(file_path, 'r') as file:
            self.index = json.load(file)


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
                        forward_index.add_document(article_id, tokens, tokenized_title, doc_length)  # Update this line
    except json.JSONDecodeError as error:
        print(f"Error decoding JSON in file {file_path}: {error}")
    except Exception as e:
        print(f"An unexpected error occurred in file {file_path}: {e}")