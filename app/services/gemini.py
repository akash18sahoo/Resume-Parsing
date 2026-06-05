import os
import json
import copy
from typing import Optional
from google import genai
from google.genai import types
from fastapi import HTTPException, status
from dotenv import load_dotenv

from app.models.resume import ResumeOutput

# Load environment variables
load_dotenv()

# Configure Google Gemini API using the new google-genai SDK
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise RuntimeError("GEMINI_API_KEY environment variable is not set in .env file.")

client = genai.Client(api_key=API_KEY)

# Choose model (defaulting to gemini-2.5-flash)
MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

# Fields that Gemini's Schema does not support (from Pydantic v2 JSON schema output)
_GEMINI_UNSUPPORTED_FIELDS = {"default", "title", "$schema", "additionalProperties", "examples"}

def _resolve_refs(schema: dict, defs: dict) -> dict:
    """
    Recursively resolves all $ref entries in a JSON schema using the provided $defs map.
    This is needed because Pydantic v2 uses $ref for nested model schemas.
    """
    if not isinstance(schema, dict):
        return schema

    # If this node is a $ref, replace it with the referenced definition
    if "$ref" in schema:
        ref_key = schema["$ref"].split("/")[-1]
        resolved = copy.deepcopy(defs.get(ref_key, {}))
        return _resolve_refs(resolved, defs)

    result = {}
    for key, value in schema.items():
        if key == "$defs":
            # Skip — we've already extracted defs; don't embed them inline
            continue
        elif isinstance(value, dict):
            result[key] = _resolve_refs(value, defs)
        elif isinstance(value, list):
            result[key] = [
                _resolve_refs(item, defs) if isinstance(item, dict) else item
                for item in value
            ]
        else:
            result[key] = value
    return result


def _strip_unsupported(schema: dict) -> dict:
    """
    Recursively removes JSON Schema fields that the Gemini API does not support.
    Gemini rejects: 'default', 'title', '$schema', 'additionalProperties', 'examples'.
    """
    if not isinstance(schema, dict):
        return schema

    cleaned = {}
    for key, value in schema.items():
        if key in _GEMINI_UNSUPPORTED_FIELDS:
            continue
        elif isinstance(value, dict):
            cleaned[key] = _strip_unsupported(value)
        elif isinstance(value, list):
            cleaned[key] = [
                _strip_unsupported(item) if isinstance(item, dict) else item
                for item in value
            ]
        else:
            cleaned[key] = value
    return cleaned


def build_gemini_schema(model) -> dict:
    """
    Converts a Pydantic model to a Gemini-compatible JSON schema dict by:
    1. Extracting the raw Pydantic v2 JSON schema
    2. Resolving all $ref/$defs references inline
    3. Stripping all Gemini-incompatible fields (default, title, etc.)
    """
    raw_schema = model.model_json_schema()
    defs = raw_schema.get("$defs", {})
    resolved = _resolve_refs(raw_schema, defs)
    return _strip_unsupported(resolved)


# Pre-build schema once at module load
RESUME_SCHEMA = build_gemini_schema(ResumeOutput)


# Define prompt instruction
PARSE_INSTRUCTION = """
You are an expert resume parsing system. Your task is to analyze the provided resume and extract all relevant candidate profile details into the requested schema structure.

Rules:
1. Do not invent, hallucinate, or extrapolate details. Only extract facts present in the text or image.
2. If a field is not found in the resume, leave it as null (or an empty list/array where appropriate).
3. Normalize fields like dates where possible (e.g., "Jan 2020" or "2020-01").
4. If the resume is an image, perform OCR visually and extract the layout contents.
5. In 'total_experience_years', calculate or estimate the total years of professional experience across all roles (as a float, e.g. 5.5). If not possible to estimate, set it to null.
6. For 'is_current' in work experience, check if the job is ongoing (e.g., end date is "Present", "Current", "Now", or null/blank while starting date is specified).
"""


async def parse_resume_text(text: str) -> ResumeOutput:
    """
    Sends extracted resume text to Gemini with a cleaned structured output schema.
    Returns validated ResumeOutput Pydantic model.
    """
    try:
        prompt = f"{PARSE_INSTRUCTION}\n\nHere is the resume content:\n{text}"

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=RESUME_SCHEMA,
            )
        )

        if not response.text:
            raise ValueError("Empty response received from Gemini API.")

        data = json.loads(response.text)
        return ResumeOutput(**data)

    except json.JSONDecodeError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Failed to parse Gemini output as JSON: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Gemini API error: {str(e)}"
        )


async def parse_resume_image(image_bytes: bytes, mime_type: str) -> ResumeOutput:
    """
    Sends resume image bytes directly to Gemini Vision model with a cleaned schema.
    Returns validated ResumeOutput Pydantic model.
    """
    try:
        prompt = f"{PARSE_INSTRUCTION}\n\nPlease analyze this resume image and extract its details."

        image_part = types.Part.from_bytes(data=image_bytes, mime_type=mime_type)

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=[prompt, image_part],
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=RESUME_SCHEMA,
            )
        )

        if not response.text:
            raise ValueError("Empty response received from Gemini API.")

        data = json.loads(response.text)
        return ResumeOutput(**data)

    except json.JSONDecodeError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Failed to parse Gemini vision output as JSON: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Gemini Vision API error: {str(e)}"
        )


async def parse_resume(
    text: Optional[str],
    image_bytes: Optional[bytes],
    mime_type: str
) -> ResumeOutput:
    """
    Main router function to invoke the appropriate Gemini mode.
    """
    if text:
        return await parse_resume_text(text)
    elif image_bytes:
        return await parse_resume_image(image_bytes, mime_type)
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No parsing input provided (both text and image bytes are empty)"
        )
