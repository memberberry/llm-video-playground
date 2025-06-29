from fastapi import APIRouter, Depends
from typing import List, Dict, Any
from .. import models
from .. import database

router = APIRouter(
    prefix="/database",
    tags=["Access DB"],
)

@router.get("/history", response_model=List[models.History])
def get_history():
    return database.get_history()

@router.get("/history_with_videos", response_model=List[Dict[str, Any]])
def get_history_with_videos():
    return database.get_history_with_videos()

@router.get("/history/{hash}", response_model=models.HistoryWithVideos)
def get_event_from_history_with_videos_by_hash(hash: str):
    return database.get_event_from_history_with_videos_by_hash(hash)
