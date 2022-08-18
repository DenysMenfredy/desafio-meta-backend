from typing import Optional

from sqlmodel import Field, SQLModel

class Tag(SQLModel, table=True):
    id : Optional[int] = Field(primary_key=True)
    name : str