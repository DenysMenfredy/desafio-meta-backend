from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Card(Base):
    __tablename__ = 'card'
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    texto = Column(Text, nullable=False)
    data_criacao = Column(DateTime, nullable=False, default=datetime.utcnow)
    data_modificacao = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    tags = relationship('Tag', secondary='card_has_tag', back_populates='cards')

class Tag(Base):
    __tablename__ = 'tag'
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)
    cards = relationship('Card', secondary='card_has_tag', back_populates='tags')

class CardHasTag(Base):
    __tablename__ = 'card_has_tag'
    card_id = Column(Integer, ForeignKey('card.id'), primary_key=True, nullable=False)
    tag_id = Column(Integer, ForeignKey('tag.id'), primary_key=True, nullable=False)