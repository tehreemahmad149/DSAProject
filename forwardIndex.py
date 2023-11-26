# forwardIndex.py
class ForwardIndex:
    def __init__(self):
        self.index = {}

    def add_document(self, doc_id, keywords):
        self.index[doc_id] = keywords

    def get_keywords_for_document(self, doc_id):
        return self.index.get(doc_id, [])

    def get_original_document_id(self, ranked_document_id):
        # Implement as needed based on your actual requirements
        pass
