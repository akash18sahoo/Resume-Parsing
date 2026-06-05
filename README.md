# 🤖 Gemini AI Resume Parser

> **⚡ Local Web App Link:** [http://localhost:8000](http://localhost:8000) (Click here to open the application when running locally)

An intelligent, full-stack resume parsing system that extracts candidate information from multiple file formats (PDF, DOCX, TXT, and Images) and converts it into structured, validated JSON using **FastAPI** and the modern **Google GenAI SDK** (`gemini-2.5-flash`).

Featuring a premium, single-page dark-mode frontend with glassmorphism design, real-time file upload, parsing status animations, and interactive JSON visualization.

---

## 🚀 Key Features

- **Multi-Format Ingestion**: Supports parsing resumes from PDF (`.pdf`), Word Documents (`.docx`), Plain Text (`.txt`), and Images (`.png`, `.jpg`, `.jpeg`, `.webp`).
- **Structured JSON Output**: Guarantees highly accurate JSON matching a robust Pydantic schema (including contact details, education, work experience, projects, skills, and certifications).
- **Modern SDK Integration**: Uses the new `google-genai` client SDK with native schema enforcement.
- **Pydantic-to-Gemini Schema Cleaner**: Includes a custom parser that translates complex Pydantic v2 schemas into API-compliant Gemini schemas, resolving type/metadata compatibility issues.
- **Vibrant Glassmorphism UI**: Beautiful, interactive dark-mode user interface with a drag-and-drop file target, live parsing states, and expandable/collapsible JSON views.
- **FastAPI Backend**: Built on a high-performance, asynchronous FastAPI backend with CORS support and clean endpoint routing.

---

## 🛠️ Tech Stack

### Backend
- **Framework**: FastAPI (Asynchronous Python Web Framework)
- **AI Integration**: Google GenAI SDK (`google-genai>=1.0.0`)
- **Model**: `gemini-2.5-flash`
- **Data Validation**: Pydantic v2
- **Document Extractors**:
  - `PyMuPDF` (high-performance PDF text extractor)
  - `python-docx` (Microsoft Word XML parser)
  - `Pillow` (image formatting and processing)

### Frontend
- **Structure**: Vanilla HTML5 (semantic layout, drag-and-drop file uploads)
- **Styling**: Pure CSS3 (Dark-mode, Glassmorphism, CSS Grid & Flexbox, smooth custom transition keyframes)
- **Logic**: Vanilla JavaScript (`fetch` API, state management, dynamic DOM rendering)
- **Typography**: Google Fonts (Inter & Outfit)

---

## 📁 Project Structure

```text
resumeparsing/
├── app/
│   ├── __init__.py
│   ├── main.py               # FastAPI app initialization, middleware & static mounts
│   ├── models/
│   │   ├── __init__.py
│   │   └── resume.py         # Pydantic response models (ResumeOutput, ParseResponse)
│   ├── routers/
│   │   ├── __init__.py
│   │   └── resume.py         # API Endpoints (/api/v1/parse & /api/v1/health)
│   ├── services/
│   │   ├── __init__.py
│   │   ├── file_parser.py    # Raw text extraction from PDF, DOCX, TXT
│   │   └── gemini.py         # Gemini client wrapper & Pydantic schema helper
│   └── static/
│       └── index.html        # Premium Glassmorphism web app frontend
├── .env.example              # Template for environment configuration
├── .gitignore                # Excludes private study guides, venv, and keys
├── requirements.txt          # Python dependencies list
└── README.md                 # Project documentation
```

---

## ⚙️ Installation & Setup

### 1. Clone & Navigate to Workspace
```bash
git clone https://github.com/akash18sahoo/Resume-Parsing.git
cd Resume-Parsing
```

### 2. Configure Virtual Environment

**On Windows:**
```powershell
python -m venv venv
.\venv\Scripts\activate
```

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Setup Environment Variables
Create a `.env` file in the root directory:
```bash
# Copy template
cp .env.example .env
```
Open `.env` and configure your settings:
```ini
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-2.5-flash
PORT=8000
```
> Get your free Gemini API Key from the [Google AI Studio Console](https://aistudio.google.com/).

### 5. Run the Server
Start the FastAPI server locally:
```bash
uvicorn app.main:app --reload
```
- **Web App URL**: `http://127.0.0.1:8000/`
- **Interactive Swagger Documentation**: `http://127.0.0.1:8000/docs`

---

## 📡 API Reference

### 1. Parse Resume
- **Endpoint**: `/api/v1/parse`
- **Method**: `POST`
- **Content-Type**: `multipart/form-data`
- **Request Body**:
  - `file`: The resume file (PDF, DOCX, TXT, or Image)

**Sample Success Response (`200 OK`)**:
```json
{
  "success": true,
  "data": {
    "contact_info": {
      "name": "Jane Doe",
      "email": "jane.doe@example.com",
      "phone": "+1-555-0199",
      "location": "San Francisco, CA",
      "website": "https://janedoe.dev"
    },
    "education": [
      {
        "institution": "Stanford University",
        "degree": "B.S. in Computer Science",
        "field_of_study": "Computer Science",
        "start_date": "2018",
        "end_date": "2022",
        "gpa": "3.8"
      }
    ],
    "work_experience": [
      {
        "company": "Tech Corp",
        "position": "Software Engineer",
        "start_date": "June 2022",
        "end_date": "Present",
        "description": "Designed and maintained scalable FastAPI microservices."
      }
    ],
    "skills": ["Python", "FastAPI", "PostgreSQL", "Docker", "Git", "React"],
    "projects": [],
    "certifications": []
  },
  "error": null
}
```

### 2. Health Check
- **Endpoint**: `/api/v1/health`
- **Method**: `GET`
- **Response**:
  ```json
  {
    "status": "healthy",
    "model": "gemini-2.5-flash"
  }
  ```

---

## 🛡️ Validation & Reliability Details

- **Schema Cleaner Engine**: Pydantic v2's native JSON Schema outputs include unsupported fields like `"default"`, `"title"`, `$ref`, and `$defs` which trigger schema errors in the Gemini API. The customized `build_gemini_schema()` parses the Pydantic metadata graph recursively, resolving referenced schemas inline and filtering out disallowed fields.
- **Dynamic Input Routing**: 
  - Standard text resumes (PDF, DOCX, TXT) have their text extracted and sent as a structured text prompt for high token efficiency.
  - Image resumes (PNG, JPG, WEBP) are sent as image bytes (`image/png`, etc.) directly to the Gemini Vision multimodal model to bypass OCR step-loss.

---

## 📄 License
This project is licensed under the MIT License. See the LICENSE file for details.
