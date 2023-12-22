
'''class InvertedIndex:
    def __init__(self):
        self.index = {}
    
    def read_lexicon(self,file_path):
        lexicon_words = set()
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                for item in enumerate(data):
                    lexicon_words =  item.get('Word', '')
        except json.JSONDecodeError as error:
            print(f"Error decoding JSON in file {file_path}: {error}")
            
        except Exception as e:
            print(f"An unexpected error occurred in file {file_path}: {error}")
            
        return lexicon_words
    

    def add_entry(self, keyword, doc_id):
        if keyword not in self.index:
            self.index[keyword] = [] #empty list for that keyword
        if doc_id not in self.index[keyword]:
            self.index[keyword].append(doc_id)

    def build_inverted_index(self, output_file_path, lexicon_path):
        # Read lexicon file
        lexicon_words = self.read_lexicon(lexicon_path)

        # Read forward index file
        with open(output_file_path, 'r') as file:
            lines = file.readlines()

        current_doc_id = None
        current_keywords = []

        for line in lines:
            if line.startswith('Document ID:'):
                current_doc_id = line.split(':')[-1].strip()
            elif line.startswith('Keywords:'):
                current_keywords = [kw.strip() for kw in line.split(':')[-1].split(',')]
                for keyword in current_keywords:
                    if keyword in lexicon_words:
                        self.add_entry(keyword, current_doc_id)
                       
    def write_to_file(self, inverted_index_file_path):
        with open(inverted_index_file_path, 'w') as file:
            for keyword, doc_ids in self.index.items():
                file.write(f"{keyword}: {', '.join(doc_ids)}\n")

    def search(self, keyword):
        return self.index.get(keyword, [])'''
        
'''import json
import os

class InvertedIndex:
    def __init__(self):
        self.index = {}

    def read_lexicon(self, file_path):
        lexicon_words = set()
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                for item in data:
                    lexicon_words.add(item.get('Word', ''))
        except json.JSONDecodeError as error:
            print(f"Error decoding JSON in file {file_path}: {error}")
        except Exception as e:
            print(f"An unexpected error occurred in file {file_path}: {error}")
        print(lexicon_words)
        return lexicon_words

    def read_forward_index(self, file_path):
        forward_index = {}
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                for item in data:
                    doc_id = item.get('Document ID', '')
                    keywords = item.get('Keywords', '').split(', ')
                    forward_index[doc_id] = keywords
        except json.JSONDecodeError as error:
            print(f"Error decoding JSON in file {file_path}: {error}")
        except Exception as e:
            print(f"An unexpected error occurred in file {file_path}: {e}")
        return forward_index


    def add_entry(self, keyword, doc_id):
        if keyword not in self.index:
            self.index[keyword] = []  # empty list for that keyword
        if doc_id not in self.index[keyword]:
            self.index[keyword].append(doc_id)

    def build_inverted_index(self, forward_index_file, lexicon_file):
        # Read lexicon file
        lexicon_words = self.read_lexicon(lexicon_file)

        # Read forward index file
        forward_index = self.read_forward_index(forward_index_file)

        # Build inverted index
        for doc_id, keywords in forward_index.items():
            for keyword in keywords:
                if keyword in lexicon_words:
                    self.add_entry(keyword, doc_id)

    def write_to_file(self, inverted_index_file_path):
        with open(inverted_index_file_path, 'w', encoding='utf-8') as file:
            json.dump(self.index, file, indent=2)

    def search(self, keyword):
        return self.index.get(keyword, [])'''

'''class InvertedIndex:
    def __init__(self):
        self.index = {}

    def read_lexicon(self, file_path):
        lexicon_words = set()
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                for item in data:
                    lexicon_words.add(item.get('Word', ''))
        except json.JSONDecodeError as error:
            print(f"Error decoding JSON in file {file_path}: {error}")
        except Exception as e:
            print(f"An unexpected error occurred in file {file_path}: {e}")
        return lexicon_words

    def read_forward_index(self, file_path):
        forward_index = {}
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                for item in data:
                    doc_id = item.get('Document ID', '')
                    keywords = item.get('Keywords', '').split(', ')
                    forward_index[doc_id] = keywords
        except json.JSONDecodeError as error:
            print(f"Error decoding JSON in file {file_path}: {error}")
        except Exception as e:
            print(f"An unexpected error occurred in file {file_path}: {e}")
        return forward_index

    def add_entry(self, keyword, doc_id):
        if keyword not in self.index:
            self.index[keyword] = []  # empty list for that keyword
        if doc_id not in self.index[keyword]:
            self.index[keyword].append(doc_id)

    def build_inverted_index(self, forward_index_file, lexicon_file):
        # Read lexicon file
        lexicon_words = self.read_lexicon(lexicon_file)

        # Read forward index file
        forward_index = self.read_forward_index(forward_index_file)

        # Build inverted index
        for doc_id, keywords in forward_index.items():
            for keyword in keywords:
                if keyword in lexicon_words:
                    self.add_entry(keyword, doc_id)

    def write_to_file(self, inverted_index_file_path):
        inverted_index_list = [{'keyword': keyword, 'doc_ids': doc_ids} for keyword, doc_ids in self.index.items()]
        with open(inverted_index_file_path, 'w', encoding='utf-8') as file:
            json.dump(inverted_index_list, file, indent=2)


    def search(self, keyword):
        return self.index.get(keyword, [])'''
        
        
import json
import os
import re
from class_forwardIndex import ForwardIndex


class InvertedIndex:
    def __init__(self):
        # Initialize the inverted index as a dictionary with keywords mapping to document IDs
        self.index = {}

    def build_inverted_index(self, forward_index_path, lexicon_path):
        # Read forward index and lexicon from JSON files
        with open(forward_index_path, 'r', encoding='utf-8') as forward_file:
            forward_index = json.load(forward_file)

        with open(lexicon_path, 'r', encoding='utf-8') as lexicon_file:
            lexicon = json.load(lexicon_file)

        # Iterate through the lexicon to build the inverted index
        for word_info in lexicon:
            word_id = word_info["Word ID"]
            word = word_info['Word']
            # Initialize the inverted index entry for the current keyword
            self.index[word] = {"Word ID": word_id, "Document IDs": []}

            # Iterate through the forward index to find documents containing the current keyword
            for data in forward_index:
                keywords = data['Keywords']
                doc_id = data['Document ID']
                if word in keywords:
                    self.index[word]["Document IDs"].append(doc_id)

    def save_inverted_index_to_json(self, output_file_path):
        # Save the inverted index to a JSON file
        with open(output_file_path, 'w', encoding='utf-8') as json_file:
            json.dump(self.index, json_file, indent=1)

    def search_inverted_index(self, keyword):
        # Search the inverted index for a keyword and return the list of document IDs
        return self.index.get(keyword, {}).get("Document IDs", [])


<<<<<<< Updated upstream
=======
        for keyword in keywords:
            # Determine the relevant barrel for the word ID
            print(keyword)
            word_id = self.get_word_id(keyword)
            print(word_id)
            barrel_path = get_barrel_for_word_id(word_id)
            completed_barrel_path = f"C:\\DSAProject\\barrel_created\\{barrel_path}.json"
            # Load the inverted index from the relevant barrel
            print(completed_barrel_path)
            inverted_index = self.load_inverted_index_from_barrel(completed_barrel_path)
            # print(self.index)
            unique_hashed_document_ids.update(self.index.get(keyword, {}).get("Document IDs", []))
        return list(unique_hashed_document_ids)
>>>>>>> Stashed changes

 

