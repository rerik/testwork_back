from pydantic import BaseModel
from datetime import datetime


class File(BaseModel):
    name: str
    extension: str
    size: int
    path: str
    created_at: datetime
    updated_at: datetime
    comment: str
