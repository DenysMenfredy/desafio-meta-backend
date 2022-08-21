from typing import Optional

from pydantic import Field, BaseModel

class Tag(BaseModel):
    """This class represents a tag schema."""
    id : Optional[int]
    name : str 

    class Config: # configurações do pydantic
        orm_mode = True # para usar o ORM do SQLAlchemy

    def __str__(self):
        return f'<Tag(id={self.id}, name={self.name})>'

class TagCreate(BaseModel):
    """This class represents a tag schema for creation."""
    name: str

class TagAdd(BaseModel):
    """This class represents a tag schema to be used when adding a tag for a card."""
    name: str
    
class TagUpdate(BaseModel):
    """This class represents a tag schema for updating."""
    name: str
