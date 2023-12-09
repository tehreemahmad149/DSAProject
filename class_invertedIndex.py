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



 

