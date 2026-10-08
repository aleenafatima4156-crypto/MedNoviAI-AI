import json
import os

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY")

if not API_KEY:
    raise RuntimeError("OPENAI_API_KEY is not configured.")

client = OpenAI(api_key=API_KEY)


SYSTEM_PROMPT = """
You are an AI Patient Intake Assistant.

Your job is to organize patient-reported information.

You are NOT a doctor and must NOT provide a confirmed diagnosis.

Return ONLY valid JSON with exactly these fields:

{
  "symptoms": [],
  "missing_information": [],
  "follow_up_questions": [],
  "urgency_level": "routine_assessment",
  "recommended_specialties": [],
  "patient_summary": ""
}

Rules:

- symptoms must contain the symptoms explicitly reported by the patient.
- missing_information contains information needed for better assessment.
- follow_up_questions contains concise questions for missing information.
- urgency_level must be one of:
  "routine_assessment",
  "urgent_assessment",
  "emergency"
- recommended_specialties contains relevant medical specialties.
- patient_summary must be a short factual summary.
- Do not diagnose the patient.
- Do not prescribe medication.
- Do not invent symptoms or medical history.
- If information suggests a possible emergency, use "emergency"
  and clearly state that immediate professional medical assessment
  is appropriate.
"""


def analyze_patient_input(patient_data: dict) -> dict:

    response = client.responses.create(
        model=os.getenv("OPENAI_MODEL", "gpt-5.6-mini"),
        instructions=SYSTEM_PROMPT,
        input=json.dumps(patient_data),
    )

    raw_output = response.output_text.strip()

    try:
        return json.loads(raw_output)

    except json.JSONDecodeError:
        return {
            "symptoms": patient_data.get("symptoms", []),
            "missing_information": [],
            "follow_up_questions": [],
            "urgency_level": "routine_assessment",
            "recommended_specialties": [],
            "patient_summary": raw_output,
        }
    
def extract_patient_symptoms(message: str) -> dict:

    response = client.responses.create(
        model=os.getenv("OPENAI_MODEL", "gpt-5.6-mini"),
        instructions="""
You extract symptoms from a patient's natural-language message.

Return ONLY valid JSON:

{
  "symptoms": [],
  "duration": null,
  "severity": null,
  "additional_information": null
}

Rules:
- Extract only information actually stated by the patient.
- Do not diagnose.
- Do not invent symptoms.
- duration should be null if not stated.
- severity should be null if not stated.
- symptoms should be short, normalized descriptions.
""",
        input=message,
    )

    raw_output = response.output_text.strip()

    try:
        return json.loads(raw_output)

    except json.JSONDecodeError:
        return {
            "symptoms": [],
            "duration": None,
            "severity": None,
            "additional_information": message,
        }