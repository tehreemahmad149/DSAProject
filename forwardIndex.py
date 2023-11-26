# forwardIndex.py
class ForwardIndex:
    def __init__(self):
        self.index = {}

    def add_document(self, doc_id, keywords):
        self.index[doc_id] = keywords

    def get_keywords_for_document(self, doc_id):
        return self.index.get(doc_id, [])

    def get_all_documents(self):
        return list(self.index.keys())