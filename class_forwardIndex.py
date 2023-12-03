class ForwardIndex:
    def __init__(self):
        # Initialize attributes
        self.index = {}           # Document ID to (keywords, frequencies, positions) dictionary
        self.lexicon = {}         # Dictionary of unique keywords in the entire dataset (word -> (frequency, positions))
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

    def save_forwardIndex_to_txt(self, output_file_path):
        # Save the forward index to a TXT file
        with open(output_file_path, 'w', encoding='utf-8') as txtfile:
            for doc_id, (keywords, frequencies, positions) in self.index.items():
                # Output information directly
                txtfile.write(f"Document ID: {doc_id}\n")
                txtfile.write(f"Keywords: {keywords}")
                txtfile.write(f"Frequencies: {frequencies}")
                txtfile.write(f"Positions: {positions}\n")

    def save_lexicon_to_txt(self, lexicon_file_path):
        # Save the lexicon to a TXT file
        with open(lexicon_file_path, 'w', encoding='utf-8') as txtfile:
            txtfile.write("Word ID\tWord\n")
            for word in self.lexicon:
                word_id = self.lexicon[word]
                txtfile.write(f"{word_id}\t{word}\n")
