from fastapi import FastAPI
from .db.conn import connect_to_db, connect_to_sqlite_db
from .routers import card, tag
from .schemas.card import Card
from .schemas.tag import Tag
from .schemas.card_has_tag import CardHasTag
from .db.tables import metadata_obj
from sqlalchemy.ext.declarative import declarative_base

engine = connect_to_sqlite_db() # conexão com o banco de dados
if engine:
    print('Connected to database')

Base = declarative_base()
# Base.metadata.create_all(bind=engine) 
metadata_obj.create_all(bind=engine) # criação da tabelas no banco de dados


app = FastAPI() # criação do app

app.include_router(card.router) # incluindo o router de cards
app.include_router(tag.router) # incluindo o router de tags

@app.get("/", status_code=200)
async def root():
    return {"message": "Hello World"}
