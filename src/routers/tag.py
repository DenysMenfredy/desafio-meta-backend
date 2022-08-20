from ..db.conn import connect_to_db
from ..schemas.card import Card, CardCreate, CardGet, CardUpdate
from ..schemas.tag import Tag, TagCreate, TagUpdate
from ..schemas.card_has_tag import CardHasTag
from typing import Optional, List
from fastapi import APIRouter, Request, Response, Depends, HTTPException
from datetime import datetime
from sqlalchemy.orm import Session
from ..db import models

router = APIRouter()

engine = connect_to_db()

@router.get("/tags", status_code=200, response_model=List[Tag])
async def get_tags():
    with Session(engine) as session:
        tags = session.query(models.Tag).all()
        return tags

@router.get("/tags/{id}", status_code=200, tags=["tags"])
async def get_tag(id: int):
    with Session(engine) as session:
        tag = session.query(models.Tag).filter(models.Tag.id == id).first()
        if not tag:
            raise HTTPException(status_code=404, detail="Tag not found")
        return tag

@router.post("/tags", status_code=201, tags=["tags"])
async def create_tag(tag_info: TagCreate):
    tag_db = models.Tag(name=tag_info.name)
    with Session(engine) as session:
        session.add(tag_db)
        session.commit()
        session.refresh(tag_db)
        return {
            'message': 'Tag created successfully',
            'tag': tag_db
        }

@router.put("/tags/{id}", status_code=200, tags=["tags"])
async def update_tag(tag_id: int, tag: TagUpdate):
    with Session(engine) as session:
        tag_db = session.query(models.Tag).filter(models.Tag.id == tag_id).first()
        if not tag_db:
            raise HTTPException(status_code=404, detail="Tag not found")
        tag_db.name = tag.name
        session.commit()
        session.refresh(tag_db)
        return {
            'message': 'Tag updated successfully',
            'tag': tag_db
        }

@router.delete("/tags/{id}", status_code=200, tags=["tags"])
async def delete_tag(tag_id: int):
    with Session(engine) as session:
        tag_db = session.query(models.Tag).filter(models.Tag.id == tag_id).first()
        if not tag_db:
            raise HTTPException(status_code=404, detail="Tag not found")
        session.delete(tag_db)
        session.commit()
        return {
            'message': 'Tag deleted successfully'
        }

@router.get("/tags/{name}/cards", response_model=List[Card], status_code=200, tags=["tags"])
async def get_tag_cards(name: str):
    with Session(engine) as session:
        tag = session.query(models.Tag).filter(models.Tag.name == name).first()
        if not tag:
            raise HTTPException(status_code=404, detail="Tag not found")
        cards = tag.cards
        return cards