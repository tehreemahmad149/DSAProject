import preprocessing
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import json
import os
import string
import re
folder_path = '\\Users\\tehre\\OneDrive\\Documents\\JSONFILES'
class InvertedIndex:
    def __init__(self):
        self.index = {}

    def add_document(self, document_id, keywords):
        for keyword in keywords:
            if keyword in self.index:
                # If the keyword is already in the index, append the document_id
                if document_id not in self.index[keyword]:
                    self.index[keyword].append(document_id)
            else:
                # If the keyword is not in the index, create a new list with document_id
                self.index[keyword] = [document_id]

    def search(self, keyword):
        # Retrieve the list of document_ids associated with the keyword
        return self.index.get(keyword, [])

#  Usage:
inverted_index = InvertedIndex()
i = 0
for filename in os.listdir(folder_path):
    file_path = os.path.join(folder_path, filename)
    if os.path.isfile(file_path) and filename.endswith('.json'):
        for article_id, content_tokens in preprocessing.extract_content_and_id_from_json(file_path):
            i = i+1
            document_article_id = f"{filename}_{i}"  # Unique ID combining filename and i
            inverted_index.add_document(document_article_id, content_tokens)

result = inverted_index.search("help")
print("Documents containing 'help':", result)
