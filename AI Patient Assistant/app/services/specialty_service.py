SPECIALTY_RULES = {
    "Cardiology": [
        "chest pain",
        "heart pain",
        "palpitations",
        "irregular heartbeat",
        "shortness of breath",
    ],
    "Neurology": [
        "headache",
        "migraine",
        "dizziness",
        "numbness",
        "seizure",
        "memory problems",
    ],
    "Dermatology": [
        "rash",
        "itching",
        "acne",
        "skin irritation",
        "skin infection",
    ],
    "Gastroenterology": [
        "stomach pain",
        "abdominal pain",
        "diarrhea",
        "constipation",
        "vomiting",
        "acid reflux",
    ],
    "ENT": [
        "sore throat",
        "ear pain",
        "hearing problem",
        "sinus",
        "runny nose",
    ],
    "Orthopedics": [
        "back pain",
        "joint pain",
        "knee pain",
        "bone pain",
        "muscle pain",
    ],
    "Pulmonology": [
        "cough",
        "breathing difficulty",
        "wheezing",
        "lung pain",
    ],
    "General Medicine": [
        "fever",
        "fatigue",
        "weakness",
        "body pain",
    ],
}


def recommend_specialties(symptoms: list[str]) -> list[str]:
    matched_specialties = []

    normalized_symptoms = [
        symptom.lower().strip()
        for symptom in symptoms
        if symptom
    ]

    for specialty, keywords in SPECIALTY_RULES.items():
        for symptom in normalized_symptoms:
            if any(keyword in symptom for keyword in keywords):
                if specialty not in matched_specialties:
                    matched_specialties.append(specialty)

    if not matched_specialties:
        matched_specialties.append("General Medicine")

    return matched_specialties