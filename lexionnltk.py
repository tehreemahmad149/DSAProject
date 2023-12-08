import nltk
import json
from nltk.corpus import wordnet as wn

def build_lexicon():
    lexicon = []
    word_id = 1

    for synset in list(wn.all_synsets()):
        for lemma in synset.lemmas():
            word = lemma.name()
            data = {"Word ID": word_id, "Word": word}
            lexicon.append(data)
            word_id += 1

    return lexicon

def save_lexicon_to_json(lexicon, output_file):
    with open(output_file, 'w', encoding='utf-8') as json_file:
        json.dump(lexicon, json_file, indent=2)

lexicon = build_lexicon()
save_lexicon_to_json(lexicon, 'C:\\DSAProject\\lexicon.json')
word_synsets = wn.synsets('semiramis')

if word_synsets:
    print(f"'draco' found in WordNet. Synsets: {word_synsets}")
else:
    print("'draco' not found in WordNet.")
