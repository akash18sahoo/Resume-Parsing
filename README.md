# Resume Parser - Gemini AI

An intelligent resume parsing API built with **FastAPI** and **Google Gemini AI**. Upload resumes in PDF, DOCX, TXT, or image formats and get structured JSON output with extracted candidate information.

## 🚀 Features

- 📄 Multi-format support: PDF, DOCX, TXT, PNG, JPG, JPEG, WEBP
- 🤖 Powered by Google Gemini AI for intelligent extraction
- ⚡ Fast async API with FastAPI + Uvicorn
- 📊 Structured JSON output with Pydantic validation
- 🔒 File size and type validation

## 📁 Project Structure

```
resumeparsing/
├── app/
│   ├── main.py           # FastAPI application entry point
│   ├── routers/
│   │   └── resume.py     # Resume parsing API routes
│   ├── services/
│   │   ├── gemini.py     # Gemini AI integration
│   │   └── file_parser.py # File reading utilities
│   └── models/
│       └── resume.py     # Pydantic data models
├── .env                  # Environment variables (create from .env.example)
├── .env.example          # Example environment file
├── requirements.txt      # Python dependencies
└── README.md
```

## 🛠️ Setup

### 1. Activate Virtual Environment
```bash
# Windows
.\venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 2. Configure Environment
```bash
copy .env.example .env
# Then edit .env and add your GEMINI_API_KEY
```

Get your API key at: https://aistudio.google.com/apikey

### 3. Run the Server
```bash
uvicorn app.main:app --reload
```

API will be available at: http://localhost:8000  
Interactive docs: http://localhost:8000/docs

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/parse` | Upload and parse a resume |
| GET | `/api/v1/health` | Health check |
| GET | `/docs` | Swagger UI |

## 📦 Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| google-generativeai | ≥0.8.0 | Gemini AI API |
| fastapi | ≥0.115.0 | Web framework |
| uvicorn | ≥0.32.0 | ASGI server |
| PyPDF2 / pdfminer.six / pymupdf | latest | PDF parsing |
| python-docx | ≥1.1.0 | Word document parsing |
| Pillow | ≥11.0.0 | Image processing |
| pydantic | ≥2.10.0 | Data validation |
| python-dotenv | ≥1.0.0 | Environment management |
