import json
import os
import re
from class_forwardIndex import ForwardIndex
from barrels import get_barrel_for_word_id


class InvertedIndex:
    def __init__(self, lexicon_path=None):
        # Initialize the inverted index as a dictionary with keywords mapping to document IDs
        self.index = {}
        if lexicon_path:
            self.load_lexicon(lexicon_path)

    # These below 2 functions are for creating the inverted index but the rest are for search and modification purposes
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
            for hashed_doc_id, doc_info in forward_index.items():
                keywords = doc_info['Keywords']
                if word in keywords:
                    self.index[word]["Document IDs"].append(hashed_doc_id)

    def save_inverted_index_to_json(self, output_file_path):
        # Save the inverted index to a JSON file
        with open(output_file_path, 'w', encoding='utf-8') as json_file:
            json.dump(self.index, json_file, indent=1)

    # old function
    # def search_inverted_index(self, keywords):
    #     # Search the inverted index for keywords and return the list of document IDs
    #     document_ids = []
    #     for keyword in keywords:
    #         # document_ids.append(self.index[keyword])
    #         # print(document_ids)
    #         document_ids.extend(self.index.get(keyword, {}).get("Document IDs", []))
    #     return document_ids

    def search_inverted_index(self, keywords):
        # Search the inverted index for keywords and return the list of unique document IDs
        unique_hashed_document_ids = set()

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

    def load_inverted_index_from_barrel(self, barrel_path):
        with open(barrel_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

            # Update the index with the loaded data
            for word, word_data in data.items():
                if word not in self.index:
                    self.index[word] = {"Word ID": word_data["Word ID"], "Document IDs": set()}
                self.index[word]["Document IDs"].update(word_data["Document IDs"])

    def get_word_id(self, word):
        # Return the word ID for a given keyword
        return self.index.get(word, {}).get("Word ID", None)

    def sort_inverted_index(self, file_path):

        with open(file_path, 'r', encoding='utf-8') as file:
                    inverted_index = json.load(file)
                    sorted_inverted_index = {keyword: inverted_index[keyword] for keyword in sorted(inverted_index)}

        with open(file_path, 'w', encoding='utf-8') as file:
                json.dump(sorted_inverted_index, file, indent=2)
    
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

    # def load_inverted_index_from_barrel(self, completed_barrel_path):
    #     with open(completed_barrel_path, 'r', encoding='utf-8') as file:
    #         data = json.load(file)

    #     # Update the index with the loaded data
    #     for word, word_data in data.items():
    #         if word not in self.index:
    #             self.index[word] = {"Word ID": word_data["Word ID"], "Document IDs": []}
    #         self.index[word]["Document IDs"].extend(word_data["Document IDs"])

    # this may become irrelevant if "load_inverted_index_from_barrel" is implemented successfully
    # def load_from_json(self, file_path):
    #     with open(file_path, 'r') as file:
    #         data = json.load(file)

    #     # Update the index with the loaded data
    #         for word, word_data in data.items():
    #             if word not in self.index:
    #                 self.index[word] = {"Word ID": word_data["Word ID"], "Document IDs": []}
    #             self.index[word]["Document IDs"].extend(word_data["Document IDs"])