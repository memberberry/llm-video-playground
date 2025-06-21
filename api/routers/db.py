from fastapi import APIRouter, Depends
from typing import List
from .. import models
from .. import database

router = APIRouter(
    prefix="/database",
    tags=["Access DB"],
)

@router.get("/history", response_model=List[models.History])
def get_history():
    return database.get_history()
