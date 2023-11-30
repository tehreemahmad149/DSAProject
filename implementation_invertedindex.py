# import re
import json
from class_invertedIndex import InvertedIndex

# Usage
lexicon_file_path = '/home/gosal/tehreem-s-DSAprojectRepo/lexicon.txt'
forward_index_file_path = '/home/gosal/tehreem-s-DSAprojectRepo/forward_index.txt'
output_file = '/home/gosal/tehreem-s-DSAprojectRepo/inverted_index.txt'

inverted_index = InvertedIndex()
# inverted_index.build_index(lexicon_file_path, forward_index_file_path)
# inverted_index.write_index_to_file(output_file)

# Example search for the keyword 'please'
result = inverted_index.search("please", output_file)
print(f"Documents containing 'please': {result}")