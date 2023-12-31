from fastapi import APIRouter, Depends, UploadFile
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from database import get_db

from services import file as FileService
from dto import file as FileDTO

from datetime import datetime
from os.path import exists, join, getsize
from os import remove, mkdir, rename, walk, sep

from logging import warning

from yaml import safe_load


router = APIRouter()

with open('config.yml') as f:
    STORAGE_PATH = safe_load(f)["storage_path"]


# something about naming of names and paths in this code
#
# storage/dir/file.ext
#             ^^^^     name
#
# storage/dir/file.ext
#             ^^^^^^^^ filename
#
# storage/dir/file.ext
#         ^^^          path
#
# storage/dir/file.ext
#         ^^^^^^^^^^^^ filepath
#
# storage/dir/file.ext
# ^^^^^^^^^^^^^^^^^^^^ fullpath


@router.post("/upload", tags=["file"])
async def create_upload_file(file: UploadFile, path: str = "", comment: str = "", db: Session = Depends(get_db)):

    # check of given path and create it if it doesn't exist
    if not exists(join(STORAGE_PATH, path)):
        mkdir(join(STORAGE_PATH, path))

    fullpath = join(STORAGE_PATH, path, file.filename)

    point = file.filename.rfind('.')

    name = file.filename[:point]
    extension = file.filename[point:]

    file_data = {
        "name": name,
        "extension": extension,
        "size": file.size,
        "path": path,
        "updated_at": datetime.now(),
        "comment": comment
    }

    # if file exists yet, just update it
    if exists(fullpath):
        old_file = FileService.get_file(join(path, file.filename), db)
        file_data["created_at"] = old_file.created_at
        FileService.update_file(FileDTO.File(**file_data), join(path, file.filename), db)
    else:
        file_data["created_at"] = datetime.now()
        FileService.create_file(FileDTO.File(**file_data), db)

    with open(fullpath, 'wb+') as new_file:
        new_file.write(file.file.read())

    return {"filename": file.filename}


@router.post("/update", tags=["file"])
async def update_file(filepath: str, name: str = None, path: str = None, comment: str = None,
                      db: Session = Depends(get_db)):

    # because we can't update file we haven't
    if exists(join(STORAGE_PATH, filepath)):

        # commented as impossible case
        # if not exists(join(STORAGE_PATH, path)):
        #     mkdir(join(STORAGE_PATH, path))

        file = FileService.get_file(filepath, db)

        # change name and location if it needs
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
        warning(f"No file {filepath} to update")


@router.post("/actualize", tags=["file"])
async def actualize(db: Session = Depends(get_db)):

    ans = {
        "removed": [],
        "created": []
    }

    # check if files in DB really exists
    files = FileService.get_all_files(db)
    for file in files:
        filepath = join(file.path, file.name) + file.extension
        if not exists(join(STORAGE_PATH, filepath)):
            FileService.remove_file(filepath, db)
            ans["removed"].append(filepath)

    # check if files in storage are registered in DB
    for root, dirs, files in walk(STORAGE_PATH):
        for filename in files:
            path = sep.join(root.split(sep)[1:])
            file = FileService.get_file(join(path, filename), db)
            if not file:
                name, extension = filename.split('.')
                file_data = {
                    "name": name,
                    "extension": extension,
                    "size": getsize(join(STORAGE_PATH, path, filename)),
                    "path": path,
                    "created_at": datetime.now(),
                    "updated_at": datetime.now(),
                    "comment": "created automatically from file manually added to the storage"
                }
                FileService.create_file(FileDTO.File(**file_data), db)
                ans["created"].append(join(path, filename))

    return ans


@router.get("/download", tags=["file"])
async def download_file(filepath: str = None):
    fullpath = STORAGE_PATH + filepath
    if exists(fullpath):
        return FileResponse(path=fullpath)
    else:
        warning(f"No file {filepath} to download")


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
