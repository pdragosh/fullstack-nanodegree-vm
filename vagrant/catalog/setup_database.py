import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from datetime import datetime

def _now():
    return datetime.now()

Base = declarative_base()

class Category(Base):
    __tablename__ = 'Category'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    created = Column(DateTime, nullable=False, default=_now)
    user = Column(String(80), nullable=False)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'name': self.name,
            'created': self.created,
            'user': self.user
        }


class Item(Base):
    __tablename__ = 'Item'

    id = Column(Integer, primary_key=True)
    title = Column(String(80), nullable=False)
    description = Column(String(250))
    created = Column(DateTime, nullable=False, default=_now)
    user = Column(String(80))
    category_id = Column(Integer, ForeignKey('Category.id'))
    category = relationship(Category)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'created': self.created,
            'user': self.user,
            'category_id': self.category_id
        }


engine = create_engine('sqlite:///catalog.db')


Base.metadata.create_all(engine)
