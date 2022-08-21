from .conn import connect_to_db, connect_to_test_db, connect_to_sqlite_db
from typing import Optional, List, Tuple
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
    """This class is used to create a CRUD interface for the database"""
    def __init__(self) -> None:
        # self.engine = connect_to_db()
        self.engine = connect_to_sqlite_db()

    def create_card(self, card_info: CardCreateSchema)->Tuple:
        """This method creates a card in the database
        
        Args:
            - card_info: CardCreateSchema
        
        Returns:
            - card: CardModel
            - tags: List[TagModel]
        """
        card_db = CardModel(texto=card_info.texto) # create a card object 
        try:
            with Session(self.engine, expire_on_commit=False) as session:
                db_tags = session.query(TagModel).all() # get all the tags in the database
                for tag in card_info.tags: # for each tag in the card_info
                    if tag.name not in [tag.name for tag in db_tags]: # if the tag is not in the database
                        db_tag = TagModel(name=tag.name) # create a tag object
                        session.add(db_tag) # add the tag to the database
                        card_db.tags.append(db_tag) # add the tag to the card
                    else: # if the tag is in the database
                        tag_db = session.query(TagModel).filter(TagModel.name == tag.name).first() # get the tag from the database
                        card_db.tags.append(tag_db) # add the tag to the card
                _ = card_db.tags # get the tags from the card
                session.add(card_db) # add the card to the database
                session.commit() # commit the changes to the database
                session.refresh(card_db) # refresh the card
            return card_db, card_info.tags
        except Exception as e:
            raise Exception('Error creating card', e)

    def get_card(self, card_id: int)->Optional[CardModel]:
        """
        This method gets a card from the database.
        
        Args:
            - card_id: int
        
        Returns:
            - card: CardModel
        """
        with Session(self.engine, expire_on_commit=False) as session:
            card = session.query(CardModel).filter(CardModel.id == card_id).first()
            if not card: # if the card is not in the database
                return None # return None
            _ = card.tags 
        return card

    def get_cards(self)->List[CardModel]:
        """
        This method gets all the cards from the database.
        
        Returns:
            - cards: List[CardModel]
        """
        with Session(self.engine, expire_on_commit=False) as session:
            cards = session.query(CardModel).all()
            if not cards: # if there are no cards in the database
                return [] # return an empty list

        return cards
    
    def update_card(self, card_id:int,  card_info: CardUpdateSchema)->Optional[CardModel]:
        """This method updates a card in the database.
        
        Args:
            - card_id: int
            - card_info: CardUpdateSchema
        
        Returns:
            - card: CardModel
        """
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

    def delete_card(self, card_id: int)->None:
        """This method deletes a card from the database.
        
        Args:
            - card_id: int
        """
        with Session(self.engine, expire_on_commit=False) as session:
            card_db = session.query(CardModel).filter(CardModel.id == card_id).first()
            if not card_db:
                raise Exception('Error deleting card')
            session.delete(card_db)
            session.commit()
            return card_db

    def create_tag(self, tag_info: TagCreateSchema)->TagModel:
        """This method creates a tag in the database;
        
        Args:
            - tag_info: TagCreateSchema

        Returns:
            - tag: TagModel
        """
        tag_db = TagModel(name=tag_info.name)
        try:
            with Session(self.engine, expire_on_commit=False) as session:
                session.add(tag_db)
                session.commit()
                session.refresh(tag_db)
            return tag_db
        except Exception as e:
            raise Exception('Error creating tag', e)

    def get_tag(self, tag_id: int)->Optional[TagModel]:
        """This method gets a tag from the database.
        
        Args:
            - tag_id: int
            
        Returns:
            - tag: TagModel
        """
        with Session(self.engine, expire_on_commit=False) as session:
            tag = session.query(TagModel).filter(TagModel.id == tag_id).first()
            if not tag:
                return None
            return tag

    def get_tags(self)->List[TagModel]:
        """This method gets all the tags from the database.
        
        Returns:
            - tags: List[TagModel]
        """
        with Session(self.engine, expire_on_commit=False) as session:
            tags = session.query(TagModel).all()
            if not tags: # if there are no tags in the database
                return [] # return an empty list
            return tags

    def update_tag(self, tag_id:int, tag_info: TagUpdateSchema)->Optional[TagModel]:
        """This method updates a tag in the database.
        
        Args:
            - tag_id: int
            - tag_info: TagUpdateSchema
            
        Returns:
            - tag: TagModel"""
        with Session(self.engine, expire_on_commit=False) as session:
            tag_db = session.query(TagModel).filter(TagModel.id == tag_id).first()
            if not tag_db: # if the tag is not in the database
                return None # return None
            tag_db.name = tag_info.name
            session.commit()
            session.refresh(tag_db)
            return tag_db

    def delete_tag(self, tag_id: int)->None:
        """This method deletes a tag from the database.
        
        Args:
            - tag_id: int
        """
        with Session(self.engine, expire_on_commit=False) as session:
            tag_db = session.query(TagModel).filter(TagModel.id == tag_id).first()
            if not tag_db:
                return None
            session.delete(tag_db)
            session.commit()

    def get_cards_by_tag(self, tag_name:str)->Optional[List[CardModel]]:
        """This method gets all the cards from the database that have 
            the tag with the name tag_name.
            
        Args:
            - tag_name: str
            
        Returns:
            - cards: List[CardModel]"""
        with Session(self.engine, expire_on_commit=False) as session:
            tag = session.query(TagModel).filter(TagModel.name == tag_name).first()
            if not tag: # if the tag is not in the database
                return None # return None
            cards = tag.cards # get the cards that have the tag
        return cards