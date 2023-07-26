from models.file import File
from sqlalchemy.orm import Session
from dto.file import File as FileData


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

    try:
        db.add(file)
        db.commit()
        db.refresh(file)
    except Exception as e:
        print(e)

    return file


def get_file(filepath: str, db: Session):
    point = filepath.rfind('.')
    slash = filepath.rfind('/')
    path = filepath[:slash+1]
    name = filepath[slash+1:point]
    extension = filepath[point:]
    return db.query(File).filter(
        File.name == name,
        File.extension == extension,
        File.path == path
    ).first()
