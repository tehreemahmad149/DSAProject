import math
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

totalDocumentLengthFile = "/home/gosal/Documents/DSA/project/DSAProject/total_doc_len.json"

class Ranking:
    def __init__(self, forward_index, inverted_index):
        self.forward_index = forward_index
        self.inverted_index = inverted_index

    @staticmethod
    def calculate_bm25f_score(forward_index, query, doc_id, k1=1.5, b=0.75, title_boost=1.2):
        print("inside the bm25f function")

        # Get frequency of each word using forward index to further calculate the document length
        doc_info = forward_index.get_info_for_document(doc_id)
        document_length = doc_info.get('Doc_length')
        print(f"Document length: {document_length}")

        # Access the corpus_size
        forward_index.load_total_doc_length(totalDocumentLengthFile)
        total_doc_length = forward_index.get_total_doc_length()
        # print(f"Corpus size: {total_doc_length}")


        # calculate average document length
        # avg_doc_length = np.mean([doc_length for _, Frequencies, _, _ in forward_index.index.values()])
        # print(avg_doc_length)   

        #calc num_documents
        num_documents = len(forward_index.get_all_document_ids())
        print(num_documents)

        #calc avg doc length
        avg_doc_length = total_doc_length / num_documents

        # Query term frequencies
        qtf = {term: query.count(term) for term in set(query)}

        # BM25F score calculation
        score = 0
        keywords = [word for sublist in [item[1]["Keywords"] for item in forward_index.index.items()] for word in sublist]
        for term in query:
            print("hello")
            if (term) in keywords:
                print("world")
                # doc_title = (forward_index.get_info_for_document(doc_id)).get('Title')
                # Boost the score if the term is found in the title
                boost = title_boost if term in (forward_index.get_info_for_document(doc_id)).get('Title') else 1.0
                print(boost)

                # Replace forward_index.index_size with the actual number of documents in the forward index
                idf = math.log((num_documents + 0.5) / (forward_index.get_document_frequency(term) + 0.5) + 1.0)
                print(idf)

                # Calculate the fraction part
                doc_freq = forward_index.get_info_for_document(doc_id)
                # frequency = doc_freq["Frequencies"].get(term, 0)
                numerator = doc_freq["Frequencies"].get(term, 0) * (k1 + 1)
                denominator = doc_freq["Frequencies"].get(term, 0) + k1 * (1 - b + b * (document_length / avg_doc_length))
                denominator += qtf[term] if term in qtf else 0
                # Final calculation
                score += boost * idf * (numerator / denominator)

        #debugging
        print(score)
        print("score is calculated and about to be returned")
        return score


    def rank_documents(self, query_tokenized, k1=1.5, b=0.75, title_boost=1.2):
        #debugging
        print(query_tokenized) #to be assured that the right query is being passed

        # Get document texts using forward index
        #this code below looks for the queried keyword/keywords in the inverted index and retrieves the relevant document_id section of the words.
        doc_texts = []
        for doc_id in self.inverted_index.search_inverted_index(query_tokenized):
            doc_info = self.forward_index.get_info_for_document(doc_id)
            # Extract keywords for the document
            keywords = doc_info.get('Keywords', [])
            doc_texts.append(' '.join(keywords))
        
        #debugging for the above for loop...
        doc_ids = self.inverted_index.search_inverted_index(query_tokenized)
        print("Document IDs:")
        for doc_id in doc_ids:
            print(doc_id)
            # for i, doc_text in enumerate(doc_texts):
            #     print(f"Document {i + 1}: {doc_text}")
            # print(self.forward_index.get_info_for_document(doc_id).get('Keywords', []))

            # for doc_id in self.inverted_index.search_inverted_index(query_tokenized):
            #     print(doc_id)
            # Check if doc_texts is empty
        if not doc_texts:
            # Handle the case where there are no relevant documents
            print("document list is empty")
            return

        # Initialize TF-IDF vectorizer
        tfidf_vectorizer = TfidfVectorizer()
        #debugging
        print("Initialize TF-IDF vectorizer")

        # Calculate TF-IDF matrix
        tfidf_matrix = tfidf_vectorizer.fit_transform(doc_texts)

        # Calculate cosine similarity between query and documents
        query_vector = tfidf_vectorizer.transform([' '.join(query_tokenized)])
        cosine_similarities = cosine_similarity(query_vector, tfidf_matrix).flatten()
        
        #debugging
        # print(len(cosine_similarities))
        # print(cosine_similarities)
        #debugging
        print("Calculate cos similarity between query and documents")


        # Combine scores using weighted sum
        scores = {}
        for i, doc_id in enumerate(self.inverted_index.search_inverted_index(query_tokenized)):

            bm25f_score = Ranking.calculate_bm25f_score(self.forward_index, query_tokenized, doc_id, k1, b, title_boost)
            print(bm25f_score)
            # Combine with cosine similarity
            total_score = 0.6 * cosine_similarities[i] + 0.4 * bm25f_score

            scores[doc_id] = total_score
            

        #debugging
        print("combining scores using weighted sum")

        # Sort the documents by score in descending order
        ranked_documents = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return ranked_documents

