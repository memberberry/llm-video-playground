import logging
from typing import List, Dict, Any
from google import genai
from fastapi import APIRouter, HTTPException
from api.core.settings import settings
from google.genai import errors
from api.routers.videos import get_uploaded_file
from pydantic import BaseModel
from api.database import add_history_entry
from api.models import GeminiFileRequest, GeminiStructRequest
log = logging.getLogger(__name__)
log.setLevel(settings.LOG_LEVEL)

client = genai.Client(api_key=settings.GEMINI_API_KEY)
router = APIRouter()


router = APIRouter(
    prefix="/gemini",
    tags=["Request Gemini"],
)

@router.post("/with_videos")
def request_gemini_files(request: GeminiFileRequest) -> Dict[str, Any]:
    uploads = [get_uploaded_file(name) for name in request.files]
    try:
        response = client.models.generate_content(
            model=request.model,
            contents=[
                *uploads,
                request.prompt
            ]
        )

    except errors.APIError as e:
        log.error(f"Gemini API error occurred: {e}")
        raise HTTPException(status_code=500, detail=str(e))

    add_history_entry(
        prompt=request.prompt,
        model=request.model,
        output=response.text,
        structured_output=None,
        videos=request.files
    )

    return {"text": response.text}

@router.get("/models")
def list_gemini_models():
    try:
        models = client.models.list()
        return {"models": [model.name for model in models]}
    
    except errors.APIError as e:
        log.error(f"Gemini API error occurred: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/with_videos_struct")
def request_gemini_files_struct(request: GeminiStructRequest) -> Dict[str, Any]:
    uploads = [get_uploaded_file(name) for name in request.files]
    
    try:
        response = client.models.generate_content(
            model=request.model,
            contents=[
                *uploads,
                request.prompt
            ],
            config={
                "response_mime_type": "application/json",
                "response_schema": request.response_schema
            }
        )

    except errors.APIError as e:
        log.error(f"Gemini API error occurred: {e}")
        raise HTTPException(status_code=500, detail=str(e))

    output_for_db = response.parsed

    add_history_entry(
        prompt=request.prompt,
        model=request.model,
        output=None,
        structured_output=output_for_db,
        videos=request.files
    )

    return {"parsed": response.parsed}
