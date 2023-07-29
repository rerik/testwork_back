from fastapi import APIRouter, Depends, UploadFile
from sqlalchemy.orm import Session
from database import get_db

from services import file as FileService
from dto import file as FileDTO

from datetime import datetime
from os.path import exists


router = APIRouter()


STORAGE_PATH = "storage/"


@router.post('/', tags=["file"])
async def create(data: FileDTO.File = None, db: Session = Depends(get_db)):
    return FileService.create_file(data, db)


@router.post("/uploadfile/")
async def create_upload_file(file: UploadFile, path: str = "", comment: str = "", db: Session = Depends(get_db)):

    fullpath = STORAGE_PATH + path + file.filename

    point = file.filename.rfind('.')

    name = file.filename[:point]
    extension = file.filename[point:]

    if exists(fullpath):
        old_file = FileService.get_file(path + file.filename, db)
        file_data = {
            "name": name,
            "extension": extension,
            "size": file.size,
            "path": path,
            "created_at": old_file.created_at,
            "updated_at": datetime.now(),
            "comment": comment
        }
        FileService.update_file(FileDTO.File(**file_data), path + file.filename, db)
    else:
        file_data = {
            "name": name,
            "extension": extension,
            "size": file.size,
            "path": path,
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
            "comment": comment
        }
        FileService.create_file(FileDTO.File(**file_data), db)

    with open(STORAGE_PATH + path + file.filename, 'wb+') as new_file:
        new_file.write(file.file.read())

    return {"filename": file.filename}


@router.get('/', tags=["file"])
async def get(filepath: str = None, db: Session = Depends(get_db)):
    match filepath:
        case "*":
            return FileService.get_all_files(db)
        case _:
            return FileService.get_file(filepath, db)