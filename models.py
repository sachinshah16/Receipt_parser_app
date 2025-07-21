# models.py
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, String, Float, Integer

Base = declarative_base()

class Receipt(Base):
    __tablename__ = 'receipts'
    id = Column(Integer, primary_key=True)
    vendor = Column(String)
    amount = Column(Float)
    date = Column(String)
