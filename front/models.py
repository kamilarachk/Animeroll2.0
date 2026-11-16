from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey, Numeric, Boolean, Text, JSON
from database import Base, engine

class User(Base):
    __tablename__ = 'users' 
    id = Column(Integer, primary_key=True)  
    email = Column(String, nullable=False)
    password_hash = Column(String, nullable=False)
    name = Column(String, nullable=False) 
    role = Column(String, default="client")
    created_at = Column(TIMESTAMP)
     
class Orders(Base): 
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)  
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(String, nullable=False)
    total_price = Column(Numeric(10, 2))
    address = Column(String, nullable=False)
    created_at = Column(TIMESTAMP)

class Orders_items(Base):
    __tablename__ = 'orders_items'
    id = Column(Integer, primary_key=True)  
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False) 
    quantity = Column(Integer, default=1)
    price_at_moment = Column(Numeric(10, 2))

class Products(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True) 
    category_id = Column(Integer, ForeignKey("categories.id")) 
    name = Column(String, nullable=False) 
    price = Column(Numeric(10, 2))
    description = Column(Text, nullable=False) 
    attributes = Column(JSON) 
    image_url = Column(String, default="image/logo2.png")

class Categories(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True) 
    name = Column(String, nullable=False)
    sort_order = Column(Integer)

class Conversation(Base): 
    __tablename__ = 'conversations'
    id = Column(Integer, primary_key=True) 
    client_id = Column(Integer, ForeignKey("users.id")) 
    manager_id = Column(Integer, ForeignKey("users.id"))
    product_id = Column(Integer, ForeignKey("products.id")) 
    status = Column(String, nullable=False)
    created_at = Column(TIMESTAMP)

class Messages(Base):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id")) 
    sender_id = Column(Integer, ForeignKey("users.id")) 
    text = Column(Text)
    is_read = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP)