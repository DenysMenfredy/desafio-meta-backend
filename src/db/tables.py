from sqlalchemy import Column, Integer, String, DateTime, Text, MetaData, Table, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

metadata_obj = MetaData()

cards = Table('card', metadata_obj,
    Column('id', Integer, primary_key=True, nullable=False, autoincrement=True),
    Column('texto', Text, nullable=False),
    Column('data_criacao', DateTime, nullable=False, default=datetime.utcnow),
    Column('data_modificacao', DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow),
)

tags = Table('tag', metadata_obj,
    Column('id', Integer, primary_key=True, nullable=False, autoincrement=True),
    Column('name', String(50), nullable=False, unique=True),
)

card_has_tag = Table('card_has_tag', metadata_obj,
    Column('card_id', Integer, primary_key=True, nullable=False),
    Column('tag_id', Integer, primary_key=True, nullable=False)
)

