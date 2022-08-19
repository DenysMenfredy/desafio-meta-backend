from ..db.conn import connect_to_db
from ..models.card import Card
from ..models.tag import Tag
from ..models.card_has_tag import CardHasTag
from sqlmodel import SQLModel, Session, select, insert, update, delete
from typing import Optional, List
from fastapi import APIRouter, Request, Response, Depends, HTTPException
from datetime import datetime

router = APIRouter()

engine = connect_to_db()

# session = Session(engine)

@router.post('/cards')
def create_card(card: Card, tags:str):
    tags = tags.split(',')
    for tag in tags:
        tag = Tag(name=tag)
        card_has_tag = CardHasTag(card_id=card.id, tag_id=tags.id)
    with Session(engine) as session:
        session.add(card.card)
        session.add(card.tags)
        session.add(card_has_tag)
        session.commit()

    return Response(status_code=201, 
                    content={
                        'message': 'Card created',
                        'card': card,
                        'tags': tags
                    })

@router.get('/cards/{id}')
def get_card(id: int) -> Card:
    with Session(engine) as session:
        statement = select(Card).where(Card.id == id)
        results = session.exec(statement)
        if results.first() is None:
            return None
        else:
            return results.first()


@router.get('/cards')
def get_cards() -> List[Card]:
    with Session(engine) as session:
        statement = select(Card)
        results = session.exec(statement)
        print(results)
        return results.fetchall()

@router.delete('/cards/{id}')
def delete_card(id: int) -> Card:
    return Card.delete(id=id)

@router.put('/cards/{id}')
def update_card(id: int, texto: str, data_criacao: str, data_modificacao: str) -> Card:
    return Card.update(id=id, texto=texto, data_criacao=data_criacao, data_modificacao=data_modificacao)

# @router.get('/cards', response_model=List[Card])
# def get_card_by_tag(tag: str) -> List[Card]:
#     return Card.get_by_tag(tag=tag)

    
