from flask import Flask, render_template, request, \
redirect, url_for, jsonify, flash
from flask import session as login_session
import random, string
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model import User, Base, Category, CategoryItem
import random
import string

# IMPORTS FOR gconnect i.e Google Connect Login
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

app = Flask(__name__)
#Mult-threading as sqllite by default does not allow more than 1 thread to access

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Item Catalog Application"

engine = create_engine('sqlite:///shoplocal.db', \
                connect_args={'check_same_thread':False})
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

#Home page
@app.route("/")
@app.route("/home")
def homePage():
    if not login_session.get('username'):
        #listing all the categories and passing it to the html for display
        categories = session.query(Category).all()
        items = session.query(CategoryItem).all()
        return render_template('homepage.html',categories = categories,
            items =items)
    else:
        categories = session.query(Category).all()
        items = session.query(CategoryItem).all()
        user = login_session.get('username')
        return render_template('homepage.html',categories = categories,
        items =items,user=user)

#Show Category Item
@app.route("/category/<int:category_id>")
def showCategoryItem(category_id):
    if not login_session.get('username'):
        categories = session.query(Category).all()

        items = session.query(CategoryItem). \
        filter_by(category_id=category_id).all()

        item_category = session.query(Category). \
        filter_by(id=category_id).first()
        #print (item_category.category_name)
        return render_template('itemcategory.html',
        categories = categories,items =items, item_category = item_category)
    else:
        categories = session.query(Category).all()

        items = session.query(CategoryItem). \
        filter_by(category_id=category_id).all()

        item_category = session.query(Category). \
        filter_by(id=category_id).first()

        user = login_session.get('username')
        #print (item_category.category_name)
        return render_template('itemcategory.html',
        categories = categories,items =items,
        item_category = item_category,user = user)

#Show Item Description
@app.route("/category/item/<int:item_category_id>")
def showCategoryItemDescribtion(item_category_id):
        if not login_session.get('username'):
            item_category = session.query(CategoryItem). \
            filter_by(id=item_category_id).first()

            category = session.query(Category). \
            filter_by(id=item_category.category_id).first()

            return render_template('itemcategorydetails.html',
            item_category = item_category, category = category)
        else:
            item_category = session.query(CategoryItem). \
            filter_by(id=item_category_id).first()

            category = session.query(Category). \
            filter_by(id=item_category.category_id).first()

            user = login_session.get('username')

            return render_template('itemcategorydetails.html',
            item_category = item_category, category = category, user = user)

#Add Item
@app.route("/addcategoryitem",methods=['GET','POST'])
def addcategoryitem():
    if not login_session.get('username'):
        return render_template('login.html')
    try:
        if request.method == 'POST':
            category_id=int(request.form['category'])
            #user = login_session.get('username')
            category = session.query(Category).filter_by(id=category_id).first()
            creator = session.query(User).filter_by(email_id=login_session.get('username')).first()
            print(login_session.get('username'))
            print(creator.email_id)
            categoryitem = CategoryItem(category_item_name=request.form['title'],
            category_item_description=request.form['description'],
            user=creator,category=category)
            session.add(categoryitem)
            session.commit()
            flash("Item Added Successfully")

            categories = session.query(Category).all()

            items = session.query(CategoryItem). \
            filter_by(category_id=category_id).all()

            item_category = session.query(Category). \
            filter_by(id=category_id).first()

            user = creator.email_id

            return render_template('itemcategory.html',
            categories = categories,items =items,
            item_category = item_category,user = user)
        else:
            categories = session.query(Category).all()
            user = login_session.get('username')
            return render_template('additemcatalog.html',categories = categories,user = user)
    except  Exception as e:
        session.rollback()
        return e.message

#Edit Item
@app.route("/editcategoryitem/<int:item_category_id>",methods=['GET','POST'])
def editCategoryItem(item_category_id):
    editedItem = session.query(CategoryItem). \
    filter_by(id=item_category_id).first()
    #print("ankit rawat is here")
    if not login_session.get('username'):
        return render_template('login.html')
    if request.method == 'POST':
        #Fetching data from user input
        if request.form['title']:
            editedItem.category_item_name = request.form['title']
        if request.form['description']:
            editedItem.category_item_description = request.form['description']
        if request.form['category']:
            editedItem.category_id = request.form['category']
        session.add(editedItem)
        session.commit()
        flash("Item is updated successfully")

        categories = session.query(Category).all()

        items = session.query(CategoryItem). \
        filter_by(category_id=editedItem.category_id).all()

        item_category = session.query(Category). \
        filter_by(id=editedItem.category_id).first()

        user = login_session.get('username')

        return render_template('itemcategory.html',
        categories = categories,items =items,
        item_category = item_category,user = user)

    else:
        item_category = session.query(CategoryItem). \
        filter_by(id=item_category_id).first()

        categories = session.query(Category).all()

        item_category_name = session.query(Category). \
        filter_by(id=item_category.category_id).first()

        user = login_session.get('username')
        return render_template('edititemcatalog.html',
        item_category = item_category, categories = categories,
        item_category_name = item_category_name, user = user)

