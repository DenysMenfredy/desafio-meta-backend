from ..db.conn import connect_to_db
from ..models.tag import Tag

from typing import Optional, List

def create_tag(name: str) -> Tag:
    return Tag(name=name)

def get_tag(id: int) -> Tag:
    return Tag.get(id=id)

def get_tags() -> List[Tag]:
    return Tag.all()

def delete_tag(id: int) -> Tag:
    return Tag.delete(id=id)

def update_tag(name: str) -> Tag:
    return Tag.update(name=name)

