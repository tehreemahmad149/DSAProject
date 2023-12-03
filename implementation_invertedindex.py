# import re
import json
import os
from class_invertedIndex import InvertedIndex

def load_config(config_path='config.json'):
    # Load configuration from config.json
    if os.path.exists(config_path):
        with open(config_path, 'r') as config_file:
            return json.load(config_file)
     # Throw error otherwise
    else:
    # Throw error otherwise
        print(f"Config file {config_path} not found. Using default configuration.")
        return {}


