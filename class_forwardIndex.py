import json
import os
import re

class ForwardIndex:
    def __init__(self):
        # Initialize attributes
        self.index = {}           # Document ID to (keywords, frequencies, positions, title) mapping
        self.lexicon = {}         # Set of unique keywords in the entire dataset
        self.next_word_id = 1     # Counter for generating unique word IDs
    
    def add_document(self, doc_id, keywords, title):
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

    # Store title information
        self.index[doc_id] = (keywords, frequencies, positions, title)

    # Update lexicon with the new unique words from the document, 
    # assigning Word IDs and incrementing them
        for word in set(keywords):
            if word not in self.lexicon:
                self.lexicon[word] = (self.next_word_id) 
                self.next_word_id += 1

    def get_info_for_document(self, doc_id):
    # Return all information (keywords, frequencies, positions, title) associated with a specific document ID
        return self.index.get(doc_id, ((), {}, {}, ""))

    def get_original_document_id(self, ranked_document_id):
        # Retrieving original document ID based on ranking (not yet implemented)
        pass

    def get_lexicon(self):
        # Return the lexicon dictionary
        return self.lexicon

    def get_word_id(self, word):
        # Return the word ID for a given keyword
        return self.lexicon.get(word, (None, None))[0]
    

    def get_all_document_ids(self):
        # Replace this placeholder with the actual method or attribute
        # that returns a list of all document IDs
        return list(self.index.keys())


    def save_forwardIndex_to_json(self, output_file_path):
    # Save the forward index to a TXT file
        with open(output_file_path, 'w', encoding='utf-8') as json_file:
            data_list = []
            for doc_id, (keywords, frequencies, positions, title) in self.index.items():
            # Converting keywords to string
                keyword_str = ', '.join(map(str, keywords))
                frequencies_str = list(map(str, frequencies))
                positions_str = list(map(str, positions))
                data = {"Document ID": doc_id, "Keywords": keyword_str, "Frequencies": frequencies, "Positions": positions, "Title": title}  # Include the Title field
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

    def rank_documents(self, query):
        # Use the ranking functions from the separate file
        from ranking import Ranking

        # Call the ranking function with the forward index instance and the query
        return Ranking.rank_documents(self, query)
    
    def get_document_frequency(self, term):
    # Count the number of documents containing the given term
        return sum(1 for doc_id, (keywords, _, _, _) in self.index.items() if term in keywords)