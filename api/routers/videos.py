import logging
from typing import List
import base64
import os
import aiofiles
from fastapi import APIRouter, File, HTTPException, UploadFile, BackgroundTasks
from api.core.settings import settings
from api.database import (
    add_video_entry,
    get_videos,
    get_video,
    soft_delete_video,
)
from api.models import Video
from api.services import upload_video_to_gemini_and_update_db, get_file_name, client

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


router = APIRouter(
    prefix="/videos",
    tags=["Manage Videos"],
)


@router.post("/upload")
async def upload_video(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    """
    Uploads a video file, generates a thumbnail, and stores metadata in the database.
    The actual upload and processing happens in the background.
    """

    video_dir = settings.VIDEO_STORAGE_DIR
    display_name = get_file_name(file.filename)

    file_path = os.path.join(video_dir, file.filename)

    async with aiofiles.open(file_path, 'wb') as out_file:
        contents = await file.read()
        await out_file.write(contents)

    
    video_id = add_video_entry(
        display_name=display_name,
        mime_type=file.content_type,
        size_bytes=len(contents),
        path=file_path
    )


    upload_video_to_gemini_and_update_db(
        video_id,
        file_path,
        display_name,
        file.content_type,
    )


    return {"message": "successfully uploaded and saved video", "video_id": video_id, "display_name": display_name, "path": file_path}



@router.get("/", response_model=List[Video])
async def list_videos():
    """
    Lists all uploaded video files from the local database.
    """
    try:
        videos_from_db = get_videos()
        print(f"Retrieved {len(videos_from_db)} videos from the database.")
        response_videos = []
        for video_data in videos_from_db:
            video_dict = dict(video_data)
            print("video_dict:", video_dict)
            if video_dict.get("thumbnail") != None:
                video_dict["thumbnail"] = base64.b64encode(video_dict["thumbnail"]).decode("utf-8")
            else:
                raise ValueError("Thumbnail is None, cannot encode to base64")
            response_videos.append(Video(**video_dict))
        return response_videos
        
    except Exception as e:
        log.error(f"Error retrieving videos: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{video_id}")
async def delete_video(video_id: int):
    """
    This endpoint deletes a video from the local storage and Gemini.
    It marks the video as deleted in our database.
    """
    try:
        video_data = get_video(video_id)
        if not video_data:
            raise HTTPException(status_code=404, detail="Video not found")

        if video_data.get("path") and os.path.exists(video_data["path"]):
            os.remove(video_data["path"])
            log.info(f"Deleted file {video_data['path']} from local storage.")

        if video_data["gemini_name"]:
            try:
                client.files.delete(name=video_data["gemini_name"])
                log.info(f"Deleted file {video_data['gemini_name']} from Gemini.")
                
            except Exception as e:
                # Log the error but proceed to mark as deleted in our DB
                log.error(f"Could not delete file {video_data['gemini_name']} from Gemini: {e}")
        
        soft_delete_video(video_id)
        
        return {
            "status": "deleted",
            "video_id": video_id
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
