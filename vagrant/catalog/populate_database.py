from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from setup_database import Category, Base, Item
import json

from pprint import pprint

engine = create_engine('sqlite:///catalog.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

with open('initial_data.json') as data_file:    
    data = json.load(data_file)
#pprint(data)

for category in data['Category']:
    pprint(category)
    new_category = Category(id=category['id'], name=category['name'])
    session.add(new_category)
    session.commit()

exit

# Menu for UrbanBurger
#restaurant1 = Restaurant(name="Urban Burger")

#session.add(restaurant1)
#session.commit()

#menuItem2 = MenuItem(name="Veggie Burger", description="Juicy grilled veggie patty with tomato mayo and lettuce",
#                     price="$7.50", course="Entree", restaurant=restaurant1)

#session.add(menuItem2)
#session.commit()


#menuItem1 = MenuItem(name="French Fries", description="with garlic and parmesan",
#                     price="$2.99", course="Appetizer", restaurant=restaurant1)

##session.add(menuItem1)
# session.commit()


