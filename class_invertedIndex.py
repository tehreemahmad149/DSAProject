class InvertedIndex:
    def __init__(self):
        self.index = {}

    def read_lexicon(self, lexicon_path):
        lexicon_words = set()

        with open(lexicon_path, 'r', encoding='utf-8') as lexicon_file:
            # Skip the header line
            next(lexicon_file)
            for line in lexicon_file:
                word = line.split('\t')[-1].strip()
                lexicon_words.add(word)
        return lexicon_words #all the words in the lexicon
    

    def add_entry(self, keyword, doc_id):
        if keyword not in self.index:
            self.index[keyword] = [] #empty list for that keyword
        if doc_id not in self.index[keyword]:
            self.index[keyword].append(doc_id) 

    def build_inverted_index(self, file_path, lexicon_path):
        # Read lexicon file
        lexicon_words = self.read_lexicon(lexicon_path)

        # Read forward index file
        with open(file_path, 'r') as file:
            lines = file.readlines()

        current_doc_id = None
        current_keywords = []

        for line in lines:
            if line.startswith('Document ID:'):
                current_doc_id = line.split(':')[-1].strip()
            elif line.startswith('Keywords:'):
                current_keywords = [kw.strip() for kw in line.split(':')[-1].split(',')]
                for keyword in current_keywords:
                    if keyword in lexicon_words:
                        self.add_entry(keyword, current_doc_id)
                       
    def write_to_file(self, output_file):
        with open(output_file, 'w') as file:
            for keyword, doc_ids in self.index.items():
                file.write(f"{keyword}: {', '.join(doc_ids)}\n")

    def search(self, keyword):
        return self.index.get(keyword, [])

