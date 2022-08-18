from typing import Union
from fastapi import FastAPI
from sqlmodel import SQLModel
from .db.conn import connect_to_db
from .routers import card, tag


engine = connect_to_db()

SQLModel.metadata.create_all(engine)

app = FastAPI()

app.include_router(card.router)
# app.include_router(tag.router)

@app.get("/", status_code=200)
async def root():
    return {"message": "Hello World"}
