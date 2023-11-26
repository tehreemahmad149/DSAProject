import re
import json

class InvertedIndex:
    def __init__(self):
        self.index = {}

    def parse_document(self, document):
        match = re.search(r"Document ID: (\S+)Keywords: (.+)", document)
        if match:
            document_id = match.group(1)
            keywords = [keyword.strip() for keyword in match.group(2).split(',')]
            return document_id, keywords
        return None, None

    def build_index(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                document_id, keywords = self.parse_document(line)
                if document_id and keywords:
                    self.add_document(document_id, keywords)

    def add_document(self, document_id, keywords):
        for keyword in keywords:
            if keyword in self.index:
                # If the keyword is already in the index, append the document_id
                if document_id not in self.index[keyword]:
                    self.index[keyword].append(document_id)
            else:
                # If the keyword is not in the index, create a new list with document_id
                self.index[keyword] = [document_id]

    def write_index_to_file(self, output_file):
        with open(output_file, 'w', encoding='utf-8') as file:
            for keyword, doc_ids in self.index.items():
                line = f"{keyword}: {json.dumps(doc_ids)}\n"
                file.write(line)

    def search(self, keyword):
        return self.index.get(keyword, [])

# Usage:
inverted_index = InvertedIndex()
file_path = '\\DSAProject\\invertedindex\\forward_index.txt'
inverted_index.build_index(file_path)

# Write the inverted index to a file
output_file = '\\DSAProject\\invertedindex\\inverted_index.txt'
inverted_index.write_index_to_file(output_file)

# Example search for the keyword 'certiorari'
result = inverted_index.search("politically")
print("Documents containing 'politically':", result)
