import uvicorn
from fastapi import FastAPI
from database import engine, Base
from routers import file as FileRouter


if __name__ == '__main__':

    Base.metadata.create_all(bind=engine)

    app = FastAPI()
    app.include_router(FileRouter.router, prefix="/file")

    uvicorn.run(
        app="main:app",
        host="0.0.0.0",
        port=8080,
        reload=True
    )
