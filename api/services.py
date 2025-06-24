import io
import time
import logging
import cv2
import numpy as np
from typing import Optional
from api.exceptions import GeminiUploadFailed
from google import genai
from google.genai.types import UploadFileConfig

from api.core.settings import settings
from api.database import (
    get_video,
    update_video_upload_failed,
    update_video_upload_success,
)

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

if not settings.GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY environment variable not set.")

client = genai.Client(api_key=settings.GEMINI_API_KEY)


def get_file_name(file):
    file_name = "".join(file.split(".")[:-1])
    file_name = "".join(file_name.split("/")[-1:])
    return file_name


def generate_thumbnail(video_path: str) -> bytes:
    """Generates a thumbnail from a video file."""
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        raise ValueError("Could not open video file")

    ret, frame = cap.read()
    cap.release()

    if not ret:
        raise ValueError("Could not read frame from video")

    is_success, buffer = cv2.imencode(".jpg", frame)
    if not is_success:
        raise ValueError("Could not encode frame to JPEG")

    return buffer.tobytes()


def upload_video_to_gemini_and_update_db(
    video_id: int,
    file_path: str,
    display_name: str,
    mime_type: Optional[str],
):
    """Uploads a video to Gemini, generates a thumbnail, and updates the database."""
    try:
        # Upload the file to Gemini
        print(f"Uploading file: {display_name}")
        upload = client.files.upload(
            file=display_name,
            mime_type=mime_type
        )

        while upload.state.name == "PROCESSING":
            print("Waiting for processing...")
            time.sleep(2)
            upload = client.files.get(name=upload.name)

        if upload.state.name == "FAILED":
            raise GeminiUploadFailed(f"upload status: {upload.state.name}")

        # Generate thumbnail
        thumbnail_bytes = generate_thumbnail(file_path)


        update_video_upload_success(
            video_id=video_id,
            video_uri=upload.uri,
            thumbnail=thumbnail_bytes,
            gemini_name=upload.name,
        )
        print(f"File {display_name} processed and database updated.")

    except Exception as e:
        log.error(f"Error processing video {display_name}: {e}")
        update_video_upload_failed(video_id)
        raise e


def get_uploaded_file(video_id: int):
    """
    Retrieves an uploaded file from the database and returns a genai.File object.
    """
    video_data = get_video(video_id)
    if not video_data or not video_data["gemini_name"]:
        raise ValueError(f"Video with ID {video_id} not found or not uploaded to Gemini.")
    
    return client.files.get(name=video_data["gemini_name"])
