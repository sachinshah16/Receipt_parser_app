
# db.py
from sqlalchemy import create_engine, Column, Integer, String, Float, Date
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base

# Setup SQLite database
engine = create_engine('sqlite:///receipts.db')

# Create session
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

# Base class
Base = declarative_base()
Base.query = db_session.query_property()

# Receipt table model
class Receipt(Base):
    __tablename__ = 'receipts'
    id = Column(Integer, primary_key=True)
    vendor = Column(String(100))
    amount = Column(Float)
    date = Column(String)  # If you're sure of date format, change to Date

# Run this once to create the table
def init_db():
    Base.metadata.create_all(bind=engine)

# Execute if this file is run directly
if __name__ == '__main__':
    init_db()
    print("✔️ Table 'receipts' created in receipts.db")
