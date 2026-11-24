"""
AIML Symptom-to-Department Classifier Training Script
Uses TF-IDF Vectorization and Multinomial Logistic Regression to map
free-text symptoms into recommended medical departments.
"""

import os
import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_PATH = os.path.join(BASE_DIR, "symptoms_dataset.csv")
MODEL_PATH = os.path.join(BASE_DIR, "symptom_classifier.joblib")


def train_model():
    print("=" * 60)
    print("🏥 Training MediLink Symptom-to-Department Classifier")
    print("=" * 60)

    if not os.path.exists(DATASET_PATH):
        raise FileNotFoundError(f"Dataset not found at {DATASET_PATH}")

    df = pd.read_csv(DATASET_PATH)
    print(f"Loaded {len(df)} symptom-department samples across {df['department'].nunique()} departments:")
    for dept, count in df['department'].value_counts().items():
        print(f"  - {dept}: {count} samples")

    X = df["symptoms"]
    y = df["department"]

    # Stratified split to ensure all departments are represented in test set
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
    )

    pipeline = Pipeline([
        ("tfidf", TfidfVectorizer(
            ngram_range=(1, 2),
            lowercase=True,
            stop_words="english",
            max_features=1500
        )),
        ("classifier", LogisticRegression(
            C=3.0,
            max_iter=1000,
            solver="lbfgs"
        ))
    ])

    print("\nFitting TF-IDF + Logistic Regression Pipeline...")
    pipeline.fit(X_train, y_train)

    # Evaluation
    y_pred = pipeline.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print(f"\n✅ Model Evaluation Accuracy on Test Set: {acc * 100:.2f}%")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, zero_division=0))

    # Fit on all data before saving for maximum coverage in demo
    pipeline.fit(X, y)
    joblib.dump(pipeline, MODEL_PATH)
    print(f"💾 Model pipeline successfully saved to: {MODEL_PATH}")

    # Sample tests
    sample_queries = [
        "severe tightness in chest radiating to left arm and sweating",
        "swollen painful knee joint cannot walk after running",
        "acid reflux burning stomach pain after food",
        "child high fever with coughing and crying"
    ]
    print("\n🧪 Sample Inference Tests:")
    for query in sample_queries:
        probs = pipeline.predict_proba([query])[0]
        classes = pipeline.classes_
        top_idx = probs.argmax()
        pred_dept = classes[top_idx]
        conf = probs[top_idx]
        print(f"  • '{query}'")
        print(f"    -> Predicted: {pred_dept} (Confidence: {conf * 100:.1f}%)\n")

    print("=" * 60)
    print("🚀 Training Complete! Classifier is ready for production API.")
    print("=" * 60)
    return pipeline


if __name__ == "__main__":
    train_model()
