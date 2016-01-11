
#
# 1. Configuration Information
#
# Catalog Application
#

This is a web-server application that serves a catalog of categories and the items in each category. It supports
authentication vis Google Login. If logged in, users may create, edit and delete their own items.

It was built using Python 2.7.6

Modules Used:

flask v0.10.1
sqlalchemy v0.8.4
oauth 1.0.1
oauth2client v1.4.12

#
# 2. Installation Instructions

#
# OPTIONAL: Setup the database
#

python setup_database.py

This should create the catalog.db in the directory.

#
# OPTIONAL: Initial populate the database
#

Uses the file initial_data.json. Modify that file if you want to change what gets initially loaded.

python populate_database.py

#
# Dump the database
#

python dump_database.py

#
# 3. Running the application
#
# Run the catalog webserver application
#

python application.py

#
# To access the application, enter the URL of the machine and use the default port 5000 in your webserver:
#

eg.

http://127.0.0.1:5000/


#
# 4. Endpoints
#
# NOTE: Substitute the URL and PORT values for the actual values where the webserver is being hosted.
#
# Eg. Local instance on your machine running on port 5000
#
# http://localhost:5000/
#

#
# Create a new category
#

http://URL:PORT/catalog/new/

#
# Edit a category - supply the integer ID of the category you wish to edit
#

http://URL:PORT/catalog/{CATEGORY_ID}/edit/

#
# Delete a category - supply the integer ID of the category you wish to delete
#

http://URL:PORT/catalog/{CATEGORY_ID}/delete/

#
# create a new item - - supply the integer ID of the category you want the item to appear in
#

http://URL:PORT/catalog/{CATEGORY_ID}/new/

#
# Edit an item - supply the integer ID of the category and the integer ID of the Item you wish to edit
#

http://URL:PORT/catalog/{CATEGORY_ID}/items/{ITEM_ID}/edit/

#
# Delete an item - supply the integer ID of the category and the integer ID of the Item you wish to delete
#

http://URL:PORT/catalog/{CATEGORY_ID}/items/{ITEM_ID}/delete

#
# 5. JSON Representations
#
# To obtain a JSON representation of the catalog, category, or items in a category the following access points are defined
#

#
# The whole catalog
#

http://URL:PORT/catalog/JSON

#
# A category - must supply the integer ID of the category
#

http://URL:PORT/catalog/{CATEGORY_ID}/JSON

#
# An item in a category - must supply the integer ID of the category and the integer ID of the item
#

http://URL:PORT/catalog/{CATEGORY_ID}/item/{ITEM_ID}/JSON

