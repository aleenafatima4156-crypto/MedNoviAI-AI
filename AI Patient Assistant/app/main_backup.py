from fastapi import FastAPI
from app.schemas.patient import PatientInput
from app.database import initialize_database, seed_doctors
from app.services.specialty_service import recommend_specialties
from app.services.safety_service import assess_safety
from app.schemas.patient import PatientInput, ChatRequest
from app.services.followup_service import (
    generate_follow_up_questions
)
from app.services.conversation_service import (
    add_message,
    get_conversation,
    clear_conversation
)
from app.services.doctor_service import find_doctors_by_specialty
app = FastAPI(
    title="AI Patient Assistant API",
    description="AI-powered patient intake, symptom processing, specialty guidance, and safety support.",
    version="1.0.0",
)
initialize_database()
seed_doctors()
@app.get("/")
def home():
    return {
        "message": "AI Patient Assistant API is running",
        "status": "success",
        "version": "1.0.0",
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "AI Patient Assistant",
    }


@app.post("/patient/intake")
def patient_intake(patient: PatientInput):
    return {
        "message": "Patient intake received successfully",
        "patient": patient.model_dump(),
    }
@app.post("/patient/analyze")
def analyze_patient(patient: PatientInput):

    symptoms = patient.symptoms

    if not symptoms:
        return {
            "status": "success",
            "analysis": {
                "symptoms": [],
                "missing_information": [
                    "Patient symptoms are required."
                ],
                "follow_up_questions": [
                    "What symptoms are you experiencing?"
                ],
                "urgency_level": "unknown",
                "recommended_specialties": [],
                "patient_summary": "Insufficient information for analysis.",
            }
        }

    specialties = recommend_specialties(symptoms)
    missing_information, follow_up_questions = (
        generate_follow_up_questions(
            symptoms=symptoms,
            duration=patient.duration,
            severity=patient.severity,
            additional_information=patient.additional_information
        )
    )
    doctors = find_doctors_by_specialty(specialties)
    safety = assess_safety(
        symptoms,
        patient.additional_information
    )

    return {
        "status": "success",
        "analysis": {
            "symptoms": symptoms,
            "missing_information": missing_information,
            "follow_up_questions": follow_up_questions,
            "urgency_level": safety["urgency_level"],
            "requires_urgent_attention": (
                safety["requires_urgent_attention"]
            ),
            "matched_indicators": safety["matched_indicators"],
            "safety_message": safety["safety_message"],
            "recommended_specialties": specialties,
            "recommended_doctors": doctors,
            "patient_summary": (
                f"Patient reported the following symptoms: "
                f"{', '.join(symptoms)}."
            ),
        }
    }

@app.post("/chat")
def chat(request: ChatRequest):

    add_message(
        request.conversation_id,
        "user",
        request.message
    )

    history = get_conversation(
        request.conversation_id
    )

    return {
        "status": "success",
        "conversation_id": request.conversation_id,
        "message": request.message,
        "conversation_history": history,
        "message_count": len(history)
    }
@app.delete("/chat/{conversation_id}")
def delete_chat(conversation_id: str):

    clear_conversation(conversation_id)

    return {
        "status": "success",
        "message": "Conversation cleared",
        "conversation_id": conversation_id
    }