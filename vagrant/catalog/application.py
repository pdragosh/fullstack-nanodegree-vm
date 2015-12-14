from flask import Flask, render_template, request, redirect, jsonify, url_for, make_response
from flask import session as login_session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from setup_database import Base, Category, Item
from functools import wraps
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import uuid, httplib2, json, requests

#
# Create our flask application
#
app = Flask(__name__)

#
# For authentication with google+
#
CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Catalog Web Client"

#
# Database engine creation
#
engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

#
# Helper methods
#

#
# Helps determine if the user is actually logged in
#
def login_required(wrapped_function):
    @wraps(wrapped_function)
    def wrapper(*args, **kwargs):
        if 'username' not in login_session:
            return redirect('/login')
        return wrapped_function(*args, **kwargs)
    return wrapper

#
# Cleans up general login information
#
def cleanupLogin():
    if 'username' in login_session:
        del login_session['username']
    if 'email' in login_session:
        del login_session['email']
    if 'login_social' in login_session:
        del login_session['login_social']

#
# Cleans up anything in the session
# that we save for Google+ Login
#
def cleanUpGoogle():
    #
    # Clean up general login infor
    #
    cleanupLogin()
    #
    # Clean up google+ specific information
    #
    if 'access_token' in login_session:
        del login_session['access_token'] 
    if 'gplus_id' in login_session:
        del login_session['gplus_id']
    if 'picture' in login_session:
        del login_session['picture']

#
# Routing requests
#

#
# General logging in, save some state information regarding
# the user then redirect
#
@app.route('/login')
def showLogin():
    login_session['state'] = str(uuid.uuid4())
    return render_template('login.html', STATE=login_session['state'])

#
# General logout. Determine what social app was used to login and
# then redirect to its logout
#
@app.route('/logout')
def logout():
    #
    # Are they logged in?
    #
    if 'login_social' not in login_session:
        cleanupLogin()
        return redirect('/')
    #
    # Is it google+?
    #
    if login_session['login_social'] == 'google':
        return redirect('/gdisconnect')
    #
    # Should not get here
    #
    print "Warning could not determine login info to logout"
    cleanupLogin()
    return redirect('/')

#
# Google+ logging in
#
@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Store that we used google +
    login_session['login_social'] = 'google';

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    return output

#
# google+ logging out
#
@app.route('/gdisconnect')
def gdisconnect():
    if 'access_token' not in login_session:
	cleanUpGoogle()
	return redirect('/')

    access_token = login_session['access_token']
    print 'In gdisconnect access token is %s', access_token
    print 'User name is: ' 
    print login_session['username']
    if access_token is None:
 	print 'Access Token is None'
    	response = make_response(json.dumps('Current user not connected.'), 401)
    	response.headers['Content-Type'] = 'application/json'
    	return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is '
    print result
    if result['status'] == '200':
        cleanUpGoogle()
        return redirect('/')
    else:
        cleanUpGoogle()
        print 'Failed to logout of google+'
        return redirect('/')

#
# Return JSON representation of a catalog category
#
@app.route('/catalog/<int:category_id>/items/JSON')
def categoryItemJSON(category_id):
    items = session.query(Item).filter_by(
        category_id=category_id).all()
    return jsonify(Item=[i.serialize for i in items])

#
# Return JSON representation of a catalog category's item
#
@app.route('/catalog/<int:category_id>/item/<int:item_id>/JSON')
def itemJSON(category_id, item_id):
    item = session.query(Item).filter_by(id=item_id).one()
    return jsonify(item=item.serialize)

#
# Return JSON representation of the catalog
#
@app.route('/categories/JSON')
def categoryJSON():
    category = session.query(Category, Item).join(Item).all()
    print category
    return jsonify(categories=[r.serialize for r in category])

#
# Home page entry
#
@app.route('/')
@app.route('/catalog/')
def showCatalog():
    categories = session.query(Category).all()
    #TODO filter most recent
    mostrecent = session.query(Item).all()
    return render_template('categories.html',
                           categories=categories,
                           items=mostrecent,
                           category=None,
                           current_item=None)

