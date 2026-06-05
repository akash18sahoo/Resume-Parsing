import time
from fastapi import APIRouter, UploadFile, File, HTTPException, status
from app.models.resume import ParseResponse, ResumeOutput
from app.services.file_parser import extract_content
from app.services.gemini import parse_resume

router = APIRouter()

@router.post(
    "/parse",
    response_model=ParseResponse,
    status_code=status.HTTP_200_OK,
    summary="Upload and parse a resume",
    description="Uploads a PDF, DOCX, TXT, or Image resume and extracts structured details using Gemini AI."
)
async def parse_resume_endpoint(file: UploadFile = File(...)):
    start_time = time.time()
    
    # 1. Read file bytes
    try:
        file_bytes = await file.read()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to read uploaded file: {str(e)}"
        )
        
    filename = file.filename or "unknown_file"
    
    try:
        # 2. Extract content based on file type (either text or image bytes)
        text, image_bytes, file_type = await extract_content(file_bytes, filename)
        
        # Determine appropriate MIME type for images
        mime_type = file.content_type or "application/octet-stream"
        
        # 3. Call Gemini to parse details
        parsed_data = await parse_resume(text, image_bytes, mime_type)
        
        processing_time_ms = int((time.time() - start_time) * 1000)
        
        return ParseResponse(
            success=True,
            filename=filename,
            file_type=file_type,
            parsed_data=parsed_data,
            processing_time_ms=processing_time_ms,
            error=None
        )
        
    except HTTPException as he:
        # Re-raise HTTP exceptions from validation or extraction
        processing_time_ms = int((time.time() - start_time) * 1000)
        return ParseResponse(
            success=False,
            filename=filename,
            file_type="unknown",
            parsed_data=None,
            processing_time_ms=processing_time_ms,
            error=he.detail
        )
    except Exception as e:
        processing_time_ms = int((time.time() - start_time) * 1000)
        return ParseResponse(
            success=False,
            filename=filename,
            file_type="unknown",
            parsed_data=None,
            processing_time_ms=processing_time_ms,
            error=f"An unexpected parsing error occurred: {str(e)}"
        )

@router.get(
    "/health",
    status_code=status.HTTP_200_OK,
    summary="API Health check"
)
async def health_check():
    import os
    return {
        "status": "healthy",
        "model": os.getenv("GEMINI_MODEL", "gemini-1.5-flash"),
        "version": "1.0.0",
        "supported_formats": ["pdf", "docx", "txt", "png", "jpg", "jpeg", "webp"]
    }
