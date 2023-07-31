import uvicorn
from fastapi import FastAPI
from database import engine, Base
from routers import file as FileRouter
from services.file import check_folder

from logging import basicConfig, WARNING, CRITICAL

from yaml import safe_load


Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(FileRouter.router, prefix="/file")

if __name__ == '__main__':

    with open('config.yml') as f:
        config = safe_load(f)

    check_folder(config["storage_path"])

    basicConfig(level=WARNING, filename="warnings.log", filemode="w")
    basicConfig(level=CRITICAL, filename="criticals.log", filemode="w")

    uvicorn.run(
        app="main:app",
        host="0.0.0.0",
        port=config["port"],
        reload=True
    )
