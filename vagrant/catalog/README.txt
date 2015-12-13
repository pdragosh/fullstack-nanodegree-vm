


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
# Run the catalog webserver application
#

python application.py
