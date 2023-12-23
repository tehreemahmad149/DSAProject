import json
import tkinter as tk
import os
from class_forwardIndex import ForwardIndex
from class_forwardIndex import build_forward_index
from class_invertedIndex import InvertedIndex
from extract_guiData import extract_metadata_from_json
from datetime import datetime

def prompt_user_for_article():
    root = tk.Tk()
    root.title("Article Entry")

    # Labels
    tk.Label(root, text="Enter article data:").grid(row=0, column=0, padx=10, pady=5)

    # Text Entry
    article_var = tk.StringVar()
    
    tk.Entry(root, textvariable=article_var, width=50).grid(row=0, column=1, padx=10, pady=5)

    def save_article():
        article_data = json.loads(article_var.get())
        append_article_to_json_file(article_data)
        root.destroy()

    # Save Button
    tk.Button(root, text="Save Article", command=save_article).grid(row=1, column=0, columnspan=2, pady=10)

    root.mainloop()


def append_article_to_json_file(article_data, json_file_path=r"C:\DSAProject\test\newarticles.json"):
    try:
        with open(json_file_path, "r", encoding="utf-8") as file:
            articles = json.load(file)
            articles.append(article_data)

        with open(json_file_path, "w", encoding="utf-8") as file:
            json.dump(articles, file, ensure_ascii=False, indent=2)

        print("Article appended successfully!")
        append_article_to_forward_file()
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def append_article_to_forward_file(json_file_path="C:\\DSAProject\\FI.json"):
    try:
        forward_index = ForwardIndex() 
        print("obj created")  # Create a new instance of ForwardIndex
        build_forward_index(r"C:\DSAProject\test", forward_index)  # Build the forward index
        print("extra foward built\n")

        # Open the file and directly assign the content to existing_data
        with open(json_file_path, "r", encoding="utf-8") as file:
            print("foward file open\n")
            try:
                existing_data = json.load(file)
                print("prev data loaded\n")
            except json.JSONDecodeError as e:
                print(f"JSONDecodeError: {e}")
    except json.JSONDecodeError:
        # If the file is empty or not a valid JSON, start with an empty dictionary
        existing_data = {}

    new_structure = forward_index.index
    print("foward into new struct built\n")
    existing_data.update(new_structure)
    print("update foward built\n")

    # Step 4: Write the modified data back to the file

    with open(json_file_path, "w", encoding="utf-8") as file:
        print(" fowarddump open in file built\n")
        json.dump(existing_data, file, ensure_ascii=False, indent=2)
        print(" foward dumped close in file built\n")
    
    with open(r"C:\DSAProject\Lexi.json", "r", encoding="utf-8") as file:
        print(" lexi load open in file built\n")
        existing_lexi = json.load(file)
        print(" lexui load close in file built\n")
    last_word_id = existing_lexi[-1]["Word ID"]+1
    lexicon_list = []
    for word, word_id in forward_index.lexicon.items():
        data = {"Word ID": last_word_id, "Word": word}
        lexicon_list.append(data)
        last_word_id = last_word_id+1
    
    print(lexicon_list)
    
    

    with open(r"C:\DSAProject\Lexi.json", "w", encoding="utf-8") as file:
        update_lexi = existing_lexi + lexicon_list
        print(" lexidump open in file built\n")
        json.dump(update_lexi, file, ensure_ascii=False, indent=2)
        print(" lexi dump in file built\n")

    print("Forward\\lexicon appended successfully!")
    total_doc_length_file = r"C:\DSAProject\total_doc_len.json"
    with open(total_doc_length_file, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
            total_doc_length = data["total_doc_length"]
            total_doc_length = total_doc_length+ forward_index.total_doc_length
            
    with open(total_doc_length_file, 'w', encoding='utf-8') as json_file:
            json.dump({"total_doc_length": total_doc_length}, json_file, indent=2)
            
            
    #code for meta data files
    metadata_dict = {}
    metadata_dict.update(extract_metadata_from_json("C:\\DSAProject\\metadata.json"))
    #new meta data dict completed
    json_file_path="C:\\DSAProject\\metadata.json"
    try:
        with open(json_file_path, "r", encoding="utf-8") as file:
            print("meta file open\n")
            try:
                existing_data = json.load(file)
                print("prev data loaded\n")
            except json.JSONDecodeError as e:
                print(f"JSONDecodeError: {e}")
    except json.JSONDecodeError:
        # If the file is empty or not a valid JSON, start with an empty dictionary
        existing_data = {}

    existing_data.update(metadata_dict)
    print("meta dict built full\n")

    # Step 4: Write the modified data back to the file

    with open(json_file_path, "w", encoding="utf-8") as file:
        print(" meta dump open in file built\n")
        json.dump(existing_data, file, ensure_ascii=False, indent=2)
        print(" meta dumped close in file built\n")    
    append_article_to_inverted_file()


def append_article_to_inverted_file():
    inverted_index = InvertedIndex()
    inverted_index.build_inverted_index("C:\\DSAProject\\FI.json", r"C:\DSAProject\Lexi.json")
    inverted_index.save_inverted_index_to_json(r"C:\DSAProject\II.json")
    json_file_path=r"C:\DSAProject\test\newarticles.json"
    with open(json_file_path, "w", encoding="utf-8") as file:
            json.dump([], file, ensure_ascii=False, indent=2)

# Call the function to update indices
prompt_user_for_article()