
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


user = User(email_id="emailsenduser@gmail.com")
user.hash_password("email_id")
session.add(user)
session.commit()

user1 = User(email_id="abc@gmail.com")
user1.hash_password("abcdefg")
session.add(user1)
session.commit()

print "added User"

category = Category(category_name="Electronics",
                    category_description="electronic items - mobile,laptop,tv",
                    user=user)

session.add(category)
session.commit()


category1 = Category(category_name="Cars",
                     category_description="BMW, Audi, Mazda",
                     user=user)
session.add(category1)
session.commit()


category2 = Category(category_name="Clothing",
                     category_description="Clothing - Jeans,T-shirt,Dresses",
                     user=user1)
session.add(category2)
session.commit()


category3 = Category(category_name="Books",
                     category_description="GMAT,SAT,Computers",
                     user=user1)
session.add(category3)
session.commit()

print "added Categories"

# User 1 Category 1
categoryitem = CategoryItem(category_item_name="HP Black 15.6 Laptop",
                            category_item_description="HP Black 15.6 15-f233wm \
                             Laptop PC with Intel Celeron N3050 Processor, 4GB \
                             RAM,500 GB Hard Drive and windows 10 Home",
                            user=user, category=category)
session.add(categoryitem)
session.commit()


categoryitem1 = CategoryItem(category_item_name="Microsoft Surface Pro 4 ",
                             category_item_description="Microsoft Surface Pro 4 Core m3 6th Gen - (4 GB/128 GB SSD/Windows 10 Home) 1724 2 in 1 Laptop  (12.3 inch, SIlver, 0.76 kg)",
                             user=user, category=category)
session.add(categoryitem1)
session.commit()

# User 1 Category 2
categoryitem2 = CategoryItem(category_item_name="2018 BMW 2 Series",
                             category_item_description="BMW's replacement for the outgoing 1 Series coupe, the 2Series, rounds out the sporting credentials of its spirited predecessor with sleeker styling, a more upscale cabin and numerous new technology features. It won't disappoint those seeking a small luxury two-door with engaging driving dynamics.",
                             user=user, category=category1)
session.add(categoryitem2)
session.commit()

categoryitem3 = CategoryItem(category_item_name="Audi A3 Sportback e-tron",
                             category_item_description="A pleasing blend of hybrid and hatchback",
                             user=user, category=category1)
session.add(categoryitem3)
session.commit()
# User2 Category2

categoryitem4 = CategoryItem(category_item_name="Faux Leather Leggings",
                             category_item_description="Add instant richness to your workwear or after-hours attire with these faux leather leggings that are a must-have for your wardrobe.",
                             user=user1, category=category2)
session.add(categoryitem4)
session.commit()

categoryitem5 = CategoryItem(category_item_name="GAP - Mid rise best girlfriend jeans",
                             category_item_description="Our smart denim wash techniques have helped save 60 million liters of water, while cutting down on energy use. ",
                             user=user1, category=category2)
session.add(categoryitem5)
session.commit()
# User2 Category 3


categoryitem6 = CategoryItem(category_item_name="Force of Nature: A Novel",
                             category_item_description="Five women go on a hike. Only four return. Jane Harper, the New York Times bestselling author of The Dry, asks: How well do you really know the people you work with? ",
                             user=user1, category=category3)
session.add(categoryitem6)
session.commit()

categoryitem7 = CategoryItem(category_item_name="Freshwater by Akwaeke Emezi",
                             category_item_description="An extraordinary debut novel, Freshwater explores the surreal experience of having a fractured self. It centers around a young Nigerian woman, Ada, who develops separate selves within her as a result of being born with one foot on the other side. Unsettling, heartwrenching, dark, and powerful, Freshwater is a sharp evocation of a rare way of experiencing the world, one that illuminates how we all construct our identities.",
                             user=user1, category=category3)
session.add(categoryitem7)
session.commit()
# user = session.query(User).filter_by(email_id='rawatankit90.ca@gmail.com').
# one()
# if not user:
#     abort(400)
# print user.password_hash
