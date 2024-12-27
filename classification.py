import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import pickle

# Train the classification model
def train_classifier(csv_file):
    # Load the dataset
    data = pd.read_csv(csv_file)
    X = data["Text"]
    y = data["Category"]

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Extract features using TF-IDF vectorization
    vectorizer = TfidfVectorizer(stop_words='english')
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)

    # Train the Random Forest classifier
    model = RandomForestClassifier()
    model.fit(X_train_vec, y_train)

    # Evaluate the model
    accuracy = model.score(X_test_vec, y_test)
    print(f"Model Accuracy: {accuracy:.2f}")

    # Save the model and vectorizer to a file
    with open("text_classifier.pkl", "wb") as f:
        pickle.dump((model, vectorizer), f)

    print("Model training completed and saved as text_classifier.pkl")

# Predict category for new text
def predict_category(text):
    # Load the model and vectorizer
    with open("text_classifier.pkl", "rb") as f:
        model, vectorizer = pickle.load(f)
    # Transform the text into vectorized form
    text_vec = vectorizer.transform([text])
    # Predict the category
    return model.predict(text_vec)[0]
