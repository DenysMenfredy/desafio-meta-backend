from ..db.conn import connect_to_db
from ..models.card import Card
from ..models.tag import Tag
from sqlmodel import SQLModel, Session
from typing import Optional, List
from fastapi import APIRouter

router = APIRouter()

engine = connect_to_db()

session = Session(engine)

@router.post('/cards', response_model=Card)
async def create_card(texto: str, data_criacao: str, data_modificacao: str) -> Card:
    card = Card(texto=texto, data_criacao=data_criacao, data_modificacao=data_modificacao)
    session.add(card)
    session.commit()

@router.get('/cards/{id}', response_model=Card)
def get_card(id: int) -> Card:
    return Card.get(id=id)

@router.get('/cards/all', response_model=List[Card])
def get_cards() -> List[Card]:
    return Card.all()

@router.delete('/cards/{id}', response_model=Card)
def delete_card(id: int) -> Card:
    return Card.delete(id=id)

@router.put('/cards/{id}', response_model=Card)
def update_card(id: int, texto: str, data_criacao: str, data_modificacao: str) -> Card:
    return Card.update(id=id, texto=texto, data_criacao=data_criacao, data_modificacao=data_modificacao)

@router.get('/cards', response_model=List[Card])
def get_card_by_tag(tag: str) -> List[Card]:
    return Card.get_by_tag(tag=tag)

    