#Delete Item
@app.route("/deleteategoryitem/<int:item_category_id>",methods=['GET','POST'])
def deleteCategoryItem(item_category_id):
    if not login_session.get('username'):
        return render_template('login.html')

    itemToDelete = session.query(CategoryItem). \
        filter_by(id=item_category_id).first()

    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        return redirect(
            url_for('homePage'))
    else:
        user = login_session.get('username')
        return render_template('deleteitemcatalog.html', item_delete = itemToDelete,user = user)

    #item_category = item_category, category = category)


#login page
@app.route("/login")
def login():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template(
        'login.html',STATE=state)

#registration
@app.route("/registration")
def registration():
    return render_template(
        'registration.html')

#Validate User name and password to check valid user
@app.route("/loginValidation",methods=['GET','POST'])
def  loginValidation():
    if request.method == 'POST':
        #Fetching data from user input
        email_id = request.form['email_id']
        password = request.form['psw']
        try:
            userAlreadyPresent = session.query(User). \
            filter_by(email_id=email_id).first()
            #print (userAlreadyPresent.email_id)
            if userAlreadyPresent:
                #print("Password"+password)
                #Comparing DB and user Input
                isPassMatch = userAlreadyPresent.verify_password(password)
                if isPassMatch:
                    #state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    #                for x in xrange(32))
                    login_session['username']=email_id
                    #login_session['state'] = state
                    flash("Login Successful")
                    return redirect(url_for('homePage'))
                else:
                    return "Incorrect User Name and Password"
            else:
                flash("Invalid User ID")
                return redirect(url_for('login'))
        except Exception as e:
                return e.message
    else:
        return render_template(
            'login.html')

#User Registration Validation and Creation
@app.route("/register",methods=['GET','POST'])
def register():
    if request.method == 'POST':
        #Fetching data from user input
        email_id = request.form['email_id']
        password = request.form['psw']
        try:
            userAlreadyPresent = session.query(User). \
            filter_by(email_id=email_id).first()
            if userAlreadyPresent:
                flash("User added Successful")
                return "User Exists|Please Login"
            else:
                user = User(email_id=email_id)
                user.hash_password(password)
                session.add(user)
                session.commit()
                #state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                #                    for x in xrange(32))
                login_session['username']  = email_id
                #login_session['state'] = state
                return redirect(url_for('homePage'))
        except:
                return "Some Exception"
    else:
        return render_template(
            'registration.html')

#Logout
@app.route("/logout")
def logout():
    #removing user session from server
    #Checking the access token of google sign on
    access_token = login_session.get('access_token')
    if access_token is None:
        #Check to see if the user is login via application login. If so then remove the user
        if login_session.get('username'):
            login_session.pop('username', None)
            return redirect(url_for('homePage'))
        else:
            print 'Access Token is None'
            flash("User is not logged in")
            return redirect(url_for('homePage'))
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is '
    print result
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        #del login_session['email']
        del login_session['name']
        del login_session['picture']
        flash("Successfully Disconnected")
        return redirect(url_for('homePage'))
    else:
        flash('Failed to revoke token for given user.', 400)
        return redirect(url_for('homePage'))

## Create anti-forgery state token for google login
# @app.route("/glogin")
# def glogin():
#     state = ''.join(random.choice(string.ascii_uppercase + string.digits)
#                     for x in xrange(32))
#     login_session['state'] = state
#     #return "The current session state is %s" % login_session['state']
#     return render_template('glogin.html',STATE=state)

@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code from google
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
    print ("credentials is ")
    print (credentials)
    print ("result is")
    print (result)
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

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

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['name'] = data['name']
    login_session['picture'] = data['picture']
    login_session['username'] = data['email']

    output = ''
    output += '<h1>Welcome, '
    output += login_session['name']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("You are now logged in as %s" % login_session['name'])
    print "done!"
    return output
#Main Program
if __name__ == '__main__':
    #login sessionsecret key
    app.secret_key = "whoamitocreateyou"
    #Debug Mode for autorun
    app.debug = True
    #Multi-threading
    app.run(host='0.0.0.0', port=5000,threaded=True)
