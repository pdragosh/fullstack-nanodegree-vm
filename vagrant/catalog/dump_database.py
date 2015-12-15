from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from setup_database import Category, Base, Item
import json

from pprint import pprint

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

categories = session.query(Category).all()

for c in categories:
    print c.serialize
    items = session.query(Item).filter_by(category_id=c.id).all()
    for i in items:
        print i.serialize

