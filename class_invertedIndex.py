import json
import re

class InvertedIndex:
    def __init__(self):
        self.index = {}

    def build_index(self, lexicon_file_path, forward_index_file_path):
        # Read the lexicon file to get the list of words
        with open(lexicon_file_path, 'r', encoding='utf-8') as lexfile:
            words = [line.split('\t')[1].strip() for line in lexfile if not line.startswith("Word ID")]

        # Initialize the inverted index
        for word in words:
            self.index[word] = []

        # Read the forward index file to build the inverted index
        with open(forward_index_file_path, 'r', encoding='utf-8') as forwardfile:
            forward_data = forwardfile.read()

        # Split the forward data into individual document entries
        document_entries = forward_data.split('-' * 40 + '\n\n\n')

        # Iterate through document entries
        for document_entry in document_entries:
            doc_id_match = re.search(r'Document ID: (\S+)', document_entry)
            if doc_id_match:
                doc_id = doc_id_match.group(1).strip()
                # Iterate through words in the lexicon
                for word in words:
                    if word in document_entry:
                        self.index[word].append(doc_id)

    def write_index_to_file(self, output_file):
        with open(output_file, 'w', encoding='utf-8') as file:
            for keyword, doc_ids in self.index.items():
                line = f"{keyword}: {json.dumps(doc_ids)}\n"
                file.write(line)
                
    def search(self, keyword, output_file):
        with open(output_file, 'r', encoding='utf-8') as file:
            inverted_data = file.read()

        match = re.search(fr"{keyword}: (\[.+?\])", inverted_data)
        if match:
            doc_ids_str = match.group(1)
            doc_ids = json.loads(doc_ids_str)
            return doc_ids
        else:
            return []