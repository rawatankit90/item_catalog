from flask import Flask, render_template, request, \
redirect, url_for, jsonify, flash
from flask import session as login_session
import random, string
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model import User, Base, Category, CategoryItem


app = Flask(__name__)

#Mult-threading as sqllite by default does not allow more than 1 thread to access
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
    return render_template(
        'login.html')

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
    login_session.pop('username', None)
    return redirect(url_for('homePage'))


#Main Program
if __name__ == '__main__':
    #login sessionsecret key
    app.secret_key = "whoamitocreateyou"
    #Debug Mode for autorun
    app.debug = True
    #Multi-threading
    app.run(host='0.0.0.0', port=5000,threaded=True)
