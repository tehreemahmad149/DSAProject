import math
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from barrels import get_barrel_for_word_id
import sys

totalDocumentLengthFile = "C:\\DSAProject\\total_doc_len.json"

class Ranking:
    def __init__(self, forward_index, inverted_index):
        self.forward_index = forward_index
        self.inverted_index = inverted_index

    @staticmethod
    def calculate_bm25f_score(forward_index, query, doc_id, k1=1.5, b=0.75, title_boost=1.2):
        # Get frequency of each word using forward index to further calculate the document length
        doc_info = forward_index.get_info_for_document(doc_id)
        document_length = doc_info.get('Doc_length')
        print(f"Document length: {document_length}")

        # Access the corpus_size
        forward_index.load_total_doc_length(totalDocumentLengthFile)
        total_doc_length = forward_index.get_total_doc_length()
        # print(f"Corpus size: {total_doc_length}")  

        #calc num_documents
        num_documents = len(forward_index.get_all_document_ids())

        #calc avg doc length
        avg_doc_length = total_doc_length / num_documents

        # Query term frequencies
        qtf = {term: query.count(term) for term in set(query)}

        # BM25F score calculation
        score = 0
        keywords = [word for sublist in [item[1]["Keywords"] for item in forward_index.index.items()] for word in sublist]
        for term in query:
            if (term) in keywords:
                # doc_title = (forward_index.get_info_for_document(doc_id)).get('Title')
                # Boost the score if the term is found in the title
                boost = title_boost if term in (forward_index.get_info_for_document(doc_id)).get('Title', []) else 1.0

                # Replace forward_index.index_size with the actual number of documents in the forward index
                idf = math.log((num_documents + 0.5) / (forward_index.get_document_frequency(term) + 0.5) + 1.0)

                # Calculate the fraction part
                doc_freq = forward_index.get_info_for_document(doc_id)
                # frequency = doc_freq["Frequencies"].get(term, 0)
                numerator = doc_freq["Frequencies"].get(term, 0) * (k1 + 1)
                denominator = doc_freq["Frequencies"].get(term, 0) + k1 * (1 - b + b * (document_length / avg_doc_length))
                denominator += qtf[term] if term in qtf else 0
                # Final calculation
                score += boost * idf * (numerator / denominator)

                #debugging
                print(f"boost: {boost}")
                print(f"idf: {idf}")
                print(f"numerator: {numerator}")
                print(f"denominator: {denominator}")
                print(f"score: {score}")
        return score

    def get_barrel_id(self, query_tokenized):
        barrels = []
        for word in query_tokenized:
            wordId = self.forward_index.get_word_id(word)
            print(wordId)
            if(wordId):
                barrels.append(get_barrel_for_word_id(wordId))
        return barrels

    def rank_documents(self, query_tokenized, k1=1.5, b=0.75, title_boost=1.2):
        #debugging
        print(query_tokenized) #to be assured that the right query is being passed

        barrels = self.get_barrel_id(query_tokenized)
        print(f"barrels: {barrels}")

        # Create a dictionary to store inverted indices for each barrel
        barrel_inverted_indices = {}
        # for each word in tokenized query, getting the relevant barrel to look for in.
        for barrel in barrels:
            barrel_path = f"C:\\DSAProject\\barrel_created\\{barrel}.json"
            #create an instance of inverted_index
            inverted_index = self.inverted_index
            inverted_index.load_inverted_index_from_barrel(barrel_path)
            barrel_inverted_indices[barrel] = inverted_index # Working fine till here

        # load relevant data from barrel
        # inverted_index_instance.load_inverted_index_from_barrel(f"{barrel}.json")

        # Get document texts using forward index
        #this code below looks for the queried keyword/keywords in the inverted index and retrieves the relevant document_id section of the words.
        doc_texts = []
        for barrel, inverted_index in barrel_inverted_indices.items():
            print(f"Barrel: {barrel}")
            # print(f"Inverted Index: {inverted_index.index}")
            print("=" * 30)
            for doc_id in inverted_index.search_inverted_index(query_tokenized):
                doc_info = self.forward_index.get_info_for_document(doc_id)
                # Extract keywords for the document
                keywords = doc_info.get('Keywords', [])
                doc_texts.append(' '.join(keywords))
        # print(doc_texts)

        # Initialize TF-IDF vectorizer
        tfidf_vectorizer = TfidfVectorizer()

        # Calculate TF-IDF matrix
        tfidf_matrix = tfidf_vectorizer.fit_transform(doc_texts)

        # Calculate cosine similarity between query and documents
        query_vector = tfidf_vectorizer.transform([' '.join(query_tokenized)])
        cosine_similarities = cosine_similarity(query_vector, tfidf_matrix).flatten()

        # Combine scores using weighted sum
        scores = {}
        for barrel, inverted_index in barrel_inverted_indices.items():
            for i, doc_id in enumerate(inverted_index.search_inverted_index(query_tokenized)):
                bm25f_score = Ranking.calculate_bm25f_score(self.forward_index, query_tokenized, doc_id, k1, b, title_boost)

                # Combine with cosine similarity
                total_score = 0.6 * cosine_similarities[i] + 0.4 * bm25f_score
                scores[doc_id] = total_score
        
        #debugging
        print(f"cosine_similarities: {cosine_similarities}")
        print(f"bm25f_score: {bm25f_score}")
        print("combining scores using weighted sum")
        print(f"scores: {scores}")

        # Sort the documents by score in descending order
        ranked_documents = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return ranked_documents

