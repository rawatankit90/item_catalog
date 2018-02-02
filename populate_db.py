
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from model import Base, User, Category, CategoryItem

engine = create_engine('sqlite:///shoplocal.db')
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


user = User(email_id="rawatankit90@gmail.com")
user.hash_password("rawat")
session.add(user)
session.commit()

user1 = User(email_id="akardivya92.ca@gmail.com")
user1.hash_password("divya")
session.add(user1)
session.commit()

print "added User"

category = Category(category_name = "Electrnoic"
,category_description="electronic items - mobile,laptop,tv",
user=user)

session.add(category)
session.commit()


category1 = Category(category_name = "Cars"
,category_description="BMW, Audi, Mazda",
user=user)
session.add(category1)
session.commit()


category2 = Category(category_name = "Clothing"
,category_description="Clothing - Jeans,T-shirt,Dresses,Formals",
user=user1)
session.add(category2)
session.commit()


category3 = Category(category_name = "Books"
,category_description="GMAT,SAT,Computers",
user=user1)
session.add(category3)
session.commit()

print "added Categories"

##User 1 Category 1#############
categoryitem = CategoryItem(category_item_name="Dell Laptop",
category_item_description="Laptop at attractive price with latest conf",
user=user,category=category)
session.add(categoryitem)
session.commit()


categoryitem1 = CategoryItem(category_item_name="Lenovo Laptop",
category_item_description="Lenovo Laptop at attractive price with latest conf",
user=user,category=category)
session.add(categoryitem1)
session.commit()

##############User 1 Category 2#####
categoryitem2 = CategoryItem(category_item_name="BMW",
category_item_description="BMW Car at attractive price with latest conf",
user=user,category=category1)
session.add(categoryitem2)
session.commit()

categoryitem3 = CategoryItem(category_item_name="Audi",
category_item_description="Audi Car at attractive price with latest conf",
user=user,category=category1)
session.add(categoryitem3)
session.commit()
###############User2 Category2##############################

categoryitem4 = CategoryItem(category_item_name="Belk",
category_item_description="Belk Dress at attractive price with latest ",
user=user1,category=category2)
session.add(categoryitem4)
session.commit()

categoryitem5 = CategoryItem(category_item_name="JC Penny",
category_item_description="JC Penny Dress at attractive price with latest ",
user=user1,category=category2)
session.add(categoryitem5)
session.commit()
#################User2 Category 3###################


categoryitem6 = CategoryItem(category_item_name="Penguin",
category_item_description="Penguin books at attractive price with latest ",
user=user1,category=category3)
session.add(categoryitem6)
session.commit()

categoryitem7 = CategoryItem(category_item_name="JK Rowling",
category_item_description="Harry potter books at attractive price with latest ",
user=user1,category=category3)
session.add(categoryitem7)
session.commit()
# user = session.query(User).filter_by(email_id='rawatankit90.ca@gmail.com').one()
# if not user:
#     abort(400)
# print user.password_hash
