from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Date,  \
                func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
from passlib.apps import custom_app_context as pwd_context

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    email_id = Column(String(32), index=True, nullable=False)
    password_hash = Column(String(64))
    profile_pic = Column(String(100), nullable=True)
    created_on = Column(DateTime, default=func.now())

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        print (pwd_context.verify(password, self.password_hash))
        return pwd_context.verify(password, self.password_hash)


class Category(Base):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True)
    category_name = Column(String(200), nullable=True)
    category_description = Column(String(1000), nullable=False)
    created_by = Column(String(32), ForeignKey('user.email_id'))
    created_on = Column(DateTime, default=func.now())
    last_modified_on = Column(DateTime, default=func.now())
    user = relationship(User)

    @property
    def serialize(self):
        return {
           'id'                     : self.id,
           'category_name'          : self.category_name,
           'category_description'   : self.category_description
            }


class CategoryItem(Base):
    __tablename__ = 'categoryitem'
    id = Column(Integer, primary_key=True)
    category_item_name = Column(String(400), nullable=True)
    category_item_description = Column(String(1200), nullable=False)
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship(Category)
    created_by = Column(String(32), ForeignKey('user.email_id'))
    created_on = Column(DateTime, default=func.now())
    last_modified_on = Column(DateTime, default=func.now())
    user = relationship(User)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
           'id'                         : self.id,
           'category_item_name'         : self.category_item_name,
           'category_item_description'  : self.category_item_description,
           'category_id'                : self.category_id
           }


engine = create_engine('sqlite:///shoplocal.db')


Base.metadata.create_all(engine)
