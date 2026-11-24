"""
AIML Symptom Analysis Service
Maps user symptom descriptions to hospital departments with confidence scoring,
top candidates, fallback detection, and emergency overrides.
"""

import os
import joblib
import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MODEL_PATH = os.path.join(BASE_DIR, "ml", "symptom_classifier.joblib")

# Emergency keywords that immediately trigger Emergency Medicine prioritization
EMERGENCY_KEYWORDS = [
    "cardiac arrest", "unresponsive", "unconscious", "massive bleeding",
    "heavy bleeding", "crushing chest pain", "choking", "poison",
    "poisoning", "head trauma", "accident", "gunshot", "burns",
    "gasping", "pulseless", "convulsion"
]

# Fallback keyword dictionary for graceful resilience
KEYWORD_MAPPINGS = {
    "Cardiology": ["heart", "chest", "pulse", "palpitation", "angina", "cardiac", "bp", "blood pressure"],
    "Orthopedics": ["bone", "joint", "knee", "fracture", "spine", "back", "ankle", "shoulder", "arthritis", "sprain"],
    "Gastroenterology": ["stomach", "vomit", "vomiting", "abdomen", "acid", "reflux", "diarrhea", "stool", "jaundice", "liver"],
    "Neurology": ["headache", "migraine", "seizure", "numbness", "paralysis", "tremor", "stroke", "vertigo", "dizziness"],
    "Dermatology": ["skin", "rash", "itch", "itching", "acne", "pimple", "allergy", "hives", "eczema", "dandruff"],
    "Pediatrics": ["baby", "child", "infant", "toddler", "pediatric", "colic"],
    "Pulmonology": ["breath", "breathing", "cough", "asthma", "lung", "wheeze", "sputum"],
    "Emergency Medicine": ["emergency", "critical", "severe pain", "accident", "trauma", "unconscious", "collapse"]
}

DISCLAIMER_TEXT = (
    "Clinical Medical Disclaimer: This AI triage assistant utilizes validated clinical terminology models for routing guidance. "
    "It does not replace a comprehensive physician examination. For life-threatening emergencies, call 108 or proceed to the nearest emergency trauma facility immediately."
)

_cached_model = None


def get_model():
    global _cached_model
    if _cached_model is not None:
        return _cached_model

    if os.path.exists(MODEL_PATH):
        try:
            _cached_model = joblib.load(MODEL_PATH)
            return _cached_model
        except Exception as e:
            print(f"Warning: Could not load trained ML model: {e}")
            return None
    return None


class SymptomService:
    @staticmethod
    def classify_symptoms(symptom_text: str):
        """
        Classifies free-text symptoms into recommended medical department.
        Returns:
            {
                "suggested_department": str,
                "confidence": float (0-1),
                "top_candidates": list of { "department": str, "score": float },
                "fallback_used": bool,
                "is_emergency": bool,
                "disclaimer": str
            }
        """
        if not symptom_text or not symptom_text.strip():
            return {
                "suggested_department": "General Medicine",
                "confidence": 0.50,
                "top_candidates": [{"department": "General Medicine", "score": 0.50}],
                "fallback_used": True,
                "is_emergency": False,
                "disclaimer": DISCLAIMER_TEXT
            }

        text = symptom_text.strip().lower()

        # 1. Critical Emergency Override Check
        for kw in EMERGENCY_KEYWORDS:
            if kw in text:
                return {
                    "suggested_department": "Emergency Medicine",
                    "confidence": 0.95,
                    "top_candidates": [
                        {"department": "Emergency Medicine", "score": 0.95},
                        {"department": "Cardiology", "score": 0.70},
                        {"department": "General Medicine", "score": 0.50}
                    ],
                    "fallback_used": False,
                    "is_emergency": True,
                    "matched_keyword": kw,
                    "disclaimer": DISCLAIMER_TEXT
                }

        # 2. Try ML Model Inference
        model = get_model()
        if model is not None:
            try:
                probabilities = model.predict_proba([symptom_text])[0]
                classes = model.classes_
                sorted_indices = np.argsort(probabilities)[::-1]

                top_class = classes[sorted_indices[0]]
                top_prob = float(probabilities[sorted_indices[0]])

                top_candidates = []
                for idx in sorted_indices[:4]:
                    top_candidates.append({
                        "department": classes[idx],
                        "score": round(float(probabilities[idx]), 3)
                    })

                # If confidence is reasonably high, return ML prediction
                if top_prob >= 0.25:
                    return {
                        "suggested_department": top_class,
                        "confidence": round(top_prob, 3),
                        "top_candidates": top_candidates,
                        "fallback_used": False,
                        "is_emergency": top_class == "Emergency Medicine",
                        "disclaimer": DISCLAIMER_TEXT
                    }
            except Exception as e:
                print(f"ML inference error: {e}")

        # 3. Graceful Rule-Based Keyword Fallback
        matched_scores = {}
        for dept, keywords in KEYWORD_MAPPINGS.items():
            score = sum(1 for kw in keywords if kw in text)
            if score > 0:
                matched_scores[dept] = score

        if matched_scores:
            sorted_depts = sorted(matched_scores.items(), key=lambda x: x[1], reverse=True)
            best_dept = sorted_depts[0][0]
            top_candidates = [{"department": d, "score": min(0.40 + s * 0.15, 0.85)} for d, s in sorted_depts[:3]]
            return {
                "suggested_department": best_dept,
                "confidence": 0.65,
                "top_candidates": top_candidates,
                "fallback_used": True,
                "is_emergency": best_dept == "Emergency Medicine",
                "disclaimer": DISCLAIMER_TEXT
            }

        # Default fallback
        return {
            "suggested_department": "General Medicine",
            "confidence": 0.45,
            "top_candidates": [
                {"department": "General Medicine", "score": 0.45},
                {"department": "Emergency Medicine", "score": 0.20}
            ],
            "fallback_used": True,
            "is_emergency": False,
            "disclaimer": DISCLAIMER_TEXT
        }
