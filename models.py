# models.py

from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date, func
from sqlalchemy.orm import declarative_base, relationship
import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    email = Column(String, unique=True)
    budgets = relationship("Budget", back_populates="user")
    expenses = relationship("Expense", back_populates="user")

class Budget(Base):
    __tablename__ = 'budgets'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    month = Column(String)  # e.g. "2025-04"
    category = Column(String)
    limit = Column(Float)
    
    user = relationship("User", back_populates="budgets")

class Expense(Base):
    __tablename__ = 'expenses'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    category = Column(String)
    amount = Column(Float)
    date = Column(Date, default=func.current_date())
    
    user = relationship("User", back_populates="expenses")
