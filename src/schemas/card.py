from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel
from .tag import Tag, TagAdd


class Card(BaseModel):
    id : Optional[int]
    texto : str
    data_criacao : Optional[datetime] = datetime.utcnow()
    data_modificacao : Optional[datetime] = datetime.utcnow()
    tags : List[Tag] = []
    
    def __str__(self):
        return f'<Card(id={self.id}, texto={self.texto}, data_criacao={self.data_criacao}, data_modificacao={self.data_modificacao})>'

    class Config:
        orm_mode = True


class CardCreate(BaseModel):
    texto : str
    tags : List[TagAdd]

class CardGet(Card):
    tags : List[Tag]

class CardUpdate(BaseModel):
    texto: str
    tags : List[TagAdd]