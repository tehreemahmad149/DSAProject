# myapi/views.py
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.utils.decorators import method_decorator

from myapi.main import ForwardIndex, InvertedIndex, build_forward_index
from myapi.ranking import Ranking
from myapi.extract_guiData import load_metadata, display_metadata, extract_metadata_from_json
from myapi.utils.utils import process_content_generator

# Assume these are your paths, adjust them accordingly
FI_JSON_PATH = r"C:\Users\user\Documents\GitHub\DSA\myproject\myapi\FI.json"
LEXI_JSON_PATH = r"C:\Users\user\Documents\GitHub\DSA\myproject\myapi\Lexi.json"
METADATA_JSON_PATH = r"C:\Users\user\Documents\GitHub\DSA\myproject\myapi\metadata.json"
NEW_ARTICLES_JSON_PATH = r"C:\Users\user\Documents\GitHub\DSA\myproject\myapi\test\newarticles.json"

forward_index_instance = ForwardIndex()
forward_index_instance.load_from_json(FI_JSON_PATH)
forward_index_instance.load_lexicon_from_file(LEXI_JSON_PATH)

inverted_index_instance = InvertedIndex()

loaded_metadata = load_metadata(METADATA_JSON_PATH)

class SearchView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body.decode('utf-8'))
            user_query = data.get('query', '')
            tokenized_query = process_content_generator(user_query)
            ranking_instance = Ranking(forward_index_instance, inverted_index_instance)
            ranked_documents = ranking_instance.rank_documents(tokenized_query)
            doc_ids_to_display = [doc_id for doc_id, score in ranked_documents]

            if loaded_metadata:
                display_metadata(loaded_metadata, doc_ids_to_display)
                for doc_id, score in ranked_documents:
                    print(f"Document ID: {doc_id}, Score: {score}")

            search_results = [
                {
                    'title': loaded_metadata[doc_id]['json_id'],
                    'url': loaded_metadata[doc_id]['json_url'],
                    'score': score
                }
                for doc_id, score in ranked_documents
            ]

            return JsonResponse({'results': search_results})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


class AddContentView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body.decode('utf-8'))
            article_data = data.get('content', {})
            
            # Save the article data to your data files
            append_article_to_json_file(article_data)

            return JsonResponse({'success': True, 'message': 'Article added successfully'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


def append_article_to_json_file(article_data, json_file_path=NEW_ARTICLES_JSON_PATH):
    try:
        with open(json_file_path, "r", encoding="utf-8") as file:
            articles = json.load(file)
            articles.append(json.loads(article_data))

        with open(json_file_path, "w", encoding="utf-8") as file:
            json.dump(articles, file, ensure_ascii=False, indent=2)

        print("Article appended successfully!")
        append_article_to_forward_file()

        # Additional logic if needed

        return True
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return False
    
def append_article_to_forward_file(json_file_path=r"C:\Users\user\Documents\GitHub\DSA\myproject\myapi\FI.json"):
    try:
        forward_index = ForwardIndex() 
        print("obj created")  # Create a new instance of ForwardIndex
        build_forward_index(r"C:\Users\user\Documents\GitHub\DSA\myproject\myapi\test", forward_index)  # Build the forward index
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
    
    with open(r"C:\Users\user\Documents\GitHub\DSA\myproject\myapi\Lexi.json", "r", encoding="utf-8") as file:
        print(" lexi load open in file built\n")
        existing_lexi = json.load(file)
        print(" lexui load close in file built\n")
    last_word_id = existing_lexi[-1]["Word ID"]+1
    lexicon_list = []
    for word, word_id in forward_index.lexicon.items():
        if word not in [item["Word"] for item in existing_lexi]:
            data = {"Word ID": last_word_id, "Word": word}
            lexicon_list.append(data)
            last_word_id = last_word_id+1
    
    print(lexicon_list)
    
    

    with open(r"C:\Users\user\Documents\GitHub\DSA\myproject\myapi\Lexi.json", "w", encoding="utf-8") as file:
        update_lexi = existing_lexi + lexicon_list
        print(" lexidump open in file built\n")
        json.dump(update_lexi, file, ensure_ascii=False, indent=2)
        print(" lexi dump in file built\n")

    print("Forward\\lexicon appended successfully!")
    total_doc_length_file = r"C:\Users\user\Documents\GitHub\DSA\myproject\myapi\total_doc_len.json"
    with open(total_doc_length_file, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
            total_doc_length = data["total_doc_length"]
            total_doc_length = total_doc_length+ forward_index.total_doc_length
            
    with open(total_doc_length_file, 'w', encoding='utf-8') as json_file:
            json.dump({"total_doc_length": total_doc_length}, json_file, indent=2)
            
            
    #code for meta data files
    metadata_dict = {}
    metadata_dict.update(extract_metadata_from_json(r"C:\Users\user\Documents\GitHub\DSA\myproject\myapi\test\newarticles.json"))#add path of newarticles file
    #new meta data dict completed
    json_file_path=r"C:\Users\user\Documents\GitHub\DSA\myproject\myapi\metadata.json"
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
    inverted_index.build_inverted_index(r"C:\Users\user\Documents\GitHub\DSA\myproject\myapi\FI.json", r"C:\Users\user\Documents\GitHub\DSA\myproject\myapi\Lexi.json")
    inverted_index.save_inverted_index_to_json(r"C:\Users\user\Documents\GitHub\DSA\myproject\myapi\II.json")
    json_file_path=r"C:\Users\user\Documents\GitHub\DSA\myproject\myapi\test\newarticles.json"
    with open(json_file_path, "w", encoding="utf-8") as file:
            json.dump([], file, ensure_ascii=False, indent=2)