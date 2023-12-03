class ForwardIndex:
    def __init__(self):
        # Initialize attributes
        self.index = {}           # Document ID to (keywords, frequencies, positions) mapping
        self.lexicon = set()      # Set of unique keywords in the entire dataset
        self.word_id_mapping = {}  # Mapping of keywords to their corresponding word IDs
        self.next_word_id = 1     # Counter for generating unique word IDs

    def add_document(self, doc_id, keywords):
        # Add document to the index with associated keywords, frequencies, and positions
        frequencies = {}
        positions = {}
        for position, word in enumerate(keywords):
            if word not in frequencies:
                frequencies[word] = 1
                positions[word] = [position]
            else:
                frequencies[word] += 1
                positions[word].append(position)

        self.index[doc_id] = (keywords, frequencies, positions)

        # Update lexicon with new unique words from the document
        new_words = set(keywords) - self.lexicon
        self.lexicon.update(new_words)

        # Assign word IDs to new words in the document and update word_id_mapping
        for word in new_words:
            self.word_id_mapping[word] = self.next_word_id
            self.next_word_id += 1

    def get_info_for_document(self, doc_id):
        # Return (keywords, frequencies, positions) associated with a specific document ID
        return self.index.get(doc_id, ((), {}, {}))

    def get_original_document_id(self, ranked_document_id):
        # Function for retrieving original document ID based on ranking (not yet implemented)
        pass

    def get_lexicon(self):
        # Return the lexicon
        return list(self.lexicon)

    def get_word_id(self, word):
        # Return the word ID for a given keyword
        return self.word_id_mapping.get(word, None)

    def get_word_id_mapping(self):
        # Return the entire word_id_mapping
        return self.word_id_mapping

    def save_forwardIndex_to_txt(self, output_folder_path):
        # Save the forward index to multiple text files based on the starting character of document IDs
        file_paths = {}

        for doc_id, (keywords, frequencies, positions) in self.index.items():
            # Determine the file path based on the starting character of the doc_id
            start_char = doc_id[0].lower() if doc_id else 'other'
            file_path = file_paths.get(start_char, f"{output_folder_path}/forward_index_{start_char}.txt")

            with open(file_path, 'a', encoding='utf-8') as txtfile:
                keyword_str = ', '.join(map(str, keywords))
                txtfile.write(f"Document ID: {doc_id}\n")
                txtfile.write(f"Keywords: {keyword_str}\n")
                txtfile.write(f"Frequencies: {frequencies}\n")
                txtfile.write(f"Positions: {positions}\n\n")

            file_paths[start_char] = file_path

    def save_lexicon_to_txt(self, lexicon_file_path):
        # Save the lexicon to a TXT file
        with open(lexicon_file_path, 'w', encoding='utf-8') as lexfile:
            lexfile.write("Word ID\tWord\n")
            sorted_lexicon = sorted(self.get_lexicon(), key=self.get_word_id)
            for word in sorted_lexicon:
                word_id = self.get_word_id(word)
                lexfile.write(f"{word_id}\t{word}\n")
