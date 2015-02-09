from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from sqlalchemy import Table, Column, Integer, String, DateTime, ForeignKey, Float


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
  items = relationship("Item", backref="user")
  bids = relationship("Bid",backref="user")
  
class Bid(Base):
  __tablename__ = "bids"
  
  id = Column(Integer, primary_key=True)
  price = Column(Float, nullable=False)
  user_id = Column(Integer, ForeignKey('users.id'),nullable=False)
  item_id = Column(Integer, ForeignKey('items.id'),nullable=False)
  

Base.metadata.create_all(engine)

bob = User(username="bob", password="bob1")
joe = User(username="joe", password="joe1")
sally = User(username="sally", password="sally1")

baseball = Item(name="baseball",description="autographed baseball")

bob.items.append(baseball)

bid1 = Bid(price=22.95, user=sally, item=baseball)
bid2 = Bid(price=21.97, user=joe, item=baseball)

session.add_all([bob, joe, sally, baseball, bid1, bid2])
session.commit()

highest_bid = None

for item in bob.items:
  for bid in item.bids:
    if highest_bid == None:
      highest_bid = bid
    elif bid.price > highest_bid.price:
      highest_bid = bid
  print "The highest bid on " + item.name + " is " + str(highest_bid.price) + " by " + highest_bid.user.username
  