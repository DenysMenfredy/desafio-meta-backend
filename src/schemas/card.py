from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel
from .tag import Tag, TagAdd


class Card(BaseModel):
    """This class represents a card schema."""
    id : Optional[int]
    texto : str
    data_criacao : Optional[datetime] = datetime.utcnow()
    data_modificacao : Optional[datetime] = datetime.utcnow()
    
    def __str__(self):
        return f'<Card(id={self.id}, texto={self.texto}, data_criacao={self.data_criacao}, data_modificacao={self.data_modificacao})>'

    class Config: # configurações do pydantic
        orm_mode = True # para usar o ORM do SQLAlchemy


class CardCreate(BaseModel):
    """This class represents a card schema for creation."""
    texto : str
    tags : List[TagAdd]

class CardGet(Card):
    """This class represents a card schema for getting."""
    tags : List[Tag]

class CardUpdate(BaseModel):
    """This class represents a card schema for updating."""
    texto: str
    tags : List[TagAdd]