#
# Create a new category
#
@app.route('/catalog/new/', methods=['GET', 'POST'])
def newCategory():
    if request.method == 'POST':
        newCategory = Category(name=request.form['name'])
        session.add(newCategory)
        session.commit()
        return redirect(url_for('showCatalog'))
    else:
        return render_template('newCategory.html')
#
# Edit category name
#
@app.route('/catalog/<int:category_id>/edit/', methods=['GET', 'POST'])
def editCategory(category_id):
    editedCategory = session.query(
        Category).filter_by(id=category_id).one()
    if request.method == 'POST':
        if request.form['value']:
            editedCategory.name = request.form['value']
            return redirect(url_for('showCatalog'))
    else:
        return render_template(
            'editCategory.html', category=editedCategory)

#
# Delete a category
#
@app.route('/catalog/<int:category_id>/delete/', methods=['GET', 'POST'])
def deleteCategory(category_id):
    categoryToDelete = session.query(
        Category).filter_by(id=category_id).one()
    if request.method == 'POST':
        session.delete(categoryToDelete)
        session.commit()
        return redirect(
            url_for('showCatalog', category_id=category_id))
    else:
        return render_template(
            'deleteCategory.html', category=categoryToDelete)
#
# Show items from a category
#
@app.route('/catalog/<int:category_id>/')
@app.route('/catalog/<int:category_id>/items/')
def showItems(category_id):
    categories = session.query(Category).all()
    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(Item).filter_by(
        category_id=category_id).all()
    return render_template('categories.html', categories=categories,
                           items=items, category=category,
                           current_item=None)

#
# Show individual item
#
@app.route('/catalog/<int:category_id>/item/<int:item_id>')
def showItem(category_id, item_id):
    print 'show item'
    categories = session.query(Category).all()
    category = session.query(Category).filter_by(id=category_id).one()
    current_item = session.query(Item).filter_by(id=item_id).one()
    items = session.query(Item).filter_by(category_id=category_id).all()
    print current_item.title
    return render_template('categories.html', categories=categories,
                           items=items, category=category, current_item=current_item)

#
# Create a new item for a category
#
@app.route(
    '/catalog/<int:category_id>/items/new/', methods=['GET', 'POST'])
def newItem(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    if request.method == 'POST':
        newItem = Item(title=request.form['title'],
                       description=request.form['description'],
                       category_id=category_id)
        session.add(newItem)
        session.commit()

        return redirect(url_for('showCatalog', category=category))
    else:
        return render_template('newItem.html', category=category)

#
# Edit a category item
#
@app.route('/catalog/<int:category_id>/items/<int:item_id>/edit/',
           methods=['GET', 'POST'])
def editItem(category_id, item_id):
    category = session.query(Category).filter_by(id=category_id).one()
    editedItem = session.query(Item).filter_by(id=item_id).one()
    if request.method == 'POST':
        if request.form['name'] == 'item_title':
            editedItem.title = request.form['value']
        if request.form['name'] == 'item_description':
            editedItem.description = request.form['value']
        session.add(editedItem)
        session.commit()
        return redirect(url_for('showCatalog', category=category))
    else:
        return render_template(
            'editItem.html', category=category, item=editedItem)

#
# Delete a cateogry item
#
@app.route('/catalog/<int:category_id>/items/<int:item_id>/delete',
           methods=['GET', 'POST'])
def deleteItem(category_id, item_id):
    category = session.query(Category).filter_by(id=category_id).one()
    itemToDelete = session.query(Item).filter_by(id=item_id).one()
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        return redirect(url_for('showCatalog', category_id=category_id))
    else:
        return render_template('deleteItem.html', item=itemToDelete, category=category)

#
# Startup the flask application
#
if __name__ == '__main__':
    app.debug = True
    app.secret_key = 'fkldsjfeofjeijfewljfkds'
    app.run(host='0.0.0.0', port=8000)
