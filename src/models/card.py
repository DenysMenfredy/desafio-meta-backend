from typing import Optional
from datetime import datetime
from sqlmodel import Field, SQLModel

class Card(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True)
    texto : str
    data_criacao : datetime = Field(default_factory=datetime.utcnow, nullable=False)
    data_modificacao : datetime
    # tags : str

    def __str__(self):
        return f'<Card(id={self.id}, texto={self.texto}, data_criacao={self.data_criacao}, data_modificacao={self.data_modificacao})>'
