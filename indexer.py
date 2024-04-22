import os
import pickle
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import TfidfVectorizer

class Indexer:
    def __init__(self, documents):
        self.vectorizer = TfidfVectorizer(stop_words='english')  # Using English stop words
        self.documents = documents
        self.tfidf_matrix = self._build_index()

    def _build_index(self):
        return self.vectorizer.fit_transform(self.documents)

    def save_index(self, filename):
        with open(filename, 'wb') as f:
            pickle.dump((self.vectorizer, self.tfidf_matrix), f)

def load_documents_from_directory(directory):
    documents = []
    for filename in os.listdir(directory):
        if filename.endswith('.html'):
            filepath = os.path.join(directory, filename)
            html_content = None
            # Try reading with UTF-8 first
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    html_content = f.read()
            except UnicodeDecodeError:
                # If UTF-8 fails, try reading with Latin-1
                try:
                    with open(filepath, 'r', encoding='iso-8859-1') as f:
                        html_content = f.read()
                except UnicodeDecodeError as e:
                    print(f"Failed to read {filename} with UTF-8 and Latin-1 encodings: {e}")
                    continue  # Skip to the next file

            if html_content:
                text_content = extract_text_from_html(html_content)
                documents.append(text_content)
    return documents


def extract_text_from_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    for script in soup(["script", "style"]):  # remove all script and style elements
        script.extract()
    text = soup.get_text()
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text_content = '\n'.join(chunk for chunk in chunks if chunk)
    return text_content

def preprocess_and_save_documents(directory, output_filename):
    documents = load_documents_from_directory(directory)
    indexer = Indexer(documents)
    indexer.save_index(output_filename)

if __name__ == "__main__":
    documents_directory = 'htmlFiles'
    output_filename = 'documents.pickle'

    # Preprocess and save documents
    preprocess_and_save_documents(documents_directory, output_filename)
