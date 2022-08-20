from ..db.conn import connect_to_db
from ..schemas.card import Card, CardCreate, CardGet, CardUpdate
from ..schemas.tag import Tag
from ..schemas.card_has_tag import CardHasTag
from typing import Optional, List
from fastapi import APIRouter, Request, Response, Depends, HTTPException
from datetime import datetime
from sqlalchemy.orm import Session
from ..db import models

router = APIRouter()

engine = connect_to_db()

# session = Session(engine)

@router.get("/cards", status_code=200, response_model=List[CardGet])
async def get_cards():
    with Session(engine, expire_on_commit=False) as session:
        cards = session.query(models.Card).all()
        if not cards:
            return []
        for card in cards:
            card.tags = session.query(models.Tag)\
                .join(models.CardHasTag)\
                .join(models.Card)\
                .filter(models.Card.id == card.id)\

        return cards

@router.get("/cards/{id}", status_code=200, tags=["cards"])
async def get_card(id: int):
    with Session(engine, expire_on_commit=False) as session:
        card = session.query(models.Card).filter(models.Card.id == id).first()
        if not card:
            raise HTTPException(status_code=404, detail="Card not found")
        return card

@router.post("/cards", status_code=201, tags=["cards"])
async def create_card(card_info: CardCreate):
    card_db = models.Card(texto=card_info.texto)
    with Session(engine, expire_on_commit=False) as session:
        db_tags = session.query(models.Tag).all()
        for tag in card_info.tags:
            if tag.name not in [tag.name for tag in db_tags]:
                db_tag = models.Tag(name=tag.name)
                session.add(db_tag)
                card_db.tags.append(db_tag)
            else:
                tag_db = session.query(models.Tag).filter(models.Tag.name == tag.name).first()
                card_db.tags.append(tag_db)
        session.add(card_db)
        session.commit()
        session.refresh(card_db)
        
        return {
            'message': 'Card created successfully',
            'card': card_db
        }
    
@router.put("/cards/{id}", status_code=200, tags=["cards"])
async def update_card(card_id: int, card: CardUpdate):
    with Session(engine, expire_on_commit=False) as session:
        card_db = session.query(models.Card).filter(models.Card.id == card_id).first()
        if not card_db:
            raise HTTPException(status_code=404, detail="Card not found")
        card_db.texto = card.texto
        card_db.tags = []
        db_tags = session.query(models.Tag).all()
        for tag in card.tags:
            if tag.name not in [tag.name for tag in db_tags]:
                db_tag = models.Tag(name=tag.name)
                session.add(db_tag)
                card_db.tags.append(db_tag)
            else:
                tag_db = session.query(models.Tag).filter(models.Tag.name == tag.name).first()
                card_db.tags.append(tag_db)
        session.commit()
        session.refresh(card_db)
        # card_db.data_modificacao = datetime.utcnow()
        return card
    
@router.delete("/cards/{id}", status_code=200, tags=["cards"])
async def delete_card(card_id: int):
    with Session(engine) as session:
        card_db = session.query(models.Card).filter(models.Card.id == card_id).first()
        if not card_db:
            raise HTTPException(status_code=404, detail="Card not found")
        session.delete(card_db)
        session.commit()
        return {
            'message': 'Card deleted successfully'
        }
