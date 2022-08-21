from typing import Optional, List
from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from ..schemas.card import Card, CardCreate, CardGet, CardUpdate
from ..schemas.tag import Tag, TagCreate, TagUpdate
from ..schemas.card_has_tag import CardHasTag
from ..db.crud import DBCrud

router = APIRouter()

crud = DBCrud()

@router.get("/tags", status_code=200, response_model=List[Tag])
async def get_tags():
    tags = crud.get_tags()

    return tags

@router.get("/tags/{id}", status_code=200, tags=["tags"])
async def get_tag(id: int):
    tag = crud.get_tag(id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    return tag

@router.post("/tags", status_code=201, tags=["tags"])
async def create_tag(tag_info: TagCreate):
    if tag_info.name in [tag.name for tag in crud.get_tags()]:
        raise HTTPException(status_code=400, detail="Tag name already exists")
    try:
        tag = crud.create_tag(tag_info)
        return {
            'message': 'Tag criada com sucesso',
            'tag': tag
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=e)

@router.put("/tags/{id}", status_code=200, tags=["tags"])
async def update_tag(id: int, tag: TagUpdate):
    tag_db = crud.update_tag(id, tag)
    if not tag_db:
        raise HTTPException(status_code=404, detail="Tag not found")
    return {
        'message': 'Tag atualizada com sucesso',
        'tag': tag_db
    }

@router.delete("/tags/{id}", status_code=200, tags=["tags"])
async def delete_tag(id: int):
    try:
        crud.delete_tag(id)
        return {
            'message': 'Tag deletada com sucesso'
        }
    except Exception as e:
        raise HTTPException(status_code=404, detail="Tag not found")

@router.get("/tags/{name}/cards", response_model=List[Card], status_code=200, tags=["tags"])
async def get_tag_cards(name: str):
    cards = crud.get_cards_by_tag(name)
    if not cards:
        raise HTTPException(status_code=404, detail="Tag not found")
    return cards