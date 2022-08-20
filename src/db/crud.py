from .conn import connect_to_db, connect_to_test_db, connect_to_sqlite_db
from typing import Optional, List
from sqlalchemy.orm import Session
from .models import Card as CardModel, Tag as TagModel
print(__package__)
import sys
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.abspath(os.path.join(dir_path, os.pardir)))

from schemas.card import Card as CardSchema, CardCreate as CardCreateSchema,\
                           CardGet as CardGetSchema, CardUpdate as CardUpdateSchema
from schemas.tag import Tag as TagSchema, TagCreate as TagCreateSchema, \
                          TagUpdate as TagUpdateSchema

class DBCrud:
    def __init__(self) -> None:
        # self.engine = connect_to_db()
        self.engine = connect_to_sqlite_db()

    def create_card(self, card_info: CardCreateSchema):
        card_db = CardModel(texto=card_info.texto)
        try:
            with Session(self.engine, expire_on_commit=False) as session:
                db_tags = session.query(TagModel).all()
                for tag in card_info.tags:
                    if tag.name not in [tag.name for tag in db_tags]:
                        db_tag = TagModel(name=tag.name)
                        session.add(db_tag)
                        card_db.tags.append(db_tag)
                    else:
                        tag_db = session.query(TagModel).filter(TagModel.name == tag.name).first()
                        card_db.tags.append(tag_db)
                _ = card_db.tags
                session.add(card_db)
                session.commit()
                session.refresh(card_db)
            return card_db, card_info.tags
        except Exception as e:
            raise Exception('Error creating card', e)

    def get_card(self, card_id: int):
        with Session(self.engine, expire_on_commit=False) as session:
            card = session.query(CardModel).filter(CardModel.id == card_id).first()
            if not card:
                return None
            _ = card.tags
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
                return None
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
            _ = card_db.tags
            session.commit()
            session.refresh(card_db)
            return card_db

    def delete_card(self, card_id: int):
        with Session(self.engine, expire_on_commit=False) as session:
            card_db = session.query(CardModel).filter(CardModel.id == card_id).first()
            if not card_db:
                raise Exception('Error deleting card')
            session.delete(card_db)
            session.commit()
            return card_db

    def create_tag(self, tag_info: TagCreateSchema):
        tag_db = TagModel(name=tag_info.name)
        try:
            with Session(self.engine, expire_on_commit=False) as session:
                session.add(tag_db)
                session.commit()
                session.refresh(tag_db)
            return tag_db
        except Exception as e:
            raise Exception('Error creating tag', e)

    def get_tag(self, tag_id: int):
        with Session(self.engine, expire_on_commit=False) as session:
            tag = session.query(TagModel).filter(TagModel.id == tag_id).first()
            if not tag:
                return None
            return tag

    def get_tags(self):
        with Session(self.engine, expire_on_commit=False) as session:
            tags = session.query(TagModel).all()
            if not tags:
                return []
            return tags
    def update_tag(self, tag_id:int, tag_info: TagUpdateSchema):
        with Session(self.engine, expire_on_commit=False) as session:
            tag_db = session.query(TagModel).filter(TagModel.id == tag_id).first()
            if not tag_db:
                return None
            tag_db.name = tag_info.name
            session.commit()
            session.refresh(tag_db)
            return tag_db

    def delete_tag(self, tag_id: int):
        with Session(self.engine, expire_on_commit=False) as session:
            tag_db = session.query(TagModel).filter(TagModel.id == tag_id).first()
            if not tag_db:
                return None
            session.delete(tag_db)
            session.commit()
            return tag_db

    def get_cards_by_tag(self, tag_name:str):
        with Session(self.engine, expire_on_commit=False) as session:
            tag = session.query(TagModel).filter(TagModel.name == tag_name).first()
            if not tag:
                return None
            cards = tag.cards
        return cards