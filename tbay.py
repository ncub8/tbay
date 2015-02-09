from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from sqlalchemy import Table, Column, Integer, String, DateTime


engine = create_engine('postgresql://action:action@localhost:5432/tbay')
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


class Item(Base):
  __tablename__ = "items"
  
  id = Column(Integer, primary_key=True)
  name = Column(String, nullable=False)
  description = Column(String)
  start_time = Column(DateTime, default=datetime.utcnow)
  
  user_id = Column(Integer, ForeignKey('users.id'),nullable=False)
  bids = relationship("Bid", backref="item")
  

  
  
class User(Base):
  __tablename__ = "users"
  
  id = Column(Integer, primary_key=True)
  username = Column(String, nullable=False)
  password = Column(String, nullable=False)
  items = relationship("Item", backref="users")
  
class Bid(Base):
  __tablename__ = "bids"
  
  id = Column(Integer, primary_key=True)
  price = Column(String, nullable=False)
  user_id = Column(Integer, ForeignKey('users.id'),nullable=False)
  item_id = Column(Integer, ForeignKey('items.id'),nullable=False)
  
  
  
Base.metadata.create_all(engine)