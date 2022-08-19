from typing import Optional

from sqlmodel import Field, SQLModel, UniqueConstraint

class Tag(SQLModel, table=True):
    __tablename__: str = 'tags'
    __table_args__ = (UniqueConstraint('name'),)
    id : Optional[int] = Field(primary_key=True, nullable=False)
    name : str = Field(nullable=False)

    def __str__(self):
        return f'<Tag(id={self.id}, name={self.name})>'

