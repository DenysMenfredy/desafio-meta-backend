from typing import Optional, List
from datetime import datetime
from sqlmodel import Field, SQLModel


class Card(SQLModel, table=True):
    __tablename__: str = 'cards'
    id: Optional[int] = Field(primary_key=True, nullable=False)
    texto : str
    data_criacao : Optional[datetime] = Field(default=datetime.utcnow, nullable=True)
    data_modificacao : Optional[datetime] = Field(default=None, nullable=True)
    # tags : str

    def __str__(self):
        return f'<Card(id={self.id}, texto={self.texto}, data_criacao={self.data_criacao}, data_modificacao={self.data_modificacao})>'

