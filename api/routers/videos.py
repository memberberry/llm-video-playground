import time
import io
import logging
from typing import Optional

from google import genai
from google.genai.types import UploadFileConfig
from fastapi import APIRouter, File, HTTPException, UploadFile

from api.core.settings import settings

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

# This is a placeholder for your Gemini client initialization.
# In a real application, you would initialize this client in a more
# robust way, for example, in your app's startup event.
# You should replace "YOUR_API_KEY" with your actual key,
# preferably loaded from environment variables.
if not settings.GEMINI_API_KEY:
    # This is not recommended for production.
    # It's better to fail or have a clear configuration error.
    raise RuntimeError("GEMINI_API_KEY environment variable not set.")

client = genai.Client(api_key=settings.GEMINI_API_KEY)

router = APIRouter(
    prefix="/videos",
    tags=["Manage Videos"],
)

def get_file_name(file):

    # remove extension like ".mp4"
    file_name = "".join(file.split(".")[:-1])
    # remove path like "path/to/file/file_name"
    file_name = "".join(file_name.split("/")[-1:])
    return file_name

def get_uploaded_file(name: str):
    """
    Retrieves an uploaded file by its name.
    """
    try:
        # The python SDK uses `genai.get_file(name=name)`
        return client.files.get(name=name)
    except genai.errors.NotFoundError:
        return None  # File not found
    except Exception as e:
        log.error(f"Error retrieving file {name}: {e}")
        raise e

def upload_file_to_gemini(
    file: io.IOBase, display_name: str, mime_type: Optional[str]
):
    """
    Uploads file contents to Gemini and waits for it to be processed.
    """
    print(f"Uploading file contents for: {display_name}")
    # The python SDK uses `genai.upload_file`

    file_config = UploadFileConfig(
        display_name=display_name,
        mime_type=mime_type or "application/octet-stream"
    )

    upload = client.files.upload(
        file=file,
        config=file_config,
    )

    while upload.state.name == "PROCESSING":
        print("Waiting for processing...")
        time.sleep(2)
        # The python SDK uses `genai.get_file(name=upload.name)`
        upload = client.files.get(name=upload.name)

    if upload.state.name == "FAILED":
        print("Upload failed")
        raise ValueError(f"File upload failed: {upload.state.name}")

    return upload


@router.post("/upload")
async def upload_video(file: UploadFile = File(...)):
    """
    Uploads a video file to Google Gemini.
    """
    try:
        # Read the file content
        contents = await file.read()
        display_name = get_file_name(file.filename)
        # Upload the file to Gemini
        gemini_file = upload_file_to_gemini(
            file=io.BytesIO(contents),
            display_name=display_name,
            mime_type=file.content_type,
        )

        print(f"File uploaded successfully: {gemini_file}")

        return {
            "filename": file.filename,
            "display_name": display_name,
            "gemini_uri": gemini_file.uri,
            "gemini_name": gemini_file.name,
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/")
async def list_videos():
    """
    Lists all uploaded video files from Google Gemini.
    """
    try:
        files = client.files.list()
        return [
            {
                "name": f.name,
                "display_name": f.display_name,
                "uri": f.uri,
                "create_time": f.create_time,
                "mime_type": f.mime_type,
                "size": f.size_bytes,
                "length": f.video_metadata['videoDuration'] if f.video_metadata else None,
            }
            for f in files
        ]
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{display_name}")
async def delete_video(name: str):
    """
    Deletes a file from Google Gemini by its name.
    """
    try:
        #...delete(name: str, config: Optional[DeleteFileConfig] = None)
        # DeleteFileConfig():
        #     httpOptions: Optional[HttpOptions] = None

        # class HttpOptions(_common.BaseModel):
        #   """HTTP options to be used in each of the requests."""

        #   base_url: Optional[str] = Field(
        #       default=None,
        #       description="""The base URL for the AI platform service endpoint.""",
        #   )
        #   api_version: Optional[str] = Field(
        #       default=None, description="""Specifies the version of the API to use."""
        #   )
        #   headers: Optional[dict[str, str]] = Field(
        #       default=None,
        #       description="""Additional HTTP headers to be sent with the request.""",
        #   )
        #   timeout: Optional[int] = Field(
        #       default=None, description="""Timeout for the request in milliseconds."""
        #   )
        #   client_args: Optional[dict[str, Any]] = Field(
        #       default=None, description="""Args passed to the HTTP client."""
        #   )
        #   async_client_args: Optional[dict[str, Any]] = Field(
        #       default=None, description="""Args passed to the async HTTP client."""
        #   )
        #   extra_body: Optional[dict[str, Any]] = Field(
        #       default=None,
        #       description="""Extra parameters to add to the request body.""",
        #   )
        #   retry_options: Optional[HttpRetryOptions] = Field(
        #       default=None, description="""HTTP retry options for the request."""
        #   )

        client.files.delete(name=name)
        return {
            "status": "deleted", 
            "upload_name": name
            }
    
    except Exception as e:
        # Handle cases where the file is not found or other API errors
        raise HTTPException(status_code=500, detail=str(e))
