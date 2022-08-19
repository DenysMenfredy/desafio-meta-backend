from sqlmodel import SQLModel, Field

class CardHasTag(SQLModel, table=True):
    """This class represents a many-to-many relationship between cards and tags."""
    card_id : int = Field(primary_key=True, nullable=False)
    tag_id : int = Field(primary_key=True, nullable=False)

    def __str__(self):
        return f'<CardHasTag(card_id={self.card_id}, tag_id={self.tag_id})>'