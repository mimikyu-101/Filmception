import joblib
import json
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import nltk

# Download NLTK data (only once)
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')

class MovieGenrePredictor:
    def __init__(self, model_path='lightgbm_genre_classifier.pkl', 
                 tfidf_path='tfidf_vectorizer.pkl',
                 genres_path='genre_columns.json'):
        # Load model, vectorizer, and genre list
        self.model = joblib.load(model_path)
        self.tfidf = joblib.load(tfidf_path)
        with open(genres_path, 'r') as f:
            self.genre_columns = json.load(f)
    
    def preprocess_text(self, text):
        # Lowercase
        text = text.lower()
        # Remove special chars
        text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
        # Tokenize
        tokens = word_tokenize(text)
        # Remove stopwords
        stop_words = set(stopwords.words('english'))
        tokens = [word for word in tokens if word not in stop_words]
        # Lemmatize
        lemmatizer = WordNetLemmatizer()
        tokens = [lemmatizer.lemmatize(word) for word in tokens]
        return ' '.join(tokens)
    
    def predict(self, summary):
        # Preprocess
        processed_summary = self.preprocess_text(summary)
        # Transform
        X_new = self.tfidf.transform([processed_summary])
        # Predict
        preds = self.model.predict(X_new)
        # Get genres
        genres = [self.genre_columns[i] for i, val in enumerate(preds[0]) if val == 1]
        return genres

# Example usage (optional)
if __name__ == "__main__":
    predictor = MovieGenrePredictor()
    summary = "A young boy discovers he has magical powers and must save the world from an evil wizard."
    print("Predicted Genres:", predictor.predict(summary))
