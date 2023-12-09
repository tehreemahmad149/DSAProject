import math
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class Ranking:
    def __init__(self, forward_index, inverted_index):
        self.forward_index = forward_index
        self.inverted_index = inverted_index

    @staticmethod
    def calculate_bm25f_score(forward_index, query, doc_id, k1=1.5, b=0.75, title_boost=1.2):
    # Calculate BM25F score for a document
        keywords, frequencies, _, title = forward_index.get_info_for_document(doc_id)

    # Document length
        doc_length = sum(frequencies.values())

    # Average document length
        avg_doc_length = np.mean([sum(freq.values()) for _, freq, _, _ in forward_index.index.values()])

    # Query term frequencies
        qtf = {term: query.count(term) for term in set(query)}

    # BM25F score calculation
        score = 0
        for term in query:
            if term in keywords:
            # Boost the score if the term is found in the title
                boost = title_boost if term in title else 1.0

            # Replace forward_index.index_size with the actual number of documents in the forward index
                num_documents = len(forward_index.get_all_document_ids())
                idf = math.log((num_documents + 0.5) / (forward_index.get_document_frequency(term) + 0.5) + 1.0)
                numerator = frequencies[term] * (k1 + 1)
                denominator = frequencies[term] + k1 * (1 - b + b * (doc_length / avg_doc_length))
                denominator += qtf[term] if term in qtf else 0
                score += boost * idf * (numerator / denominator)

        return score

    def rank_documents(self, query, k1=1.5, b=0.75, title_boost=1.2):
        # Get document texts using forward index
        doc_texts = [' '.join(self.forward_index.get_info_for_document(doc_id)[0]) for doc_id in self.inverted_index.search_inverted_index(query[0])]

        # Check if doc_texts is empty
        if not doc_texts:
            # Handle the case where there are no relevant documents
            return []

        # Initialize TF-IDF vectorizer
        tfidf_vectorizer = TfidfVectorizer()

        # Calculate TF-IDF matrix
        tfidf_matrix = tfidf_vectorizer.fit_transform(doc_texts)

        # Calculate cosine similarity between query and documents
        query_vector = tfidf_vectorizer.transform([' '.join(query)])
        cosine_similarities = cosine_similarity(query_vector, tfidf_matrix).flatten()

        # Combine scores using weighted sum
        scores = {}
        for i, doc_id in enumerate(self.inverted_index.search_inverted_index(query[0])):
            bm25f_score = Ranking.calculate_bm25f_score(self.forward_index, query, doc_id, k1, b, title_boost)
            # Combine with cosine similarity
            total_score = 0.6 * cosine_similarities[i] + 0.4 * bm25f_score

            scores[doc_id] = total_score

        # Sort the documents by score in descending order
        ranked_documents = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return ranked_documents

