from .conn import connect_to_db
from typing import Optional, List
from sqlalchemy.orm import Session
from .models import Card as CardModel, Tag as TagModel
from ..schemas.card import Card as CardSchema, CardCreate as CardCreateSchema,\
                     CardGet as CardGetSchema, CardUpdate as CardUpdateSchema
from ..schemas.tag import Tag as TagSchema, TagCreate as TagCreateSchema


class DBCrud:
    def __init__(self) -> None:
        self.engine = connect_to_db()

    def create_card(self, card_info: CardCreateSchema):
        card_db = CardModel(texto=card_info.texto)
        try:
            with Session(self.engine, expire_on_commit=False) as session:
                db_tags = session.query(TagModel).all()
                for tag in card_info.tags:
                    if tag.name not in [tag.name for tag in db_tags]:
                        db_tag = TagSchema(name=tag.name)
                        session.add(db_tag)
                        card_db.tags.append(db_tag)
                    else:
                        tag_db = session.query(TagModel).filter(TagModel.name == tag.name).first()
                        card_db.tags.append(tag_db)
                session.add(card_db)
                session.commit()
                session.refresh(card_db)
        except Exception as e:
            raise Exception('Error creating card', e)

    def get_card(self, id: int):
        with Session(self.engine, expire_on_commit=False) as session:
            card = session.query(CardModel).filter(CardModel.id == id).first()
            if not card:
                raise Exception('Card not found')
            return card

    def get_cards(self):
        with Session(self.engine, expire_on_commit=False) as session:
            cards = session.query(CardModel).all()
            if not cards:
                return []
            return cards
    
    def update_card(self, card_id:int,  card_info: CardUpdateSchema):
        with Session(self.engine, expire_on_commit=False) as session:
            card_db = session.query(CardModel).filter(CardModel.id == card_id).first()
            if not card_db:
                raise Exception('Card not found')
            card_db.tags = []
            db_tags = session.query(TagModel).all()
            for tag in card_info.tags:
                if tag.name not in [tag.name for tag in db_tags]:
                    db_tag = TagModel(name=tag.name)
                    session.add(db_tag)
                    card_db.tags.append(db_tag)
                else:
                    tag_db = session.query(TagModel).filter(TagModel.name == tag.name).first()
                    card_db.tags.append(tag_db)
            card_db.texto = card_info.texto
            session.commit()
            session.refresh(card_db)
            return card_db


