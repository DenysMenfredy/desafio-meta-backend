from typing import Optional

from pydantic import Field, BaseModel

class Tag(BaseModel):
    id : Optional[int]
    name : str 

    class Config:
        orm_mode = True

    def __str__(self):
        return f'<Tag(id={self.id}, name={self.name})>'

class TagCreate(BaseModel):
    name: str

class TagAdd(BaseModel):
    name: str
    
class TagUpdate(BaseModel):
    name: str
