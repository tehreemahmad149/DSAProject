# forwardIndex.py
class ForwardIndex:
    def __init__(self):
        self.index = {}
        self.lexicon = []
        self.word_id_mapping = {}
        self.next_word_id = 1

    def add_document(self, doc_id, keywords):
        self.index[doc_id] = keywords

        for word in keywords:
            if word not in self.word_id_mapping:
                self.word_id_mapping[word] = self.next_word_id
                self.next_word_id += 1
                self.lexicon.append(word)

    def get_keywords_for_document(self, doc_id):
        return self.index.get(doc_id, [])

    def get_original_document_id(self, ranked_document_id):
        # Implement as needed based on your actual requirements
        pass

    def get_lexicon(self):
        return list(self.lexicon)

    def get_word_id(self, word):
        return self.word_id_mapping.get(word, None)

    def get_word_id_mapping(self):
        return self.word_id_mapping
