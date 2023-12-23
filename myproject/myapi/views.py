# myapi/views.py
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.utils.decorators import method_decorator

from myapi.main import ForwardIndex, InvertedIndex
from myapi.ranking import Ranking
from myapi.extract_guiData import load_metadata, display_metadata
from myapi.utils.utils import process_content_generator

# Assume these are your paths, adjust them accordingly
FI_JSON_PATH = 'myapi/FI.json'
LEXI_JSON_PATH = 'myapi/Lexi.json'
METADATA_JSON_PATH = 'myapi/metadata.json'
NEW_ARTICLES_JSON_PATH = 'myapi/test/newarticles.json'

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
            articles.append(article_data)

        with open(json_file_path, "w", encoding="utf-8") as file:
            json.dump(articles, file, ensure_ascii=False, indent=2)

        print("Article appended successfully!")

        # Additional logic if needed

        return True
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return False
    