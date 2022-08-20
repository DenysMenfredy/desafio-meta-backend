from pydantic import BaseModel

class CardHasTag(BaseModel):
    """This class represents a many-to-many relationship between cards and tags."""
    card_id : int 
    tag_id : int 

    def __str__(self):
        return f'<CardHasTag(card_id={self.card_id}, tag_id={self.tag_id})>'