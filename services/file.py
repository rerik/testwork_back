from models.file import File
from sqlalchemy.orm import Session
from dto.file import File as FileData

from logging import info, critical

from os.path import exists
from os import mkdir


def parse_path(path: str) -> tuple[str, str, str]:

    point = path.rfind('.')
    slash = path.rfind('/')

    name = path[slash + 1:point]
    extension = path[point:]
    path = path[:slash + 1]

    return path, name, extension


def execute(file, db: Session) -> None:
    try:
        db.add(file)
        db.commit()
        db.refresh(file)
    except Exception as e:
        critical(e)


def create_file(data: FileData, db: Session) -> File:

    file = File(
        name=data.name,
        extension=data.extension,
        size=data.size,
        path=data.path,
        created_at=data.created_at,
        updated_at=data.updated_at,
        comment=data.comment
    )

    execute(file, db)

    return file


def update_file(data: FileData, filepath: str, db: Session):

    path, name, extension = parse_path(filepath)

    file = db.query(File).filter(
        File.name == name,
        File.extension == extension,
        File.path == path
    ).first()

    file.name = data.name
    file.extension = data.extension
    file.size = data.size
    file.path = data.path
    file.created_at = data.created_at
    file.updated_at = data.updated_at
    file.comment = data.comment

    execute(file, db)

    return file


def get_file(filepath: str, db: Session):

    path, name, extension = parse_path(filepath)

    return db.query(File).filter(
        File.name == name,
        File.extension == extension,
        File.path == path
    ).first()


def get_all_files(db: Session):
    return db.query(File).all()


def search(path: str, db: Session):
    return db.query(File).filter(
        File.path.ilike(path)
    ).all()


def remove_file(filepath: str, db: Session):

    path, name, extension = parse_path(filepath)

    file = db.query(File).filter(
        File.name == name,
        File.extension == extension,
        File.path == path
    ).delete()

    db.commit()

    return file


def check_folder(path: str):
    if not exists(path):
        mkdir(path)
        info(f"folder {path} was created")
