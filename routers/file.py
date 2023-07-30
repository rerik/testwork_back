from fastapi import APIRouter, Depends, UploadFile
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from database import get_db

from services import file as FileService
from dto import file as FileDTO

from datetime import datetime
from os.path import exists, join
from os import remove, mkdir, rename


router = APIRouter()


STORAGE_PATH = "storage"


@router.post("/upload", tags=["file"])
async def create_upload_file(file: UploadFile, path: str = "", comment: str = "", db: Session = Depends(get_db)):

    if not exists(join(STORAGE_PATH, path)):
        mkdir(join(STORAGE_PATH, path))

    fullpath = join(STORAGE_PATH, path, file.filename)

    point = file.filename.rfind('.')

    name = file.filename[:point]
    extension = file.filename[point:]

    if exists(fullpath):
        old_file = FileService.get_file(join(path, file.filename), db)
        file_data = {
            "name": name,
            "extension": extension,
            "size": file.size,
            "path": path,
            "created_at": old_file.created_at,
            "updated_at": datetime.now(),
            "comment": comment
        }
        FileService.update_file(FileDTO.File(**file_data), join(path, file.filename), db)
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

    with open(fullpath, 'wb+') as new_file:
        new_file.write(file.file.read())

    return {"filename": file.filename}


@router.post("/update", tags=["file"])
async def update_file(filepath: str, name: str = None, path: str = None, comment: str = None,
                      db: Session = Depends(get_db)):
    if exists(join(STORAGE_PATH, filepath)):
        if not exists(join(STORAGE_PATH, path)):
            mkdir(join(STORAGE_PATH, path))
        file = FileService.get_file(filepath, db)
        if name or path:
            rename(
                join(STORAGE_PATH, filepath),
                join(STORAGE_PATH, path or file.path, name or file.name) + file.extension)
        file_data = {
            "name": name or file.name,
            "extension": file.extension,
            "size": file.size,
            "path": path or file.path,
            "created_at": file.created_at,
            "updated_at": datetime.now(),
            "comment": comment or file.comment
        }
        FileService.update_file(FileDTO.File(**file_data), filepath, db)
    else:
        print(f"No file {filepath} to update")


@router.get("/download", tags=["file"])
async def download_file(filepath: str = None):
    fullpath = STORAGE_PATH + filepath
    if exists(fullpath):
        return FileResponse(path=fullpath)
    else:
        print(f"No file {filepath} to download")


@router.get('/', tags=["file"])
async def get_all(db: Session = Depends(get_db)):
    return FileService.get_all_files(db)


@router.get('/{filepath}', tags=["file"])
async def get(filepath: str = None, db: Session = Depends(get_db)):
    return FileService.get_file(filepath, db)


@router.get('/search/{filepath}', tags=["file"])
async def search(filepath: str = None, db: Session = Depends(get_db)):
    return FileService.search(filepath, db)


@router.delete('/{filepath}', tags=["file"])
async def delete(filepath: str = None, db: Session = Depends(get_db)):
    fullpath = STORAGE_PATH + filepath
    if exists(fullpath):
        remove(fullpath)
    FileService.remove_file(filepath, db)
