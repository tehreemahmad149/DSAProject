import json
import os
import re
from class_invertedIndex import InvertedIndex


 
file_path = 'C:\\DSAProject\\II.json'
with open(file_path, 'r', encoding='utf-8') as file:
            inverted_index = json.load(file)
            sorted_inverted_index = {keyword: inverted_index[keyword] for keyword in sorted(inverted_index)}

with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(sorted_inverted_index, file, indent=2)