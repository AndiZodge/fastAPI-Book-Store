from sqlalchemy import Column, String, Integer, Boolean, LargeBinary
from database import Base

class User(Base):
    __tablename__ = 'user_details'
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(30), unique=True, index=True)
    email_id = Column(String(30))
    password = Column(String(200))
    mobile_number = Column(String(15))
    is_admin = Column(Boolean)
    
class Book(Base):
    __tablename__ = 'book_details'
    
    id = Column(Integer, primary_key=True, index=True)
    book_name = Column(String(30), unique=True)
    image = Column(LargeBinary(length=100000))
    genre = Column(String(20))
    description = Column(String(30))
    cost_per_book = Column(Integer)
    quantity_available = Column(Integer)
    
class UserBook(Base):
    __tablename__ = 'user_books_details'
    
    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer)
    user_id = Column(Integer)
    quantity = Column(Integer)
    total_cost = Column(Integer)