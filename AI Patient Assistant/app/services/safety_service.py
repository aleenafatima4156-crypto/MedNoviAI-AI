EMERGENCY_KEYWORDS = [
    "severe chest pain",
    "crushing chest pain",
    "difficulty breathing",
    "cannot breathe",
    "severe breathing difficulty",
    "unconscious",
    "loss of consciousness",
    "severe bleeding",
    "heavy bleeding",
    "stroke symptoms",
    "face drooping",
    "sudden weakness",
    "severe allergic reaction",
    "anaphylaxis",
    "seizure",
]


def assess_safety(symptoms: list[str], additional_information: str | None = None):
    text_parts = symptoms.copy()

    if additional_information:
        text_parts.append(additional_information)

    combined_text = " ".join(text_parts).lower()

    matched_keywords = []

    for keyword in EMERGENCY_KEYWORDS:
        if keyword in combined_text:
            matched_keywords.append(keyword)

    if matched_keywords:
        return {
            "urgency_level": "emergency",
            "requires_urgent_attention": True,
            "matched_indicators": matched_keywords,
            "safety_message": (
                "The information provided may indicate a potentially "
                "urgent situation. The patient should seek immediate "
                "professional medical assessment or local emergency care."
            ),
        }

    return {
        "urgency_level": "routine_assessment",
        "requires_urgent_attention": False,
        "matched_indicators": [],
        "safety_message": (
            "No emergency indicator was identified from the provided "
            "information. This does not rule out a medical emergency."
        ),
    }