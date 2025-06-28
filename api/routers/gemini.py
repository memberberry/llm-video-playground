import logging
from typing import Dict, Any
from fastapi import APIRouter, HTTPException
from api.core.settings import settings
from google.genai import errors
from api.services import get_uploaded_file, client
from api.database import add_history_entry
from api.models import GeminiFileRequest, GeminiStructRequest
log = logging.getLogger(__name__)
log.setLevel(settings.LOG_LEVEL)

router = APIRouter()


router = APIRouter(
    prefix="/gemini",
    tags=["Request Gemini"],
)

@router.post("/with_videos")
def request_gemini_files(request: GeminiFileRequest) -> Dict[str, Any]:
    uploads = [get_uploaded_file(id) for id in request.video_ids]
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
        video_ids=request.video_ids
    )

    return {"text": response.text}

@router.get("/models")
def list_gemini_models():
    try:
        models = client.models.list()
        return {"models": [model.name.split("/")[1] for model in models]}
    
    except errors.APIError as e:
        log.error(f"Gemini API error occurred: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/with_videos_struct")
def request_gemini_files_struct(request: GeminiStructRequest) -> Dict[str, Any]:
    uploads = [get_uploaded_file(id) for id in request.video_ids]
    
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
        video_ids=request.video_ids
    )

    return {"parsed": response.parsed}
