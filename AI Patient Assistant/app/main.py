import json
from fastapi import FastAPI
from app.schemas.patient import PatientInput
from app.database import initialize_database, seed_doctors
from app.services.specialty_service import recommend_specialties
from app.services.safety_service import assess_safety
from app.ai_service import (
    analyze_patient_input,
    extract_patient_symptoms,
)
from app.schemas.patient import (
    PatientInput,
    ChatRequest,
    SymptomMessage,
)
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
    # First perform our local safety assessment
    safety_result = assess_safety(
        patient.symptoms,
        patient.additional_information
    )

    # Generate follow-up questions locally
    missing_information, follow_up_questions = generate_follow_up_questions(
        patient.symptoms,
        patient.duration,
        patient.severity,
        patient.additional_information
    )

    # Local specialty recommendation
    recommended_specialties = recommend_specialties(patient.symptoms)

    # Doctor matching from database
    recommended_doctors = find_doctors_by_specialty(
        recommended_specialties
    )

    # Prepare patient information for AI
    patient_data = {
        "patient_name": patient.patient_name,
        "age": patient.age,
        "gender": patient.gender,
        "symptoms": patient.symptoms,
        "duration": patient.duration,
        "severity": patient.severity,
        "additional_information": patient.additional_information,
    }

    # Real AI analysis
    ai_analysis = analyze_patient_input(patient_data)

    return {
        "status": "success",

        "ai_analysis": ai_analysis,

        "safety": safety_result,

        "follow_up": {
            "missing_information": missing_information,
            "questions": follow_up_questions,
        },

        "recommended_specialties": recommended_specialties,

        "recommended_doctors": recommended_doctors,
    }

@app.post("/patient/extract-symptoms")
def extract_symptoms(request: SymptomMessage):

    extracted = extract_patient_symptoms(
        request.message
    )

    return {
        "status": "success",
        "conversation_id": request.conversation_id,
        "original_message": request.message,
        "extracted": extracted,
    }

@app.post("/patient/analyze-message")
def analyze_patient_message(request: SymptomMessage):
    try:
        add_message(
            request.conversation_id,
            "user",
            request.message
        )

        history = get_conversation(
            request.conversation_id
        )

        extracted = extract_patient_symptoms(
            request.message
        )

        patient_data = {
            "symptoms": extracted.get("symptoms", []),
            "duration": extracted.get("duration"),
            "severity": extracted.get("severity"),
            "additional_information": extracted.get(
                "additional_information"
            ),
            "conversation_history": history
        }

        ai_analysis = analyze_patient_input(
            patient_data
        )

        specialties = ai_analysis.get(
            "recommended_specialties",
            []
        )

        doctors = find_doctors_by_specialty(
            specialties
        )

        safety_result = assess_safety(
            patient_data["symptoms"],
            patient_data["additional_information"]
        )

        add_message(
            request.conversation_id,
            "assistant",
            json.dumps(ai_analysis)
        )

        return {
            "status": "success",
            "conversation_id": request.conversation_id,
            "original_message": request.message,
            "extracted_information": extracted,
            "ai_analysis": ai_analysis,
            "safety": safety_result,
            "recommended_doctors": doctors
        }

    except Exception as e:
        return {
            "status": "error",
            "message": "Unable to process the request.",
            "error": str(e)
        }
@app.get("/conversation/{conversation_id}")
def get_conversation_history(conversation_id: str):
    return {
        "status": "success",
        "conversation_id": conversation_id,
        "messages": get_conversation(conversation_id),
    }

@app.delete("/conversation/{conversation_id}")
def delete_conversation(conversation_id: str):
    clear_conversation(conversation_id)

    return {
        "status": "success",
        "conversation_id": conversation_id,
        "message": "Conversation cleared successfully."
    }