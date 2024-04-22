import unittest
from flask import Flask, request, jsonify
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

class Processor:
    def __init__(self, vectorizer, tfidf_matrix):
        self.vectorizer = vectorizer
        self.tfidf_matrix = tfidf_matrix

    def preprocess_query(self, query):
        # Preprocess the query similarly to how documents were preprocessed
        # Here we assume the query needs to be lowered in case. Further preprocessing can be added
        return query.lower()

    def search(self, query, top_k=5):
        # Process the query first
        processed_query = self.preprocess_query(query)
        query_vector = self.vectorizer.transform([processed_query])
        cosine_similarities = cosine_similarity(query_vector, self.tfidf_matrix).flatten()
        top_indices = cosine_similarities.argsort()[-top_k:][::-1]
        return top_indices

@app.route('/search', methods=['POST'])
def handle_search():
    data = request.get_json()
    query = data.get('query', '')
    
    if not query:
        return jsonify({'error': 'Query parameter missing in request'}), 400

    try:
        # Load the vectorizer and TF-IDF matrix from a pickle file
        with open('documents.pickle', 'rb') as f:
            vectorizer, tfidf_matrix = pickle.load(f)

        processor = Processor(vectorizer, tfidf_matrix)
        top_indices = processor.search(query)
        
        # Convert numpy indices to list and send back as JSON
        results = {'top_indices': top_indices.tolist()}
        return jsonify(results)
    except Exception as e:
        return jsonify({'error': str(e)}), 500











if __name__ == '__main__':
    app.run(debug=True)
    # unittest.main()
