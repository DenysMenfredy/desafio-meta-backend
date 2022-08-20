from typing import Optional, List
from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from ..schemas.card import Card, CardCreate, CardGet, CardUpdate
from ..schemas.tag import Tag
from ..schemas.card_has_tag import CardHasTag
from ..db.crud import DBCrud


router = APIRouter()

crud = DBCrud()


@router.get("/cards", status_code=200, response_model=List[Card])
async def get_cards():
    cards = crud.get_cards()

    return cards

@router.get("/cards/{id}", status_code=200, tags=["cards"])
async def get_card(id: int):
    card = crud.get_card(id)
    if not card:
        raise HTTPException(status_code=404, detail="Card not found")
    return card

@router.post("/cards", status_code=201, tags=["cards"])
async def create_card(card_info: CardCreate):
    try:
        card, tags = crud.create_card(card_info)
        return {
            'message': 'Card criado com sucesso',
            'card': card,
            'tags': tags
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=e)
    
@router.put("/cards/{id}", status_code=200, tags=["cards"])
async def update_card(id: int, card: CardUpdate):
    card_db = crud.update_card(id, card)
    if not card_db:
        raise HTTPException(status_code=404, detail="Card not found")
    return card_db
    
@router.delete("/cards/{id}", status_code=200, tags=["cards"])
async def delete_card(id: int):
    try:
        crud.delete_card(id)
        return {
            'message': 'Card deletado com sucesso'
        }
    except Exception as e:
        raise HTTPException(status_code=404, detail="Card not found")
