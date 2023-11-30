# Definition of ForwardIndex Class
class ForwardIndex:
    def __init__(self):
        # Initialize attributes
        self.index = {}         # Document ID to keywords mapping
        self.lexicon = set()     # Set of unique keywords in the entire dataset
        self.word_id_mapping = {}  # Mapping of keywords to their corresponding word IDs
        self.next_word_id = 1    # Counter for generating unique word IDs

    def add_document(self, doc_id, keywords):
        # Add document to the index with associated keywords
        self.index[doc_id] = keywords

        # Update lexicon with new unique words from the document
        new_words = set(keywords) - self.lexicon
        self.lexicon.update(new_words)

        # Assign word IDs to new words in the document and update word_id_mapping
        for word in new_words:
            self.word_id_mapping[word] = self.next_word_id
            self.next_word_id += 1

    def get_keywords_for_document(self, doc_id):
        # Return keywords associated with a specific document ID
        return self.index.get(doc_id, [])

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