# AI Patient Assistant

An AI-powered patient intake and healthcare guidance backend built with **FastAPI, OpenAI, and SQLite**.

> **Important:** This project is an intake and guidance system, not a medical diagnosis system. It does not replace a qualified healthcare professional and should not be used to make emergency medical decisions.

---

## 📌 Project Overview

The **AI Patient Assistant** accepts patient messages or structured patient information, extracts relevant symptoms, organizes the information, identifies missing details, assesses urgency, recommends relevant medical specialties, and matches available doctors from a local database.

The system also maintains conversation history so that multiple messages can belong to the same patient conversation.

### Main workflow

```text
Patient Message
      ↓
Symptom Extraction
      ↓
Patient Information Analysis
      ↓
Safety / Urgency Assessment
      ↓
Follow-up Questions
      ↓
Specialty Recommendation
      ↓
Doctor Matching
      ↓
Conversation Storage
```

---

## ✨ Features

### 1. Natural-Language Symptom Extraction

Patients can describe their symptoms in normal language, for example:

```text
I have had stomach pain for three days.
```

The AI extracts structured information such as:

- Symptoms
- Duration
- Severity
- Additional information

---

### 2. AI Patient Analysis

The system organizes the extracted information into a structured response containing:

- Reported symptoms
- Missing information
- Follow-up questions
- Urgency level
- Recommended specialties
- Patient summary

The AI is instructed not to provide a confirmed diagnosis or prescribe medication.

---

### 3. Safety and Urgency Assessment

The system includes an urgency classification:

```text
routine_assessment
urgent_assessment
emergency
```

This is intended to help route patient intake appropriately. It is not a substitute for professional medical assessment.

---

### 4. Follow-up Questions

If important information is missing, the system generates questions such as:

```text
How long have you been experiencing these symptoms?

How would you describe the severity of your symptoms?

Is there anything else about your symptoms that is important to mention?
```

---

### 5. Medical Specialty Recommendation

The system can recommend relevant specialties based on the reported symptoms.

Examples include:

- Cardiology
- Neurology
- Dermatology
- Gastroenterology
- ENT
- Orthopedics
- Pulmonology
- General Medicine

---

### 6. Doctor Matching

Available doctors are stored in SQLite and matched against recommended specialties.

Doctor information includes:

- Name
- Specialty
- Years of experience
- Availability

The included doctors are **dummy/demo data**.

---

### 7. Conversation Memory

Every conversation uses a `conversation_id`.

Messages are stored in SQLite, allowing the assistant to access previous messages from the same conversation.

Available operations:

```text
GET    /conversation/{conversation_id}
DELETE /conversation/{conversation_id}
```

---

## 🏗️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| FastAPI | REST API framework |
| OpenAI API | AI-powered language processing |
| SQLite | Local database |
| Pydantic | Request/data validation |
| Uvicorn | ASGI server |
| python-dotenv | Environment variable management |
| Swagger / OpenAPI | API documentation |

---

## 📁 Project Structure

```text
AI Patient Assistant/
│
├── .env
├── .gitignore
├── requirements.txt
├── README.md
│
├── app/
│   ├── main.py
│   ├── ai_service.py
│   ├── database.py
│   │
│   ├── data/
│   │   └── doctors.py
│   │
│   ├── schemas/
│   │   └── patient.py
│   │
│   └── services/
│       ├── conversation_service.py
│       ├── doctor_service.py
│       └── followup_service.py
│
├── data/
│   └── patient_assistant.db
│
└── venv/
```

### Module responsibilities

**`app/main.py`**
- FastAPI application
- API endpoints
- Request processing
- Response generation

**`app/ai_service.py`**
- OpenAI client
- Symptom extraction
- AI patient analysis

**`app/database.py`**
- SQLite connection
- Database initialization
- Doctor seeding

**`app/services/conversation_service.py`**
- Save messages
- Retrieve conversation history
- Clear conversations

**`app/services/doctor_service.py`**
- Search available doctors by specialty

**`app/services/followup_service.py`**
- Detect missing patient information
- Generate follow-up questions

**`app/schemas/patient.py`**
- API request validation models

---

## ⚙️ Installation

### 1. Clone or open the project

Open a terminal inside the project directory:

