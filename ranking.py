class Ranking:
    @staticmethod
    def calculate_tf_score(forward_index, query, doc_id):
        # Calculate term frequency score for a document
        keywords, frequencies, _ = forward_index.get_info_for_document(doc_id)
        tf_score = sum(frequencies.get(word, 0) for word in query)
        return tf_score

    @staticmethod
    def calculate_positional_score(forward_index, query, doc_id):
        # Calculate positional score for a document
        _, _, positions = forward_index.get_info_for_document(doc_id)
        positional_score = 0
        for i in range(len(query) - 1):
            current_word, next_word = query[i], query[i + 1]
            if current_word in positions and next_word in positions:
                min_distance = min([abs(pos1 - pos2) for pos1 in positions[current_word] for pos2 in positions[next_word]])
                positional_score += 1 / (1 + min_distance)
        return positional_score

    @staticmethod
    def calculate_date_relevance(forward_index, doc_id):
        # Placeholder for calculating date relevance, consider implementing your logic
        return 1.0

    @staticmethod
    def calculate_title_relevance(forward_index, query, doc_id):
        # Calculate title relevance for a document
        keywords, _, _ = forward_index.get_info_for_document(doc_id)
        title_relevance = sum(1 for word in query if word in keywords)
        return title_relevance

    @staticmethod
    def rank_documents(forward_index, query):
        # Rank documents based on the provided criteria
        scores = {}
        for doc_id in forward_index.index.keys():
            tf_score = Ranking.calculate_tf_score(forward_index, query, doc_id)
            positional_score = Ranking.calculate_positional_score(forward_index, query, doc_id)
            date_relevance = Ranking.calculate_date_relevance(forward_index, doc_id)
            title_relevance = Ranking.calculate_title_relevance(forward_index, query, doc_id)

            # Adjust weights as needed
            total_score = 0.3 * tf_score + 0.2 * positional_score + 0.3 * date_relevance + 0.2 * title_relevance
            scores[doc_id] = total_score

        # Sort the documents by score in descending order
        ranked_documents = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return ranked_documents