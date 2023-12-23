# myapi/views.py
import sys
from pathlib import Path
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.utils.decorators import method_decorator

project_root = str(Path(__file__).resolve().parent.parent)  # Adjust the parent count based on your project structure
sys.path.append(project_root)

from myapi.ranking import Ranking
from myapi.main import ForwardIndex, InvertedIndex
from myapi.utils.utils import process_content_generator
from myapi.extract_guiData import load_metadata, display_metadata

# Create instances of ForwardIndex and InvertedIndex
forward_index_instance = ForwardIndex()
inverted_index_instance = InvertedIndex()
forward_index_instance.load_from_json('myapi/FI.json')
forward_index_instance.load_lexicon_from_file('myapi/Lexi.json')

# Load data from JSON files
forward_index_instance.load_from_json('myapi/FI.json')
forward_index_instance.load_lexicon_from_file('myapi/Lexi.json')
loaded_metadata = load_metadata("myapi/metadata.json")

class SearchView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        try:
            # Load JSON data from the request body
            data = json.loads(request.body.decode('utf-8'))

            # Get the query from the JSON data
            user_query = data.get('query', '')

            # Tokenize the user's query using the same process as document tokenization
            tokenized_query = process_content_generator(user_query)

            # Create an instance of the Ranking class
            ranking_instance = Ranking(forward_index_instance, inverted_index_instance)

            # Search for documents based on the user's query
            ranked_documents = ranking_instance.rank_documents(tokenized_query)

            # Get doc_ids to display the metadata
            doc_ids_to_display = [doc_id for doc_id, score in ranked_documents]

            # Display the ranked documents
            if loaded_metadata:
                display_metadata(loaded_metadata, doc_ids_to_display)
                for doc_id, score in ranked_documents:
                    print(f"Document ID: {doc_id}, Score: {score}")

            # Return the ranked documents as JSON
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
            import traceback
            traceback.print_exc()  # Print the full traceback
            return JsonResponse({'error': str(e)}, status=500)