```bash
cd "AI Patient Assistant"
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

Windows CMD:

```cmd
venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🔐 Environment Variables

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=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
OPENAI_MODEL=gpt-6-luna
```

### Security

Never commit `.env` to Git.

The project should keep the following in `.gitignore`:

```text
.env
venv/
__pycache__/
*.pyc
*.db
```

Never share your API key publicly.

---

## ▶️ Running the Application

Start the FastAPI server:

```bash
python -m uvicorn app.main:app --reload
```

The API will normally be available at:

```text
http://127.0.0.1:8000
```

---

## 📚 API Documentation

FastAPI automatically provides interactive Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

Alternative ReDoc documentation:

```text
http://127.0.0.1:8000/redoc
```

---

## 🔌 API Endpoints

### `POST /patient/analyze`

Analyzes structured patient information.

Example request:

```json
{
  "patient_name": "Demo Patient",
  "age": 25,
  "gender": "Other",
  "symptoms": ["stomach pain"],
  "duration": "3 days",
  "severity": "moderate",
  "additional_information": "Pain occurs after meals."
}
```

---

### `POST /patient/extract-symptoms`

Extracts structured information from a natural-language patient message.

Example:

```json
{
  "conversation_id": "demo001",
  "message": "I have had a headache and mild fever for two days."
}
```

---

### `POST /patient/analyze-message`

Runs the main natural-language patient intake workflow.

Example:

```json
{
  "conversation_id": "demo001",
  "message": "I have had stomach pain for three days."
}
```

The response can contain:

```text
extracted_information
ai_analysis
safety
recommended_doctors
```

---

### `GET /conversation/{conversation_id}`

Returns the stored messages for a conversation.

Example:

```text
GET /conversation/demo001
```

---

### `DELETE /conversation/{conversation_id}`

Deletes the stored conversation and its messages.

Example:

```text
DELETE /conversation/demo001
```

---

## 🧪 Example Testing Flow

### Step 1 — Send a patient message

```json
{
  "conversation_id": "demo001",
  "message": "I have had stomach pain for three days."
}
```

### Step 2 — Review the response

Check:

```text
Extracted information
AI analysis
Safety assessment
Recommended doctors
```

### Step 3 — Continue the conversation

Use the same `conversation_id`:

```json
{
  "conversation_id": "demo001",
  "message": "The pain has become more noticeable today."
}
```

### Step 4 — View conversation history

```text
GET /conversation/demo001
```

### Step 5 — Clear the conversation

```text
DELETE /conversation/demo001
```

---

## 🗄️ Database

The application uses SQLite.

The database contains the following main tables:

### `conversations`

Stores conversation identifiers and creation timestamps.

### `messages`

Stores:

- Conversation ID
- Role
- Message content
- Creation timestamp

### `doctors`

Stores demo doctor information:

- Name
- Specialty
- Experience
- Availability

The database is initialized automatically when the application starts.

---

## 🛡️ Safety and Privacy

This project is designed as a technical/demo patient-intake application.

For real healthcare deployment, additional safeguards would be required, including:

- Strong authentication and authorization
- Encryption in transit and at rest
- Proper access controls
- Audit logging
- Secure secrets management
- Data retention policies
- Consent and privacy controls
- Healthcare-specific regulatory compliance
- Human clinical oversight
- Production-grade monitoring and incident handling

**Do not use real patient-identifying or sensitive health information in this development/demo version.**

---

## 🚫 What This System Does Not Do

The assistant should not:

- Provide a confirmed medical diagnosis
- Prescribe medication
- Replace a doctor
- Replace emergency medical services
- Invent patient symptoms or medical history
- Treat AI output as definitive clinical advice

The system is intended to organize patient-reported information and support the intake workflow.

---

## 🔮 Possible Future Improvements

Potential future development areas include:

- Authentication and user accounts
- Role-based access control
- Production database such as PostgreSQL
- Appointment scheduling
- Doctor availability management
- Patient dashboard
- Admin dashboard
- Secure deployment
- Automated tests
- Structured logging
- Rate limiting
- Better multilingual support
- More robust clinical safety rules
- Human-review workflow
- Production-grade privacy and compliance controls

---

## 📌 Development Status

Current implementation includes:

- FastAPI backend
- OpenAI integration
- Natural-language symptom extraction
- Structured AI analysis
- Safety assessment
- Follow-up question generation
- Specialty recommendation
- Doctor matching
- SQLite persistence
- Conversation memory
- Conversation retrieval
- Conversation deletion
- Swagger API documentation

---

## 👨‍💻 Development

This project is intended as an educational/software-development implementation of an AI-assisted patient intake workflow.

Before using it with real patients or real healthcare data, the system should undergo appropriate security, privacy, clinical, legal, and regulatory review.
