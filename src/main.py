from fastapi import FastAPI

from src.db.db import create_db_and_tables
from src.router.app_router import router

app = FastAPI()

app.include_router(router)


@app.on_event('startup')
def startup():
    create_db_and_tables()
    print("Database initialized")
