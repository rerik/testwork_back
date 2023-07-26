from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db

from services import file as FileService
from dto import file as FileDTO


router = APIRouter()


@router.post('/', tags=["file"])
async def create(data: FileDTO.File = None, db: Session = Depends(get_db)):
    return FileService.create_file(data, db)


@router.get('/', tags=["file"])
async def get(filepath: str = None, db: Session = Depends(get_db)):
    return FileService.get_file(filepath, db)
