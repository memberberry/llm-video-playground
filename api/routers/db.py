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
