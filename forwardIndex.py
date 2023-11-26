# forward_index.py

class ForwardIndex:
    def __init__(self):
        self.index = {}

    def add_document(self, doc_id, terms):
        for term in terms:
            if term in self.index:
                self.index[term].append(doc_id)
            else:
                self.index[term] = [doc_id]

    def get_documents_for_term(self, term):
        return self.index.get(term, [])

    def get_original_document_id(self, ranked_document_id):
        # Implement as needed based on your actual requirements
        pass
