from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from setup_database import Category, Base, Item
import json

from pprint import pprint

engine = create_engine('sqlite:///catalog.db')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

with open('initial_data.json') as data_file:    
    data = json.load(data_file)

for category in data['Category']:
    pprint(category)
    new_category = Category(id=category['id'], name=category['name'], user=category['user'])
    session.add(new_category)
    session.commit()
    if 'Item' in category:
        for item in category['Item']:
            pprint(item)
            new_item = Item(id=item['id'], title=item['title'], description=item['description'], user=item['user'], category_id=category['id'])
            session.add(new_item)
            session.commit()
exit

