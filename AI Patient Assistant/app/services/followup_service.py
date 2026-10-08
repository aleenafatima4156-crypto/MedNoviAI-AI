def generate_follow_up_questions(
    symptoms: list[str],
    duration: str | None,
    severity: str | None,
    additional_information: str | None
) -> tuple[list[str], list[str]]:

    missing_information = []
    questions = []

    if not symptoms:
        missing_information.append("symptoms")
        questions.append(
            "What symptoms are you experiencing?"
        )
        return missing_information, questions

    if not duration:
        missing_information.append("duration")
        questions.append(
            "How long have you been experiencing these symptoms?"
        )

    if not severity:
        missing_information.append("severity")
        questions.append(
            "How would you describe the severity of your symptoms?"
        )

    if not additional_information:
        missing_information.append(
            "additional_information"
        )
        questions.append(
            "Is there anything else about your symptoms "
            "that you think is important to mention?"
        )

    return missing_information, questions